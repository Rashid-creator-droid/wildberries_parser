from typing import List

from pydantic import BaseModel

from models.seller import Seller


class Characteristic(BaseModel):
    name: str
    value: str

class Price(BaseModel):
    basic: int
    product: int
    logistics: int
    return_: int


class Size(BaseModel):
    name: str
    origName: str
    wh: int
    price: Price


class WoolCoat(BaseModel):
    id: int
    url: str
    name: str
    price: int 
    description: str | None = None
    img_urls: List[str]
    characteristics: List[Characteristic]
    seller: Seller
    sizes: List[Size]
    total_stock: int
    rating: float | None = None
    reviews_count: int
