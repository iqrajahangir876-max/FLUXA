from app import create_app
from app.database import init_db


def test_health():

    app = create_app()

    app.config["TESTING"] = True

    with app.test_client() as client:

        response = client.get(
            "/api/health"
        )

        assert response.status_code == 200

        assert response.get_json()["status"] == "success"


def test_create_presentation(tmp_path):

    db_path = str(
        tmp_path / "test.db"
    )

    app = create_app()

    app.config["TESTING"] = True

    app.config["DATABASE_PATH"] = db_path

    init_db(db_path)

    with app.test_client() as client:

        response = client.post(
            "/api/presentations",
            json={
                "title": "Test Presentation",
                "description": "Created during Sprint 1"
            }
        )

        assert response.status_code == 201

        data = response.get_json()

        assert (
            data["presentation"]["title"]
            == "Test Presentation"
        )