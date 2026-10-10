
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

    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "")
    OPENROUTER_FALLBACK_MODEL = os.getenv("OPENROUTER_FALLBACK_MODEL", "")


    OPENROUTER_BASE_URL = os.getenv(
        "OPENROUTER_BASE_URL",
        "https://openrouter.ai/api/v1"
    )
