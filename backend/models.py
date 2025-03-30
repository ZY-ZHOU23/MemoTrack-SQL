"""
Database models for the Personal Memo System.
This file defines all SQLAlchemy models that represent the database tables.
It includes models for users, categories, entries, metrics, and tags.
"""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# Association table for many-to-many relationship between entries and tags
entry_tags = Table(
    'entry_tags',
    Base.metadata,
    Column('entry_id', Integer, ForeignKey('entries.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class User(Base):
    """
    User model representing system users.
    Contains basic user information and relationships to other entities.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    categories = relationship("Category", back_populates="owner")
    entries = relationship("Entry", back_populates="owner")
    metrics = relationship("Metric", back_populates="owner")

class Category(Base):
    """
    Category model for organizing entries.
    Represents different types or groups of entries.
    """
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="categories")
    entries = relationship("Entry", back_populates="category")

class Entry(Base):
    """
    Entry model representing individual memos or notes.
    Contains the main content and metadata for each entry.
    """
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    category_id = Column(Integer, ForeignKey("categories.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="entries")
    category = relationship("Category", back_populates="entries")
    tags = relationship("Tag", secondary=entry_tags, back_populates="entries")

class Metric(Base):
    """
    Metric model for tracking user-specific metrics and goals.
    Used for monitoring progress and achievements.
    """
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    value = Column(Integer)
    target = Column(Integer, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="metrics")

class Tag(Base):
    """
    Tag model for categorizing entries with keywords.
    Enables flexible categorization and search functionality.
    """
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    entries = relationship("Entry", secondary=entry_tags, back_populates="tags") 