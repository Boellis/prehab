"""
Handles CRUD for Exercises. Supports fetching from local SQLite or from Firestore when a query parameter is provided.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from typing import List

from app.db.database import get_db
from app.db.models import Exercise, Favorite, Saved, User, Rating
from app.schemas.exercise import (
    ExerciseCreate,
    ExerciseResponse,
    ExerciseUpdate
)
from app.core.security import get_current_user_id

# Firestore client
from app.firebase_admin import db_firestore  

router = APIRouter(prefix="/exercises", tags=["Exercises"])

@router.get("/", response_model=List[ExerciseResponse])
def get_exercises(
    request: Request,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
):
    """
    Retrieve public exercises and user's private exercises with pagination.
    Uses subqueries to correctly count favorites and saves and calculates average rating.
    """
    # Fetch from Firestore
    if request.query_params.get('use_cloud') == 'true':
        exercises_firestore = db_firestore.collection('exercises').stream()
        response_list = []
        for doc in exercises_firestore:
            data = doc.to_dict()
            # Convert types as needed; assume Firestore documents match the ExerciseResponse schema.
            response_list.append(data)
        return response_list
    
    # Fetch from SQLite
    else:
        # Subquery for counting favorites
        favorite_subq = (
            db.query(
                Favorite.exercise_id,
                func.count(Favorite.id).label("favorite_count")
            )
            .group_by(Favorite.exercise_id)
            .subquery()
        )

        # Subquery for counting saves
        save_subq = (
            db.query(
                Saved.exercise_id,
                func.count(Saved.id).label("save_count")
            )
            .group_by(Saved.exercise_id)
            .subquery()
        )

        query = (
            db.query(
                Exercise,
                func.coalesce(favorite_subq.c.favorite_count, 0).label("favorite_count"),
                func.coalesce(save_subq.c.save_count, 0).label("save_count")
            )
            .outerjoin(favorite_subq, favorite_subq.c.exercise_id == Exercise.id)
            .outerjoin(save_subq, save_subq.c.exercise_id == Exercise.id)
            .filter((Exercise.is_public == True) | (Exercise.owner_id == current_user_id))
            .offset(skip)
            .limit(limit)
        )

        results = query.all()

        # Get the user's favorite and saved exercise IDs separately
        user_fav_ids = {fav.exercise_id for fav in db.query(Favorite).filter(Favorite.user_id == current_user_id).all()}
        user_save_ids = {s.exercise_id for s in db.query(Saved).filter(Saved.user_id == current_user_id).all()}

        response_list = []
        for (exercise, fav_count, save_count) in results:
            avg_rating = db.query(func.avg(Rating.rating)).filter(Rating.exercise_id == exercise.id).scalar() or 0.0
            response_list.append(
                ExerciseResponse(
                    id=exercise.id,
                    name=exercise.name,
                    description=exercise.description,
                    difficulty=exercise.difficulty,
                    is_public=exercise.is_public,
                    owner_id=exercise.owner_id,
                    favorite_count=fav_count,
                    save_count=save_count,
                    user_has_favorited=(exercise.id in user_fav_ids),
                    user_has_saved=(exercise.id in user_save_ids),
                    average_rating=round(avg_rating, 2),
                    video_url=exercise.video_url
                )
            )

        return response_list

@router.post("/", response_model=ExerciseResponse)
def create_exercise(
    exercise: ExerciseCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    Create a new exercise (public or private) owned by the current user.
    """
    new_exercise = Exercise(
        name=exercise.name,
        description=exercise.description,
        difficulty=exercise.difficulty,
        is_public=exercise.is_public,
        owner_id=user_id,
        video_url=exercise.video_url
    )

    db.add(new_exercise)
    db.commit()
    db.refresh(new_exercise)
    # Return with zero counts, obviously, as it's new
    return ExerciseResponse(
        id=new_exercise.id,
        name=new_exercise.name,
        description=new_exercise.description,
        difficulty=new_exercise.difficulty,
        is_public=new_exercise.is_public,
        owner_id=new_exercise.owner_id,
        favorite_count=0,
        save_count=0,
        user_has_favorited=False,
        user_has_saved=False,
        video_url=exercise.video_url

    )

@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise_by_id(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    if not exercise.is_public and exercise.owner_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this exercise")

    favorite_count = db.query(func.count(distinct(Favorite.id))).filter(Favorite.exercise_id == exercise_id).scalar()
    save_count = db.query(func.count(distinct(Saved.id))).filter(Saved.exercise_id == exercise_id).scalar()
    avg_rating = db.query(func.avg(Rating.rating)).filter(Rating.exercise_id == exercise_id).scalar() or 0.0

    user_has_favorited = bool(
        db.query(Favorite)
        .filter(Favorite.exercise_id == exercise_id, Favorite.user_id == current_user_id)
        .first()
    )
    user_has_saved = bool(
        db.query(Saved)
        .filter(Saved.exercise_id == exercise_id, Saved.user_id == current_user_id)
        .first()
    )

    return ExerciseResponse(
        id=exercise.id,
        name=exercise.name,
        description=exercise.description,
        difficulty=exercise.difficulty,
        is_public=exercise.is_public,
        owner_id=exercise.owner_id,
        favorite_count=favorite_count,
        save_count=save_count,
        user_has_favorited=user_has_favorited,
        user_has_saved=user_has_saved,
        average_rating=round(avg_rating, 2),
        video_url=exercise.video_url

    )

@router.put("/{exercise_id}", response_model=ExerciseResponse)
def update_exercise(
    exercise_id: int,
    exercise_update: ExerciseUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """
    Update an exercise. Only the creator (owner) can update the exercise.
    """
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    if exercise.owner_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this exercise")

    for field, value in exercise_update.dict(exclude_unset=True).items():
        setattr(exercise, field, value)

    db.commit()
    db.refresh(exercise)

    favorite_count = db.query(func.count(distinct(Favorite.id))).filter(Favorite.exercise_id == exercise.id).scalar()
    save_count = db.query(func.count(distinct(Saved.id))).filter(Saved.exercise_id == exercise.id).scalar()
    avg_rating = db.query(func.avg(Rating.rating)).filter(Rating.exercise_id == exercise.id).scalar() or 0.0

    user_has_favorited = bool(
        db.query(Favorite)
        .filter(Favorite.exercise_id == exercise.id, Favorite.user_id == current_user_id)
        .first()
    )
    user_has_saved = bool(
        db.query(Saved)
        .filter(Saved.exercise_id == exercise.id, Saved.user_id == current_user_id)
        .first()
    )

    return ExerciseResponse(
        id=exercise.id,
        name=exercise.name,
        description=exercise.description,
        difficulty=exercise.difficulty,
        is_public=exercise.is_public,
        owner_id=exercise.owner_id,
        favorite_count=favorite_count,
        save_count=save_count,
        user_has_favorited=user_has_favorited,
        user_has_saved=user_has_saved,
        average_rating=round(avg_rating, 2),
        video_url=exercise.video_url

    )


@router.delete("/{exercise_id}", status_code=204)
def delete_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """
    Delete an exercise.
    Only the creator (owner) of the exercise can delete it, regardless of its visibility.
    """
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    if exercise.owner_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this exercise")

    db.delete(exercise)
    db.commit()

@router.get("/{exercise_id}/users")
def get_users_for_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    if not exercise.is_public and exercise.owner_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this exercise")

    favorited_users = (
        db.query(User.id, User.username)
        .join(Favorite, Favorite.user_id == User.id)
        .filter(Favorite.exercise_id == exercise_id)
        .all()
    )

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