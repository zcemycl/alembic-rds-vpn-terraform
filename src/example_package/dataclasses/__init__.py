from sqlalchemy import (
    Column,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB

from .common import Role

metadata = MetaData()


friendship = Table(
    "friendship",
    metadata,
    Column(
        "parent_person_id",
        Integer,
        ForeignKey("person.id"),
        primary_key=True,
        index=True,
        unique=False,
    ),
    Column(
        "child_person_id",
        Integer,
        ForeignKey("person.id"),
        primary_key=True,
        index=True,
        unique=False,
    ),
    UniqueConstraint(
        "parent_person_id", "child_person_id", name="friendship_case"
    ),
)

person_skill_link = Table(
    "person_skill_link",
    metadata,
    Column(
        "person_id",
        Integer,
        ForeignKey("person.id"),
        primary_key=True,
        index=True,
        unique=False,
    ),
    Column(
        "skill_id",
        Integer,
        ForeignKey("skill.id"),
        primary_key=True,
        index=True,
        unique=False,
    ),
    UniqueConstraint("person_id", "skill_id", name="person_skill_case"),
)

person = Table(
    "person",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("firstname", String),
    Column("lastname", String),
    Column("others", JSONB),
    Column("role", Enum(Role)),
)

skill = Table(
    "skill",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
)
