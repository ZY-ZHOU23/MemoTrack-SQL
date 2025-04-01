"""
Category model for organizing metrics in the Personal Memo System.
Defines the database schema for categories and their hierarchical relationships.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class Category(Base, TimestampMixin):
    """
    Category model for organizing metrics.
    Supports hierarchical categories and user-specific organization.
    """
    __tablename__ = "categories"

    # Primary key and basic category information
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    
    # Category hierarchy and status
    parent_category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))
    is_active = Column(Boolean, default=True)

    # Relationships with other entities
    user = relationship("User", back_populates="categories")
    parent = relationship("Category", remote_side=[id], backref="children") 