"""
Endpoints for saving/unsaving an exercise.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Saved, Exercise
from app.core.security import get_current_user_id

router = APIRouter(prefix="/saves", tags=["Saves"])

@router.post("/{exercise_id}", status_code=204)
def save_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """
    Save an exercise for the authenticated user.
    """
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    existing = db.query(Saved).filter(
        Saved.user_id == current_user_id,
        Saved.exercise_id == exercise_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already saved")

    new_save = Saved(user_id=current_user_id, exercise_id=exercise_id)
    db.add(new_save)
    db.commit()

@router.delete("/{exercise_id}", status_code=204)
def unsave_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """
    Unsave an exercise for the authenticated user.
    """
    saved_record = db.query(Saved).filter(
        Saved.user_id == current_user_id,
        Saved.exercise_id == exercise_id
    ).first()

    if not saved_record:
        raise HTTPException(status_code=404, detail="Save record not found")

    db.delete(saved_record)
    db.commit()
