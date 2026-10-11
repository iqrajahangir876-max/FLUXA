"""FT-12 / T27 - Convert AI response into structured slide data."""

import pytest

from app.services.slide_parser import (
    AIResponseError,
    extract_json,
    parse_slide_content,
    to_slide_records,
)


def test_extract_json_plain():
    assert extract_json('{"a": 1}') == {"a": 1}


def test_extract_json_strips_code_fences():
    assert extract_json('```json\n{"a": 1}\n```') == {"a": 1}


def test_extract_json_ignores_surrounding_prose():
    assert extract_json('Here you go: {"a": 1} Enjoy!') == {"a": 1}


@pytest.mark.parametrize("text", ["", "   ", "no json", "[1, 2]", "{broken"])
def test_extract_json_rejects_bad_input(text):
    with pytest.raises(AIResponseError):
        extract_json(text)


OUTLINE = [{"slide_number": 1, "title": "Planned", "purpose": ""}]


def test_parse_slide_content_falls_back_to_outline_title():
    data = {"slides": [{"key_points": ["  one ", "", 5, "two"]}]}
    slides = parse_slide_content(data, OUTLINE)
    assert slides == [
        {"slide_number": 1, "title": "Planned", "key_points": ["one", "two"]}
    ]


def test_parse_slide_content_requires_key_points():
    with pytest.raises(AIResponseError):
        parse_slide_content({"slides": [{"key_points": []}]}, OUTLINE)


def test_to_slide_records_matches_slides_table_format():
    records = to_slide_records(
        [{"slide_number": 1, "title": "Intro", "key_points": ["A", "B"]}]
    )
    assert records == [
        {"slide_order": 1, "title": "Intro", "content": "- A\n- B"}
    ]
