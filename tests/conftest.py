import asyncio

import pytest

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine

from app.database import get_async_engine
from app.main import app
from example_package.dataclasses import metadata


@pytest.fixture(scope="session")
def event_loop() -> asyncio.AbstractEventLoop:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True)
async def get_engine():
    db_url = "postgresql+asyncpg://postgres:postgres@localhost/postgres"
    engine = create_async_engine(db_url)

    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)

        yield conn
        engine.sync_engine.dispose()


@pytest_asyncio.fixture(autouse=True)
async def test_async_client(get_engine) -> AsyncClient:
    def _local_engine():
        try:
            yield get_engine
        finally:
            pass

    app.dependency_overrides[get_async_engine] = _local_engine
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
