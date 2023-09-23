from sqlalchemy import Column, Integer, MetaData, String, Table
from sqlalchemy.dialects.postgresql import JSONB

metadata = MetaData()

persons = Table(
    "persons",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("firstname", String),
    Column("lastname", String),
    Column("others", JSONB),
)
