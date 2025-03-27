"""
Endpoints for saving/unsaving an exercise.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Saved, Exercise
from app.core.security import get_current_user_id

router = APIRouter(prefix="/saves", tags=["Saves"])

# Endpoint to save exercise
@router.post("/{exercise_id}", status_code=204)
def save_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(404, "Exercise not found")
    # Check if exercise exsists and if not, save exercise
    existing = db.query(Saved).filter(
        Saved.user_id == current_user_id,
        Saved.exercise_id == exercise_id
    ).first()
    if existing:
        raise HTTPException(400, "Already saved")
    new_save = Saved(user_id=current_user_id, exercise_id=exercise_id)
    db.add(new_save)
    db.commit()
    
# Endpoint to unsave exercise
@router.delete("/{exercise_id}", status_code=204)
def unsave_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    # Find the saved record and delete it
    saved_record = db.query(Saved).filter(
        Saved.user_id == current_user_id,
        Saved.exercise_id == exercise_id
    ).first()
    if not saved_record:
        raise HTTPException(404, "Save record not found")
    db.delete(saved_record)
    db.commit()

# Endpoint to list the saved exercises
@router.get("/")
def list_saves(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    # Return a list of exercise IDs that the user saved
    saved_ex_ids = db.query(Saved.exercise_id).filter(Saved.user_id == current_user_id).all()
    return {"saved_exercise_ids": [r[0] for r in saved_ex_ids]}
