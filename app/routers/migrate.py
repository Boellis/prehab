"""
Provides an endpoint to migrate local SQLite exercise data to Firestore.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Exercise
from app.firebase_admin import db_firestore  # Firestore client
from app.schemas.exercise import ExerciseResponse

router = APIRouter(prefix="/migrate", tags=["Migrate"])

@router.post("/exercises", status_code=200)
def migrate_exercises(db: Session = Depends(get_db)):
    
    # Migrate all exercises from local SQLite to Firestore.
    exercises_local = db.query(Exercise).all()
    if not exercises_local:
        raise HTTPException(status_code=404, detail="No exercises found to migrate")
    
    for ex in exercises_local:
        doc_data = {
            "id": ex.id,
            "name": ex.name,
            "description": ex.description,
            "difficulty": ex.difficulty,
            "is_public": ex.is_public,
            "owner_id": ex.owner_id,
            "favorite_count": 0,
            "save_count": 0,
            "average_rating": 0.0,
            "video_url": ex.video_url
        }
        db_firestore.collection('exercises').document(str(ex.id)).set(doc_data)
    
    return {"message": "Migration successful"}
