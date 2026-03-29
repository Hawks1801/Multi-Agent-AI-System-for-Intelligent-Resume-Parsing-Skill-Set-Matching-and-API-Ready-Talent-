import os
import json
from app.agents.orchestrator import ResumeOrchestrator
from app.models.domain.matcher import JobDescription
from app.models.domain.resume import ResumeData, Skill, Experience, Education
from unittest.mock import MagicMock

# 1. Create a Mock Parser that doesn't need OpenAI
class MockParser:
    def parse(self, file_path: str) -> ResumeData:
        return ResumeData(
            full_name="John Doe",
            email="john.doe@example.com",
            phone="+1-555-010-999",
            location="San Francisco, CA",
            summary="Experienced Software Engineer",
            skills=[
                Skill(name="Python", proficiency="Expert"),
                Skill(name="JS", proficiency="Expert"), # Test normalization
                Skill(name="K8s", proficiency="Intermediate"), # Test normalization
                Skill(name="FastAPI", proficiency="Expert"),
                Skill(name="Docker", proficiency="Expert"),
                Skill(name="PostgreSQL", proficiency="Expert")
            ],
            experience=[
                Experience(
                    company="TechCorp",
                    role="Senior Engineer",
                    duration="2021-Present",
                    responsibilities=["Built microservices"]
                )
            ],
            education=[
                Education(
                    institution="UC Berkeley",
                    degree="BS",
                    field="Computer Science",
                    year="2018"
                )
            ]
        )

def validate_mock_system():
    print("--- Running MOCK System Validation (No API Key Required) ---\n")
    
    # Setup Orchestrator
    orchestrator = ResumeOrchestrator()
    # Inject Mock Parser
    orchestrator.parser = MockParser()
    
    jd = JobDescription(
        title="Senior Python Backend Engineer",
        description="We are looking for a Senior Python Engineer with experience in FastAPI, Docker, and PostgreSQL.",
        required_skills=["Python", "FastAPI", "PostgreSQL", "Docker"],
        nice_to_have_skills=["AWS", "Kubernetes", "Redis"]
    )
    
    resume_path = "data/samples/sample_resume.txt"
    
    print(f"Processing Resume: {resume_path} (Using Mock Parser)")
    print(f"Target Role: {jd.title}\n")
    
    result = orchestrator.run(file_path=resume_path, job_description=jd)
    
    if result.get("errors"):
        print("Errors:", result["errors"])
        return

    candidate = result["normalized_resume"]
    match = result["match_result"]
    
    print(f"Candidate: {candidate.full_name}")
    print("-" * 30)
    
    print("Normalized Skills (Demonstrating Taxonomy Mapping):")
    for skill in candidate.skills:
        print(f" - {skill.name}")
    print("-" * 30)
    
    print(f"Overall Match Score: {match.overall_score:.2f}")
    print(f"Semantic Similarity: {match.semantic_similarity:.2f}")
    print(f"Skill Match Score: {match.skill_match_score:.2f}")
    print("-" * 30)
    
    print("Strengths:")
    for strength in match.strengths:
        print(f" + {strength}")
        
    print("\nMissing Skills & Upskilling:")
    for gap in match.missing_skills:
        print(f" ! {gap.missing_skill}: {gap.upskilling_path}")

if __name__ == "__main__":
    validate_mock_system()
