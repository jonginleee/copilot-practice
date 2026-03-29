from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base

DB_FILE = Path(__file__).resolve().parents[1] / "data" / "kiosk.sqlite3"
DATABASE_URL = f"sqlite:///{DB_FILE.as_posix()}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def init_db() -> None:
    # Ensure model metadata is loaded before table creation.
    from app.db import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
