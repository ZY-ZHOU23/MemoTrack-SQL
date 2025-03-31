from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.api import deps
from backend.models.entry import Entry
from backend.models.user import User
from backend.models.tag import Tag
from backend.schemas.entry import EntryCreate, EntryUpdate, EntryResponse

router = APIRouter()

@router.get("/", response_model=List[EntryResponse])
def read_entries(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
    category_id: int = None,
) -> Any:
    """
    Retrieve entries.
    """
    query = db.query(Entry).filter(Entry.user_id == current_user.id)
    if category_id:
        query = query.filter(Entry.category_id == category_id)
    entries = query.offset(skip).limit(limit).all()
    
    # Add category names and tag lists to the response
    result = []
    for entry in entries:
        entry_dict = {
            "id": entry.id,
            "user_id": entry.user_id,
            "title": entry.title,
            "content": entry.content,
            "category_id": entry.category_id,
            "priority": entry.priority,
            "status": entry.status,
            "created_at": entry.created_at,
            "updated_at": entry.updated_at,
            "category": entry.category.name if entry.category else None,
            "tags": [tag.name for tag in entry.tags] if entry.tags else []
        }
        result.append(entry_dict)
    
    return result

@router.post("/", response_model=EntryResponse)
def create_entry(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    entry_in: EntryCreate,
) -> Any:
    """
    Create new entry.
    """
    # Extract tags from the input
    entry_data = entry_in.model_dump()
    tag_names = entry_data.pop("tags", []) if "tags" in entry_data else []
    
    # Create the entry without tags
    entry = Entry(
        **entry_data,
        user_id=current_user.id
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    
    # Process tags
    if tag_names:
        for tag_name in tag_names:
            # Skip empty tags
            if not tag_name or tag_name.strip() == "":
                continue
                
            # Look for existing tag or create new one
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                db.commit()
                db.refresh(tag)
            
            # Associate tag with entry
            entry.tags.append(tag)
        
        db.commit()
        db.refresh(entry)
    
    # Include category name and tags in response
    response = {
        "id": entry.id,
        "user_id": entry.user_id,
        "title": entry.title,
        "content": entry.content,
        "category_id": entry.category_id,
        "priority": entry.priority,
        "status": entry.status,
        "created_at": entry.created_at,
        "updated_at": entry.updated_at,
        "category": entry.category.name if entry.category else None,
        "tags": [tag.name for tag in entry.tags] if entry.tags else []
    }
    
    return response

@router.put("/{entry_id}", response_model=EntryResponse)
def update_entry(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    entry_id: int,
    entry_in: EntryUpdate,
) -> Any:
    """
    Update an entry.
    """
    entry = db.query(Entry).filter(
        Entry.id == entry_id,
        Entry.user_id == current_user.id
    ).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    # Extract tags
    tag_names = entry_in.model_dump().pop("tags", []) if hasattr(entry_in, "tags") else []
    
    # Update entry fields
    for field, value in entry_in.model_dump(exclude_unset=True).items():
        if field != "tags":  # Skip tags as we handle them separately
            setattr(entry, field, value)
    
    # Handle tags if provided
    if tag_names:
        # Clear existing tags
        entry.tags = []
        
        # Process new tags
        for tag_name in tag_names:
            # Skip empty tags
            if not tag_name or tag_name.strip() == "":
                continue
                
            # Look for existing tag or create new one
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                db.commit()
                db.refresh(tag)
            
            # Associate tag with entry
            entry.tags.append(tag)
    
    db.add(entry)
    db.commit()
    db.refresh(entry)
    
    # Include category name and tags in response
    response = {
        "id": entry.id,
        "user_id": entry.user_id,
        "title": entry.title,
        "content": entry.content,
        "category_id": entry.category_id,
        "priority": entry.priority,
        "status": entry.status,
        "created_at": entry.created_at,
        "updated_at": entry.updated_at,
        "category": entry.category.name if entry.category else None,
        "tags": [tag.name for tag in entry.tags] if entry.tags else []
    }
    
    return response

@router.delete("/{entry_id}")
def delete_entry(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    entry_id: int,
) -> Any:
    """
    Delete an entry.
    """
    entry = db.query(Entry).filter(
        Entry.id == entry_id,
        Entry.user_id == current_user.id
    ).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    db.delete(entry)
    db.commit()
    return {"status": "success"} 