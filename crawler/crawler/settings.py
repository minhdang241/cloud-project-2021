import os

from dotenv import load_dotenv
from pydantic import BaseSettings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
print("NAAAA", os.path.join(BASE_DIR, "crawler/.env"))
load_dotenv(os.path.join(BASE_DIR, "crawler/.env"))


class Settings(BaseSettings):

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
    LIMIT_CAREERS: str = os.getenv("LIMIT_CAREERS")
    LIMIT_PAGE: str = os.getenv("LIMIT_PAGE")


settings = Settings()


BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

DOWNLOAD_DELAY = 0.5

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
