from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.api import deps
from backend.models.metric import Metric
from backend.models.entry import Entry
from backend.models.user import User
from backend.schemas.metric import MetricCreate, MetricUpdate, MetricResponse

router = APIRouter()

@router.get("/", response_model=List[MetricResponse])
def read_metrics(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
    entry_id: int = None,
    category: str = None,
) -> Any:
    """
    Retrieve metrics.
    """
    query = db.query(Metric).join(Entry).filter(Entry.user_id == current_user.id)
    if entry_id:
        query = query.filter(Metric.entry_id == entry_id)
    if category:
        query = query.filter(Metric.category == category)
    metrics = query.offset(skip).limit(limit).all()
    return metrics

@router.post("/", response_model=MetricResponse)
def create_metric(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    metric_in: MetricCreate,
) -> Any:
    """
    Create new metric.
    """
    # Verify entry belongs to user
    entry = db.query(Entry).filter(
        Entry.id == metric_in.entry_id,
        Entry.user_id == current_user.id
    ).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    metric = Metric(**metric_in.model_dump())
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric

@router.put("/{metric_id}", response_model=MetricResponse)
def update_metric(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    metric_id: int,
    metric_in: MetricUpdate,
) -> Any:
    """
    Update a metric.
    """
    metric = db.query(Metric).join(Entry).filter(
        Metric.id == metric_id,
        Entry.user_id == current_user.id
    ).first()
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    
    for field, value in metric_in.model_dump(exclude_unset=True).items():
        setattr(metric, field, value)
    
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric

@router.delete("/{metric_id}")
def delete_metric(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    metric_id: int,
) -> Any:
    """
    Delete a metric.
    """
    metric = db.query(Metric).join(Entry).filter(
        Metric.id == metric_id,
        Entry.user_id == current_user.id
    ).first()
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    
    db.delete(metric)
    db.commit()
    return {"status": "success"} 