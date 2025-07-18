from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def get_token(email, password):
    r = client.post("/auth/login", json={"email": email, "password": password})
    return r.json()["access_token"]

def setup_user_project_and_token():
    user = {"username": "issueuser", "email": "issueuser@example.com", "password": "issuepass123"}
    client.post("/auth/register", json=user)
    token = get_token(user["email"], user["password"])
    headers = {"Authorization": f"Bearer {token}"}
    # Create project
    proj_data = {"name": "Issue Project", "description": "Project for issues"}
    r = client.post("/projects", json=proj_data, headers=headers)
    project_id = r.json()["id"]
    return user, token, project_id

def test_issue_crud():
    user, token, project_id = setup_user_project_and_token()
    headers = {"Authorization": f"Bearer {token}"}
    # Create issue
    issue_data = {
        "title": "Test Issue",
        "description": "Issue desc",
        "status": "open",
        "priority": "high",
        "assigned_to": None
    }
    r = client.post(f"/projects/{project_id}/issues", json=issue_data, headers=headers)
    assert r.status_code == 200
    issue = r.json()
    issue_id = issue["id"]
    # Get issues for project
    r = client.get(f"/projects/{project_id}/issues", headers=headers)
    assert r.status_code == 200
    assert any(i["id"] == issue_id for i in r.json())
    # View single issue
    r = client.get(f"/issues/{issue_id}", headers=headers)
    assert r.status_code == 200
    assert r.json()["id"] == issue_id 