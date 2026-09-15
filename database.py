"""
Data Access Layer - cau hinh ket noi Database (SQLAlchemy engine/session).
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def getDb():
    """Dependency cung cap 1 DB session cho moi request, dam bao dong session sau khi dung."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
