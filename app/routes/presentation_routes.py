from flask import Blueprint, request, current_app

from app.database import get_connection
from app.models.presentation import Presentation


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