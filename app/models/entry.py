from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class Entry(Base, TimestampMixin):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    priority = Column(Enum('low', 'medium', 'high', name='entry_priority'), default='medium')
    status = Column(Enum('draft', 'published', 'archived', name='entry_status'), default='published')

    # Relationships
    user = relationship("User", back_populates="entries")
    category = relationship("Category", back_populates="entries")
    metrics = relationship("Metric", back_populates="entry", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary="entry_tags", back_populates="entries") 