import json
from pathlib import Path

import pytest

from httpx import AsyncClient
from sqlalchemy.sql import insert

from example_package.dataclasses import person


@pytest.mark.asyncio
async def test_root(test_async_client: AsyncClient):
    resp = await test_async_client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"Hello": "World"}


@pytest.mark.asyncio
async def test_async_persons(get_engine, test_async_client: AsyncClient):
    conn = get_engine
    with open(Path("tests/test_data/base-persons.json"), "r") as f:
        jsons = json.load(f)

    await conn.execute(insert(person).values(jsons))
    resp = await test_async_client.get("/async/persons")
    assert resp.status_code == 200
    assert len(resp.json()) == 2
