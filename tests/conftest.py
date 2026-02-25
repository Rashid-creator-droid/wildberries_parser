import pytest
from types import SimpleNamespace
from services.parser import Parser


class DummyConfig:
    def __init__(self):
        self.base_url = "https://example.test"
        self.product_base_api_template = "https://api.example/{product_id}"
        self.products_api_url = "/search"
        self.product_url_template = "/product/{product_id}"
        self.product_api_prefix = "/card"
        self.image_url_prefix = "/img/{image_number}"

        self.request = SimpleNamespace(
            headers=SimpleNamespace(model_dump=lambda **kw: {}),
            params=None,
        )
        self.search = SimpleNamespace(model_dump=lambda **kw: {})
        self.filters = SimpleNamespace(
            model_dump=lambda **kw: {},
            rating_min=0,
            rating_max=5
        )


@pytest.fixture
async def parser():
    cfg = DummyConfig()
    p = Parser(cfg)
    yield p
    await p.close()
