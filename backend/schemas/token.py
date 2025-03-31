from typing import Optional
from pydantic import BaseModel
from .user import UserResponse

class Token(BaseModel):
    access_token: str
    token_type: str
    user: Optional[UserResponse] = None

class TokenPayload(BaseModel):
    sub: Optional[int] = None 