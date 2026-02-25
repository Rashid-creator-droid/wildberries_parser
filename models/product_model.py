from pydantic import BaseModel
from typing import List




class Price(BaseModel):
    basic: int
    product: int

class Size(BaseModel):
    name: str
    price: Price

class Product(BaseModel):
    id: int
    name: str
    sizes: List[Size]
    totalQuantity: int
    rating: float
    feedbacks: int

class ProductList(BaseModel):
    products: List[Product]


class ProductOptions(BaseModel):
    name: str
    value: str
    charc_type: int
    is_variable: bool | None = None
    variable_value_IDs: List[int] | None = None
    variable_values: List[str] | None = None


class ProductCard(BaseModel):
    description: str
    options: List[ProductOptions]