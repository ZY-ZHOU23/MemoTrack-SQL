from typing import Optional
from pydantic import BaseModel
from .base import BaseSchema, TimestampSchema

class MetricBase(BaseSchema):
    metric_type: str
    metric_name: str
    value: float
    unit: Optional[str] = None
    entry_id: int

class MetricCreate(MetricBase):
    pass

class MetricUpdate(MetricBase):
    metric_type: Optional[str] = None
    metric_name: Optional[str] = None
    value: Optional[float] = None
    unit: Optional[str] = None
    entry_id: Optional[int] = None

class MetricInDBBase(MetricBase, TimestampSchema):
    id: int

    class Config:
        from_attributes = True

class Metric(MetricInDBBase):
    pass

class MetricResponse(MetricInDBBase):
    pass 