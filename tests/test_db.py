import json
from pathlib import Path

from sqlalchemy.sql import insert, select

import example_package.dataclasses.orm as d
from example_package.dataclasses import person


def test_db(get_engine):
    engine = get_engine

    with open(Path("tests/test_data/create-persons.json"), "r") as f:
        jsons = json.load(f)

    stmt = insert(person).values(jsons)
    with engine.begin() as conn:
        _ = conn.execute(stmt)


def test_orm_link(test_session2):
    p1 = d.person(firstname="1", lastname="1", others={}, role="developer")
    s1 = d.skill(name="python", persons=[p1])
    p2 = d.person(
        firstname="2",
        lastname="2",
        others={},
        role="developer",
        parent_friendships=[p1],
    )
    test_session2.add_all([p1, s1, p2])
    test_session2.commit()

    p1_ = test_session2.execute(
        select(d.person).where(d.person.id == p1.id)
    ).scalar()

    assert s1.id == p1_.skills[0].id
    assert p1_.parent_friendships == []
    assert p1_.child_friendships[0].id == p2.id
    assert p1.child_friendships[0].id == p2.id
    assert p2.child_friendships == []
    assert p2.parent_friendships == [p1]

    test_session2.query(d.skill).filter(d.skill.id == s1.id).delete()
    test_session2.commit()

    test_session2.query(d.person).filter(d.person.id == p2.id).delete()
    test_session2.commit()
