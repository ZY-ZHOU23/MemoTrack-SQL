from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.api import deps
from backend.models.tag import Tag
from backend.models.entry import Entry
from backend.models.user import User
from backend.schemas.tag import TagCreate, TagUpdate, TagResponse

router = APIRouter()

@router.get("/", response_model=List[TagResponse])
def read_tags(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve tags.
    """
    tags = db.query(Tag).join(Tag.entries).filter(
        Entry.user_id == current_user.id
    ).distinct().offset(skip).limit(limit).all()
    return tags

@router.post("/", response_model=TagResponse)
def create_tag(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    tag_in: TagCreate,
) -> Any:
    """
    Create new tag.
    """
    tag = Tag(**tag_in.model_dump())
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag

@router.put("/{tag_id}", response_model=TagResponse)
def update_tag(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    tag_id: int,
    tag_in: TagUpdate,
) -> Any:
    """
    Update a tag.
    """
    tag = db.query(Tag).join(Tag.entries).filter(
        Tag.id == tag_id,
        Entry.user_id == current_user.id
    ).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    for field, value in tag_in.model_dump(exclude_unset=True).items():
        setattr(tag, field, value)
    
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag

@router.delete("/{tag_id}")
def delete_tag(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    tag_id: int,
) -> Any:
    """
    Delete a tag.
    """
    tag = db.query(Tag).join(Tag.entries).filter(
        Tag.id == tag_id,
        Entry.user_id == current_user.id
    ).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    db.delete(tag)
    db.commit()
    return {"status": "success"} 