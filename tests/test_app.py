import json
from pathlib import Path

from fastapi.testclient import TestClient

import example_package.dataclasses.orm as d


def test_root(test_client: TestClient):
    resp = test_client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"Hello": "World"}


def test_persons(test_session, test_client: TestClient):
    with open(Path("tests/test_data/base-persons.json"), "r") as f:
        jsons = json.load(f)
    ps = [d.person(**tmpjson) for tmpjson in jsons]
    ps[1].parent_friendships = [ps[0]]
    test_session.add_all(ps)
    test_session.commit()

    resp = test_client.get("/persons")
    assert resp.status_code == 200
