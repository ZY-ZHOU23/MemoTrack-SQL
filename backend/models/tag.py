from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

# Association table for many-to-many relationship between entries and tags
entry_tags = Table(
    'entry_tags',
    Base.metadata,
    Column('entry_id', Integer, ForeignKey('entries.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)

class Tag(Base, TimestampMixin):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    # Relationships
    entries = relationship("Entry", secondary=entry_tags, back_populates="tags") 