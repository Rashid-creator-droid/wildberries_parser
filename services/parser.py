import math
from typing import List

import asyncio                     
import httpx                       

from core.settings import PER_PAGE, COOKIES
from models.main_config import AppConfig
from models.product_model import ProductList, ProductCard
from models.seller import Seller
from services.url_product_generate import ProductURLGenerator
from utils.price import CurrencyConverter


class Parser:
    def __init__(self, config: AppConfig):
        self.config = config
        self.url_gen = ProductURLGenerator(config)
        self.convert_currency = CurrencyConverter
        self.cookies = COOKIES

    async def _fetch_page(
        self,
        base_url: str,
        use_params: bool = False,
        filters: bool = False,
        page: int | None = 1,
    ) -> dict:
        params = None

        if use_params and self.config.request.params:
            params = {
                **self.config.request.params.model_dump(),
                **self.config.search.model_dump(),
                "page": page,
            }
            if filters:
                params.update(self.config.filters.model_dump())

        headers = self.config.request.headers.model_dump(by_alias=True)

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=base_url,
                params=params,
                cookies=self.cookies,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()

    async def get_total_items(self, use_filters: bool = False) -> int:
        url = self.url_gen.generate_base_search_url()
        data = await self._fetch_page(
            page=1, base_url=url, use_params=True, filters=use_filters
        )
        return data.get("total", 0)

    async def fetch_card_list_page(
        self, page: int, use_filters: bool = False
    ) -> ProductList:
        url = self.url_gen.generate_base_search_url()
        data = await self._fetch_page(
            page=page, base_url=url, use_params=True, filters=use_filters
        )
        return ProductList.model_validate(data)

    async def fetch_product_card(self, product_id: int) -> ProductCard:
        card_url = self.url_gen.generate_product_card_api_url(product_id)
        data = await self._fetch_page(base_url=card_url)
        return ProductCard.model_validate(data)

    async def fetch_seller_info(self, supplier_id: int) -> Seller:
        seller_url = self.url_gen.generate_seller_api_info_url(supplier_id)
        data = await self._fetch_page(base_url=seller_url)
        return Seller.model_validate(data)

    async def process_product(self, product) -> dict:
        first_size = product.sizes[0]
        product_card = await self.fetch_product_card(product.id)
        seller = await self.fetch_seller_info(
            product_card.selling.supplier_id
        )

        image_count = product_card.media.photo_count
        convert_to_rub = self.convert_currency.convert_rub_cop
        return {
            "article": product.id,
            "name": product.name,
            "product_url": self.url_gen.generate_product_page_url(product.id),
            "price_basic": convert_to_rub(first_size.price.basic),
            "price_sale": convert_to_rub(first_size.price.product),
            "description": product_card.description,
            "images": ", ".join(
                self.url_gen.generate_product_image_url(product.id, i)
                for i in range(1, image_count + 1)
            ),
            "options": str(product_card.options),
            "seller_name": seller.seller_name,
            "seller_url": self.url_gen.generate_seller_url(
                seller.supplier_id
            ),
            "sizes": ", ".join(s.name for s in product.sizes),
            "quantity": product.totalQuantity,
            "rating": product.review_rating,
            "feedbacks": product.feedbacks,
        }

    async def fetch_all_products(
        self,
        limit_pages: int | None = None,
        limit_per_page: int | None = None,
        use_filters: bool = False,
    ) -> List[dict]:
        total_items = await self.get_total_items(use_filters=use_filters)

        all_products: List[dict] = []

        total_pages = math.ceil(total_items / PER_PAGE)

        if limit_pages and total_pages >= limit_pages:
            total_pages = limit_pages

        for page in range(0, total_pages):
            page_data = await self.fetch_card_list_page(
                page=page, use_filters=use_filters
            )
            products = page_data.products

            if limit_per_page:
                products = products[:limit_per_page]

            tasks = [self.process_product(p) for p in products]
            results = await asyncio.gather(*tasks)

            for product_dict in results:
                print(
                    f"Processing product {product_dict['article']}: "
                    f"{product_dict['name']}"
                )
            all_products.extend(results)

        return all_products