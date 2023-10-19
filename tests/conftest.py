import pytest

from sqlalchemy.engine import Engine, create_engine

from example_package.dataclasses import metadata


@pytest.fixture(scope="session")
def get_engine() -> Engine:
    db_url = "postgresql://postgres:postgres@localhost/postgres"
    engine = create_engine(db_url)

    metadata.drop_all(bind=engine)
    metadata.create_all(bind=engine)

    yield engine
