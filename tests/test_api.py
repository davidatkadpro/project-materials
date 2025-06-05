from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Project materials API"}


def test_create_and_list_project():
    project = {"id": 1, "name": "Build House"}
    resp = client.post("/projects", json=project)
    assert resp.status_code == 200
    assert resp.json()["name"] == "Build House"

    list_resp = client.get("/projects")
    assert list_resp.status_code == 200
    assert any(p["id"] == 1 for p in list_resp.json())
