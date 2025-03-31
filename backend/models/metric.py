"""
Metric model for tracking various measurements in the Personal Memo System.
Defines the database schema for storing different types of metrics
associated with entries.
"""

from sqlalchemy import Column, Integer, String, Numeric, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class Metric(Base, TimestampMixin):
    """
    Metric model for tracking measurements and progress.
    Supports different types of metrics (financial, health, productivity, etc.)
    with customizable units and values.
    """
    __tablename__ = "metrics"

    # Primary key and basic metric information
    id = Column(Integer, primary_key=True, index=True)
    entry_id = Column(Integer, ForeignKey("entries.id", ondelete="CASCADE"), nullable=False)
    
    # Metric type and details
    metric_type = Column(Enum('financial', 'health', 'productivity', 'custom', name='metric_type'), nullable=False)
    metric_name = Column(String(100), nullable=False)
    value = Column(Numeric(10, 2), nullable=False)
    unit = Column(String(50))

    # Relationship with parent entry
    entry = relationship("Entry", back_populates="metrics") 