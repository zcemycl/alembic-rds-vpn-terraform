import json
from pathlib import Path

from sqlalchemy.sql import delete, insert, select

import example_package.dataclasses.orm as d
from example_package.dataclasses import friendship, person


def test_db(get_engine):
    engine = get_engine

    with open(Path("tests/test_data/create-persons.json"), "r") as f:
        jsons = json.load(f)

    stmt = insert(person).values(jsons)
    with engine.begin() as conn:
        _ = conn.execute(stmt)


def test_db_core_link(get_engine):
    engine = get_engine

    with open(Path("tests/test_data/base-persons.json"), "r") as f:
        jsons = json.load(f)

    with engine.begin() as conn:
        _ = conn.execute(insert(person).values(jsons))
        _ = conn.execute(
            insert(friendship).values(
                [{"parent_person_id": 1, "child_person_id": 2}]
            )
        )
        d = delete(person).where(person.c.id == 1)
        conn.execute(d)


def test_orm_link(test_session2):
    ps = []
    with open(Path("tests/test_data/base-persons.json"), "r") as f:
        jsons = json.load(f)

    for tmpjson in jsons:
        tmpp = d.person(**tmpjson)
        ps.append(tmpp)
    ps[1].parent_friendships = [ps[0]]
    s1 = d.skill(name="python", persons=[ps[0]])
    test_session2.add_all(ps + [s1])
    test_session2.commit()

    p1_ = test_session2.execute(
        select(d.person).where(d.person.id == ps[0].id)
    ).scalar()

    assert s1.id == p1_.skills[0].id
    assert p1_.parent_friendships == []
    assert p1_.child_friendships[0].id == ps[1].id
    assert ps[0].child_friendships[0].id == ps[1].id
    assert ps[1].child_friendships == []
    assert ps[1].parent_friendships == [ps[0]]

    test_session2.query(d.skill).filter(d.skill.id == ps[0].id).delete()
    test_session2.commit()

    test_session2.query(d.person).filter(d.person.id == ps[1].id).delete()
    test_session2.commit()
