import os
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def get_token(email, password):
    r = client.post("/auth/login", json={"email": email, "password": password})
    return r.json()["access_token"]

def setup_user_and_token():
    user = {"username": "projuser", "email": "projuser@example.com", "password": "projpass123", "role": "admin"}
    client.post("/auth/register", json=user)
    token = get_token(user["email"], user["password"])
    return user, token

def test_project_crud():
    user, token = setup_user_and_token()
    headers = {"Authorization": f"Bearer {token}"}
    # Create project
    proj_data = {"name": "Test Project", "description": "A test project"}
    r = client.post("/projects", json=proj_data, headers=headers)
    assert r.status_code == 200
    project = r.json()
    project_id = project["id"]
    # Get all projects
    r = client.get("/projects", headers=headers)
    assert r.status_code == 200
    assert any(p["id"] == project_id for p in r.json())
    # Get single project
    r = client.get(f"/projects/{project_id}", headers=headers)
    assert r.status_code == 200
    assert r.json()["id"] == project_id
    # Update project
    update_data = {"name": "Updated Project", "description": "Updated desc"}
    r = client.put(f"/projects/{project_id}", json=update_data, headers=headers)
    assert r.status_code == 200
    assert r.json()["name"] == "Updated Project"
    # Delete project
    r = client.delete(f"/projects/{project_id}", headers=headers)
    assert r.status_code == 200
    # Confirm deletion
    r = client.get(f"/projects/{project_id}", headers=headers)
    assert r.status_code == 404 