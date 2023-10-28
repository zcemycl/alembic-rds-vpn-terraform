import pytest

from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root(test_async_client: AsyncClient):
    resp = await test_async_client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"Hello": "World"}


@pytest.mark.asyncio
async def test_async_persons(test_async_client: AsyncClient):
    resp = await test_async_client.get("/async/persons")
    assert resp.status_code == 200
    assert len(resp.json()) == 0
