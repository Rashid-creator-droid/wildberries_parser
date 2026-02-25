from pathlib import Path
from typing import List, Dict, Any
import pandas as pd
import asyncio
import gc


class Exporter:
    def __init__(self, filename: str = "products.xlsx"):
        self.filename = Path(filename)

    def append_batch(self, products: List[Dict[str, Any]]):

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
