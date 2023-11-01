import sqlalchemy as sa
from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    Column,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR
from sqlalchemy.orm import declarative_base, relationship

from .common import Role

Base = declarative_base()
metadata = Base.metadata


class TSVector(sa.types.TypeDecorator):
    impl = TSVECTOR


class friendship(Base):
    __tablename__ = "friendship"
    parent_person_id = Column(
        "parent_person_id",
        Integer,
        ForeignKey("person.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
        unique=False,
    )
    child_person_id = Column(
        "child_person_id",
        Integer,
        ForeignKey("person.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
        unique=False,
    )
    __table_args__ = (
        UniqueConstraint(
            "parent_person_id", "child_person_id", name="friendship_case"
        ),
    )


class person_skill_link(Base):
    __tablename__ = "person_skill_link"
    person_id = Column(
        "person_id",
        Integer,
        ForeignKey("person.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
        unique=False,
    )
    skill_id = Column(
        "skill_id",
        Integer,
        ForeignKey("skill.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
        unique=False,
    )
    __table_args__ = (
        UniqueConstraint("person_id", "skill_id", name="person_skill_case"),
    )


class article(Base):
    __tablename__ = "article"
    id = Column("id", Integer, primary_key=True)
    title = Column("title", String)
    description = Column("description", String)
    factors = Column("factors", Vector(20))

    __ts_vector__ = Column(
        TSVector(),
        sa.Computed(
            "to_tsvector('english', title || ' ' || description)",
            persisted=True,
        ),
    )
    __table_args__ = (
        Index("ix_video___ts_vector__", __ts_vector__, postgresql_using="gin"),
    )


class person(Base):
    __tablename__ = "person"
    id = Column("id", Integer, primary_key=True)
    firstname = Column("firstname", String)
    lastname = Column("lastname", String)
    others = Column("others", JSONB)
    role = Column("role", Enum(Role))
    skills = relationship(
        "skill",
        secondary=person_skill_link.__table__,
        back_populates="persons",
    )
    parent_friendships = relationship(
        "person",
        secondary=friendship.__table__,
        primaryjoin=id == friendship.parent_person_id,
        secondaryjoin=id == friendship.child_person_id,
        back_populates="parent_friendships",
    )
    child_friendships = relationship(
        "person",
        secondary=friendship.__table__,
        primaryjoin=id == friendship.child_person_id,
        secondaryjoin=id == friendship.parent_person_id,
        back_populates="parent_friendships",
    )


class skill(Base):
    __tablename__ = "skill"
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    persons = relationship(
        "person",
        secondary=person_skill_link.__table__,
        back_populates="skills",
    )
