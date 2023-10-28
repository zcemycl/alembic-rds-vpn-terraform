from fastapi import Depends, FastAPI
from sqlalchemy.sql import select

from example_package.dataclasses import person

from .database import get_async_engine

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
    conn=Depends(get_async_engine),
):
    stmt = select(person)
    res = await conn.execute(stmt)

    return [
        dict(zip(person.columns.keys(), list(tmp))) for tmp in res.fetchall()
    ]
