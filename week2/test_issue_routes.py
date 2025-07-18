import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

import pytest
from fastapi.testclient import TestClient
from main import app
from datetime import datetime

client = TestClient(app)

# Helper to get JWT token for a user
def get_token(email, password):
    r = client.post("/auth/login", json={"email": email, "password": password})
    return r.json()["access_token"]

@pytest.fixture(scope="module")
def setup_users_and_project():
    # Register two users
    user1 = {"username": "issueowner", "email": "issueowner@example.com", "password": "pw123456"}
    user2 = {"username": "issueassignee", "email": "issueassignee@example.com", "password": "pw654321"}
    client.post("/auth/register", json=user1)
    client.post("/auth/register", json=user2)
    token1 = get_token(user1["email"], user1["password"])
    token2 = get_token(user2["email"], user2["password"])
    # User1 creates a project
    headers1 = {"Authorization": f"Bearer {token1}"}
    r = client.post("/projects", json={"name": "Proj1", "description": "desc"}, headers=headers1)
    print("Project creation response:", r.status_code, r.json())
    project_json = r.json()
    project_id = project_json["id"] if "id" in project_json else None
    assert project_id is not None, f"Project creation failed: {project_json}"
    return {"token1": token1, "token2": token2, "project_id": project_id}

def test_issue_crud_and_permissions(setup_users_and_project):
    token1 = setup_users_and_project["token1"]
    token2 = setup_users_and_project["token2"]
    project_id = setup_users_and_project["project_id"]
    headers1 = {"Authorization": f"Bearer {token1}"}
    headers2 = {"Authorization": f"Bearer {token2}"}

    # User1 creates an issue
    issue_data = {
        "title": "Bug1",
        "description": "desc",
        "status": "open",
        "priority": "high",
        "assigned_to": None
    }
    r = client.post(f"/projects/{project_id}/issues", json=issue_data, headers=headers1)
    assert r.status_code == 200
    issue_id = r.json()["id"]

    # User1 can get all issues for their project
    r = client.get(f"/projects/{project_id}/issues", headers=headers1)
    assert r.status_code == 200
    assert len(r.json()) >= 1

    # User2 cannot get issues for a project they don't own
    r = client.get(f"/projects/{project_id}/issues", headers=headers2)
    assert r.status_code == 404

    # User1 can get the issue by id
    r = client.get(f"/issues/{issue_id}", headers=headers1)
    assert r.status_code == 200

    # User2 cannot get the issue by id (not assigned, not owner)
    r = client.get(f"/issues/{issue_id}", headers=headers2)
    assert r.status_code == 403

    # User1 can update the issue
    update_data = {"status": "closed"}
    r = client.put(f"/issues/{issue_id}", json=update_data, headers=headers1)
    assert r.status_code == 200
    assert r.json()["status"] == "closed"

    # User2 cannot update the issue
    r = client.put(f"/issues/{issue_id}", json=update_data, headers=headers2)
    assert r.status_code == 403

    # User1 can delete the issue
    r = client.delete(f"/issues/{issue_id}", headers=headers1)
    assert r.status_code == 204

    # User2 cannot delete the issue (already deleted, but test 404)
    r = client.delete(f"/issues/{issue_id}", headers=headers2)
    assert r.status_code == 404

    # Cannot create/update/delete without token
    r = client.post(f"/projects/{project_id}/issues", json=issue_data)
    assert r.status_code == 401
    r = client.put(f"/issues/{issue_id}", json=update_data)
    assert r.status_code == 401
    r = client.delete(f"/issues/{issue_id}")
    assert r.status_code == 401 