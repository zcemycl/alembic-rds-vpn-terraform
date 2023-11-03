import pytest

from fastapi.testclient import TestClient
from sqlalchemy.engine import Engine, create_engine

from app.database import get_sync_engine
from app.main import app
from example_package.dataclasses import metadata


@pytest.fixture(autouse=True)
def get_engine() -> Engine:
    db_url = "postgresql://postgres:postgres@localhost/postgres"
    engine = create_engine(db_url)

    # Comment these 2 lines out for alembic migration test
    metadata.drop_all(bind=engine)
    metadata.create_all(bind=engine)

    with engine.begin() as conn:
        yield conn
        engine.dispose()


@pytest.fixture(scope="function", autouse=True)
def test_client(get_engine) -> TestClient:
    def _local_engine():
        try:
            yield get_engine
        finally:
            pass

    app.dependency_overrides[get_sync_engine] = _local_engine
    with TestClient(app) as client:
        yield client
