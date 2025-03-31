from typing import Optional, List
from pydantic import BaseModel
from .base import BaseSchema, TimestampSchema

class EntryBase(BaseSchema):
    title: str
    content: str
    priority: str = "medium"
    status: str = "published"
    category_id: int

class EntryCreate(EntryBase):
    tags: List[str] = []

class EntryUpdate(EntryBase):
    title: Optional[str] = None
    content: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    category_id: Optional[int] = None
    tags: Optional[List[str]] = None

class EntryInDBBase(EntryBase, TimestampSchema):
    id: int
    user_id: int

class Entry(EntryInDBBase):
    pass

class EntryResponse(EntryInDBBase):
    category: Optional[str] = None
    tags: List[str] = [] 