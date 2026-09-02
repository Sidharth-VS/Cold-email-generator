from fastapi import status


def test_create_portfolio(client):
    register_payload = {
        "email": "portfolio@example.com",
        "username": "portuser",
        "password": "SecurePass123!",
    }
    client.post("/users/register", json=register_payload)

    login_payload = {
        "email": "portfolio@example.com",
        "password": "SecurePass123!",
    }
    token = client.post("/users/login", json=login_payload).json()["access_token"]

    portfolio_payload = {
        "tech_stack": "Python, FastAPI, SQLAlchemy",
        "link": "https://github.com/testuser/portfolio",
    }
    response = client.post(
        "/portfolio/",
        json=portfolio_payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["tech_stack"] == portfolio_payload["tech_stack"]
    assert data["link"] == portfolio_payload["link"]
    assert "id" in data
    assert "user_id" in data
    assert "created_at" in data


def test_list_portfolios(client):
    register_payload = {
        "email": "list@example.com",
        "username": "listuser",
        "password": "SecurePass123!",
    }
    client.post("/users/register", json=register_payload)

    login_payload = {
        "email": "list@example.com",
        "password": "SecurePass123!",
    }
    token = client.post("/users/login", json=login_payload).json()["access_token"]

    portfolio_payload = {
        "tech_stack": "Python, FastAPI",
        "link": "https://github.com/listuser/portfolio",
    }
    client.post("/portfolio/", json=portfolio_payload, headers={"Authorization": f"Bearer {token}"})

    response = client.get("/portfolio/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["tech_stack"] == "Python, FastAPI"


def test_get_portfolio_not_found(client):
    register_payload = {
        "email": "notfound@example.com",
        "username": "notfounduser",
        "password": "SecurePass123!",
    }
    client.post("/users/register", json=register_payload)

    login_payload = {
        "email": "notfound@example.com",
        "password": "SecurePass123!",
    }
    token = client.post("/users/login", json=login_payload).json()["access_token"]

    response = client.get("/portfolio/999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_portfolio(client):
    register_payload = {
        "email": "update@example.com",
        "username": "updateuser",
        "password": "SecurePass123!",
    }
    client.post("/users/register", json=register_payload)

    login_payload = {
        "email": "update@example.com",
        "password": "SecurePass123!",
    }
    token = client.post("/users/login", json=login_payload).json()["access_token"]

    create_response = client.post(
        "/portfolio/",
        json={"tech_stack": "Python", "link": "https://github.com/updateuser/portfolio"},
        headers={"Authorization": f"Bearer {token}"},
    )
    portfolio_id = create_response.json()["id"]

    update_response = client.put(
        f"/portfolio/{portfolio_id}",
        json={"tech_stack": "Python, Django", "link": "https://github.com/updateuser/django"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert update_response.status_code == status.HTTP_200_OK
    data = update_response.json()
    assert data["tech_stack"] == "Python, Django"
    assert data["link"] == "https://github.com/updateuser/django"


def test_delete_portfolio(client):
    register_payload = {
        "email": "delete@example.com",
        "username": "deleteuser",
        "password": "SecurePass123!",
    }
    client.post("/users/register", json=register_payload)

    login_payload = {
        "email": "delete@example.com",
        "password": "SecurePass123!",
    }
    token = client.post("/users/login", json=login_payload).json()["access_token"]

    create_response = client.post(
        "/portfolio/",
        json={"tech_stack": "Python", "link": "https://github.com/deleteuser/portfolio"},
        headers={"Authorization": f"Bearer {token}"},
    )
    portfolio_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/portfolio/{portfolio_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    get_response = client.get(f"/portfolio/{portfolio_id}", headers={"Authorization": f"Bearer {token}"})
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_create_portfolio_unauthorized(client):
    response = client.post("/portfolio/", json={"tech_stack": "Python", "link": "https://example.com"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
