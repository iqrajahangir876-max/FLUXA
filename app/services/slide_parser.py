"""FT-12 / T27 - Convert Claude/AI responses into structured slide data."""

import json
import re


class AIResponseError(ValueError):
    """Raised when an AI response cannot be turned into valid slide data."""


_FENCE = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE)


def extract_json(text: str) -> dict:
    """Parse a JSON object from raw AI text.

    Handles responses wrapped in Markdown code fences or surrounded by
    extra prose.
    """

    if not isinstance(text, str) or not text.strip():
        raise AIResponseError("AI returned an empty response.")

    cleaned = _FENCE.sub("", text.strip()).strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        start, end = cleaned.find("{"), cleaned.rfind("}")

        if start == -1 or end <= start:
            raise AIResponseError("AI returned invalid JSON.") from None

        try:
            data = json.loads(cleaned[start:end + 1])
        except json.JSONDecodeError as error:
            raise AIResponseError("AI returned invalid JSON.") from error

    if not isinstance(data, dict):
        raise AIResponseError("AI response must be a JSON object.")

    return data


def _clean_text(value, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AIResponseError(f"Slide field '{field}' must be a non-empty string.")

    return value.strip()


def parse_outline(data: dict, slide_count: int) -> dict:
    """Validate an outline response.

    Returns {"title": str, "slides": [{"slide_number", "title", "purpose"}]}.
    """

    slides = data.get("slides")

    if not isinstance(slides, list) or not slides:
        raise AIResponseError("Outline must contain a non-empty slides list.")

    if len(slides) != slide_count:
        raise AIResponseError(
            f"Expected {slide_count} slides, but AI returned {len(slides)}."
        )

    outline = []

    for index, slide in enumerate(slides, start=1):
        if not isinstance(slide, dict):
            raise AIResponseError("Each outline slide must be an object.")

        purpose = slide.get("purpose", "")

        outline.append({
            "slide_number": index,
            "title": _clean_text(slide.get("title"), "title"),
            "purpose": purpose.strip() if isinstance(purpose, str) else "",
        })

    return {
        "title": _clean_text(data.get("title"), "title"),
        "slides": outline,
    }


def parse_slide_content(data: dict, outline: list) -> list:
    """Validate slide-content response against the outline.

    Returns [{"slide_number", "title", "key_points": [str, ...]}].
    """

    slides = data.get("slides")

    if not isinstance(slides, list):
        raise AIResponseError("Slide content must contain a slides list.")

    if len(slides) != len(outline):
        raise AIResponseError(
            f"Expected content for {len(outline)} slides, "
            f"but AI returned {len(slides)}."
        )

    parsed = []

    for index, (slide, planned) in enumerate(zip(slides, outline), start=1):
        if not isinstance(slide, dict):
            raise AIResponseError("Each slide must be an object.")

        points = slide.get("key_points")

        if not isinstance(points, list):
            raise AIResponseError("Slide field 'key_points' must be a list.")

        points = [p.strip() for p in points if isinstance(p, str) and p.strip()]

        if not points:
            raise AIResponseError(f"Slide {index} has no key points.")

        title = slide.get("title")

        parsed.append({
            "slide_number": index,
            "title": title.strip()
            if isinstance(title, str) and title.strip()
            else planned["title"],
            "key_points": points,
        })

    return parsed


def to_slide_records(slides: list) -> list:
    """Convert parsed slides into rows matching the `slides` table.

    `content` is stored as bullet lines ("- point"), which is the format
    the frontend SlidePreview already renders.
    """

    return [
        {
            "slide_order": slide["slide_number"],
            "title": slide["title"],
            "content": "\n".join(f"- {p}" for p in slide["key_points"]),
        }
        for slide in slides
    ]
