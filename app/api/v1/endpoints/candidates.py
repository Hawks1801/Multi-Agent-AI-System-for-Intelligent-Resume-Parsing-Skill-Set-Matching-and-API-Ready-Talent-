from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict
import json
import os
from app.core.security import get_api_key

router = APIRouter()

@router.get("/{id}/skills")
async def get_candidate_skills(id: str, api_key: str = Depends(get_api_key)):
    """Retrieves the skill profile for a specific candidate from the trained dataset."""
    gt_path = "data/samples/ground_truth_resumes.json"
    if not os.path.exists(gt_path):
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    with open(gt_path, "r") as f:
        all_resumes = json.load(f)
        match = next((r for r in all_resumes if r["id"] == id), None)
        
    if not match:
        raise HTTPException(status_code=404, detail=f"Candidate with ID {id} not found")
        
    return {
        "candidate_id": id,
        "name": match["name"],
        "skills": match["skills"]
    }
