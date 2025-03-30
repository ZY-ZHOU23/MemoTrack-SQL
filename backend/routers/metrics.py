"""
Metrics router for the Personal Memo System.
This file handles all metric-related API endpoints, including CRUD operations
and metric-specific functionality for tracking user progress and goals.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.Metric)
def create_metric(
    metric: schemas.MetricCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Create a new metric.
    Requires authentication and associates the metric with the current user.
    """
    db_metric = models.Metric(**metric.dict(), owner_id=current_user.id)
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric

@router.get("/", response_model=List[schemas.Metric])
def read_metrics(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Retrieve a list of metrics for the current user.
    Supports pagination through skip and limit parameters.
    """
    metrics = db.query(models.Metric).filter(
        models.Metric.owner_id == current_user.id
    ).offset(skip).limit(limit).all()
    return metrics

@router.get("/{metric_id}", response_model=schemas.Metric)
def read_metric(
    metric_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Retrieve a specific metric by ID.
    Verifies that the metric belongs to the current user.
    """
    metric = db.query(models.Metric).filter(
        models.Metric.id == metric_id,
        models.Metric.owner_id == current_user.id
    ).first()
    if metric is None:
        raise HTTPException(status_code=404, detail="Metric not found")
    return metric

@router.put("/{metric_id}", response_model=schemas.Metric)
def update_metric(
    metric_id: int,
    metric: schemas.MetricCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Update an existing metric.
    Verifies ownership and updates all fields.
    """
    db_metric = db.query(models.Metric).filter(
        models.Metric.id == metric_id,
        models.Metric.owner_id == current_user.id
    ).first()
    if db_metric is None:
        raise HTTPException(status_code=404, detail="Metric not found")
    
    for key, value in metric.dict().items():
        setattr(db_metric, key, value)
    
    db.commit()
    db.refresh(db_metric)
    return db_metric

@router.delete("/{metric_id}")
def delete_metric(
    metric_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Delete a metric.
    Verifies ownership before deletion.
    """
    db_metric = db.query(models.Metric).filter(
        models.Metric.id == metric_id,
        models.Metric.owner_id == current_user.id
    ).first()
    if db_metric is None:
        raise HTTPException(status_code=404, detail="Metric not found")
    
    db.delete(db_metric)
    db.commit()
    return {"message": "Metric deleted successfully"}

@router.put("/{metric_id}/value")
def update_metric_value(
    metric_id: int,
    value: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Update the value of a metric.
    Useful for tracking progress towards goals.
    """
    db_metric = db.query(models.Metric).filter(
        models.Metric.id == metric_id,
        models.Metric.owner_id == current_user.id
    ).first()
    if db_metric is None:
        raise HTTPException(status_code=404, detail="Metric not found")
    
    db_metric.value = value
    db.commit()
    db.refresh(db_metric)
    return db_metric 