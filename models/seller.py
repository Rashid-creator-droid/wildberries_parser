from typing import Optional

from pydantic import BaseModel


class Seller(BaseModel):
    name: str
    url: Optional[str]