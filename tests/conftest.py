import asyncio

import pytest

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

import example_package.dataclasses.orm as d
from app.database import get_async_session
from app.main import app


@pytest.fixture(scope="session")
def event_loop() -> asyncio.AbstractEventLoop:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
def get_engine_orm() -> AsyncEngine:
    db_url = "postgresql+asyncpg://postgres:postgres@localhost/postgres"
    engine = create_async_engine(
        db_url,
        pool_recycle=1800,
        # connect_args={
        #     "server_settings": {
        #         "tcp_keepalives_idle": "600",
        #         "tcp_keepalives_interval": "30",
        #         "tcp_keepalives_count": "10",
        #     }
        # },
    )

    yield engine
    engine.sync_engine.dispose()


@pytest_asyncio.fixture(autouse=True)
async def test_session_orm(get_engine_orm: AsyncEngine) -> AsyncSession:
    async with get_engine_orm.begin() as conn:
        await conn.run_sync(d.Base.metadata.drop_all)
        await conn.run_sync(d.Base.metadata.create_all)
        _local_async_session = async_sessionmaker(
            expire_on_commit=False, class_=AsyncSession, bind=get_engine_orm
        )
        async with _local_async_session(bind=conn) as sess:
            yield sess
            await sess.flush()
            await sess.rollback()


@pytest_asyncio.fixture(autouse=True)
async def test_async_client(test_session_orm: AsyncSession) -> AsyncClient:
    def _local_session():
        try:
            yield test_session_orm
        finally:
            pass

    app.dependency_overrides[get_async_session] = _local_session
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
