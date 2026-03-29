from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class JobDescription(BaseModel):
    title: str
    description: str
    required_skills: List[str]
    nice_to_have_skills: List[str] = Field(default_factory=list)
    experience_level: Optional[str] = None

class SkillGap(BaseModel):
    missing_skill: str
    upskilling_path: str = Field(description="Suggested path to acquire this skill")

class MatchResult(BaseModel):
    candidate_id: str
    overall_score: float = Field(ge=0.0, le=1.0)
    skill_match_score: float
    semantic_similarity: float
    missing_skills: List[SkillGap]
    strengths: List[str]
    interview_plan: Optional[Any] = None # Will hold InterviewPlan
