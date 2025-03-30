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
    pass

class EntryUpdate(EntryBase):
    title: Optional[str] = None
    content: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    category_id: Optional[int] = None

class EntryInDBBase(EntryBase, TimestampSchema):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class Entry(EntryInDBBase):
    pass

class EntryResponse(EntryInDBBase):
    pass 