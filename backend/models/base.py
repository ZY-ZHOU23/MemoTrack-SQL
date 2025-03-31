"""
Base model configuration for SQLAlchemy.
This module provides the base class for all database models and common mixins.
"""

from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime

# Create declarative base class for all models
Base = declarative_base()

class TimestampMixin:
    """
    Mixin class that adds timestamp columns to models.
    Automatically tracks creation and update times for database records.
    """
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 