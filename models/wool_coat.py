from typing import List

from pydantic import BaseModel

from models.seller import Seller


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
    rating: float | None
    eviews_count: int
