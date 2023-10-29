import json
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy.sql import insert

from example_package.dataclasses import person


def test_root(test_client: TestClient):
    resp = test_client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"Hello": "World"}


def test_async_persons(get_engine, test_client):
    conn = get_engine
    with open(Path("tests/test_data/base-persons.json"), "r") as f:
        jsons = json.load(f)

    conn.execute(insert(person).values(jsons))
    resp = test_client.get("/persons")
    assert resp.status_code == 200
    assert len(resp.json()) == 2
