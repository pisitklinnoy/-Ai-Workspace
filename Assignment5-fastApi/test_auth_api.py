"""
Automated Test for Signup, Login, and Profile Endpoints using FastAPI TestClient.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_signup_and_login_flow():
    # 1. Test Health Root
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

    # 2. Test User Signup (Registration)
    signup_payload = {
        "username": "testuser",
        "email": "testuser@example.com",
        "full_name": "Test User",
        "password": "Password123"
    }
    signup_res = client.post("/api/v1/auth/signup", json=signup_payload)
    assert signup_res.status_code == 201
    data = signup_res.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"
    # Ensure sensitive fields like password or hashed_password are NOT exposed!
    assert "password" not in data
    assert "hashed_password" not in data

    # 3. Test Duplicate Signup (Conflict)
    dup_res = client.post("/api/v1/auth/signup", json=signup_payload)
    assert dup_res.status_code == 409

    # 4. Test User Login (Signin)
    login_payload = {
        "username": "testuser",
        "password": "Password123"
    }
    login_res = client.post("/api/v1/auth/login", json=login_payload)
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    token = token_data["access_token"]

    # 5. Test Access Protected /me Endpoint with JWT Bearer Token
    headers = {"Authorization": f"Bearer {token}"}
    me_res = client.get("/api/v1/auth/me", headers=headers)
    assert me_res.status_code == 200
    me_data = me_res.json()
    assert me_data["username"] == "testuser"
    assert me_data["email"] == "testuser@example.com"

    print("SUCCESS: All Authentication API tests passed successfully!")

if __name__ == "__main__":
    test_signup_and_login_flow()
