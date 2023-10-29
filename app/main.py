from typing import Union

from fastapi import Depends, FastAPI
from sqlalchemy.sql import select

from example_package.dataclasses import person

from .database import get_sync_engine

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/persons")
def get_persons(conn=Depends(get_sync_engine)):
    stmt = select(person)
    res = conn.execute(stmt)
    return [
        dict(zip(person.columns.keys(), list(tmp))) for tmp in res.fetchall()
    ]
