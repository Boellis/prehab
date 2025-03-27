"""
Endpoints to rate an exercise from 1-5.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Rating, Exercise
from app.schemas.rating import RateExerciseRequest
from app.core.security import get_current_user_id

router = APIRouter(prefix="/ratings", tags=["Ratings"])
# Endpoint to rate an exercise
@router.post("/{exercise_id}", status_code=204)
def rate_exercise(
    exercise_id: int,
    req: RateExerciseRequest,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    # Get the current exercise
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    # Throw error is we dont have an exercise to rate
    if not exercise:
        raise HTTPException(404, "Exercise not found")
    # Find existing rating
    existing_rating = db.query(Rating).filter(
        Rating.user_id == current_user_id,
        Rating.exercise_id == exercise_id
    ).first()
    # Update rating if theres an existing one
    if existing_rating:
        existing_rating.rating = req.rating
    # Otherwise, create a rating
    else:
        new_rating = Rating(user_id=current_user_id, exercise_id=exercise_id, rating=req.rating)
        db.add(new_rating)
    db.commit()
