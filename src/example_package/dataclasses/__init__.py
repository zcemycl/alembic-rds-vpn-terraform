from enum import Enum as EnumType

from sqlalchemy import (
    Column,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
)
from sqlalchemy.dialects.postgresql import JSONB

metadata = MetaData()


class Role(str, EnumType):
    developer = "developer"
    maintainer = "maintainer"
    viewer = "viewer"


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
