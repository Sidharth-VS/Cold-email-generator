from unittest.mock import patch
from fastapi import status


def test_generate_email(client):
    register_payload = {
        "email": "email@example.com",
        "username": "emailuser",
        "password": "securepassword123",
    }
    client.post("/users/register", json=register_payload)

    login_payload = {
        "email": "email@example.com",
        "password": "securepassword123",
    }
    token = client.post("/users/login", json=login_payload).json()["access_token"]

    mock_job_details = [
        {
            "role": "Backend Engineer",
            "experience": "3+ years",
            "skills": ["Python", "FastAPI", "SQLAlchemy"],
            "description": "We are looking for a backend engineer...",
        }
    ]

    with patch("app.routes.mails.Generator") as MockGenerator, \
         patch("app.routes.mails.get_webpage_text", return_value="<html>Job Description</html>"), \
         patch("app.services.portfolio.Portfolio") as MockPortfolio:

        mock_generator = MockGenerator.return_value
        mock_generator.extract_job_details.return_value = mock_job_details
        mock_generator.generate_mail.return_value = "Dear Hiring Manager, I am excited to apply..."

        mock_portfolio = MockPortfolio.return_value
        mock_portfolio.query.return_value = [{"links": "https://github.com/testuser/project1"}]

        response = client.post(
            "/mails/generate?job_url=https://example.com/job",
            headers={"Authorization": f"Bearer {token}"},
        )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["job_url"] == "https://example.com/job"
    assert "generated_email" in data
    assert "id" in data
    assert "user_id" in data
    assert "created_at" in data


def test_list_emails(client):
    register_payload = {
        "email": "listemails@example.com",
        "username": "listemailsuser",
        "password": "securepassword123",
    }
    client.post("/users/register", json=register_payload)

    login_payload = {
        "email": "listemails@example.com",
        "password": "securepassword123",
    }
    token = client.post("/users/login", json=login_payload).json()["access_token"]

    mock_job_details = [
        {
            "role": "Engineer",
            "experience": "2+ years",
            "skills": ["Python"],
            "description": "Job description...",
        }
    ]

    with patch("app.routes.mails.Generator") as MockGenerator, \
         patch("app.routes.mails.get_webpage_text", return_value="<html>Job</html>"), \
         patch("app.services.portfolio.Portfolio") as MockPortfolio:

        mock_generator = MockGenerator.return_value
        mock_generator.extract_job_details.return_value = mock_job_details
        mock_generator.generate_mail.return_value = "Generated email content"

        mock_portfolio = MockPortfolio.return_value
        mock_portfolio.query.return_value = []

        client.post(
            "/mails/generate?job_url=https://example.com/job1",
            headers={"Authorization": f"Bearer {token}"},
        )
        client.post(
            "/mails/generate?job_url=https://example.com/job2",
            headers={"Authorization": f"Bearer {token}"},
        )

    response = client.get("/mails/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2


def test_get_email(client):
    register_payload = {
        "email": "getemail@example.com",
        "username": "getemailuser",
        "password": "securepassword123",
    }
    client.post("/users/register", json=register_payload)

    login_payload = {
        "email": "getemail@example.com",
        "password": "securepassword123",
    }
    token = client.post("/users/login", json=login_payload).json()["access_token"]

    mock_job_details = [
        {
            "role": "Engineer",
            "experience": "2+ years",
            "skills": ["Python"],
            "description": "Job description...",
        }
    ]

    with patch("app.routes.mails.Generator") as MockGenerator, \
         patch("app.routes.mails.get_webpage_text", return_value="<html>Job</html>"), \
         patch("app.services.portfolio.Portfolio") as MockPortfolio:

        mock_generator = MockGenerator.return_value
        mock_generator.extract_job_details.return_value = mock_job_details
        mock_generator.generate_mail.return_value = "Generated email content"

        mock_portfolio = MockPortfolio.return_value
        mock_portfolio.query.return_value = []

        create_response = client.post(
            "/mails/generate?job_url=https://example.com/job",
            headers={"Authorization": f"Bearer {token}"},
        )
        email_id = create_response.json()["id"]

    response = client.get(f"/mails/{email_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == email_id


def test_generate_email_unauthorized(client):
    response = client.post("/mails/generate?job_url=https://example.com/job")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_email(client):
    register_payload = {
        "email": "delete@example.com",
        "username": "deleteuser",
        "password": "securepassword123",
    }
    client.post("/users/register", json=register_payload)

    login_payload = {
        "email": "delete@example.com",
        "password": "securepassword123",
    }
    token = client.post("/users/login", json=login_payload).json()["access_token"]

    mock_job_details = [
        {
            "role": "Engineer",
            "experience": "2+ years",
            "skills": ["Python"],
            "description": "Job description...",
        }
    ]

    with patch("app.routes.mails.Generator") as MockGenerator, \
         patch("app.routes.mails.get_webpage_text", return_value="<html>Job</html>"), \
         patch("app.services.portfolio.Portfolio") as MockPortfolio:

        mock_generator = MockGenerator.return_value
        mock_generator.extract_job_details.return_value = mock_job_details
        mock_generator.generate_mail.return_value = "Generated email content"

        mock_portfolio = MockPortfolio.return_value
        mock_portfolio.query.return_value = []

        create_response = client.post(
            "/mails/generate?job_url=https://example.com/job",
            headers={"Authorization": f"Bearer {token}"},
        )
        email_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/mails/{email_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    get_response = client.get(f"/mails/{email_id}", headers={"Authorization": f"Bearer {token}"})
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
