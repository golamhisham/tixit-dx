import os
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def get_token(email, password):
    r = client.post("/auth/login", json={"email": email, "password": password})
    return r.json()["access_token"]

def setup_admin_and_member():
    admin = {"username": "adminuser", "email": "admin@example.com", "password": "adminpass123", "role": "admin"}
    member = {"username": "memberuser", "email": "member@example.com", "password": "memberpass123", "role": "member"}
    client.post("/auth/register", json=admin)
    client.post("/auth/register", json=member)
    admin_token = get_token(admin["email"], admin["password"])
    member_token = get_token(member["email"], member["password"])
    return admin, admin_token, member, member_token

def test_rbac_project_delete():
    admin, admin_token, member, member_token = setup_admin_and_member()
    # Member creates a project
    headers_member = {"Authorization": f"Bearer {member_token}"}
    proj_data = {"name": "RBAC Project", "description": "RBAC test"}
    r = client.post("/projects", json=proj_data, headers=headers_member)
    assert r.status_code == 200
    project_id = r.json()["id"]
    # Member cannot delete project
    r = client.delete(f"/projects/{project_id}", headers=headers_member)
    assert r.status_code == 403
    # Admin can delete project
    headers_admin = {"Authorization": f"Bearer {admin_token}"}
    r = client.delete(f"/projects/{project_id}", headers=headers_admin)
    assert r.status_code == 200
    # Member cannot access admin-only route
    r = client.delete(f"/projects/{project_id}", headers=headers_member)
    assert r.status_code == 403 