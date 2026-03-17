"""
Main FastAPI application entry point.

This module initializes and configures the FastAPI server for the
AI Documentation Generator backend API.
"""
from fastapi import FastAPI

# Initialize FastAPI application instance
# This creates the main application object that will handle all HTTP requests
app = FastAPI(
    title="AI Documentation Generator",
    description="Backend API for generating documentation using AI",
    version="1.0.0"
)


@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message.
    
    This endpoint is used to verify that the API server is running correctly.
    
    Returns:
        dict: A dictionary containing a welcome message
    """
    return {
        "message": "AI Documentation Generator API is running"
    }

