import os

from dotenv import load_dotenv


load_dotenv()


class Config:

    DEBUG = os.getenv(
        "FLASK_DEBUG",
        "False"
    ).lower() == "true"

    PORT = int(
        os.getenv(
            "PORT",
            "5000"
        )
    )

    DATABASE_PATH = os.getenv(
        "DATABASE_PATH",
        "instance/fluxa.db"
    )