import json
from pathlib import Path

import pytest

from sqlalchemy.orm import selectinload
from sqlalchemy.sql import select

import example_package.dataclasses.orm as d


@pytest.mark.asyncio
async def test_orm_person(test_session_orm):
    with open(Path("tests/test_data/base-persons.json"), "r") as f:
        jsons = json.load(f)

    ps = [d.person(**tmpjson) for tmpjson in jsons]

    test_session_orm.add_all(ps)
    await test_session_orm.commit()

    p1_ = (
        await test_session_orm.execute(
            select(d.person).where(d.person.id == ps[0].id)
        )
    ).scalar()
    assert p1_.id == ps[0].id


@pytest.mark.asyncio
async def test_orm_link(test_session_orm):
    ps = []
    with open(Path("tests/test_data/base-persons.json"), "r") as f:
        jsons = json.load(f)

    for tmpjson in jsons:
        tmpp = d.person(**tmpjson)
        ps.append(tmpp)
    ps[1].parent_friendships = [ps[0]]
    s1 = d.skill(name="python", persons=[ps[0]])
    test_session_orm.add_all(ps + [s1])
    await test_session_orm.commit()

    p1_promise = await test_session_orm.execute(
        select(d.person)
        .where(d.person.id == ps[0].id)
        .options(selectinload(d.person.parent_friendships))
        .options(selectinload(d.person.child_friendships))
    )
    p1_ = p1_promise.scalar()
    await test_session_orm.refresh(
        ps[1], attribute_names=["child_friendships"]
    )

    assert s1.id == p1_.skills[0].id
    assert p1_.parent_friendships == []
    assert p1_.child_friendships[0].id == ps[1].id
    assert ps[0].child_friendships[0].id == ps[1].id
    assert ps[1].child_friendships == []
    assert ps[1].parent_friendships == [ps[0]]

    s1_ = (
        await test_session_orm.execute(
            select(d.skill).where(d.skill.id == s1.id)
        )
    ).scalar()
    await test_session_orm.delete(s1_)
    await test_session_orm.commit()

    p2_ = (
        await test_session_orm.execute(
            select(d.person).where(d.person.id == ps[1].id)
        )
    ).scalar()
    await test_session_orm.delete(p2_)
    await test_session_orm.commit()


@pytest.mark.asyncio
async def test_article_tsvector(test_session_orm):
    sess = test_session_orm
    a1 = d.article(
        title="introduction", description="I am Leo", factors=20 * [1]
    )
    a2 = d.article(title="summary", description="Bye Bye!", factors=20 * [10])
    a3 = d.article(
        title="methodology",
        description="I am using pgvector",
        factors=20 * [2],
    )
    all_a = [a1, a3, a2]
    sess.add_all(all_a)
    await sess.commit()

    stmt = select(d.article).where(d.article.ts_vector.match("Leo"))
    a_res = (await sess.execute(stmt)).scalars().all()
    assert (
        a_res[0].title + ":" + a_res[0].description
        == a1.title + ":" + a1.description
    )


@pytest.mark.skip(reason="timeout in github actions")
@pytest.mark.asyncio
async def test_article_pgvector(test_session_orm):
    sess = test_session_orm
    a1 = d.article(
        title="introduction", description="I am Leo", factors=20 * [1]
    )
    a2 = d.article(title="summary", description="Bye Bye!", factors=20 * [10])
    a3 = d.article(
        title="methodology",
        description="I am using pgvector",
        factors=20 * [2],
    )
    all_a = [a1, a3, a2]
    sess.add_all(all_a)
    await sess.commit()

    stmt = select(d.article.title).order_by(
        d.article.factors.l2_distance(a1.factors)
    )
    a_res = (await sess.execute(stmt)).scalars().all()
    for i in range(len(all_a)):
        assert a_res[i] == all_a[i].title
