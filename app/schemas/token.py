"""
Pydantic schemas for JWT tokens.
"""

from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: int 

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    scope: Optional[str] = None

class RefreshTokenRequest(BaseModel):
    refresh_token: str
