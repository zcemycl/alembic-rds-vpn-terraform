from typing import Union

from fastapi import Depends, FastAPI
from loguru import logger
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

import example_package.dataclasses.orm as d

from .database import get_session

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/persons")
def get_persons(session: Session = Depends(get_session)):
    stmt = select(d.person)
    res = session.execute(stmt).scalars().all()
    jsons = [tmpres.__dict__ for tmpres in res]
    logger.info(jsons)
    return jsons
