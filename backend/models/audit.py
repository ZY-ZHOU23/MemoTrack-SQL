"""
Audit logging model for tracking changes in the Personal Memo System.
Defines the database schema for storing audit logs of all database operations.
"""

from sqlalchemy import Column, Integer, String, Enum, JSON, ForeignKey
from .base import Base, TimestampMixin

class AuditLog(Base, TimestampMixin):
    """
    Audit log model for tracking database changes.
    Records all insert, update, and delete operations with detailed information
    about the changes made.
    """
    __tablename__ = "audit_log"

    # Primary key and audit information
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    
    # Operation details
    action_type = Column(Enum('insert', 'update', 'delete', name='audit_action_type'), nullable=False)
    table_name = Column(String(50), nullable=False)
    record_id = Column(Integer, nullable=False)
    changes = Column(JSON)  # Stores the actual changes made to the record 