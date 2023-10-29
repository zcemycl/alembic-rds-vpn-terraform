import json
from pathlib import Path

from sqlalchemy.sql import select

import example_package.dataclasses.orm as d


def test_orm_link(test_session):
    ps = []
    with open(Path("tests/test_data/base-persons.json"), "r") as f:
        jsons = json.load(f)

    for tmpjson in jsons:
        tmpp = d.person(**tmpjson)
        ps.append(tmpp)
    ps[1].parent_friendships = [ps[0]]
    s1 = d.skill(name="python", persons=[ps[0]])
    test_session.add_all(ps + [s1])
    test_session.commit()

    p1_ = test_session.execute(
        select(d.person).where(d.person.id == ps[0].id)
    ).scalar()

    assert s1.id == p1_.skills[0].id
    assert p1_.parent_friendships == []
    assert p1_.child_friendships[0].id == ps[1].id
    assert ps[0].child_friendships[0].id == ps[1].id
    assert ps[1].child_friendships == []
    assert ps[1].parent_friendships == [ps[0]]

    test_session.query(d.skill).filter(d.skill.id == ps[0].id).delete()
    test_session.commit()

    test_session.query(d.person).filter(d.person.id == ps[1].id).delete()
    test_session.commit()
