import json
from pathlib import Path

from sqlalchemy.sql import delete, insert

from example_package.dataclasses import friendship, person


def test_db(get_engine):
    conn = get_engine

    with open(Path("tests/test_data/create-persons.json"), "r") as f:
        jsons = json.load(f)

    stmt = insert(person).values(jsons)
    conn.execute(stmt)


def test_db_core_link(get_engine):
    conn = get_engine

    with open(Path("tests/test_data/base-persons.json"), "r") as f:
        jsons = json.load(f)

    _ = conn.execute(insert(person).values(jsons))
    _ = conn.execute(
        insert(friendship).values(
            [{"parent_person_id": 1, "child_person_id": 2}]
        )
    )
    d = delete(person).where(person.c.id == 1)
    conn.execute(d)
