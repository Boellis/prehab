"""
Handles CRUD operations for Exercises.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Exercise
from app.schemas.exercise import ExerciseCreate, ExerciseResponse, ExerciseUpdate
from app.core.security import decode_jwt
from typing import List

router = APIRouter(prefix="/exercises", tags=["Exercises"])

# Define the OAuth2 scheme dependency
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user_id(token: str = Depends(oauth2_scheme)):
    """
    A dependency to get the current user ID from the OAuth2 token.
    The token is extracted from the 'Authorization: Bearer <token>' header.
    """
    try:
        payload = decode_jwt(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token."
        )

    if payload.get("scope") != "access_token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token scope."
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload."
        )
    return int(user_id)

@router.post("/", response_model=ExerciseResponse)
def create_exercise(
    exercise_create: ExerciseCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    
    # Create a new exercise. Must be authenticated.
    new_exercise = Exercise(
        title=exercise_create.title,
        description=exercise_create.description,
        difficulty=exercise_create.difficulty,
        is_public=exercise_create.is_public,
        owner_id=current_user_id
    )
    db.add(new_exercise)
    db.commit()
    db.refresh(new_exercise)
    return new_exercise

@router.get("/", response_model=List[ExerciseResponse])
def list_public_exercises(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
):
    """
    Retrieve a list of all public exercises with pagination.
    Must be authenticated to see them.
    """
    exercises = db.query(Exercise).filter(Exercise.is_public == True).offset(skip).limit(limit).all()
    return exercises

@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise_by_id(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """
    Get a specific exercise by ID.
    If the exercise is public, anyone authenticated can see it.
    If the exercise is private (is_public=False), only the owner can see it.
    """
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    # Check visibility
    if not exercise.is_public and exercise.owner_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this exercise")

    return exercise

@router.put("/{exercise_id}", response_model=ExerciseResponse)
def update_exercise(
    exercise_id: int,
    exercise_update: ExerciseUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    
    # Update an exercise. Only the owner can update it.
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    # Check ownership
    if exercise.owner_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this exercise")

    # Update fields if provided
    if exercise_update.title is not None:
        exercise.title = exercise_update.title
    if exercise_update.description is not None:
        exercise.description = exercise_update.description
    if exercise_update.difficulty is not None:
        exercise.difficulty = exercise_update.difficulty
    if exercise_update.is_public is not None:
        exercise.is_public = exercise_update.is_public

    db.commit()
    db.refresh(exercise)
    return exercise

@router.delete("/{exercise_id}", status_code=204)
def delete_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """
    Delete an exercise. Only the owner can delete it.
    Returns 204 (no content) on success.
    """
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    if exercise.owner_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this exercise")

    db.delete(exercise)
    db.commit()
    return
