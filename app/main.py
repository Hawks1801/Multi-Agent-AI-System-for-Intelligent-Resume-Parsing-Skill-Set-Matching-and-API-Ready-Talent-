from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router

app = FastAPI(
    title="Error404",
    description="Advanced Multi-Agent system for resume parsing, skill normalization, and semantic matching.",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Health"])
def root():
    return {"message": "Welcome to the Multi-Agent Resume Intelligence API", "status": "operational"}

@app.get("/health", tags=["Health"])
def health_check():
    """Returns the health status of the API and underlying agents."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "agents": ["Parser", "Normalizer", "Matcher", "Interviewer"]
    }
