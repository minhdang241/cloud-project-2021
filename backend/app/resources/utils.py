import psycopg2

from app.core.config import settings
from app.db.postgres.setup_postgres import SessionLocal


def get_db():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


def connect_psycopg2():
    return psycopg2.connect(
        dbname=settings.POSTGRES_DB_NAME,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
    )
