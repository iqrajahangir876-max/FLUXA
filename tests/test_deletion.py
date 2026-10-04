from app import create_app
from app.database import init_db


def make_client(tmp_path):
    db_path = str(tmp_path / "test.db")
    app = create_app()
    app.config["TESTING"] = True
    app.config["DATABASE_PATH"] = db_path
    init_db(db_path)
    return app.test_client()


def create_presentation(client, title="Deck"):
    response = client.post(
        "/api/presentations",
        json={"title": title, "description": "Sprint 1"}
    )
    return response.get_json()["presentation"]["id"]


def add_slide(client, pid, title, **extra):
    response = client.post(
        f"/api/presentations/{pid}/slides",
        json={"title": title, "content": f"{title} body", **extra}
    )
    return response.get_json()["slide"]


def test_delete_presentation(tmp_path):
    client = make_client(tmp_path)
    pid = create_presentation(client)

    response = client.delete(f"/api/presentations/{pid}")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Presentation deleted successfully"

    check = client.get(f"/api/presentations/{pid}")
    assert check.status_code == 404


def test_delete_presentation_not_found(tmp_path):
    client = make_client(tmp_path)
    response = client.delete("/api/presentations/999")
    assert response.status_code == 404


def test_delete_presentation_also_deletes_its_slides(tmp_path):
    client = make_client(tmp_path)
    pid = create_presentation(client)
    add_slide(client, pid, "A")
    add_slide(client, pid, "B")

    client.delete(f"/api/presentations/{pid}")

    check = client.get(f"/api/presentations/{pid}/slides")
    assert check.status_code == 404


def test_delete_slide(tmp_path):
    client = make_client(tmp_path)
    pid = create_presentation(client)
    slide = add_slide(client, pid, "Intro")

    response = client.delete(f"/api/presentations/{pid}/slides/{slide['id']}")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Slide deleted successfully"

    check = client.get(f"/api/presentations/{pid}/slides/{slide['id']}")
    assert check.status_code == 404


def test_delete_slide_not_found(tmp_path):
    client = make_client(tmp_path)
    pid = create_presentation(client)
    response = client.delete(f"/api/presentations/{pid}/slides/999")
    assert response.status_code == 404


def test_delete_slide_from_wrong_presentation_returns_404(tmp_path):
    client = make_client(tmp_path)
    pid_a = create_presentation(client, "A")
    pid_b = create_presentation(client, "B")
    slide = add_slide(client, pid_a, "Only in A")

    response = client.delete(f"/api/presentations/{pid_b}/slides/{slide['id']}")
    assert response.status_code == 404