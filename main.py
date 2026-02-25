import argparse
import asyncio
from tqdm.asyncio import tqdm_asyncio

from core.data_loader import DataLoader
from core.exporter import Exporter
from services.parser import Parser


async def main(
    limit_per_page: int | None, limit_pages: int | None, use_filters: bool
):
    config = DataLoader().get_config()
    parser = Parser(config)
    exporter = Exporter(
        filters=config.filters if use_filters else None, search=config.search
    )
    batch: list[dict] = []
    total_saved = 0

    try:
        total_items = await parser.get_total_items(use_filters=use_filters)

        async for prod in tqdm_asyncio(
            parser.iter_products(
                limit_per_page=limit_per_page,
                limit_pages=limit_pages,
                use_filters=use_filters,
            ),
            total=total_items,
            desc="Parsing products",
        ):
            total_saved += 1
            batch.append(prod)

            if len(batch) >= 50:
                await exporter.append_batch_async(batch)
                batch.clear()

        if batch:
            await exporter.append_batch_async(batch)

    finally:
        await parser.close()
    if use_filters:
        print(
            f"\nТоваров прошедших фильтрацию - {total_saved} из {total_items} загружено"
        )
    else:
        print(f"\nЗагружено {total_saved} товаров")


if __name__ == "__main__":
    parser_cli = argparse.ArgumentParser(description="Wildberries Parser")
    parser_cli.add_argument(
        "--limit-per-page",
        type=int,
        default=None,
        help="Максимальное количество товаров на странице",
    )
    parser_cli.add_argument(
        "--limit-pages",
        type=int,
        default=None,
        help="Максимальное количество страниц для парсинга",
    )
    parser_cli.add_argument(
        "--use-filters",
        action="store_true",
        help="Применять фильтры (rating, price и т.д.)",
    )

    args = parser_cli.parse_args()

    asyncio.run(
        main(
            limit_per_page=args.limit_per_page,
            limit_pages=args.limit_pages,
            use_filters=args.use_filters,
        )
    )
