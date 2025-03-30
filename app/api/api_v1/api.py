from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, users, categories, entries, metrics, tags, analytics

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(entries.router, prefix="/entries", tags=["entries"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
api_router.include_router(tags.router, prefix="/tags", tags=["tags"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"]) 