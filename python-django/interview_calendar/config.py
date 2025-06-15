import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/postgres")

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TEST_DATABASE_URI",
        "postgresql+psycopg://postgres:postgres@localhost:5432/test_db"
    )
    TESTING = True
    WTF_CSRF_ENABLED = False