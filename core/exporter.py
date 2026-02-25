from pathlib import Path
from typing import List, Dict, Any
import pandas as pd
import asyncio
import gc

from core.logger import Logger
from models.main_config import SearchConfig
from models.filter import Filters


class Exporter:
    def __init__(
        self,
        filters: Filters | None = None,
        search: SearchConfig | None = None,
        base_name: str = "products.xlsx",
    ):
        self.filters = filters
        self.search = search
        self.base_name = base_name
        self.filename = self._generate_filename()

    def _generate_filename(self) -> Path:
        parts = ["parse"]

        if self.search and self.search.query:
            parts.append(self.search.query.replace(" ", "_"))

        if self.filters:
            parts.append(
                f"{self.filters.rating_min}-{self.filters.rating_max}"
            )
            parts.append(f"{self.filters.price_min}-{self.filters.price_max}")
            if self.filters.country:
                parts.append(f"{self.filters.country.name}")

        filename_stem = "_".join(parts)
        filename = Path(f"{filename_stem}.xlsx")

        counter = 1
        while filename.exists():
            filename = Path(f"{filename_stem}_{counter}.xlsx")
            counter += 1

        Logger.info(f"Файл для сохранения: {filename.name}")
        return filename

    def append_batch(self, products: List[Dict[str, Any]]):
        Logger.debug(f"append_batch, {len(products)} записей")
        if not products:
            return

        df = pd.DataFrame(products)
        mode = "a" if self.filename.exists() else "w"

        writer_kwargs = {"engine": "openpyxl", "mode": mode}
        if mode == "a":
            writer_kwargs["if_sheet_exists"] = "overlay"

        with pd.ExcelWriter(self.filename, **writer_kwargs) as writer:
            if mode == "a":
                ws = writer.sheets.get("Sheet1")
                startrow = ws.max_row if ws is not None else 0
                header = startrow == 0
            else:
                startrow = 0
                header = True

            df.to_excel(writer, index=False, header=header, startrow=startrow)

        products.clear()
        del df
        gc.collect()

    async def append_batch_async(self, products: List[Dict[str, Any]]):
        await asyncio.to_thread(self.append_batch, products)
