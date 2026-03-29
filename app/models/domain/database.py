from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship, JSON, Column
from datetime import datetime

class Candidate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    email: Optional[str] = Field(None, index=True)
    phone: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None
    
    # Store complex structures as JSON
    skills: List[dict] = Field(default_factory=list, sa_column=Column(JSON))
    experience: List[dict] = Field(default_factory=list, sa_column=Column(JSON))
    education: List[dict] = Field(default_factory=list, sa_column=Column(JSON))
    
    created_at: datetime = Field(default_factory=datetime.utcnow)

class JobMatch(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    candidate_id: int = Field(foreign_key="candidate.id")
    job_title: str
    score: float
    match_details: dict = Field(default_factory=dict, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
