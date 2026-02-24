from pydantic import BaseModel


class Seller(BaseModel):
    name: str
    url: str | None