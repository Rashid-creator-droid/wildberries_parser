from pydantic import BaseModel, HttpUrl

from models.filter import SearchConfig
from models.request import RequestConfig


class AppConfig(BaseModel):
    base_url: HttpUrl
    search: SearchConfig
    request: RequestConfig
