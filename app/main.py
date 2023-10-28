from fastapi import Depends, FastAPI
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

# import example_package.dataclasses.orm as d
from example_package.dataclasses import person

from .database import get_async_session

app = FastAPI()


# @app.on_event("startup")
# async def create_db():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(d.Base.metadata.create_all)

# @app.on_event("shutdown")
# async def del_db():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(d.Base.metadata.drop_all)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/async/persons")
async def get_async_persons(
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(person)
    res = await session.execute(stmt)
    res = res.all()
    logger.info(res)
    return res
