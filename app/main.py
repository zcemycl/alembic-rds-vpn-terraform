from fastapi import Depends, FastAPI
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from sqlalchemy.sql.expression import func

import example_package.dataclasses.orm as d

from .database import get_async_session

# import requests


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


# @app.get("/login_page")
# async def login_page():
#     headers = {"Content-Type": "application/x-www-form-urlencoded"}
#     data = {
#         "grant_type":"client_credentials",
#         "client_id":"fake",
#         "client_secret":"fake",
#         "mock_type":"user",
#     }
#     # if grant_type == "refresh_token":
#     #     data["refresh_token"] = refresh_token
#     resp = requests.post(
#         "http://oauth:8080/default_issuer/token",
#         headers=headers,
#         data=data,
#     )
#     return {
#         **resp.json(),
#         "id_token": "7cZPgOvv?hMc6j8FqMuYhx=g45454gw?vOWZM?!vz2FB7dAf?O?63iY"
#         }
