import os

from sqlalchemy.engine import Engine, create_engine

db_url = (
    os.environ["DB_URL"]
    if "DB_URL" in os.environ
    else "postgresql://postgres:postgres@localhost/postgres"
)

engine = None


def make_engine() -> Engine:
    global engine
    if engine is None:
        engine = create_engine(db_url)
    return engine


def get_sync_engine():
    with engine.begin() as conn:
        yield conn
        conn.dispose()
