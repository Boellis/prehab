"""
Pydantic schemas for Exercises.
"""

from pydantic import BaseModel, Field
from typing import Optional

class ExerciseBase(BaseModel):
    
    # Base schema for an exercise, with common fields.
    title: str = Field(..., example="Push Ups")
    description: str = Field(..., example="A basic upper-body exercise.")
    difficulty: int = Field(..., ge=1, le=5, example=3)
    is_public: bool = Field(..., example=True)

class ExerciseCreate(ExerciseBase):

    # Schema for creating a new exercise. Inherits from ExerciseBase.
    pass

class ExerciseUpdate(BaseModel):

    # Schema for updating an existing exercise.
    title: Optional[str] = Field(None, example="Updated Title")
    description: Optional[str] = Field(None, example="Updated Description")
    difficulty: Optional[int] = Field(None, ge=1, le=5, example=2)
    is_public: Optional[bool] = Field(None, example=False)

class ExerciseResponse(ExerciseBase):
    
    # Schema for returning exercise data.
    id: int
    owner_id: int

    class Config:
        orm_mode = True
