from pydantic import BaseModel, HttpUrl

from models.filter import SearchConfig
from models.request import RequestConfig


class AppConfig(BaseModel):
    base_url: str
    products_api_url: str
    product_url_template: str
    product_base_api_template: str
    product_api_prefix: str
    image_url_prefix: str
    seller_url_prefix: str
    seller_url_template: str
    search: SearchConfig
    request: RequestConfig
