import os
import instructor
from openai import OpenAI
from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.domain.matcher import MatchResult

class InterviewQuestion(BaseModel):
    question: str = Field(description="The interview question text")
    intent: str = Field(description="The purpose of this question (e.g., verifying strength, probing gap)")
    expected_topics: List[str] = Field(description="Key terms or concepts the candidate should mention")

class InterviewPlan(BaseModel):
    questions: List[InterviewQuestion]
    rationale: str = Field(description="AI's reasoning for this interview strategy")

class InterviewerAgent:
    def __init__(self, model: str = "llama-3.3-70b-versatile"):
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
        self.model = model

    def generate_questions(self, match_result: MatchResult) -> InterviewPlan:
        """Generates tailored interview questions based on match results."""
        if os.getenv("USE_MOCK_PARSER") == "True" or not self.client:
            # High-quality mock responses for the demo
            questions = []
            for strength in match_result.strengths[:2]:
                questions.append(InterviewQuestion(
                    question=f"Can you describe a complex project where you leveraged {strength} to solve a critical problem?",
                    intent=f"Verifying depth in {strength}",
                    expected_topics=[strength, "architecture", "scalability"]
                ))
            for gap in match_result.missing_skills[:2]:
                questions.append(InterviewQuestion(
                    question=f"The role requires {gap.missing_skill}. How would you approach learning this, and are there similar concepts you have mastered?",
                    intent=f"Probing learning curve for {gap.missing_skill}",
                    expected_topics=["transferable skills", "self-learning", "conceptual mapping"]
                ))
            
            return InterviewPlan(
                questions=questions,
                rationale="Strategy focused on verifying core technical claims and assessing adaptability for specific skill gaps."
            )

        # Real LLM generation if key is present
        return self.client.chat.completions.create(
            model=self.model,
            response_model=InterviewPlan,
            messages=[
                {"role": "system", "content": "You are a Senior Technical Recruiter. Based on the candidate's strengths and skill gaps, generate a professional interview plan."},
                {"role": "user", "content": f"Match Results: {match_result.json()}"}
            ]
        )
