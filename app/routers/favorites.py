"""
Handles operations relating to favoriting exercises: favorite, unfavorite, list
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db.models import Favorite, Exercise
from app.core.security import get_current_user_id
from app.schemas.exercise import ExerciseResponse

router = APIRouter(prefix="/favorites", tags=["Favorites"])

@router.post("/{exercise_id}", status_code=204)
def favorite_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    # Check if exercise exists
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(404, "Exercise not found")
    # Check if already favorited
    existing = db.query(Favorite).filter(
        Favorite.user_id == current_user_id,
        Favorite.exercise_id == exercise_id
    ).first()
    if existing:
        raise HTTPException(400, "Already favorited")
    # Add new favorite
    fav = Favorite(user_id=current_user_id, exercise_id=exercise_id)
    db.add(fav)
    db.commit()

@router.delete("/{exercise_id}", status_code=204)
def unfavorite_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    fav = db.query(Favorite).filter(
        Favorite.user_id == current_user_id,
        Favorite.exercise_id == exercise_id
    ).first()
    if not fav:
        raise HTTPException(404, "Favorite not found")
    db.delete(fav)
    db.commit()

@router.get("/", response_model=List[ExerciseResponse])
def list_favorites(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    # Return the exercises that the user has favorited
    exercises = (
        db.query(Exercise)
        .join(Favorite, Favorite.exercise_id == Exercise.id)
        .filter(Favorite.user_id == current_user_id)
        .all()
    )
    return exercises
