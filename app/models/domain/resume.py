from typing import List, Optional
from pydantic import BaseModel, Field

class Experience(BaseModel):
    company: str = Field(description="Name of the company or organization")
    role: str = Field(description="Candidate's job title")
    duration: str = Field(description="Period of employment (e.g., 'Jan 2020 - Present')")
    responsibilities: List[str] = Field(description="Key responsibilities and achievements")
    location: Optional[str] = Field(None, description="Company location")

class Education(BaseModel):
    institution: str = Field(description="Name of the school or university")
    degree: str = Field(description="Degree obtained (e.g., 'Bachelor of Science')")
    field: str = Field(description="Field of study (e.g., 'Computer Science')")
    year: Optional[str] = Field(None, description="Year of graduation")

class Skill(BaseModel):
    name: str = Field(description="Name of the skill")
    proficiency: Optional[str] = Field(None, description="Estimated proficiency level (e.g., 'Beginner', 'Intermediate', 'Expert')")
    category: Optional[str] = Field(None, description="Skill category (e.g., 'Programming Language', 'Soft Skill')")

class Certification(BaseModel):
    name: str = Field(description="Name of the certification")
    issuer: str = Field(description="Organization that issued the certification")
    year: Optional[str] = Field(None, description="Year obtained")

class Project(BaseModel):
    title: str = Field(description="Title of the project")
    description: str = Field(description="Brief overview of the project")
    technologies: List[str] = Field(default_factory=list, description="Technologies used in the project")

class ResumeData(BaseModel):
    full_name: str = Field(description="Full name of the candidate")
    email: Optional[str] = Field(None, description="Candidate's email address")
    phone: Optional[str] = Field(None, description="Candidate's phone number")
    location: Optional[str] = Field(None, description="Candidate's current location")
    linkedin_url: Optional[str] = Field(None, description="Link to LinkedIn profile")
    summary: Optional[str] = Field(None, description="Professional summary or objective")
    experience: List[Experience] = Field(default_factory=list, description="Work experience history")
    education: List[Education] = Field(default_factory=list, description="Educational background")
    skills: List[Skill] = Field(default_factory=list, description="Technical and soft skills")
    certifications: List[Certification] = Field(default_factory=list, description="Certifications and licenses")
    projects: List[Project] = Field(default_factory=list, description="Notable projects")
    publications: List[str] = Field(default_factory=list, description="List of publications")
    raw_source_text: Optional[str] = Field(None, description="Raw text extracted from the source document")
