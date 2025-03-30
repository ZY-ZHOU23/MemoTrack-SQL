from sqlalchemy import Column, Integer, String, Enum, JSON, ForeignKey
from .base import Base, TimestampMixin

class AuditLog(Base, TimestampMixin):
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    action_type = Column(Enum('insert', 'update', 'delete', name='audit_action_type'), nullable=False)
    table_name = Column(String(50), nullable=False)
    record_id = Column(Integer, nullable=False)
    changes = Column(JSON) 