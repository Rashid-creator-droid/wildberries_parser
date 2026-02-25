from core.logger import Logger
from utils.basket_id import get_basket_id
from urllib.parse import urljoin


class ProductURLGenerator:
    def __init__(self, config):
        self.config = config
        self.base_url = self.config.base_url
        self.product_base_api_template = self.config.product_base_api_template

    def _generate_base_api_template(self, product_id: int):
        vol = product_id // 100_000
        part = product_id // 1_000
        basket_id = get_basket_id(product_id)
        result = self.product_base_api_template.format(
            product_id=product_id,
            vol=vol,
            part=part,
            basket_id=basket_id,
        )
        Logger.debug(f"Базовый URL {result} адрес товара с id = {product_id}")
        return result

    def generate_base_search_url(self) -> str:
        result = urljoin(self.base_url, self.config.products_api_url)
        Logger.debug(f"Базовый URL {result} адрес поиска")
        return result

    def generate_product_page_url(self, product_id: int) -> str:
        result = urljoin(
            self.base_url,
            self.config.product_url_template.format(product_id=product_id),
        )
        Logger.debug(
            f"Базовый URL {result} адрес страницы товара с id = {product_id}"
        )
        return result

    def generate_product_card_api_url(self, product_id: int) -> str:
        result = urljoin(
            self._generate_base_api_template(product_id),
            self.config.product_api_prefix,
        )
        Logger.debug(
            f"Базовый URL {result} карточки товара с id = {product_id}"
        )
        return result

    def generate_product_image_url(
        self, product_id: int, image_number: int = 1
    ) -> str:
        img_prefix = self.config.image_url_prefix.format(
            image_number=image_number
        )

        result = urljoin(
            self._generate_base_api_template(product_id), img_prefix
        )
        Logger.debug(
            f"Базовый URL {result} адрес изображения товара с id = {product_id}"
        )
        return result

    def generate_seller_url(self, supplier_id: int) -> str:
        result = urljoin(
            self.base_url,
            self.config.seller_url_prefix.format(supplier_id=supplier_id),
        )
        Logger.debug(
            f"Базовый URL {result} адрес продавца с id = {supplier_id}"
        )
        return result

    def generate_seller_api_info_url(self, supplier_id: int) -> str:
        result = urljoin(
            self.base_url,
            self.config.seller_url_template.format(supplier_id=supplier_id),
        )
        Logger.debug(
            f"Базовый URL {result} адрес API информации продавца с id = {supplier_id}"
        )
        return result
