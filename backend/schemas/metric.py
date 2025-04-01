from typing import Optional
from pydantic import BaseModel
from .base import BaseSchema, TimestampSchema

class MetricBase(BaseSchema):
    metric_name: str
    value: float
    unit: Optional[str] = None
    entry_id: int
    category_id: Optional[int] = None

class MetricCreate(MetricBase):
    pass

class MetricUpdate(MetricBase):
    metric_name: Optional[str] = None
    value: Optional[float] = None
    unit: Optional[str] = None
    entry_id: Optional[int] = None
    category_id: Optional[int] = None

class MetricInDBBase(MetricBase, TimestampSchema):
    id: int

class Metric(MetricInDBBase):
    pass

class MetricResponse(MetricInDBBase):
    category_name: Optional[str] = None 