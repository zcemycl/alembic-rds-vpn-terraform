from fastapi import Depends, FastAPI
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from sqlalchemy.sql.expression import func

import example_package.dataclasses.orm as d

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
    stmt = select(d.person)
    res = (await session.execute(stmt)).scalars().all()
    jsons = [tmp.as_dict() for tmp in res]
    logger.info(jsons)
    return jsons


@app.get("/async/skills")
async def get_async_skills(
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(func.distinct(d.skill.name).label("name"))
    res = (await session.execute(stmt)).mappings().all()
    logger.info(res)
    return res
