import os
import instructor
from openai import OpenAI
from sentence_transformers import SentenceTransformer, util
from typing import List, Dict, Any
from pydantic import BaseModel
from app.models.domain.resume import ResumeData, Skill
from app.models.domain.matcher import JobDescription, MatchResult, SkillGap
import torch

class ExtractedSkills(BaseModel):
    required_skills: List[str]

class MatcherAgent:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            self.client = instructor.from_openai(
                OpenAI(
                    base_url="https://api.groq.com/openai/v1",
                    api_key=api_key
                )
            )
        else:
            self.client = None
        self.llm_model = "llama-3.3-70b-versatile"

    def _extract_jd_skills(self, description: str) -> List[str]:
        """Uses LLM or the trained dataset to extract required skills."""
        if os.getenv("USE_MOCK_PARSER") == "True":
            # In mock mode, we still try to be smart about what we return
            lower_desc = description.lower()
            if "electrician" in lower_desc:
                return ["Wiring", "Electrical Systems", "Circuit Maintenance", "Safety Standards", "Blueprint Reading"]
            if "developer" in lower_desc or "engineer" in lower_desc:
                return ["Python", "JavaScript", "SQL", "Cloud Architecture", "API Design"]
            
            return ["Core Technical Competency"]

        if not self.client:
            return []
        
        try:
            result = self.client.chat.completions.create(
                model=self.llm_model,
                response_model=ExtractedSkills,
                messages=[
                    {"role": "system", "content": "Extract a list of specific technical skills required for this job description. If it's a general description, identify the most critical 5 technologies or domain skills."},
                    {"role": "user", "content": description}
                ]
            )
            return result.required_skills
        except Exception as e:
            print(f"Error extracting JD skills: {e}")
            return []

    def calculate_match(self, candidate_data: Any, job_description: JobDescription) -> MatchResult:
        """Calculates semantic match score between candidate and JD."""
        
        # 1. If required_skills is empty, try to extract them from description
        if not job_description.required_skills:
            job_description.required_skills = self._extract_jd_skills(job_description.description)
        
        # 2. Normalize and extract skills from candidate (handle dict or object)
        if isinstance(candidate_data, dict):
            skills_list = candidate_data.get("skills", [])
            candidate_id = candidate_data.get("full_name", "Unknown")
        else:
            skills_list = candidate_data.skills
            candidate_id = candidate_data.full_name

        candidate_skills = []
        for s in skills_list:
            if hasattr(s, "name"): candidate_skills.append(s.name)
            elif isinstance(s, dict): candidate_skills.append(s.get("name", ""))
            else: candidate_skills.append(str(s))
        
        # 3. Vectorize skills and JD
        candidate_embedding = self.model.encode(" ".join(candidate_skills), convert_to_tensor=True)
        jd_embedding = self.model.encode(job_description.description, convert_to_tensor=True)
        
        # 4. Calculate semantic similarity
        semantic_sim = float(util.pytorch_cos_sim(candidate_embedding, jd_embedding).item())
        
        # 5. Keyword/Direct skill matching for 'Required' skills
        required_skills = job_description.required_skills
        found_skills = [s for s in required_skills if s.lower() in [c.lower() for c in candidate_skills]]
        missing_skills = [s for s in required_skills if s.lower() not in [c.lower() for c in candidate_skills]]
        
        # STRICTOR SCORING:
        # If no technical skills are provided/found in JD, default to 0.0 to prevent false positives
        if not required_skills:
            skill_match_score = 0.0
        else:
            skill_match_score = float(len(found_skills) / len(required_skills))
        
        # HEAVY WEIGHT ON SKILLS: 
        # Semantic similarity alone shouldn't qualify a candidate. 
        # If skill match is 0, we penalize the overall score heavily.
        if skill_match_score == 0:
            overall_score = (semantic_sim * 0.1) # Max 10% if skills are totally missing
        else:
            overall_score = (0.1 * semantic_sim) + (0.9 * skill_match_score)
        
        # 6. Gap analysis
        skill_gaps = []
        for missing in missing_skills:
            skill_gaps.append(SkillGap(
                missing_skill=missing,
                upskilling_path=f"Critical Gap: This role requires {missing} which was not detected in your profile."
            ))
            
        return MatchResult(
            candidate_id=candidate_id,
            overall_score=min(1.0, float(overall_score)),
            skill_match_score=float(skill_match_score),
            semantic_similarity=float(semantic_sim),
            missing_skills=skill_gaps,
            strengths=[s for s in found_skills]
        )
