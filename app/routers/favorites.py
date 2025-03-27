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


@router.get("/", response_model=List[ExerciseResponse])
def list_favorites(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    favorites = (
        db.query(Exercise)
        .join(Favorite, Favorite.exercise_id == Exercise.id)
        .filter(Favorite.user_id == current_user_id)
        .all()
    )
    return favorites


@router.post("/{exercise_id}", status_code=204)
def favorite_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    existing = db.query(Favorite).filter(
        Favorite.user_id == current_user_id,
        Favorite.exercise_id == exercise_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already favorited")

    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    favorite = Favorite(user_id=current_user_id, exercise_id=exercise_id)
    db.add(favorite)
    db.commit()


@router.delete("/{exercise_id}", status_code=204)
def unfavorite_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user_id,
        Favorite.exercise_id == exercise_id
    ).first()

    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")

    db.delete(favorite)
    db.commit()
