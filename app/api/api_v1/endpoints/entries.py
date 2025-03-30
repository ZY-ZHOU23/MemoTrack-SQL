from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.entry import Entry
from app.models.user import User
from app.schemas.entry import EntryCreate, EntryUpdate, EntryResponse

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
    return entries

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
    entry = Entry(
        **entry_in.model_dump(),
        user_id=current_user.id
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

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
    
    for field, value in entry_in.model_dump(exclude_unset=True).items():
        setattr(entry, field, value)
    
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

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