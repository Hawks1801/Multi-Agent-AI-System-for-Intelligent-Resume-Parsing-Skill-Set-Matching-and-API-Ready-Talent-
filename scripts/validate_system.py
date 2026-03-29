import os
import json
from app.agents.orchestrator import ResumeOrchestrator
from app.models.domain.matcher import JobDescription
from dotenv import load_dotenv

load_dotenv()

def validate_system():
    print("--- Starting Multi-Agent Resume Intelligence Validation ---\n")
    
    # 1. Setup Orchestrator
    orchestrator = ResumeOrchestrator()
    
    # 2. Define Sample Job Description
    jd = JobDescription(
        title="Senior Python Backend Engineer",
        description="We are looking for a Senior Python Engineer with experience in FastAPI, Docker, and PostgreSQL. Experience with cloud platforms like AWS is a plus.",
        required_skills=["Python", "FastAPI", "PostgreSQL", "Docker"],
        nice_to_have_skills=["AWS", "Kubernetes", "Redis"]
    )
    
    # 3. Path to sample resume
    resume_path = "data/samples/sample_resume.txt"
    
    print(f"Processing Resume: {resume_path}")
    print(f"Target Role: {jd.title}\n")
    
    # 4. Run Orchestration
    try:
        result = orchestrator.run(file_path=resume_path, job_description=jd)
        
        if result.get("errors"):
            print("Errors encountered:")
            for error in result["errors"]:
                print(f" - {error}")
            return

        # 5. Display Results
        candidate = result["normalized_resume"]
        match = result["match_result"]
        
        print(f"Candidate Name: {candidate.full_name}")
        print(f"Email: {candidate.email}")
        print("-" * 30)
        
        print("Normalized Skills:")
        for skill in candidate.skills[:10]: # Top 10
            print(f" - {skill.name} ({skill.proficiency or 'N/A'})")
        print("-" * 30)
        
        print(f"Match Score: {match.overall_score:.2f}")
        print(f"Semantic Similarity: {match.semantic_similarity:.2f}")
        print(f"Skill Match Score: {match.skill_match_score:.2f}")
        print("-" * 30)
        
        print("Strengths:")
        for strength in match.strengths:
            print(f" + {strength}")
            
        print("\nMissing Skills & Upskilling:")
        for gap in match.missing_skills:
            print(f" ! {gap.missing_skill}: {gap.upskilling_path}")
            
    except Exception as e:
        print(f"Validation failed with exception: {str(e)}")

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY not found in .env. LLM-based parsing may fail.")
    validate_system()
