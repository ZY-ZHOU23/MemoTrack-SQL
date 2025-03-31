"""
Entry model for storing personal memos in the Personal Memo System.
Defines the database schema for entries and their relationships with
categories, tags, and metrics.
"""

from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class Entry(Base, TimestampMixin):
    """
    Entry model representing personal memos.
    Stores the main content and metadata for each memo entry.
    """
    __tablename__ = "entries"

    # Primary key and basic entry information
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    
    # Entry metadata and status
    priority = Column(Enum('low', 'medium', 'high', name='entry_priority'), default='medium')
    status = Column(Enum('draft', 'published', 'archived', name='entry_status'), default='published')

    # Relationships with other entities
    user = relationship("User", back_populates="entries")
    category = relationship("Category", back_populates="entries")
    metrics = relationship("Metric", back_populates="entry", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary="entry_tags", back_populates="entries") 