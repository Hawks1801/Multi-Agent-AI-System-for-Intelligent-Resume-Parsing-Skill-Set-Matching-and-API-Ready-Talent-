from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
import shutil
import os
import json
from app.agents.orchestrator import ResumeOrchestrator
from app.models.domain.matcher import JobDescription
from app.core.security import get_api_key

router = APIRouter()
orchestrator = ResumeOrchestrator()

@router.post("/")
async def match_resume(
    file: UploadFile = File(...),
    job_description_json: str = Form(...),
    api_key: str = Depends(get_api_key)
):

    # 1. Parse Job Description
    try:
        jd_data = json.loads(job_description_json)
        jd = JobDescription(**jd_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid job description JSON: {str(e)}")

    # 2. Save uploaded file temporarily
    temp_dir = "data/temp"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = f"{temp_dir}/{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # 3. Run orchestrator
        result = orchestrator.run(file_path=file_path, job_description=jd)
        
        if result.get("errors"):
            raise HTTPException(status_code=500, detail=result["errors"])
            
        return {
            "candidate": result["normalized_resume"],
            "match": result["match_result"]
        }
        
    finally:
        # 4. Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)
