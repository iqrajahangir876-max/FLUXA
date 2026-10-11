"""FT-12 / T25 - Generate presentation outline using the AI."""

import pytest

from app.prompts.outline import build_outline_prompt
from app.services import outline_service, prompt_service
from app.services.slide_parser import AIResponseError
from tests.ft12_helpers import fake_ai, outline_json


def test_outline_prompt_contains_request_details():
    prompt = build_outline_prompt("Solar energy", 5, "Students", "English")
    assert "Solar energy" in prompt and "5" in prompt and "Students" in prompt


@pytest.mark.parametrize("topic,count", [("", 5), ("  ", 5), ("X", 0), ("X", 31)])
def test_outline_prompt_validation(topic, count):
    with pytest.raises(ValueError):
        build_outline_prompt(topic, count)


def test_generate_outline(monkeypatch):
    monkeypatch.setattr(
        prompt_service, "generate_ai_response", fake_ai([outline_json(3)])
    )

    outline = outline_service.generate_outline("AI", slide_count=3)

    assert outline["title"] == "AI in Education"
    assert [s["title"] for s in outline["slides"]] == ["Slide 1", "Slide 2", "Slide 3"]


def test_generate_outline_wrong_slide_count(monkeypatch):
    monkeypatch.setattr(
        prompt_service, "generate_ai_response", fake_ai([outline_json(2)])
    )

    with pytest.raises(AIResponseError):
        outline_service.generate_outline("AI", slide_count=5)
