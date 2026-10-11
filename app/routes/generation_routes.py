"""FT-12 - API routes for AI presentation generation (T24-T27)."""

from flask import Blueprint, request, current_app

from app.config import Config
from app.services.generation_service import (
    generate_structured_slides,
    save_generated_presentation,
)
from app.services.outline_service import generate_outline
from app.services.slide_parser import AIResponseError


generation_bp = Blueprint(
    "generation",
    __name__
)


def read_request():
    """Validate the shared request body. Returns (values, error_response)."""

    data = request.get_json(silent=True)

    if not data or not isinstance(data, dict):
        return None, ({"error": "Request body must contain JSON data."}, 400)

    topic = data.get("topic")

    if not isinstance(topic, str) or not topic.strip():
        return None, ({"error": "The 'topic' field is required."}, 400)

    slide_count = data.get("slide_count", 8)

    if (
        not isinstance(slide_count, int)
        or isinstance(slide_count, bool)
        or not 1 <= slide_count <= 30
    ):
        return None, ({
            "error": "The 'slide_count' field must be between 1 and 30."
        }, 400)

    audience = data.get("audience") or "General audience"
    language = data.get("language") or "English"
    title = data.get("title", "")

    if not all(isinstance(v, str) for v in (audience, language, title)):
        return None, ({
            "error": "'audience', 'language' and 'title' must be strings."
        }, 400)

    return {
        "topic": topic.strip(),
        "slide_count": slide_count,
        "audience": audience.strip(),
        "language": language.strip(),
        "title": title.strip(),
    }, None


def run_ai(action):
    """Run an AI action and translate failures into API errors."""

    if not Config.OPENROUTER_API_KEY:
        return None, ({"error": "AI service is not configured."}, 503)

    try:
        return action(), None
    except AIResponseError as error:
        return None, ({"error": str(error)}, 502)
    except ValueError as error:
        return None, ({"error": str(error)}, 400)
    except RuntimeError as error:
        return None, ({"error": f"AI request failed: {error}"}, 502)


@generation_bp.post("/generate/outline")
def generate_outline_route():
    """T24 + T25: send the prompt to the AI and return an outline."""

    values, error = read_request()
    if error:
        return error

    outline, error = run_ai(lambda: generate_outline(
        values["topic"], values["slide_count"],
        values["audience"], values["language"],
    ))
    if error:
        return error

    return {"outline": outline}, 200


@generation_bp.post("/generate")
def generate_presentation_route():
    """T24-T27: generate a full presentation and save it."""

    values, error = read_request()
    if error:
        return error

    generated, error = run_ai(lambda: generate_structured_slides(
        values["topic"], values["slide_count"],
        values["audience"], values["language"],
    ))
    if error:
        return error

    presentation = save_generated_presentation(
        current_app.config["DATABASE_PATH"],
        title=values["title"] or generated["title"],
        description=values["topic"],
        slides=generated["slides"],
    )

    return {
        "message": "Presentation generated successfully",
        "presentation": presentation,
    }, 201