from typing import List, Optional

from pydantic import BaseModel

from .seller import Seller


class Characteristic(BaseModel):
    name: str
    value: str


class Size(BaseModel):
    name: str
    stock: int


class WoolCoat(BaseModel):
    url: str
    article: int
    name: str
    price: int
    description: str
    img_urls: List[str]
    characteristics: List[Characteristic]
    seller: Seller
    sizes: List[str]
    total_stock: int
    rating: Optional[float]
    eviews_count: int
