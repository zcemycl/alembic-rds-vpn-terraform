from fastapi.testclient import TestClient


def test_root(test_client: TestClient):
    resp = test_client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"Hello": "World"}
