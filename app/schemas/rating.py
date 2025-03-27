"""
Schema for rating an exercise.
"""

from pydantic import BaseModel, Field

class RateExerciseRequest(BaseModel):
    rating: int = Field(..., ge=1, le=5)
