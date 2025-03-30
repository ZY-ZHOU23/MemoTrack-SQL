"""
Tags router for the Personal Memo System.
This file handles all tag-related API endpoints, including CRUD operations
and tag-specific functionality for organizing entries.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.Tag)
def create_tag(
    tag: schemas.TagCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Create a new tag.
    Tags are globally unique and can be used across all entries.
    """
    db_tag = models.Tag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

@router.get("/", response_model=List[schemas.Tag])
def read_tags(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Retrieve a list of all tags.
    Supports pagination through skip and limit parameters.
    """
    tags = db.query(models.Tag).offset(skip).limit(limit).all()
    return tags

@router.get("/{tag_id}", response_model=schemas.Tag)
def read_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Retrieve a specific tag by ID.
    """
    tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@router.delete("/{tag_id}")
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Delete a tag.
    Note: This will remove the tag from all entries but won't delete the entries themselves.
    """
    tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    db.delete(tag)
    db.commit()
    return {"message": "Tag deleted successfully"}

@router.get("/{tag_id}/entries", response_model=List[schemas.Entry])
def get_entries_by_tag(
    tag_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Retrieve all entries that have a specific tag.
    Only returns entries belonging to the current user.
    Supports pagination.
    """
    tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    entries = db.query(models.Entry).filter(
        models.Entry.owner_id == current_user.id,
        models.Entry.tags.contains(tag)
    ).offset(skip).limit(limit).all()
    
    return entries 