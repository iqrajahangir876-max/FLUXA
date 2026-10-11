"""FT-12 - Orchestrates T24-T27: prompt -> outline -> content -> slide data."""

from app.database import get_connection
from app.services.outline_service import generate_outline
from app.services.slide_content_service import generate_slide_content
from app.services.slide_parser import to_slide_records


def generate_structured_slides(
    topic: str,
    slide_count: int = 8,
    audience: str = "General audience",
    language: str = "English",
) -> dict:
    """Run the full AI pipeline and return
    {"title": str, "slides": [{slide_order, title, content}]}."""

    outline = generate_outline(topic, slide_count, audience, language)
    slides = generate_slide_content(topic, outline, audience, language)

    return {
        "title": outline["title"],
        "slides": to_slide_records(slides),
    }


def save_generated_presentation(
    database_path: str,
    title: str,
    description: str,
    slides: list,
) -> dict:
    """Store a generated presentation and its slides; return the saved rows."""

    connection = get_connection(database_path)

    try:
        cursor = connection.execute(
            "INSERT INTO presentations (title, description) VALUES (?, ?)",
            (title, description),
        )
        presentation_id = cursor.lastrowid

        connection.executemany(
            """
            INSERT INTO slides (presentation_id, slide_order, title, content)
            VALUES (?, ?, ?, ?)
            """,
            [
                (presentation_id, s["slide_order"], s["title"], s["content"])
                for s in slides
            ],
        )
        connection.commit()

        presentation = dict(connection.execute(
            """
            SELECT id, title, description, created_at, updated_at
            FROM presentations WHERE id = ?
            """,
            (presentation_id,),
        ).fetchone())

        slide_rows = connection.execute(
            """
            SELECT id, presentation_id, slide_order, title,
                   content, created_at, updated_at
            FROM slides WHERE presentation_id = ?
            ORDER BY slide_order ASC, id ASC
            """,
            (presentation_id,),
        ).fetchall()
    finally:
        connection.close()

    presentation["slides"] = [dict(r) for r in slide_rows]
    presentation["slide_count"] = len(slide_rows)

    return presentation
