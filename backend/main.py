"""
Main FastAPI application entry point for the Personal Memo System.
This file initializes the FastAPI application, configures CORS, and sets up all API routes.
It serves as the central configuration point for the entire backend application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import settings
from backend.api.api_v1.api import api_router

# Initialize FastAPI application with project metadata
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS middleware for frontend communication
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Register all API routes under the API version prefix
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    """Health check endpoint to verify the API is running."""
    return {"message": "Welcome to Personal Memo System API"} 