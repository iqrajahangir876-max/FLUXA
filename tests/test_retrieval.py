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


def test_list_presentations(tmp_path):

    client = make_client(tmp_path)

    pid = create_presentation(client, "First")
    create_presentation(client, "Second")
    add_slide(client, pid, "A")

    response = client.get("/api/presentations")

    assert response.status_code == 200

    data = response.get_json()

    assert data["count"] == 2

    by_title = {p["title"]: p for p in data["presentations"]}

    assert by_title["First"]["slide_count"] == 1
    assert by_title["Second"]["slide_count"] == 0


def test_list_presentations_empty(tmp_path):

    client = make_client(tmp_path)

    response = client.get("/api/presentations")

    assert response.status_code == 200
    assert response.get_json()["count"] == 0
    assert response.get_json()["presentations"] == []


def test_get_presentation_with_ordered_slides(tmp_path):

    client = make_client(tmp_path)
    pid = create_presentation(client)

    add_slide(client, pid, "A")
    add_slide(client, pid, "B")
    add_slide(client, pid, "C", slide_order=1)

    response = client.get(f"/api/presentations/{pid}")

    assert response.status_code == 200

    presentation = response.get_json()["presentation"]

    assert presentation["id"] == pid
    assert presentation["title"] == "Deck"
    assert presentation["slide_count"] == 3

    titles = [s["title"] for s in presentation["slides"]]

    assert titles == ["C", "A", "B"]


def test_get_presentation_not_found(tmp_path):

    client = make_client(tmp_path)

    response = client.get("/api/presentations/999")

    assert response.status_code == 404


def test_list_slides(tmp_path):

    client = make_client(tmp_path)
    pid = create_presentation(client)

    add_slide(client, pid, "A")
    add_slide(client, pid, "B")

    response = client.get(f"/api/presentations/{pid}/slides")

    assert response.status_code == 200

    data = response.get_json()

    assert data["count"] == 2
    assert [s["title"] for s in data["slides"]] == ["A", "B"]


def test_list_slides_presentation_not_found(tmp_path):

    client = make_client(tmp_path)

    response = client.get("/api/presentations/999/slides")

    assert response.status_code == 404


def test_get_single_slide(tmp_path):

    client = make_client(tmp_path)
    pid = create_presentation(client)
    slide = add_slide(client, pid, "Intro")

    response = client.get(
        f"/api/presentations/{pid}/slides/{slide['id']}"
    )

    assert response.status_code == 200
    assert response.get_json()["slide"]["title"] == "Intro"


def test_get_slide_not_found(tmp_path):

    client = make_client(tmp_path)
    pid = create_presentation(client)

    response = client.get(f"/api/presentations/{pid}/slides/999")

    assert response.status_code == 404


def test_get_slide_from_other_presentation_returns_404(tmp_path):

    client = make_client(tmp_path)

    pid_a = create_presentation(client, "A")
    pid_b = create_presentation(client, "B")

    slide = add_slide(client, pid_a, "Only in A")

    response = client.get(
        f"/api/presentations/{pid_b}/slides/{slide['id']}"
    )

    assert response.status_code == 404