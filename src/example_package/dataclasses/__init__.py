from enum import Enum as EnumType

from sqlalchemy import Column, Integer, MetaData, String, Table, Enum
from sqlalchemy.dialects.postgresql import JSONB

metadata = MetaData()

class Role(str, EnumType):
    developer = "developer"
    maintainer = "maintainer"
    viewer = "viewer"

persons = Table(
    "persons",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("firstname", String),
    Column("lastname", String),
    Column("others", JSONB),
    Column("roles", Enum(Role))
)
