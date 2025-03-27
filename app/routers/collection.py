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
def get_user_collection(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Retrieve a combined list of exercises the user has favorited or saved.
    Also include whether each is favorited/saved by the user.
    """
    # Get all exercise IDs the user favorited
    fav_ids = db.query(Favorite.exercise_id).filter(Favorite.user_id == current_user_id)
    # Get all exercise IDs the user saved
    saved_ids = db.query(Saved.exercise_id).filter(Saved.user_id == current_user_id)

    fav_id_set = {f[0] for f in fav_ids}
    saved_id_set = {s[0] for s in saved_ids}

    combined_ids = fav_id_set.union(saved_id_set)

    if not combined_ids:
        return []

    # Retrieve the exercises
    exercises = (
        db.query(Exercise)
        .filter(Exercise.id.in_(combined_ids))
        .all()
    )

    # For each exercise, we also want the counts
    response_list = []
    for ex in exercises:
        # Count favorites for each exercise
        favorite_count = db.query(Favorite).filter(Favorite.exercise_id == ex.id).count()
        # Count saves
        save_count = db.query(Saved).filter(Saved.exercise_id == ex.id).count()

        response_list.append(
            ExerciseResponse(
                id=ex.id,
                name=ex.name,
                description=ex.description,
                difficulty=ex.difficulty,
                is_public=ex.is_public,
                owner_id=ex.owner_id,
                favorite_count=favorite_count,
                save_count=save_count,
                user_has_favorited=(ex.id in fav_id_set),
                user_has_saved=(ex.id in saved_id_set)
            )
        )

    return response_list
