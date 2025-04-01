"""
Metric model for tracking various measurements in the Personal Memo System.
Defines the database schema for storing different types of metrics
associated with entries and categories.
"""

from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class Metric(Base, TimestampMixin):
    """
    Metric model for tracking measurements and progress.
    Supports different types of metrics with customizable units and values.
    Links to both entries and categories.
    """
    __tablename__ = "metrics"

    # Primary key and basic metric information
    id = Column(Integer, primary_key=True, index=True)
    entry_id = Column(Integer, ForeignKey("entries.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    
    # Metric details
    metric_name = Column(String(100), nullable=False)
    value = Column(Numeric(10, 2), nullable=False)
    unit = Column(String(50))

    # Relationships
    entry = relationship("Entry", back_populates="metrics")
    category = relationship("Category") 