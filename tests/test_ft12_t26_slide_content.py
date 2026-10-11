"""FT-12 / T26 - Generate slide content using the AI."""

import pytest

from app.prompts.slide_content import build_slide_content_prompt
from app.services import prompt_service, slide_content_service
from app.services.slide_parser import AIResponseError
from tests.ft12_helpers import content_json, fake_ai

OUTLINE = {
    "title": "AI in Education",
    "slides": [
        {"slide_number": 1, "title": "Slide 1", "purpose": "P1"},
        {"slide_number": 2, "title": "Slide 2", "purpose": "P2"},
    ],
}


def test_content_prompt_includes_outline():
    prompt = build_slide_content_prompt("AI", OUTLINE["title"], OUTLINE["slides"])
    assert "Slide 1" in prompt and "Slide 2" in prompt


def test_content_prompt_requires_outline():
    with pytest.raises(ValueError):
        build_slide_content_prompt("AI", "T", [])


def test_generate_slide_content(monkeypatch):
    monkeypatch.setattr(
        prompt_service, "generate_ai_response", fake_ai([content_json(2)])
    )

    slides = slide_content_service.generate_slide_content("AI", OUTLINE)

    assert slides[0]["key_points"] == ["Point 1a", "Point 1b"]
    assert len(slides) == 2


def test_generate_slide_content_count_mismatch(monkeypatch):
    monkeypatch.setattr(
        prompt_service, "generate_ai_response", fake_ai([content_json(1)])
    )

    with pytest.raises(AIResponseError):
        slide_content_service.generate_slide_content("AI", OUTLINE)
