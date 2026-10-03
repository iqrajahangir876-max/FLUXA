from app import create_app
from app.database import init_db


def make_client(tmp_path):

    db_path = str(tmp_path / "test.db")

    app = create_app()
    app.config["TESTING"] = True
    app.config["DATABASE_PATH"] = db_path

    init_db(db_path)

    return app.test_client()


def create_presentation(client):

    response = client.post(
        "/api/presentations",
        json={"title": "Deck", "description": "Sprint 1"}
    )

    return response.get_json()["presentation"]["id"]


def test_add_slide(tmp_path):

    client = make_client(tmp_path)
    pid = create_presentation(client)

    response = client.post(
        f"/api/presentations/{pid}/slides",
        json={"title": "Intro", "content": "Welcome"}
    )

    assert response.status_code == 201

    slide = response.get_json()["slide"]

    assert slide["title"] == "Intro"
    assert slide["content"] == "Welcome"
    assert slide["slide_order"] == 1
    assert slide["presentation_id"] == pid


def test_add_slide_auto_orders_and_inserts(tmp_path):

    client = make_client(tmp_path)
    pid = create_presentation(client)

    url = f"/api/presentations/{pid}/slides"

    first = client.post(url, json={"title": "A"}).get_json()["slide"]
    second = client.post(url, json={"title": "B"}).get_json()["slide"]

    assert first["slide_order"] == 1
    assert second["slide_order"] == 2

    inserted = client.post(
        url,
        json={"title": "C", "slide_order": 1}
    ).get_json()["slide"]

    assert inserted["slide_order"] == 1


def test_add_slide_presentation_not_found(tmp_path):

    client = make_client(tmp_path)

    response = client.post(
        "/api/presentations/999/slides",
        json={"title": "X"}
    )

    assert response.status_code == 404


def test_add_slide_invalid_body(tmp_path):

    client = make_client(tmp_path)
    pid = create_presentation(client)

    response = client.post(
        f"/api/presentations/{pid}/slides",
        json={"title": 123}
    )

    assert response.status_code == 400


def test_update_slide(tmp_path):

    client = make_client(tmp_path)
    pid = create_presentation(client)

    slide = client.post(
        f"/api/presentations/{pid}/slides",
        json={"title": "Old", "content": "Old content"}
    ).get_json()["slide"]

    response = client.put(
        f"/api/presentations/{pid}/slides/{slide['id']}",
        json={"content": "New content"}
    )

    assert response.status_code == 200

    updated = response.get_json()["slide"]

    assert updated["content"] == "New content"
    assert updated["title"] == "Old"


def test_update_slide_not_found(tmp_path):

    client = make_client(tmp_path)
    pid = create_presentation(client)

    response = client.put(
        f"/api/presentations/{pid}/slides/999",
        json={"title": "X"}
    )

    assert response.status_code == 404


def test_update_slide_requires_fields(tmp_path):

    client = make_client(tmp_path)
    pid = create_presentation(client)

    slide = client.post(
        f"/api/presentations/{pid}/slides",
        json={"title": "A"}
    ).get_json()["slide"]

    response = client.put(
        f"/api/presentations/{pid}/slides/{slide['id']}",
        json={}
    )

    assert response.status_code == 400