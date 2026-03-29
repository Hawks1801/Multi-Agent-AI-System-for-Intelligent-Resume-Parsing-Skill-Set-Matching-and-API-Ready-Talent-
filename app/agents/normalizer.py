import json
import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Optional
from app.models.domain.resume import Skill
import os

class NormalizerAgent:
    def __init__(self, taxonomy_path: str = "data/taxonomy/skills_large.json", db_path: str = "data/chromadb"):
        self.db_path = db_path
        self.taxonomy = self._load_taxonomy(taxonomy_path)
        self.client = chromadb.PersistentClient(path=db_path)
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name="skills_taxonomy",
            embedding_function=self.embedding_fn
        )
        self._initialize_vector_db()
        
        # 1. Advanced Mappings
        self.synonyms = {
            "JS": "JavaScript", "K8s": "Kubernetes", "ML": "Machine Learning",
            "NLP": "Natural Language Processing", "ReactJS": "React", "React.js": "React",
            "AWS Lambda": "AWS", "Fast API": "FastAPI", "Sci-kit learn": "Scikit-learn"
        }
        
        # 2. Hierarchy Inference Map (Child -> Parent)
        self.inference_map = {
            "TensorFlow": "Deep Learning", "PyTorch": "Deep Learning",
            "React": "Frontend Development", "FastAPI": "Backend Development",
            "Docker": "DevOps", "Kubernetes": "Cloud Infrastructure",
            "Scikit-learn": "Machine Learning", "Pandas": "Data Analysis",
            "SQL": "Database Management", "AWS": "Cloud Computing"
        }
        
        # 3. Emerging Skill Store
        self.emerging_skills = []

    def _load_taxonomy(self, path: str) -> Dict:
        with open(path, "r") as f:
            return json.load(f)

    def _initialize_vector_db(self):
        """Flat list of all skills from the hierarchy and add to vector store."""
        all_skills = self._flatten_taxonomy(self.taxonomy)
        # Only add if collection is empty
        if self.collection.count() == 0:
            ids = [f"skill_{i}" for i in range(len(all_skills))]
            self.collection.add(
                documents=all_skills,
                ids=ids
            )

    def _flatten_taxonomy(self, data: any) -> List[str]:
        skills = []
        if isinstance(data, list):
            skills.extend(data)
        elif isinstance(data, dict):
            for key, value in data.items():
                skills.extend(self._flatten_taxonomy(value))
        return list(set(skills))

    def normalize(self, skill: Skill) -> Skill:
        """Normalizes a single skill and handles emerging skill detection."""
        original_name = skill.name
        
        # 1. Direct synonym mapping
        if original_name.upper() in self.synonyms:
            skill.name = self.synonyms[original_name.upper()]
            return skill

        # 2. Semantic search for closest canonical skill
        results = self.collection.query(
            query_texts=[original_name],
            n_results=1
        )
        
        if results['documents'] and results['distances'][0][0] < 0.4: # Threshold for similarity
            skill.name = results['documents'][0][0]
        else:
            # 3. Emerging Skill Detection
            print(f"FLAG: Emerging skill detected: {original_name}")
            if original_name not in self.emerging_skills:
                self.emerging_skills.append(original_name)
            
        return skill

    def infer_hierarchy(self, skills: List[Skill]) -> List[Skill]:
        """Infers parent skills based on technical stack (e.g. PyTorch -> Deep Learning)."""
        existing_names = set(s.name for s in skills)
        inferred = []
        
        for skill in skills:
            if skill.name in self.inference_map:
                parent = self.inference_map[skill.name]
                if parent not in existing_names:
                    inferred.append(Skill(name=parent, proficiency="Inferred", category="Hierarchy Expansion"))
                    existing_names.add(parent)
        
        return skills + inferred

    def estimate_proficiency(self, skill: Skill, context_text: str) -> Skill:
        """Context-aware proficiency estimation using simple heuristics."""
        import re
        if not context_text: return skill
        
        # Look for years of experience near the skill name
        pattern = rf"(\d+)\+?\s*years?.*{re.escape(skill.name)}"
        match = re.search(pattern, context_text, re.I)
        
        if match:
            years = int(match.group(1))
            if years >= 5: skill.proficiency = "Expert"
            elif years >= 2: skill.proficiency = "Intermediate"
            else: skill.proficiency = "Beginner"
        elif "expert" in context_text.lower() and skill.name.lower() in context_text.lower():
            skill.proficiency = "Expert"
            
        return skill

    def normalize_skills(self, skills: List[Skill], context_text: str = "") -> List[Skill]:
        """Full pipeline: Normalize -> Estimate Proficiency -> Infer Hierarchy."""
        # 1. Base Normalization & Emerging Skill Detection
        normalized = [self.normalize(s) for s in skills]
        
        # 2. Contextual Proficiency Estimation
        if context_text:
            normalized = [self.estimate_proficiency(s, context_text) for s in normalized]
            
        # 3. Hierarchy Inference
        final_skills = self.infer_hierarchy(normalized)
        
        return final_skills
