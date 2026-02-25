import argparse

from core.data_loader import DataLoader
from core.exporter import Exporter
from services.parser import Parser

import asyncio


async def main(limit_per_page: int, limit_pages: int, use_filters: bool):
    config = DataLoader().get_config()
    parser = Parser(config)
    exporter = Exporter("wildberries_products.xlsx")
    batch: list[dict] = []
    total_saved = 0

    try:
        async for prod in parser.iter_products(
            limit_per_page=limit_per_page,
            limit_pages=limit_pages,
            use_filters=use_filters
        ):
            total_saved += 1
            batch.append(prod)
            print(f"Processing product {prod['article']}: {prod['name']}")

            if len(batch) >= 50:
                await exporter.append_batch_async(batch)
        if batch:
            await exporter.append_batch_async(batch)

    finally:
        await parser.close()

    print(f"загружено {total_saved} товаров")


if __name__ == "__main__":
    parser_cli = argparse.ArgumentParser(description="Wildberries Parser")
    parser_cli.add_argument(
        "--limit-per-page",
        type=int,
        default=50,
        help="Максимальное количество товаров на странице",
    )
    parser_cli.add_argument(
        "--limit-pages",
        type=int,
        default=1,
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
