
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def get_database_url():
    required = [DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD]

    if not all(required):
        raise ValueError("Missing database configuration in .env")

    return (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


engine = create_engine(
    get_database_url(),
    pool_pre_ping=True
)


def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Database connection successful!")
            print(f"Test query result: {result.scalar()}")

    except (SQLAlchemyError, ValueError) as error:
        print(f"Database connection failed: {error}")


if __name__ == "__main__":
    test_connection()
