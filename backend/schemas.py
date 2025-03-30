"""
Pydantic schemas for the Personal Memo System.
This file defines the data validation and serialization schemas used throughout the API.
These schemas ensure data consistency and provide type safety for API requests and responses.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Token schemas for authentication
class Token(BaseModel):
    """
    Schema for JWT token response.
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Schema for decoded token data.
    """
    username: Optional[str] = None

# User schemas
class UserBase(BaseModel):
    """
    Base schema for user data.
    """
    username: str
    email: EmailStr

class UserCreate(UserBase):
    """
    Schema for user creation request.
    """
    password: str

class User(UserBase):
    """
    Schema for user response.
    """
    id: int
    is_active: bool

    class Config:
        from_attributes = True

# Category schemas
class CategoryBase(BaseModel):
    """
    Base schema for category data.
    """
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    """
    Schema for category creation request.
    """
    pass

class Category(CategoryBase):
    """
    Schema for category response.
    """
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Entry schemas
class EntryBase(BaseModel):
    """
    Base schema for entry data.
    """
    title: str
    content: str
    category_id: Optional[int] = None

class EntryCreate(EntryBase):
    """
    Schema for entry creation request.
    """
    pass

class Entry(EntryBase):
    """
    Schema for entry response.
    """
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    tags: List['Tag'] = []

    class Config:
        from_attributes = True

# Metric schemas
class MetricBase(BaseModel):
    """
    Base schema for metric data.
    """
    name: str
    value: int
    target: Optional[int] = None

class MetricCreate(MetricBase):
    """
    Schema for metric creation request.
    """
    pass

class Metric(MetricBase):
    """
    Schema for metric response.
    """
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Tag schemas
class TagBase(BaseModel):
    """
    Base schema for tag data.
    """
    name: str

class TagCreate(TagBase):
    """
    Schema for tag creation request.
    """
    pass

class Tag(TagBase):
    """
    Schema for tag response.
    """
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 