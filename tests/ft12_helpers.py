import json

from app import create_app
from app.database import init_db


def make_client(tmp_path):
    db_path = str(tmp_path / "test.db")
    app = create_app()
    app.config["TESTING"] = True
    app.config["DATABASE_PATH"] = db_path
    init_db(db_path)
    return app.test_client()


def outline_json(n=2):
    return json.dumps({
        "title": "AI in Education",
        "slides": [
            {"slide_number": i, "title": f"Slide {i}", "purpose": f"Purpose {i}"}
            for i in range(1, n + 1)
        ],
    })


def content_json(n=2):
    return json.dumps({
        "slides": [
            {"slide_number": i, "title": f"Slide {i}",
             "key_points": [f"Point {i}a", f"Point {i}b"]}
            for i in range(1, n + 1)
        ],
    })


def fake_ai(responses):
    """Return a stand-in for generate_ai_response that yields responses in order."""
    queue = list(responses)
    calls = []

    def _fake(prompt, system_prompt=""):
        calls.append((prompt, system_prompt))
        return queue.pop(0)

    _fake.calls = calls
    return _fake
