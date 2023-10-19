import json
from pathlib import Path

from sqlalchemy.sql import insert

from example_package.dataclasses import persons


def test_db(get_engine):
    engine = get_engine

    with open(Path("tests/test_data/base_persons.json"), "r") as f:
        jsons = json.load(f)

    stmt = insert(persons).values(jsons)
    with engine.begin() as conn:
        _ = conn.execute(stmt)
