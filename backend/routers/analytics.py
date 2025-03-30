"""
Analytics router for the Personal Memo System.
This file handles all analytics-related API endpoints, providing insights
and statistics about user's entries, categories, and metrics.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict
from datetime import datetime, timedelta
from .. import models, schemas
from ..database import get_db
from ..auth import get_current_user

router = APIRouter()

@router.get("/entries/stats")
def get_entry_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Get statistics about user's entries.
    Returns counts of entries by category and recent activity.
    """
    # Get total entries count
    total_entries = db.query(func.count(models.Entry.id)).filter(
        models.Entry.owner_id == current_user.id
    ).scalar()
    
    # Get entries by category
    entries_by_category = db.query(
        models.Category.name,
        func.count(models.Entry.id)
    ).join(models.Entry).filter(
        models.Entry.owner_id == current_user.id
    ).group_by(models.Category.name).all()
    
    # Get recent entries (last 7 days)
    recent_entries = db.query(func.count(models.Entry.id)).filter(
        models.Entry.owner_id == current_user.id,
        models.Entry.created_at >= datetime.utcnow() - timedelta(days=7)
    ).scalar()
    
    return {
        "total_entries": total_entries,
        "entries_by_category": dict(entries_by_category),
        "recent_entries": recent_entries
    }

@router.get("/metrics/progress")
def get_metrics_progress(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Get progress statistics for user's metrics.
    Returns information about goal progress and achievement rates.
    """
    metrics = db.query(models.Metric).filter(
        models.Metric.owner_id == current_user.id
    ).all()
    
    progress_data = []
    for metric in metrics:
        if metric.target:
            progress = (metric.value / metric.target) * 100
        else:
            progress = None
            
        progress_data.append({
            "metric_name": metric.name,
            "current_value": metric.value,
            "target_value": metric.target,
            "progress_percentage": progress
        })
    
    return progress_data

@router.get("/tags/usage")
def get_tag_usage(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Get statistics about tag usage.
    Returns the most frequently used tags and their distribution.
    """
    # Get tag usage count
    tag_usage = db.query(
        models.Tag.name,
        func.count(models.Entry.id)
    ).join(models.Entry.tags).join(models.Entry).filter(
        models.Entry.owner_id == current_user.id
    ).group_by(models.Tag.name).all()
    
    return {
        "tag_usage": dict(tag_usage),
        "total_unique_tags": len(tag_usage)
    }

@router.get("/activity/timeline")
def get_activity_timeline(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Get a timeline of user activity.
    Returns daily counts of entries and metric updates.
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get daily entry counts
    daily_entries = db.query(
        func.date(models.Entry.created_at).label('date'),
        func.count(models.Entry.id)
    ).filter(
        models.Entry.owner_id == current_user.id,
        models.Entry.created_at >= start_date
    ).group_by('date').all()
    
    # Get daily metric updates
    daily_metrics = db.query(
        func.date(models.Metric.updated_at).label('date'),
        func.count(models.Metric.id)
    ).filter(
        models.Metric.owner_id == current_user.id,
        models.Metric.updated_at >= start_date
    ).group_by('date').all()
    
    return {
        "daily_entries": dict(daily_entries),
        "daily_metrics": dict(daily_metrics)
    } 