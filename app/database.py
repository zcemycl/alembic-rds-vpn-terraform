import os
from typing import Iterator

from loguru import logger
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

db_async_url = (
    os.environ["DB_ASYNC_URL"]
    if "DB_ASYNC_URL" in os.environ and os.environ["DB_ASYNC_URL"]
    else "postgresql+asyncpg://postgres:postgres@localhost/postgres"
)
logger.info(f"new: {db_async_url}")

async_engine = create_async_engine(db_async_url)


# def make_async_engine() -> AsyncEngine:
#     global async_engine
#     if async_engine is None:
#         async_engine = create_async_engine(db_async_url)


async def get_async_session() -> Iterator[AsyncSession]:
    session = async_sessionmaker(
        async_engine,
        autocommit=False,
        autoflush=False,
        # bind=create_async_engine(db_async_url),
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with session() as sess:
        yield sess
