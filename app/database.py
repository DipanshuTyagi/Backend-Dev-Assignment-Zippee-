# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from app import config

# SQLAlchemy engine
engine = create_engine(
    config.SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False}  # SQLite-specific
)

# Scoped session (thread-safe for Flask apps)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Base model class
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """
    Initialize the database.

    - Imports all SQLAlchemy models so that `Base.metadata.create_all()`
      can detect them and create the corresponding tables.
    - Creates all tables in the SQLite database if they don't already exist.
    """
    # Import all models here
    from app.models.user import User
    from app.models.task import Task

    # Create tables in the database
    Base.metadata.create_all(bind=engine)