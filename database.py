"""
Module that sets up SQLAlchemy's engine, session, and Base (the declarative base for models). Using SQLite for the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Define the database URL; here, SQLite is used with a local file "test.db". This'll get placed in the root directory of your project. 
DATABASE_URL = "sqlite:///./test.db"

# Create an engine. The "check_same_thread" flag is set for SQLite to work properly with multiple threads.
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},  # Required for SQLite
    echo=True  # Echo SQL statements to help with debugging
)

# Create a configured "SessionLocal" class; this will be our database session factory.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our models using SQLAlchemy's declarative base.
Base = declarative_base()

def get_db():
    """
    Dependency that creates a new database session for a request,
    then closes the session after the request is complete.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
