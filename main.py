from core.data_loader import DataLoader
from core.exporter import Exporter
from services.parser import Parser

import asyncio


async def main():
    config = DataLoader().get_config()
    parser = Parser(config)
    exporter = Exporter("wildberries_products.xlsx")
    batch: list[dict] = []
    total_saved = 0

    try:
        async for prod in parser.iter_products(
            limit_per_page=87, limit_pages=1, use_filters=False
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
    asyncio.run(main())
