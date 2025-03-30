from sqlalchemy import Column, Integer, String, Numeric, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class Metric(Base, TimestampMixin):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    entry_id = Column(Integer, ForeignKey("entries.id", ondelete="CASCADE"), nullable=False)
    metric_type = Column(Enum('financial', 'health', 'productivity', 'custom', name='metric_type'), nullable=False)
    metric_name = Column(String(100), nullable=False)
    value = Column(Numeric(10, 2), nullable=False)
    unit = Column(String(50))

    # Relationships
    entry = relationship("Entry", back_populates="metrics") 