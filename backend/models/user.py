"""
User model for the Personal Memo System.
Defines the database schema for user accounts and their relationships
with other entities in the system.
"""

from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class User(Base, TimestampMixin):
    """
    User model representing system users.
    Stores user authentication and profile information.
    """
    __tablename__ = "users"

    # Primary key and basic user information
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # User status and activity tracking
    status = Column(Enum('active', 'inactive', 'suspended', name='user_status'), default='active')
    last_login = Column(DateTime)

    # Relationships with other entities
    categories = relationship("Category", back_populates="user", cascade="all, delete-orphan")
    entries = relationship("Entry", back_populates="user", cascade="all, delete-orphan") 