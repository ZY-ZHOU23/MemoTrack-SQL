from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from backend.api import deps
from backend.models.metric import Metric
from backend.models.entry import Entry
from backend.models.user import User
from backend.models.category import Category
from backend.models.tag import Tag, entry_tags
from backend.schemas.metric import MetricResponse

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

@router.get("/dashboard", response_model=dict)
def get_dashboard_stats(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get dashboard statistics including total entries, categories, tags,
    entries by category, and entries over time.
    """
    try:
        # Get total counts
        total_entries = db.query(func.count(Entry.id)).filter(
            Entry.user_id == current_user.id
        ).scalar() or 0
        
        print(f"Total entries for user {current_user.id}: {total_entries}")
        
        total_categories = db.query(func.count(Category.id)).filter(
            Category.user_id == current_user.id
        ).scalar() or 0
        
        print(f"Total categories for user {current_user.id}: {total_categories}")
        
        # Get total tags (unique tags used by the user)
        total_tags = db.query(func.count(func.distinct(Tag.id))).join(
            entry_tags, Tag.id == entry_tags.c.tag_id, isouter=True
        ).join(
            Entry, Entry.id == entry_tags.c.entry_id, isouter=True
        ).filter(
            Entry.user_id == current_user.id
        ).scalar() or 0
        
        print(f"Total tags for user {current_user.id}: {total_tags}")
        
        # Get recent entries
        recent_entries = db.query(
            Entry.id,
            Entry.title,
            Entry.content,
            Entry.created_at
        ).filter(
            Entry.user_id == current_user.id
        ).order_by(
            desc(Entry.created_at)
        ).limit(5).all()
        
        # Get entries by category
        entries_by_category = db.query(
            Category.name.label('category'),
            func.count(Entry.id).label('count')
        ).join(
            Entry,
            Entry.category_id == Category.id
        ).filter(
            Entry.user_id == current_user.id
        ).group_by(
            Category.name
        ).all()
        
        # Get entries over time (last 30 days)
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        
        entries_by_date_query = db.query(
            func.date(Entry.created_at).label('date'),
            func.count(Entry.id).label('count')
        ).filter(
            Entry.user_id == current_user.id,
            Entry.created_at >= start_date,
            Entry.created_at <= end_date
        ).group_by(
            func.date(Entry.created_at)
        ).all()
        
        # Format for the response
        response = {
            "totalEntries": total_entries,
            "totalCategories": total_categories,
            "totalTags": total_tags,
            "recentEntries": [
                {
                    "id": entry.id,
                    "title": entry.title,
                    "content": entry.content,
                    "created_at": entry.created_at.isoformat()
                }
                for entry in recent_entries
            ],
            "entriesByCategory": [
                {
                    "category": r.category,
                    "count": r.count
                }
                for r in entries_by_category
            ],
            "entriesByDate": [
                {
                    "date": r.date.isoformat(),
                    "count": r.count
                }
                for r in entries_by_date_query
            ]
        }
        
        print(f"Dashboard response: {response}")
        return response
    except Exception as e:
        print(f"Error in dashboard endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/", response_model=dict)
def get_analytics(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    time_range: str = "30d",
) -> Any:
    """
    Get comprehensive analytics based on time range.
    Supported time ranges: 7d, 30d, 90d, all
    """
    try:
        # Determine the date range based on the time_range parameter
        end_date = datetime.utcnow()
        
        if time_range == "7d":
            start_date = end_date - timedelta(days=7)
        elif time_range == "30d":
            start_date = end_date - timedelta(days=30)
        elif time_range == "90d":
            start_date = end_date - timedelta(days=90)
        else:  # "all" or any other value
            start_date = datetime.min
        
        # Get total entries within the time range
        total_entries = db.query(func.count(Entry.id)).filter(
            Entry.user_id == current_user.id,
            Entry.created_at >= start_date if time_range != "all" else True
        ).scalar() or 0
        
        # Get total categories used in this time range
        total_categories = db.query(func.count(func.distinct(Category.id))).join(
            Entry, Entry.category_id == Category.id
        ).filter(
            Entry.user_id == current_user.id,
            Entry.created_at >= start_date if time_range != "all" else True
        ).scalar() or 0
        
        # Get total tags used in this time range
        total_tags = db.query(func.count(func.distinct(Tag.id))).join(
            entry_tags, Tag.id == entry_tags.c.tag_id
        ).join(
            Entry, Entry.id == entry_tags.c.entry_id
        ).filter(
            Entry.user_id == current_user.id,
            Entry.created_at >= start_date if time_range != "all" else True
        ).scalar() or 0
        
        # Calculate days in range for average
        days_in_range = (end_date - start_date).days or 1  # Avoid division by zero
        average_entries_per_day = total_entries / days_in_range if days_in_range > 0 else 0
        
        # Find most active day
        most_active_day_query = db.query(
            func.date(Entry.created_at).label('date'),
            func.count(Entry.id).label('count')
        ).filter(
            Entry.user_id == current_user.id,
            Entry.created_at >= start_date if time_range != "all" else True
        ).group_by(
            func.date(Entry.created_at)
        ).order_by(
            desc('count')
        ).first()
        
        most_active_day = most_active_day_query.date.strftime('%Y-%m-%d') if most_active_day_query else 'N/A'
        
        # Find most used category
        most_used_category_query = db.query(
            Category.name,
            func.count(Entry.id).label('count')
        ).join(
            Entry, Entry.category_id == Category.id
        ).filter(
            Entry.user_id == current_user.id,
            Entry.created_at >= start_date if time_range != "all" else True
        ).group_by(
            Category.name
        ).order_by(
            desc('count')
        ).first()
        
        most_used_category = most_used_category_query.name if most_used_category_query else 'N/A'
        
        # Find most used tag
        most_used_tag_query = db.query(
            Tag.name,
            func.count(entry_tags.c.entry_id).label('count')
        ).join(
            entry_tags, Tag.id == entry_tags.c.tag_id
        ).join(
            Entry, Entry.id == entry_tags.c.entry_id
        ).filter(
            Entry.user_id == current_user.id,
            Entry.created_at >= start_date if time_range != "all" else True
        ).group_by(
            Tag.name
        ).order_by(
            desc('count')
        ).first()
        
        most_used_tag = most_used_tag_query.name if most_used_tag_query else 'N/A'
        
        # Get entries by category
        entries_by_category = db.query(
            Category.name.label('category'),
            func.count(Entry.id).label('count')
        ).join(
            Entry, Entry.category_id == Category.id
        ).filter(
            Entry.user_id == current_user.id,
            Entry.created_at >= start_date if time_range != "all" else True
        ).group_by(
            Category.name
        ).all()
        
        # Get entries by date
        entries_by_date_query = db.query(
            func.date(Entry.created_at).label('date'),
            func.count(Entry.id).label('count')
        ).filter(
            Entry.user_id == current_user.id,
            Entry.created_at >= start_date if time_range != "all" else True
        ).group_by(
            func.date(Entry.created_at)
        ).order_by(
            'date'
        ).all()
        
        # Get entries by tag
        entries_by_tag = db.query(
            Tag.name.label('tag'),
            func.count(entry_tags.c.entry_id).label('count')
        ).join(
            entry_tags, Tag.id == entry_tags.c.tag_id
        ).join(
            Entry, Entry.id == entry_tags.c.entry_id
        ).filter(
            Entry.user_id == current_user.id,
            Entry.created_at >= start_date if time_range != "all" else True
        ).group_by(
            Tag.name
        ).all()
        
        # Format the response
        response = {
            "totalEntries": total_entries,
            "totalCategories": total_categories,
            "totalTags": total_tags,
            "averageEntriesPerDay": average_entries_per_day,
            "mostActiveDay": most_active_day,
            "mostUsedCategory": most_used_category,
            "mostUsedTag": most_used_tag,
            "entriesByCategory": [
                {
                    "category": r.category,
                    "count": r.count
                }
                for r in entries_by_category
            ],
            "entriesByDate": [
                {
                    "date": r.date.isoformat(),
                    "count": r.count
                }
                for r in entries_by_date_query
            ],
            "entriesByTag": [
                {
                    "tag": r.tag,
                    "count": r.count
                }
                for r in entries_by_tag
            ]
        }
        
        print(f"Analytics response for time_range={time_range}: {response}")
        return response
        
    except Exception as e:
        print(f"Error in analytics endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") 