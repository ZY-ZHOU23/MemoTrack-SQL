from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from datetime import datetime
from backend.api import deps
from backend.models.entry import Entry
from backend.models.metric import Metric
from backend.models.user import User
from backend.models.tag import Tag
from backend.schemas.entry import EntryCreate, EntryUpdate, EntryResponse
from backend.schemas.metric import MetricCreate

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
            "tags": [tag.name for tag in entry.tags] if entry.tags else [],
            "metrics": [
                {
                    "id": metric.id,
                    "category": metric.category,
                    "metric_name": metric.metric_name,
                    "value": float(metric.value),
                    "unit": metric.unit,
                    "entry_id": metric.entry_id,
                    "created_at": metric.created_at,
                    "updated_at": metric.updated_at
                } for metric in entry.metrics
            ] if entry.metrics else []
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
    # Extract tags and metrics from the input
    entry_data = entry_in.model_dump()
    tag_names = entry_data.pop("tags", []) if "tags" in entry_data else []
    metrics_data = entry_data.pop("metrics", []) if "metrics" in entry_data else []
    
    # Handle custom created_at date if provided
    if entry_data.get("created_at"):
        created_at = entry_data["created_at"]
        if isinstance(created_at, str):
            try:
                # Parse the ISO format date string
                entry_data["created_at"] = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                # If parsing fails, use current time
                entry_data["created_at"] = datetime.utcnow()
    
    # Create the entry
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
    
    # Process metrics
    if metrics_data:
        for metric_data in metrics_data:
            # Skip metrics with empty category or metric_name
            if not metric_data.get("category") or not metric_data.get("metric_name"):
                continue
            
            # Add entry_id to metric data
            metric_data["entry_id"] = entry.id
            
            # Create metric
            metric = Metric(**metric_data)
            db.add(metric)
        
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
        "tags": [tag.name for tag in entry.tags] if entry.tags else [],
        "metrics": [
            {
                "id": metric.id,
                "category": metric.category,
                "metric_name": metric.metric_name,
                "value": float(metric.value),
                "unit": metric.unit,
                "entry_id": metric.entry_id,
                "created_at": metric.created_at,
                "updated_at": metric.updated_at
            } for metric in entry.metrics
        ] if entry.metrics else []
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
    
    # Extract tags and metrics and handle created_at
    entry_data = entry_in.model_dump(exclude_unset=True)
    tag_names = entry_data.pop("tags", None)
    metrics_data = entry_data.pop("metrics", None)
    
    # Handle custom created_at date if provided
    if "created_at" in entry_data and entry_data["created_at"]:
        created_at = entry_data["created_at"]
        if isinstance(created_at, str):
            try:
                # Parse the ISO format date string
                entry_data["created_at"] = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                # If parsing fails, remove created_at to not update it
                entry_data.pop("created_at", None)
    
    # Update entry fields
    for field, value in entry_data.items():
        setattr(entry, field, value)
    
    # Handle tags if provided
    if tag_names is not None:
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
    
    # Handle metrics if provided
    if metrics_data is not None:
        # Delete existing metrics for this entry
        db.query(Metric).filter(Metric.entry_id == entry.id).delete()
        
        # Create new metrics
        for metric_data in metrics_data:
            # Skip metrics with empty category or metric_name
            if not metric_data.get("category") or not metric_data.get("metric_name"):
                continue
            
            # Add entry_id to metric data
            metric_data["entry_id"] = entry.id
            
            # Create metric
            metric = Metric(**metric_data)
            db.add(metric)
    
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
        "tags": [tag.name for tag in entry.tags] if entry.tags else [],
        "metrics": [
            {
                "id": metric.id,
                "category": metric.category,
                "metric_name": metric.metric_name,
                "value": float(metric.value),
                "unit": metric.unit,
                "entry_id": metric.entry_id,
                "created_at": metric.created_at,
                "updated_at": metric.updated_at
            } for metric in entry.metrics
        ] if entry.metrics else []
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

@router.get("/{entry_id}", response_model=EntryResponse)
def read_entry(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    entry_id: int,
) -> Any:
    """
    Get entry by ID.
    """
    entry = db.query(Entry).filter(
        Entry.id == entry_id,
        Entry.user_id == current_user.id
    ).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    # Include category name, tags, and metrics in response
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
        "tags": [tag.name for tag in entry.tags] if entry.tags else [],
        "metrics": [
            {
                "id": metric.id,
                "category": metric.category,
                "metric_name": metric.metric_name,
                "value": float(metric.value),
                "unit": metric.unit,
                "entry_id": metric.entry_id,
                "created_at": metric.created_at,
                "updated_at": metric.updated_at
            } for metric in entry.metrics
        ] if entry.metrics else []
    }
    
    return response 