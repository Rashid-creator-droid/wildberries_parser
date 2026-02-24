from pydantic import BaseModel, Field, model_validator


class SearchFilters(BaseModel):
    rating_min: int | None = Field(None, ge=0, le=5)
    rating_max: int | None = Field(None, ge=0, le=5)

    price_min: int | None = Field(None, ge=0)
    price_max: int | None = Field(None, ge=0)

    country: str | None

    @model_validator(mode="after")
    def check_ranges(self):
        if (
            self.rating_min is not None
            and self.rating_max is not None
            and self.rating_min > self.rating_max
        ):
            raise ValueError("rating_min не может быть больше rating_max")

        if (
            self.price_min is not None
            and self.price_max is not None
            and self.price_min > self.price_max
        ):
            raise ValueError("price_min не может быть больше price_max")

        return self


class SearchConfig(BaseModel):
    query: str = Field(min_length=1)
    filters: SearchFilters