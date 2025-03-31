from typing import Optional, List
from pydantic import BaseModel
from .base import BaseSchema, TimestampSchema

class TagBase(BaseSchema):
    name: str

class TagCreate(TagBase):
    pass

class TagUpdate(TagBase):
    name: Optional[str] = None

class TagInDBBase(TagBase, TimestampSchema):
    id: int

class Tag(TagInDBBase):
    pass

class TagResponse(TagInDBBase):
    pass 