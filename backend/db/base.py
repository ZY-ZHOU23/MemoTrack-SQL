"""
Database model imports and configuration.
This module centralizes all database model imports and makes them available
for Alembic migrations and other database operations.
"""

from backend.models.base import Base
from backend.models.user import User
from backend.models.category import Category
from backend.models.entry import Entry
from backend.models.metric import Metric
from backend.models.tag import Tag
from backend.models.audit import AuditLog

# Import all models here for Alembic to detect them
# This list is used by Alembic for database migrations
__all__ = [
    "Base",
    "User",
    "Category",
    "Entry",
    "Metric",
    "Tag",
    "AuditLog"
] 