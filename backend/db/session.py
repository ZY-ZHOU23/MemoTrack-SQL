"""
Database session management.
This module handles database connection and session creation,
providing a dependency for FastAPI endpoints to access the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.core.config import settings

# Create SQLAlchemy engine with connection pooling
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Create session factory for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Database session dependency for FastAPI endpoints.
    Creates a new database session for each request and ensures it's closed properly.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 