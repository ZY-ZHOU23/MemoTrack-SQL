"""
Main FastAPI application entry point for the Personal Memo System.
This file sets up the FastAPI application, configures CORS, and includes all API routers.
It also handles database initialization and provides a health check endpoint.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import categories, entries, metrics, tags, analytics
from .auth import auth_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Personal Memo System API",
    description="API for managing personal memos, categories, and analytics",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])
app.include_router(entries.router, prefix="/api/entries", tags=["Entries"])
app.include_router(metrics.router, prefix="/api/metrics", tags=["Metrics"])
app.include_router(tags.router, prefix="/api/tags", tags=["Tags"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])

@app.get("/")
async def root():
    """
    Health check endpoint to verify the API is running.
    Returns a simple message indicating the API is operational.
    """
    return {"message": "Personal Memo System API is running"} 