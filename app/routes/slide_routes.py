from flask import Blueprint, request, current_app

from app.database import get_connection
from app.models.presentation import Slide


slide_bp = Blueprint(
    "slides",
    __name__
)


def row_to_slide(row):

    return Slide(
        id=row["id"],
        presentation_id=row["presentation_id"],
        slide_order=row["slide_order"],
        title=row["title"],
        content=row["content"],
        created_at=row["created_at"],
        updated_at=row["updated_at"]
    )


def presentation_exists(connection, presentation_id):

    row = connection.execute(
        "SELECT id FROM presentations WHERE id = ?",
        (presentation_id,)
    ).fetchone()

    return row is not None


@slide_bp.post("/<int:presentation_id>/slides")
def add_slide(presentation_id):

    data = request.get_json(silent=True)

    if not data or not isinstance(data, dict):
        return {
            "error": "Request body must contain JSON data."
        }, 400

    title = data.get("title", "")
    content = data.get("content", "")
    slide_order = data.get("slide_order")

    if not isinstance(title, str):
        return {
            "error": "The 'title' field must be a string."
        }, 400

    if not isinstance(content, str):
        return {
            "error": "The 'content' field must be a string."
        }, 400

    if slide_order is not None:
        if (
            not isinstance(slide_order, int)
            or isinstance(slide_order, bool)
            or slide_order < 1
        ):
            return {
                "error": "The 'slide_order' field must be a positive integer."
            }, 400

    title = title.strip()

    connection = get_connection(
        current_app.config["DATABASE_PATH"]
    )

    try:
        if not presentation_exists(connection, presentation_id):
            return {
                "error": "Presentation not found."
            }, 404

        max_order = connection.execute(
            """
            SELECT COALESCE(MAX(slide_order), 0) AS max_order
            FROM slides
            WHERE presentation_id = ?
            """,
            (presentation_id,)
        ).fetchone()["max_order"]

        if slide_order is None or slide_order > max_order + 1:
            # Append to the end
            slide_order = max_order + 1
        else:
            # Insert in the middle: shift later slides down
            connection.execute(
                """
                UPDATE slides
                SET slide_order = slide_order + 1
                WHERE presentation_id = ?
                  AND slide_order >= ?
                """,
                (presentation_id, slide_order)
            )

        cursor = connection.execute(
            """
            INSERT INTO slides
                (presentation_id, slide_order, title, content)
            VALUES (?, ?, ?, ?)
            """,
            (presentation_id, slide_order, title, content)
        )

        slide_id = cursor.lastrowid

        connection.commit()

        row = connection.execute(
            """
            SELECT id, presentation_id, slide_order, title,
                   content, created_at, updated_at
            FROM slides
            WHERE id = ?
            """,
            (slide_id,)
        ).fetchone()

        slide = row_to_slide(row)

    finally:
        connection.close()

    return {
        "message": "Slide added successfully",
        "slide": slide.to_dict()
    }, 201


@slide_bp.route(
    "/<int:presentation_id>/slides/<int:slide_id>",
    methods=["PUT", "PATCH"]
)
def update_slide(presentation_id, slide_id):

    data = request.get_json(silent=True)

    if not data or not isinstance(data, dict):
        return {
            "error": "Request body must contain JSON data."
        }, 400

    if "title" not in data and "content" not in data:
        return {
            "error": "Provide at least one of 'title' or 'content'."
        }, 400

    fields = []
    values = []

    if "title" in data:
        if not isinstance(data["title"], str):
            return {
                "error": "The 'title' field must be a string."
            }, 400

        fields.append("title = ?")
        values.append(data["title"].strip())

    if "content" in data:
        if not isinstance(data["content"], str):
            return {
                "error": "The 'content' field must be a string."
            }, 400

        fields.append("content = ?")
        values.append(data["content"])

    fields.append("updated_at = CURRENT_TIMESTAMP")

    connection = get_connection(
        current_app.config["DATABASE_PATH"]
    )

    try:
        if not presentation_exists(connection, presentation_id):
            return {
                "error": "Presentation not found."
            }, 404

        existing = connection.execute(
            """
            SELECT id FROM slides
            WHERE id = ? AND presentation_id = ?
            """,
            (slide_id, presentation_id)
        ).fetchone()

        if existing is None:
            return {
                "error": "Slide not found."
            }, 404

        connection.execute(
            f"""
            UPDATE slides
            SET {", ".join(fields)}
            WHERE id = ? AND presentation_id = ?
            """,
            (*values, slide_id, presentation_id)
        )

        connection.commit()

        row = connection.execute(
            """
            SELECT id, presentation_id, slide_order, title,
                   content, created_at, updated_at
            FROM slides
            WHERE id = ?
            """,
            (slide_id,)
        ).fetchone()

        slide = row_to_slide(row)

    finally:
        connection.close()

    return {
        "message": "Slide updated successfully",
        "slide": slide.to_dict()
    }, 200

@slide_bp.get("/<int:presentation_id>/slides")
def list_slides(presentation_id):

    connection = get_connection(
        current_app.config["DATABASE_PATH"]
    )

    try:
        if not presentation_exists(connection, presentation_id):
            return {
                "error": "Presentation not found."
            }, 404

        rows = connection.execute(
            """
            SELECT id, presentation_id, slide_order, title,
                   content, created_at, updated_at
            FROM slides
            WHERE presentation_id = ?
            ORDER BY slide_order ASC, id ASC
            """,
            (presentation_id,)
        ).fetchall()

        slides = [row_to_slide(row).to_dict() for row in rows]

    finally:
        connection.close()

    return {
        "presentation_id": presentation_id,
        "count": len(slides),
        "slides": slides
    }, 200


@slide_bp.get("/<int:presentation_id>/slides/<int:slide_id>")
def get_slide(presentation_id, slide_id):

    connection = get_connection(
        current_app.config["DATABASE_PATH"]
    )

    try:
        if not presentation_exists(connection, presentation_id):
            return {
                "error": "Presentation not found."
            }, 404

        row = connection.execute(
            """
            SELECT id, presentation_id, slide_order, title,
                   content, created_at, updated_at
            FROM slides
            WHERE id = ? AND presentation_id = ?
            """,
            (slide_id, presentation_id)
        ).fetchone()

        if row is None:
            return {
                "error": "Slide not found."
            }, 404

        slide = row_to_slide(row)

    finally:
        connection.close()

    return {
        "slide": slide.to_dict()
    }, 200