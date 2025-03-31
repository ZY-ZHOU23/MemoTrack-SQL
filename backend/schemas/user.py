from typing import Optional
from pydantic import BaseModel, EmailStr
from .base import BaseSchema, TimestampSchema

class UserBase(BaseSchema):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    status: Optional[str] = None

class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase, TimestampSchema):
    id: int

class User(UserInDBBase):
    pass

class UserResponse(UserInDBBase):
    pass 