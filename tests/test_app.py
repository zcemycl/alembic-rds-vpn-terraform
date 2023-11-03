import json
from pathlib import Path

import pytest

from httpx import AsyncClient

import example_package.dataclasses.orm as d


@pytest.mark.asyncio
async def test_root(test_async_client: AsyncClient):
    resp = await test_async_client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"Hello": "World"}


@pytest.mark.asyncio
async def test_async_persons(test_session_orm, test_async_client: AsyncClient):
    with open(Path("tests/test_data/base-persons.json"), "r") as f:
        jsons = json.load(f)
    ps = [d.person(**tmpjson) for tmpjson in jsons]
    test_session_orm.add_all(ps)
    await test_session_orm.commit()

    resp = await test_async_client.get("/async/persons")

    assert resp.status_code == 200
    assert len(resp.json()) == 2
