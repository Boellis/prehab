"""
Combine user's favorited & saved exercises into one list.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Exercise, Favorite, Saved
from app.core.security import get_current_user_id
from app.schemas.exercise import ExerciseResponse
from typing import List

router = APIRouter(prefix="/collection", tags=["Collection"])

@router.get("/", response_model=List[ExerciseResponse])
def get_collection(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    # Get users favorite exercises
    fav_ids = db.query(Favorite.exercise_id).filter(Favorite.user_id == current_user_id)
    # Get users saved exercises
    saved_ids = db.query(Saved.exercise_id).filter(Saved.user_id == current_user_id)
    fav_set = {f[0] for f in fav_ids}
    saved_set = {s[0] for s in saved_ids}
    # Combine saved and favorite exercises for a query
    combined_ids = fav_set.union(saved_set)

    if not combined_ids:
        return []

    # Query and return list of combined saved and favorite exercises
    exercises = db.query(Exercise).filter(Exercise.id.in_(combined_ids)).all()

    return exercises
