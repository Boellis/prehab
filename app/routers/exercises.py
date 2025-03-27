"""
Handles CRUD for Exercises. 
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db.models import Exercise
from app.schemas.exercise import ExerciseCreate, ExerciseUpdate, ExerciseResponse
from app.core.security import get_current_user_id

router = APIRouter(prefix="/exercises", tags=["Exercises"])

@router.post("/", response_model=ExerciseResponse)
def create_exercise(
    exercise: ExerciseCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Create a new exercise.
    """
    new_ex = Exercise(
        name=exercise.name,
        description=exercise.description,
        difficulty=exercise.difficulty,
        is_public=exercise.is_public,
        owner_id=current_user_id
    )
    db.add(new_ex)
    db.commit()
    db.refresh(new_ex)
    return new_ex

@router.get("/", response_model=List[ExerciseResponse])
def list_exercises(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Return all public exercises plus any private ones owned by the user.
    """
    exercises = db.query(Exercise).filter(
        (Exercise.is_public == True) | (Exercise.owner_id == current_user_id)
    ).all()
    return exercises

@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise_by_id(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    ex = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not ex:
        raise HTTPException(status_code=404, detail="Exercise not found")
    # Only owner can retrieve if not public
    if not ex.is_public and ex.owner_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this exercise")
    return ex

@router.put("/{exercise_id}", response_model=ExerciseResponse)
def update_exercise(
    exercise_id: int,
    exercise_data: ExerciseUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    ex = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not ex:
        raise HTTPException(status_code=404, detail="Exercise not found")
    if ex.owner_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this exercise")

    for field, value in exercise_data.dict(exclude_unset=True).items():
        setattr(ex, field, value)
    db.commit()
    db.refresh(ex)
    return ex

@router.delete("/{exercise_id}", status_code=204)
def delete_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    ex = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not ex:
        raise HTTPException(status_code=404, detail="Exercise not found")
    if ex.owner_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this exercise")

    db.delete(ex)
    db.commit()
