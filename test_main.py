from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_login_user():

    response = client.post(
        "/login-user", json={"username": "example", "password": "password"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Login successful", "username": "example"}

    response = client.post(
        "/login-user", json={"username": "example", "password": "wrong_password"}
    )
    assert response.status_code == 401


def test_shorten_url():
    response = client.post("/shorten", data={"original_url": "https://example.com"})
    assert response.status_code == 201
    assert "short_url" in response.text


def test_generate_qr():
    response = client.get("/generate_qr?url=https://example.com")
    assert response.status_code == 200
    assert "qr" in response.text


def test_redirect_to_original():
    response = client.get("/abc123")
    assert response.status_code == 303


def test_record_analytics():
    response = client.get("/yuh?shortened_url=abc123")
    assert response.status_code == 200


def test_link_analytics():
    response = client.get("/link-analytics?short_url=abc123")
    assert response.status_code == 200


def test_user_link_history():
    response = client.get("/history/1")
    assert response.status_code == 200
