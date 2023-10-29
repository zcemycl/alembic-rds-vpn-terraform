import pytest

from fastapi.testclient import TestClient
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

import example_package.dataclasses.orm as d
from app.database import get_session
from app.main import app


@pytest.fixture(autouse=True)
def get_engine() -> Engine:
    db_url = "postgresql://postgres:postgres@localhost/postgres"
    engine = create_engine(db_url)

    d.metadata.drop_all(bind=engine)
    d.metadata.create_all(bind=engine)

    yield engine
    engine.dispose()


@pytest.fixture(scope="function", autouse=True)
def test_session(get_engine: Engine) -> Session:
    session = sessionmaker(
        bind=get_engine, expire_on_commit=False, class_=Session
    )
    with session() as session:
        yield session
        session.close()


@pytest.fixture(scope="function", autouse=True)
def test_client(test_session: Session) -> TestClient:
    def _local_session():
        try:
            yield test_session
        finally:
            pass

    app.dependency_overrides[get_session] = _local_session
    with TestClient(app) as client:
        yield client
