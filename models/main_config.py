from pydantic import BaseModel, HttpUrl

from models.filter import SearchConfig
from models.request import RequestConfig


class AppConfig(BaseModel):
    base_api_url: HttpUrl
    product_url_template: str
    product_card_api_template: str
    search: SearchConfig
    request: RequestConfig
