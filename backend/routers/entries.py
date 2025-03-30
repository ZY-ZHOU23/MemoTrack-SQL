"""
Entries router for the Personal Memo System.
This file handles all entry-related API endpoints, including CRUD operations
and entry-specific functionality like tagging and categorization.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.Entry)
def create_entry(
    entry: schemas.EntryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Create a new entry.
    Requires authentication and associates the entry with the current user.
    """
    db_entry = models.Entry(**entry.dict(), owner_id=current_user.id)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.get("/", response_model=List[schemas.Entry])
def read_entries(
    skip: int = 0,
    limit: int = 100,
    category_id: int = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Retrieve a list of entries for the current user.
    Supports pagination and filtering by category.
    """
    query = db.query(models.Entry).filter(models.Entry.owner_id == current_user.id)
    if category_id:
        query = query.filter(models.Entry.category_id == category_id)
    entries = query.offset(skip).limit(limit).all()
    return entries

@router.get("/{entry_id}", response_model=schemas.Entry)
def read_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Retrieve a specific entry by ID.
    Verifies that the entry belongs to the current user.
    """
    entry = db.query(models.Entry).filter(
        models.Entry.id == entry_id,
        models.Entry.owner_id == current_user.id
    ).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry

@router.put("/{entry_id}", response_model=schemas.Entry)
def update_entry(
    entry_id: int,
    entry: schemas.EntryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Update an existing entry.
    Verifies ownership and updates all fields.
    """
    db_entry = db.query(models.Entry).filter(
        models.Entry.id == entry_id,
        models.Entry.owner_id == current_user.id
    ).first()
    if db_entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    for key, value in entry.dict().items():
        setattr(db_entry, key, value)
    
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.delete("/{entry_id}")
def delete_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Delete an entry.
    Verifies ownership before deletion.
    """
    db_entry = db.query(models.Entry).filter(
        models.Entry.id == entry_id,
        models.Entry.owner_id == current_user.id
    ).first()
    if db_entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    db.delete(db_entry)
    db.commit()
    return {"message": "Entry deleted successfully"}

@router.post("/{entry_id}/tags/{tag_id}")
def add_tag_to_entry(
    entry_id: int,
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Add a tag to an entry.
    Verifies ownership of both entry and tag.
    """
    entry = db.query(models.Entry).filter(
        models.Entry.id == entry_id,
        models.Entry.owner_id == current_user.id
    ).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    entry.tags.append(tag)
    db.commit()
    return {"message": "Tag added successfully"}

@router.delete("/{entry_id}/tags/{tag_id}")
def remove_tag_from_entry(
    entry_id: int,
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Remove a tag from an entry.
    Verifies ownership of the entry.
    """
    entry = db.query(models.Entry).filter(
        models.Entry.id == entry_id,
        models.Entry.owner_id == current_user.id
    ).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    entry.tags.remove(tag)
    db.commit()
    return {"message": "Tag removed successfully"} 