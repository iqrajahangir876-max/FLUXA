"""FT-12 / T24 - Send user presentation prompt to the AI."""

import pytest

from app.services import prompt_service
from app.services.slide_parser import AIResponseError
from tests.ft12_helpers import fake_ai


def test_send_prompt_returns_raw_text(monkeypatch):
    fake = fake_ai(["hello"])
    monkeypatch.setattr(prompt_service, "generate_ai_response", fake)

    assert prompt_service.send_prompt("Topic", "System") == "hello"
    assert fake.calls == [("Topic", "System")]


def test_send_prompt_rejects_empty_prompt():
    with pytest.raises(ValueError):
        prompt_service.send_prompt("   ")


def test_send_prompt_for_json_retries_on_bad_json(monkeypatch):
    fake = fake_ai(["not json", '{"ok": true}'])
    monkeypatch.setattr(prompt_service, "generate_ai_response", fake)

    assert prompt_service.send_prompt_for_json("p") == {"ok": True}
    assert len(fake.calls) == 2


def test_send_prompt_for_json_gives_up_after_max_attempts(monkeypatch):
    monkeypatch.setattr(
        prompt_service, "generate_ai_response", fake_ai(["bad", "bad"])
    )

    with pytest.raises(AIResponseError):
        prompt_service.send_prompt_for_json("p")
