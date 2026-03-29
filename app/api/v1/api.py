from fastapi import APIRouter
from app.api.v1.endpoints import resume, match, skills, candidates

api_router = APIRouter()
api_router.include_router(resume.router, prefix="/parse", tags=["resume"])
api_router.include_router(match.router, prefix="/match", tags=["match"])
api_router.include_router(skills.router, prefix="/skills", tags=["skills"])
api_router.include_router(candidates.router, prefix="/candidates", tags=["candidates"])
