from fastapi.testclient import TestClient
import json
from app.main import app

client = TestClient(app)


def test_shorten_url():
    original_url = "https://snapchat.com"
    response = client.post("/shorten", data={"original_url": original_url})
    assert response.status_code == 200
    response_json = response.json()
    assert "short_url" in response_json


def test_create_custom_url():
    response = client.post(
        "/custom_shorten",
        json={"original_url": "https://example.com", "custom_url": "example"},
    )
    assert response.status_code == 200


def test_generate_qr():
    response = client.get("/generate_qr")
    assert response.status_code == 422


def test_redirect_to_original():
    response = client.get("/{shortened_url}")
    assert response.status_code == 404


def test_record_analytics():
    response = client.get("/yuh")
    assert response.status_code == 422


def test_link_analytics():
    response = client.get("/link-analytics")
    assert response.status_code == 404


def test_user_link_history():
    response = client.get("/history/1")
    assert response.status_code == 404
