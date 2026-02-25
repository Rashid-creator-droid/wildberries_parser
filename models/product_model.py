from pydantic import BaseModel, Field
from typing import List

from models.seller import SellerID


class Price(BaseModel):
    basic: int | None = None
    product: int | None = None


class Size(BaseModel):
    name: str | None = None
    price: Price | None = None


class Product(BaseModel):
    id: int | None = None
    name: str | None = None
    sizes: List[Size] | None = None
    totalQuantity: int | None = None
    review_rating: float | None = Field(default=None, alias="reviewRating")
    feedbacks: int | None = None


class ProductList(BaseModel):
    products: List[Product] | None = None


class ProductOptions(BaseModel):
    name: str | None = None
    value: str | None = None
    charc_type: int | None = None
    is_variable: bool | None = None
    variable_value_IDs: List[int] | None = None
    variable_values: List[str] | None = None


class ProductPhoto(BaseModel):
    photo_count: int | None = None


class ProductCard(BaseModel):
    description: str | None = None
    options: List[ProductOptions] | None = None
    media: ProductPhoto | None = None
    selling: SellerID | None = None

    def simple_options(self) -> list[dict]:
        result = []
        fields = [
            "name",
            "value",
            "charc_type",
            "is_variable",
            "variable_value_IDs",
            "variable_values",
        ]
        if not self.options:
            return result

        for opt in self.options:
            opt_dict = {}
            for field in fields:
                val = getattr(opt, field, None)
                if val is not None:
                    opt_dict[field] = val
            if opt_dict:
                result.append(opt_dict)

        return result
