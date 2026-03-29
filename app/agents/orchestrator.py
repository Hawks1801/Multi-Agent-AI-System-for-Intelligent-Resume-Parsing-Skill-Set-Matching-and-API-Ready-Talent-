from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.parser import ParserAgent
from app.agents.normalizer import NormalizerAgent
from app.agents.matcher import MatcherAgent
from app.agents.interviewer import InterviewerAgent
from typing import Dict, Any

class ResumeOrchestrator:
    def __init__(self):
        self.parser = ParserAgent()
        self.normalizer = NormalizerAgent()
        self.matcher = MatcherAgent()
        self.interviewer = InterviewerAgent()
        self.workflow = self._build_workflow()

    def _build_workflow(self) -> Any:
        # 1. Initialize StateGraph
        builder = StateGraph(AgentState)

        # 2. Add Nodes
        builder.add_node("parse_resume", self._parse_node)
        builder.add_node("normalize_skills", self._normalize_node)
        builder.add_node("match_job", self._match_node)
        builder.add_node("generate_interview", self._interview_node)

        # 3. Define Edges (Linear workflow)
        builder.set_entry_point("parse_resume")
        builder.add_edge("parse_resume", "normalize_skills")
        builder.add_edge("normalize_skills", "match_job")
        builder.add_edge("match_job", "generate_interview")
        builder.add_edge("generate_interview", END)

        return builder.compile()

    def _parse_node(self, state: AgentState) -> Dict:
        """Parses the resume file."""
        try:
            resume_data = self.parser.parse(state["file_path"])
            return {"raw_resume": resume_data}
        except Exception as e:
            return {"errors": state.get("errors", []) + [f"Parsing error: {str(e)}"]}

    def _normalize_node(self, state: AgentState) -> Dict:
        """Normalizes extracted skills with context."""
        if not state.get("raw_resume"):
            return {}
        try:
            resume = state["raw_resume"]
            # Handle dict (mock) or object
            is_dict = isinstance(resume, dict)
            skills = resume.get("skills", []) if is_dict else resume.skills
            
            # Extract experience context for proficiency estimation
            exp_list = resume.get("experience", []) if is_dict else resume.experience
            context_text = ""
            for exp in exp_list:
                role = exp.get("role", "") if is_dict else exp.role
                resp = " ".join(exp.get("responsibilities", [])) if is_dict else " ".join(exp.responsibilities)
                context_text += f"{role} {resp} "

            normalized_skills = self.normalizer.normalize_skills(skills, context_text=context_text)
            
            if is_dict:
                resume["skills"] = normalized_skills
            else:
                resume.skills = normalized_skills
                
            return {"normalized_resume": resume}
        except Exception as e:
            return {"errors": state.get("errors", []) + [f"Normalization error: {str(e)}"]}

    def _match_node(self, state: AgentState) -> Dict:
        """Matches resume with job description."""
        if not state.get("normalized_resume") or not state.get("job_description"):
            return {}
        try:
            # Handle both ResumeData object and dict
            resume = state["normalized_resume"]
            match_result = self.matcher.calculate_match(resume, state["job_description"])
            return {"match_result": match_result}
        except Exception as e:
            return {"errors": state.get("errors", []) + [f"Matching error: {str(e)}"]}

    def _interview_node(self, state: AgentState) -> Dict:
        """Generates interview questions."""
        if not state.get("match_result"):
            return {}
        try:
            interview_plan = self.interviewer.generate_questions(state["match_result"])
            # Attach to match_result
            mr = state["match_result"]
            mr.interview_plan = interview_plan
            return {"match_result": mr}
        except Exception as e:
            return {"errors": state.get("errors", []) + [f"Interview error: {str(e)}"]}

    def run(self, file_path: str, job_description: Any = None) -> Dict:
        """Executes the orchestration graph."""
        initial_state = {
            "file_path": file_path,
            "job_description": job_description,
            "raw_resume": None,
            "normalized_resume": None,
            "match_result": None,
            "errors": []
        }
        return self.workflow.invoke(initial_state)
