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
        os.getenv("FRONTEND_ADDRESS", "http://localhost"),
        "http://localhost:3000",
        "http://ec2-13-250-100-229.ap-southeast-1.compute.amazonaws.com:3000"
    ]

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
    CRAWLER_IMAGE: str = os.getenv('CRAWLER_IMAGE')
    LIMIT_CAREERS: str = os.getenv("LIMIT_CAREERS")
    LIMIT_PAGE: str = os.getenv("LIMIT_PAGE")
    UPDATE_REQUEST_URL: str = os.getenv("UPDATE_REQUEST_URL")
    LIMIT_JOB: str = os.getenv("LIMIT_JOB")
    AWS_ACCESS_KEY: str = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_KEY: str = os.getenv("AWS_SECRET_KEY")
    AWS_REGION: str = os.getenv("AWS_REGION")
    SENDER: str = os.getenv("SENDER")
    RECIPIENT: str = os.getenv("RECIPIENT")
    ACCESS_TOKEN: str = os.getenv("ACCESS_TOKEN")

    AWS_COGNITO_USER_POOL: str = os.getenv("AWS_COGNITO_USER_POOL")
    AWS_COGNITO_CLIENT_ID: str = os.getenv("AWS_COGNITO_CLIENT_ID")


settings = Settings()
