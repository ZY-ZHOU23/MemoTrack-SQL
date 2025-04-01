from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from .base import BaseSchema, TimestampSchema
from .metric import MetricCreate, MetricResponse

class EntryBase(BaseSchema):
    title: str
    content: str
    priority: str = "medium"
    status: str = "published"
    category_id: Optional[int] = None
    created_at: Optional[datetime] = None

class EntryCreate(EntryBase):
    tags: List[str] = []
    metrics: Optional[List[dict]] = None

class EntryUpdate(EntryBase):
    title: Optional[str] = None
    content: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    category_id: Optional[int] = None
    tags: Optional[List[str]] = None
    created_at: Optional[datetime] = None
    metrics: Optional[List[dict]] = None

class EntryInDBBase(EntryBase, TimestampSchema):
    id: int
    user_id: int

class Entry(EntryInDBBase):
    pass

class EntryResponse(EntryInDBBase):
    category: Optional[str] = None
    tags: List[str] = []
    metrics: Optional[List[MetricResponse]] = None 