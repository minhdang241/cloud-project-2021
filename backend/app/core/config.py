import os
from typing import List

from dotenv import load_dotenv
from pydantic import BaseSettings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
load_dotenv(os.path.join(BASE_DIR, "env/.env"))


class Settings(BaseSettings):
    API_PREFIX: str = os.getenv("API_PREFIX", "/api")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "CLOUD PROJECT")
    BACKEND_CORS_ORIGINS: List[str] = [
        # React localhost
        os.getenv("FRONTEND_ADDRESS"),
        "http://localhost:3000",
        "http://localhost",
        "http://ec2-13-250-100-229.ap-southeast-1.compute.amazonaws.com:3000"
    ]
    # BACKEND_ADDRESS: str = os.getenv("BACKEND_ADDRESS")

    # Postgres db information
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
    POSTGRES_DB_NAME: str = os.getenv("POSTGRES_DB_NAME")
    SQLALCHEMY_DATABASE_URL: str = "postgresql://{}:{}@{}:{}/{}".format(
        os.getenv("POSTGRES_USER"),
        os.getenv("POSTGRES_PASSWORD"),
        os.getenv("POSTGRES_HOST"),
        os.getenv("POSTGRES_PORT"),
        os.getenv("POSTGRES_DB_NAME"),
    )

    # NAMESPACE: str = os.getenv("NAMESPACE")

    # List of docker images
    # SAMPLE_IMAGE: str = os.getenv("SAMPLE_IMAGE")


settings = Settings()
