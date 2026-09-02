from datetime import datetime
from fastapi import status
from app.models.user import User
from app.core.security import hash_password


def test_register_user(client):
    payload = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "SecurePass123!",
    }
    response = client.post("/users/register", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["user"]["email"] == payload["email"]
    assert data["user"]["username"] == payload["username"]
    assert "id" in data["user"]
    assert "otp" in data["user"]


def test_register_duplicate_email(client):
    payload = {
        "email": "duplicate@example.com",
        "username": "user1",
        "password": "SecurePass123!",
    }
    response1 = client.post("/users/register", json=payload)
    assert response1.status_code == status.HTTP_201_CREATED

    response2 = client.post("/users/register", json=payload)
    assert response2.status_code == status.HTTP_400_BAD_REQUEST


def test_login_success(client):
    register_payload = {
        "email": "login@example.com",
        "username": "loginuser",
        "password": "SecurePass123!",
    }
    reg_response = client.post("/users/register", json=register_payload)
    otp = reg_response.json()["user"]["otp"]
    client.post("/auth/verify-email", params={"email": register_payload["email"], "otp": otp})

    login_payload = {
        "email": "login@example.com",
        "password": "SecurePass123!",
    }
    response = client.post("/users/login", json=login_payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password(client):
    register_payload = {
        "email": "badlogin@example.com",
        "username": "baduser",
        "password": "SecurePass123!",
    }
    reg_response = client.post("/users/register", json=register_payload)
    otp = reg_response.json()["user"]["otp"]
    client.post("/auth/verify-email", params={"email": register_payload["email"], "otp": otp})

    login_payload = {
        "email": "badlogin@example.com",
        "password": "wrongpassword",
    }
    response = client.post("/users/login", json=login_payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user(client):
    register_payload = {
        "email": "me@example.com",
        "username": "meuser",
        "password": "SecurePass123!",
    }
    reg_response = client.post("/users/register", json=register_payload)
    otp = reg_response.json()["user"]["otp"]
    client.post("/auth/verify-email", params={"email": register_payload["email"], "otp": otp})

    login_payload = {
        "email": "me@example.com",
        "password": "SecurePass123!",
    }
    login_response = client.post("/users/login", json=login_payload)
    token = login_response.json()["access_token"]

    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "me@example.com"
    assert data["username"] == "meuser"


def test_get_current_user_unauthorized(client):
    response = client.get("/users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
