import json
from pathlib import Path

import pytest

from sqlalchemy.sql import delete, insert

from example_package.dataclasses import friendship, person


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


# @pytest.mark.asyncio
# async def test_orm_link(test_session_orm):
#     ps = []
#     with open(Path("tests/test_data/base-persons.json"), "r") as f:
#         jsons = json.load(f)

#     for tmpjson in jsons:
#         tmpp = d.person(**tmpjson)
#         ps.append(tmpp)
#     ps[1].parent_friendships = [ps[0]]
#     s1 = d.skill(name="python", persons=[ps[0]])
#     test_session_orm.add_all(ps + [s1])
#     await test_session_orm.commit()

#     p1_promise = await test_session_orm.execute(
#         select(d.person)
#         .where(d.person.id == ps[0].id)
#         .options(selectinload(d.person.parent_friendships))
#         .options(selectinload(d.person.child_friendships))
#     )
#     p1_ = p1_promise.scalar()
#     await test_session_orm.refresh(
#         ps[1], attribute_names=["child_friendships"]
#     )

#     assert s1.id == p1_.skills[0].id
#     assert p1_.parent_friendships == []
#     assert p1_.child_friendships[0].id == ps[1].id
#     assert ps[0].child_friendships[0].id == ps[1].id
#     assert ps[1].child_friendships == []
#     assert ps[1].parent_friendships == [ps[0]]

#     s1_ = (
#         await test_session_orm.execute(
#             select(d.skill).where(d.skill.id == s1.id)
#         )
#     ).scalar()
#     await test_session_orm.delete(s1_)
#     await test_session_orm.commit()

#     p2_ = (
#         await test_session_orm.execute(
#             select(d.person).where(d.person.id == ps[1].id)
#         )
#     ).scalar()
#     await test_session_orm.delete(p2_)
#     await test_session_orm.commit()
