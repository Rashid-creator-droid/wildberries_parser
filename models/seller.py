from pydantic import BaseModel, Field


class SellerID(BaseModel):
    supplier_id: int


class Seller(BaseModel):
    trademark: str | None = None
    supplier_full_name: str | None = Field(
        default=None, alias="supplierFullName"
    )
    supplier_id: int | None = Field(default=None, alias="supplierId")

    @property
    def seller_name(self) -> str | None:
        return self.trademark or self.supplier_full_name or None
