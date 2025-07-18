from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_and_login_and_me():
    # Register a new user
    register_data = {
        "username": "autotestuser",
        "email": "autotest@example.com",
        "password": "testpassword123"
    }
    r = client.post("/auth/register", json=register_data)
    assert r.status_code in (200, 400)  # 400 if user already exists

    # Login
    login_data = {
        "email": "autotest@example.com",
        "password": "testpassword123"
    }
    r = client.post("/auth/login", json=login_data)
    assert r.status_code == 200
    token = r.json()["access_token"]

    # Get current user info
    headers = {"Authorization": f"Bearer {token}"}
    r = client.get("/auth/me", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data["email"] == "autotest@example.com"
    assert data["username"] == "autotestuser" 