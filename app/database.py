import os

from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine

db_async_url = (
    os.environ["DB_ASYNC_URL"]
    if "DB_ASYNC_URL" in os.environ and os.environ["DB_ASYNC_URL"]
    else "postgresql+asyncpg://postgres:postgres@localhost/postgres"
)
logger.info(f"new: {db_async_url}")

async_engine = create_async_engine(db_async_url)


async def get_async_engine():
    async with async_engine.begin() as conn:
        yield conn
        async_engine.sync_engine.dispose()
