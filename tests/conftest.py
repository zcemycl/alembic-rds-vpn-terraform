import json
import os
from pathlib import Path

import pytest
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.sql import insert, select, update
from example_package.dataclasses import metadata

@pytest.fixture(scope="session")
def get_engine() -> Engine:
    db_url = f"postgresql://postgres:postgres@localhost/postgres"
    engine  = create_engine(db_url)

    metadata.drop_all(bind=engine)
    metadata.create_all(bind=engine)

    yield engine
