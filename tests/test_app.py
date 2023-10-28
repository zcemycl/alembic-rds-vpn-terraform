import pytest

from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root(test_async_client: AsyncClient):
    resp = await test_async_client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"Hello": "World"}
