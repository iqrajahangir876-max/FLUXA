import os

from flask import Flask
from dotenv import load_dotenv

from app.config import Config
from app.database import init_db
from app.routes.presentation_routes import presentation_bp
from app.routes.slide_routes import slide_bp


def create_app():

    load_dotenv()

    app = Flask(__name__)

    app.config.from_object(Config)

    os.makedirs(
        os.path.dirname(
            app.config["DATABASE_PATH"]
        ),
        exist_ok=True
    )

    init_db(
        app.config["DATABASE_PATH"]
    )

    app.register_blueprint(
        presentation_bp,
        url_prefix="/api/presentations"
    )

    app.register_blueprint(
        slide_bp,
        url_prefix="/api/presentations"
    )

    @app.get("/api/health")
    def health_check():

        return {
            "status": "success",
            "message": "FLUXA backend is running"
        }, 200

    return app