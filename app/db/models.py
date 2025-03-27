"""
Defines SQLAlchemy models for User, Exercise, Favorite, Saved, and Rating.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    UniqueConstraint,
    Index
)
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    """
    User model:
    - id (PK)
    - username (unique)
    - hashed_password
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
    saved_exercises = relationship("Saved", back_populates="user", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="user", cascade="all, delete-orphan")

class Exercise(Base):
    """
    Exercise model:
    - id (PK)
    - name
    - description
    - difficulty
    - is_public
    - owner_id (FK to User)
    """
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    difficulty = Column(Integer, nullable=False, default=1)
    is_public = Column(Boolean, nullable=False, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    __table_args__ = (
        Index("idx_exercises_owner_public", "owner_id", "is_public"),
    )

class Favorite(Base):
    """
    Favorite model:
    - user_id (FK to User)
    - exercise_id (FK to Exercise)
    - unique combo (user_id, exercise_id)
    """
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)

    user = relationship("User", back_populates="favorites")

    __table_args__ = (
        UniqueConstraint("user_id", "exercise_id", name="unique_user_favorite"),
    )

class Saved(Base):
    """
    Saved model:
    - user_id (FK to User)
    - exercise_id (FK to Exercise)
    - unique combo (user_id, exercise_id)
    """
    __tablename__ = "saved"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)

    user = relationship("User", back_populates="saved_exercises")

    __table_args__ = (
        UniqueConstraint("user_id", "exercise_id", name="unique_user_saved"),
    )

class Rating(Base):
    """
    Rating model:
    - user_id (FK to User)
    - exercise_id (FK to Exercise)
    - rating (1-5)
    - unique combo (user_id, exercise_id)
    """
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    rating = Column(Integer, nullable=False)

    user = relationship("User", back_populates="ratings")

    __table_args__ = (
        UniqueConstraint("user_id", "exercise_id", name="unique_user_rating"),
    )
