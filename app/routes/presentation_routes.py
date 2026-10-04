from flask import Blueprint, request, current_app

from app.database import get_connection
from app.models.presentation import Presentation, Slide


presentation_bp = Blueprint(
    "presentations",
    __name__
)


@presentation_bp.post("")
def create_presentation():

    data = request.get_json(silent=True)

    if not data:
        return {
            "error": "Request body must contain JSON data."
        }, 400

    title = data.get("title")
    description = data.get("description", "")

    if not title or not isinstance(title, str):
        return {
            "error": "The 'title' field is required and must be a string."
        }, 400

    title = title.strip()

    if not title:
        return {
            "error": "The 'title' field cannot be empty."
        }, 400

    if not isinstance(description, str):
        return {
            "error": "The 'description' field must be a string."
        }, 400

    connection = get_connection(
        current_app.config["DATABASE_PATH"]
    )

    cursor = connection.execute(
        """
        INSERT INTO presentations (title, description)
        VALUES (?, ?)
        """,
        (title, description)
    )

    presentation_id = cursor.lastrowid

    connection.commit()

    row = connection.execute(
        """
        SELECT id, title, description, created_at, updated_at
        FROM presentations
        WHERE id = ?
        """,
        (presentation_id,)
    ).fetchone()

    connection.close()

    presentation = Presentation(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        created_at=row["created_at"],
        updated_at=row["updated_at"]
    )

    return {
        "message": "Presentation created successfully",
        "presentation": presentation.to_dict()
    }, 201

@presentation_bp.get("")
def list_presentations():

    connection = get_connection(
        current_app.config["DATABASE_PATH"]
    )

    try:
        rows = connection.execute(
            """
            SELECT p.id, p.title, p.description,
                   p.created_at, p.updated_at,
                   COUNT(s.id) AS slide_count
            FROM presentations p
            LEFT JOIN slides s ON s.presentation_id = p.id
            GROUP BY p.id
            ORDER BY p.created_at DESC, p.id DESC
            """
        ).fetchall()

    finally:
        connection.close()

    presentations = []

    for row in rows:

        item = Presentation(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        ).to_dict()

        item["slide_count"] = row["slide_count"]

        presentations.append(item)

    return {
        "count": len(presentations),
        "presentations": presentations
    }, 200


@presentation_bp.get("/<int:presentation_id>")
def get_presentation(presentation_id):

    connection = get_connection(
        current_app.config["DATABASE_PATH"]
    )

    try:
        row = connection.execute(
            """
            SELECT id, title, description, created_at, updated_at
            FROM presentations
            WHERE id = ?
            """,
            (presentation_id,)
        ).fetchone()

        if row is None:
            return {
                "error": "Presentation not found."
            }, 404

        slide_rows = connection.execute(
            """
            SELECT id, presentation_id, slide_order, title,
                   content, created_at, updated_at
            FROM slides
            WHERE presentation_id = ?
            ORDER BY slide_order ASC, id ASC
            """,
            (presentation_id,)
        ).fetchall()

    finally:
        connection.close()

    presentation = Presentation(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        created_at=row["created_at"],
        updated_at=row["updated_at"]
    ).to_dict()

    slides = [
        Slide(
            id=s["id"],
            presentation_id=s["presentation_id"],
            slide_order=s["slide_order"],
            title=s["title"],
            content=s["content"],
            created_at=s["created_at"],
            updated_at=s["updated_at"]
        ).to_dict()
        for s in slide_rows
    ]

    presentation["slides"] = slides
    presentation["slide_count"] = len(slides)

    return {
        "presentation": presentation
    }, 200
@presentation_bp.delete("/<int:presentation_id>")
def delete_presentation(presentation_id):

    connection = get_connection(
        current_app.config["DATABASE_PATH"]
    )

    try:
        row = connection.execute(
            """
            SELECT id FROM presentations
            WHERE id = ?
            """,
            (presentation_id,)
        ).fetchone()

        if row is None:
            return {
                "error": "Presentation not found."
            }, 404

        connection.execute(
            "DELETE FROM slides WHERE presentation_id = ?",
            (presentation_id,)
        )

        connection.execute(
            "DELETE FROM presentations WHERE id = ?",
            (presentation_id,)
        )

        connection.commit()

    finally:
        connection.close()

    return {
        "message": "Presentation deleted successfully"
    }, 200