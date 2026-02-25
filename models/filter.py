from pydantic import BaseModel, Field, field_validator

from enums.country import CountryEnum


class Filters(BaseModel):
    rating_min: int | None = Field(0, ge=0, le=5)
    rating_max: int | None = Field(5, ge=0, le=5)

    price_min: int | None = Field(0, ge=0)
    price_max: int | None = Field(1_000_000, ge=0)

    country: CountryEnum | None = None
    
    @field_validator("country", mode="before")
    @classmethod
    def parse_country(cls, v):
        if v is None:
            return v

        if isinstance(v, str) and v.isupper():
            try:
                return CountryEnum[v]
            except KeyError:
                raise ValueError(f"Not allowed county: {v}")

        return v

    def model_dump(self, **kwargs):
        data = {}

        if self.price_min is not None or self.price_max is not None:
            data["priceU"] = f"{self.price_min * 100};{self.price_max * 100}"

        if self.country:
            data["f14177451"] = self.country.value

        return data


class SearchConfig(BaseModel):
    query: str = Field(min_length=1)
