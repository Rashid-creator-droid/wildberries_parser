from core.json_loader import DataLoader
from utils.data_save_service import save_products_to_excel
from services.parser import Parser

import asyncio

async def main():
    config = DataLoader().get_config()     
    parser = Parser(config)
    items = await parser.fetch_all_products(limit_per_page=10, limit_pages=1, use_filters=False)
    print(f"загружено {len(items)} товаров")
    save_products_to_excel(items, "wildberries_products.xlsx")

if __name__ == "__main__":
    asyncio.run(main())
