from typing import Optional
from pydantic import BaseModel
from .base import BaseSchema, TimestampSchema

class CategoryBase(BaseSchema):
    name: str
    description: Optional[str] = None
    parent_category_id: Optional[int] = None
    is_active: bool = True

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: Optional[str] = None
    is_active: Optional[bool] = None

class CategoryInDBBase(CategoryBase, TimestampSchema):
    id: int
    user_id: int

class Category(CategoryInDBBase):
    pass

class CategoryResponse(CategoryInDBBase):
    pass 