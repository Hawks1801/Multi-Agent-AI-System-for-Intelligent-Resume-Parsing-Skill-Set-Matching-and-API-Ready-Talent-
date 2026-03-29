from typing import TypedDict, List, Optional
from app.models.domain.resume import ResumeData
from app.models.domain.matcher import MatchResult, JobDescription

class AgentState(TypedDict):
    # Inputs
    file_path: str
    job_description: Optional[JobDescription]
    
    # Intermediate results
    raw_resume: Optional[ResumeData]
    normalized_resume: Optional[ResumeData]
    
    # Outputs
    match_result: Optional[MatchResult]
    errors: List[str]
