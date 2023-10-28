import json
from pathlib import Path

import pytest

from sqlalchemy.sql import delete, insert

from example_package.dataclasses import (
    friendship,
    person,
    person_skill_link,
    skill,
)


@pytest.mark.asyncio
async def test_db_core_link(get_engine):
    conn = get_engine

    with open(Path("tests/test_data/base-persons.json"), "r") as f:
        jsons = json.load(f)

    _ = await conn.execute(insert(person).values(jsons))
    _ = await conn.execute(
        insert(friendship).values(
            [{"parent_person_id": 1, "child_person_id": 2}]
        )
    )
    d = delete(person).where(person.c.id == 1)
    await conn.execute(d)


@pytest.mark.asyncio
async def test_db_skill_link(get_engine):
    conn = get_engine

    with open(Path("tests/test_data/base-persons.json"), "r") as f:
        jsons = json.load(f)

    _ = await conn.execute(insert(person).values(jsons))
    _ = await conn.execute(insert(skill).values([{"name": "python"}]))
    _ = await conn.execute(
        insert(person_skill_link).values([{"person_id": 1, "skill_id": 1}])
    )
    d = delete(skill).where(skill.c.id == 1)
    await conn.execute(d)
