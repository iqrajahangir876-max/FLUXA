"""FT-12 - End-to-end generation API (AI mocked)."""

from app.config import Config
from app.services import prompt_service
from tests.ft12_helpers import content_json, fake_ai, make_client, outline_json


def configure(monkeypatch, responses):
    monkeypatch.setattr(Config, "OPENROUTER_API_KEY", "test-key")
    monkeypatch.setattr(
        prompt_service, "generate_ai_response", fake_ai(responses)
    )


def test_generate_presentation_saves_slides(tmp_path, monkeypatch):
    client = make_client(tmp_path)
    configure(monkeypatch, [outline_json(2), content_json(2)])

    response = client.post(
        "/api/presentations/generate",
        json={"topic": "AI in Education", "slide_count": 2},
    )

    assert response.status_code == 201
    presentation = response.get_json()["presentation"]
    assert presentation["title"] == "AI in Education"
    assert presentation["slide_count"] == 2
    assert presentation["slides"][0]["content"] == "- Point 1a\n- Point 1b"

    # Saved data is readable through the existing Sprint 1 endpoints
    fetched = client.get(f"/api/presentations/{presentation['id']}")
    assert fetched.get_json()["presentation"]["slide_count"] == 2


def test_generate_uses_custom_title(tmp_path, monkeypatch):
    client = make_client(tmp_path)
    configure(monkeypatch, [outline_json(1), content_json(1)])

    response = client.post(
        "/api/presentations/generate",
        json={"topic": "AI", "slide_count": 1, "title": "My Deck"},
    )

    assert response.get_json()["presentation"]["title"] == "My Deck"


def test_generate_outline_only(tmp_path, monkeypatch):
    client = make_client(tmp_path)
    configure(monkeypatch, [outline_json(2)])

    response = client.post(
        "/api/presentations/generate/outline",
        json={"topic": "AI", "slide_count": 2},
    )

    assert response.status_code == 200
    assert len(response.get_json()["outline"]["slides"]) == 2
    assert client.get("/api/presentations").get_json()["count"] == 0


def test_generate_validation_errors(tmp_path, monkeypatch):
    client = make_client(tmp_path)
    configure(monkeypatch, [])

    url = "/api/presentations/generate"
    assert client.post(url, json={}).status_code == 400
    assert client.post(url, json={"topic": " "}).status_code == 400
    assert client.post(url, json={"topic": "X", "slide_count": 99}).status_code == 400


def test_generate_without_api_key_returns_503(tmp_path, monkeypatch):
    client = make_client(tmp_path)
    monkeypatch.setattr(Config, "OPENROUTER_API_KEY", "")

    response = client.post("/api/presentations/generate", json={"topic": "AI"})

    assert response.status_code == 503


def test_generate_bad_ai_output_returns_502_and_saves_nothing(tmp_path, monkeypatch):
    client = make_client(tmp_path)
    configure(monkeypatch, ["bad", "bad"])

    response = client.post(
        "/api/presentations/generate", json={"topic": "AI", "slide_count": 2}
    )

    assert response.status_code == 502
    assert client.get("/api/presentations").get_json()["count"] == 0
