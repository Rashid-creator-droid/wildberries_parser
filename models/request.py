from pydantic import BaseModel, Field


class RequestParams(BaseModel):
    resultset: str
    sort: str
    lang: str
    curr: str
    dest: str


class RequestHeaders(BaseModel):
    user_agent: str = Field(alias="user-agent")
    accept: str
    accept_language: str = Field(alias="accept-language")

    class Config:
        populate_by_name = True


class RequestConfig(BaseModel):
    params: RequestParams | None = None
    headers: RequestHeaders
