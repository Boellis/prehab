"""
Pydantic schemas for user creation and response.
"""

from pydantic import BaseModel, Field

class UserBase(BaseModel):
    username: str = Field(..., example="john_doe")

class UserCreate(UserBase):
    password: str = Field(..., example="mystrongpassword")

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
