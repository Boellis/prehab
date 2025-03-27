"""
Handles CRUD for Exercises. 
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from typing import List

from app.db.database import get_db
from app.db.models import Exercise, Favorite, Saved, Rating, User
from app.schemas.exercise import ExerciseCreate, ExerciseUpdate, ExerciseResponse
from app.core.security import get_current_user_id

router = APIRouter(prefix="/exercises", tags=["Exercises"])

@router.post("/", response_model=ExerciseResponse)
def create_exercise(
    exercise: ExerciseCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    # Create a new exercise
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
    
    # Return all public exercises plus any private ones owned by the user.
    # Subqueries to count favorites & saves
    fav_subq = db.query(
        Favorite.exercise_id, func.count(Favorite.id).label("favorite_count")
    ).group_by(Favorite.exercise_id).subquery()

    save_subq = db.query(
        Saved.exercise_id, func.count(Saved.id).label("save_count")
    ).group_by(Saved.exercise_id).subquery()

    # Query public + user-owned
    query = db.query(
        Exercise,
        func.coalesce(fav_subq.c.favorite_count, 0).label("favorite_count"),
        func.coalesce(save_subq.c.save_count, 0).label("save_count"),
    ).outerjoin(
        fav_subq, fav_subq.c.exercise_id == Exercise.id
    ).outerjoin(
        save_subq, save_subq.c.exercise_id == Exercise.id
    ).filter(
        (Exercise.is_public == True) | (Exercise.owner_id == current_user_id)
    )

    results = query.all()

    # Build response
    response_list = []
    for (exercise, fcount, scount) in results:
        response_list.append(ExerciseResponse(
            id=exercise.id,
            name=exercise.name,
            description=exercise.description,
            difficulty=exercise.difficulty,
            is_public=exercise.is_public,
            owner_id=exercise.owner_id,
            # optionally store these counts in the schema or an extended schema
        ))
    return response_list

@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise_by_id(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    # Query to find the exercise in the db
    ex = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not ex:
        raise HTTPException(404, "Exercise not found")

    # Only owner can view if private
    if not ex.is_public and ex.owner_id != current_user_id:
        raise HTTPException(403, "Not authorized to view this exercise")

    # Count saves
    save_count = db.query(func.count(distinct(Saved.id))).filter(Saved.exercise_id == exercise_id).scalar()
    # Average rating
    avg_rating = db.query(func.avg(Rating.rating)).filter(Rating.exercise_id == exercise_id).scalar() or 0.0

    # Build response object
    response = ExerciseResponse(
        id=ex.id,
        name=ex.name,
        description=ex.description,
        difficulty=ex.difficulty,
        is_public=ex.is_public,
        owner_id=ex.owner_id,
        save_count=save_count,
        rating=round(avg_rating, 2) 
    )
    return response


@router.put("/{exercise_id}", response_model=ExerciseResponse)
def update_exercise(
    exercise_id: int,
    exercise_data: ExerciseUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    # Query db for exercise to be updated
    ex = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not ex:
        raise HTTPException(status_code=404, detail="Exercise not found")
    if ex.owner_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this exercise")

    # Update exercise with values
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
    # Query db for exercise to be deleted
    ex = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not ex:
        raise HTTPException(status_code=404, detail="Exercise not found")
    if ex.owner_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this exercise")

    db.delete(ex)
    db.commit()

# Return a list of users who have liked and/or saved the exercise
@router.get("/{exercise_id}/users")
def get_users_for_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    # Query to find the exercise in db
    ex = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not ex:
        raise HTTPException(404, "Exercise not found")
    if not ex.is_public and ex.owner_id != current_user_id:
        raise HTTPException(403, "Not authorized to view users for a private exercise")

    # Check for all the favorited users of the exercise and return it
    favorited_users = (
        db.query(User.id, User.username)
        .join(Favorite, Favorite.user_id == User.id)
        .filter(Favorite.exercise_id == exercise_id)
        .all()
    )
    # Check for all the saved users of the exercise and return it
    saved_users = (
        db.query(User.id, User.username)
        .join(Saved, Saved.user_id == User.id)
        .filter(Saved.exercise_id == exercise_id)
        .all()
    )
    return {
        "favorited_by": favorited_users,
        "saved_by": saved_users
    }
