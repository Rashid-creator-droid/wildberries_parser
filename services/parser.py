import math

import asyncio
import httpx

from core.settings import PER_PAGE, COOKIES, PROXY_URL
from models.main_config import AppConfig
from models.product_model import ProductList, ProductCard
from models.seller import Seller
from services.url_product_generate import ProductURLGenerator
from utils.build_product import build_product_dict
from utils.price import CurrencyConverter
from core.logger import Logger


class Parser:
    def __init__(self, config: AppConfig):
        self.config = config
        self.url_gen = ProductURLGenerator(config)
        self.convert_currency = CurrencyConverter
        self.semaphore = asyncio.Semaphore(10)
        self.client = httpx.AsyncClient(
            cookies=COOKIES,
            headers=config.request.headers.model_dump(by_alias=True),
            timeout=20,
            proxy=PROXY_URL or None,
        )
        
    async def close(self):
        await self.client.aclose()

    async def _fetch_page(
        self,
        base_url: str,
        use_params: bool = False,
        filters: bool = False,
        page: int | None = 1,
    ) -> dict:
        params = None
        Logger.info(f"Запрос {base_url} page={page}")

        if use_params and self.config.request.params:
            params = {
                **self.config.request.params.model_dump(),
                **self.config.search.model_dump(),
                "page": page,
            }
            if filters:
                Logger.info(f"Использование фильтров для запроса {base_url} page={page}")
                params.update(self.config.filters.model_dump())

        response = await self.client.get(
            url=base_url,
            params=params,
        )
        response.raise_for_status()
        return response.json()

    async def get_total_items(self, use_filters: bool = False) -> int:
        url = self.url_gen.generate_base_search_url()
        data = await self._fetch_page(
            page=1, base_url=url, use_params=True, filters=use_filters
        )
        result = data.get("total", 0)
        Logger.info(f"Всего товаров для загрузки: {result}")
        return result

    async def fetch_card_list_page(
        self, page: int, use_filters: bool = False
    ) -> ProductList:
        url = self.url_gen.generate_base_search_url()
        data = await self._fetch_page(
            page=page, base_url=url, use_params=True, filters=use_filters
        )
        Logger.info(f"Получено {len(data.get('products', []))} товаров на странице {page}")
        return ProductList.model_validate(data)

    async def fetch_product_card(self, product_id: int) -> ProductCard:
        card_url = self.url_gen.generate_product_card_api_url(product_id)
        data = await self._fetch_page(base_url=card_url)
        Logger.info(f"Получена карточка товара id={product_id}")
        return ProductCard.model_validate(data)

    async def fetch_seller_info(self, supplier_id: int) -> Seller:
        seller_url = self.url_gen.generate_seller_api_info_url(supplier_id)
        data = await self._fetch_page(base_url=seller_url)
        Logger.info(f"Получена информация о продавце id={supplier_id}")
        return Seller.model_validate(data)

    async def process_product(self, product, use_filters) -> dict:
        Logger.debug(f"начало process_product id={product.id}")
        if use_filters:
            filter_ = self.config.filters
            if product.review_rating is None:
                return None
            if not (filter_.rating_min <= product.review_rating <= filter_.rating_max):
                return None

        async with self.semaphore:
            product_card = await self.fetch_product_card(product.id)
            seller = await self.fetch_seller_info(product_card.selling.supplier_id)
            return build_product_dict(
                product,
                product_card,
                seller,
                self.url_gen,
                self.convert_currency,
            )

    async def iter_products(
        self,
        limit_pages: int | None = None,
        limit_per_page: int | None = None,
        use_filters: bool = False,
    ):

        total_items = await self.get_total_items(use_filters=use_filters)
        total_pages = math.ceil(total_items / PER_PAGE)

        if limit_pages and total_pages >= limit_pages:
            Logger.info(f"Ограничение количества страниц: {limit_pages} из {total_pages}")
            total_pages = limit_pages

        for page in range(1, total_pages + 1):
            with Logger.step(f"Страница [{page}]"):
                page_data = await self.fetch_card_list_page(
                    page=page, use_filters=use_filters
                )
                products = page_data.products
                if limit_per_page:
                    Logger.info(f"Ограничение количества товаров на странице: {limit_per_page} из {len(products)}")
                    products = products[:limit_per_page]

                tasks = [
                    self.process_product(product=product, use_filters=use_filters)
                    for product in products
                ]
                results = await asyncio.gather(*tasks, return_exceptions=True)

                for result in results:
                    if result is None or isinstance(result, Exception):
                        continue
                    yield result
