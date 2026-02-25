import pytest


@pytest.mark.anyio
class TestParser:

    async def test_get_total_items_calls_fetch(self, parser, monkeypatch):

        async def fake_fetch(base_url, **kw):
            assert base_url.endswith("/search")
            return {"total": 777}

        monkeypatch.setattr(parser, "_fetch_page", fake_fetch)

        total = await parser.get_total_items(use_filters=False)
        assert total == 777
