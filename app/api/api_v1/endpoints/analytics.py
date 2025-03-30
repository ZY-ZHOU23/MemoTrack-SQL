from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.api import deps
from app.models.metric import Metric
from app.models.entry import Entry
from app.models.user import User
from app.schemas.metric import MetricResponse

router = APIRouter()

@router.get("/metrics/summary", response_model=dict)
def get_metrics_summary(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    metric_type: str = None,
    start_date: datetime = None,
    end_date: datetime = None,
) -> Any:
    """
    Get summary statistics for metrics.
    """
    query = db.query(
        Metric.metric_type,
        Metric.metric_name,
        func.avg(Metric.value).label('avg_value'),
        func.min(Metric.value).label('min_value'),
        func.max(Metric.value).label('max_value'),
        func.count(Metric.id).label('total_records')
    ).join(Entry).filter(Entry.user_id == current_user.id)

    if metric_type:
        query = query.filter(Metric.metric_type == metric_type)
    if start_date:
        query = query.filter(Metric.created_at >= start_date)
    if end_date:
        query = query.filter(Metric.created_at <= end_date)

    results = query.group_by(Metric.metric_type, Metric.metric_name).all()
    
    return {
        "summary": [
            {
                "metric_type": r.metric_type,
                "metric_name": r.metric_name,
                "avg_value": float(r.avg_value),
                "min_value": float(r.min_value),
                "max_value": float(r.max_value),
                "total_records": r.total_records
            }
            for r in results
        ]
    }

@router.get("/metrics/trend", response_model=dict)
def get_metrics_trend(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    metric_type: str = None,
    metric_name: str = None,
    days: int = 30,
) -> Any:
    """
    Get daily trend data for specific metrics.
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)

    query = db.query(
        func.date(Metric.created_at).label('date'),
        func.avg(Metric.value).label('avg_value')
    ).join(Entry).filter(
        Entry.user_id == current_user.id,
        Metric.created_at >= start_date,
        Metric.created_at <= end_date
    )

    if metric_type:
        query = query.filter(Metric.metric_type == metric_type)
    if metric_name:
        query = query.filter(Metric.metric_name == metric_name)

    results = query.group_by(func.date(Metric.created_at)).all()

    return {
        "trend": [
            {
                "date": r.date.isoformat(),
                "avg_value": float(r.avg_value)
            }
            for r in results
        ]
    }

@router.get("/entries/count", response_model=dict)
def get_entries_count(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    days: int = 30,
) -> Any:
    """
    Get count of entries by category over time.
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)

    results = db.query(
        Entry.category_id,
        func.count(Entry.id).label('count')
    ).filter(
        Entry.user_id == current_user.id,
        Entry.created_at >= start_date,
        Entry.created_at <= end_date
    ).group_by(Entry.category_id).all()

    return {
        "entries_count": [
            {
                "category_id": r.category_id,
                "count": r.count
            }
            for r in results
        ]
    } 