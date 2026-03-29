from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks
import shutil
import os
import uuid
from typing import List, Dict
from app.agents.orchestrator import ResumeOrchestrator
from app.core.security import get_api_key

router = APIRouter()
orchestrator = ResumeOrchestrator()

# In-memory store for async batch jobs (production would use Redis/Postgres)
batch_jobs: Dict[str, Dict] = {}

@router.post("/")
async def parse_resume(file: UploadFile = File(...), api_key: str = Depends(get_api_key)):
    """Parses a single resume file and returns structured data."""
    temp_dir = "data/temp"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = f"{temp_dir}/{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        result = orchestrator.run(file_path=file_path)
        if result.get("errors"):
            raise HTTPException(status_code=500, detail=result["errors"])
        return result["normalized_resume"]
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@router.post("/batch")
async def parse_resume_batch(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...), 
    api_key: str = Depends(get_api_key)
):
    """Starts a batch processing job for multiple resumes."""
    job_id = str(uuid.uuid4())
    batch_jobs[job_id] = {"status": "processing", "results": [], "total": len(files)}
    
    background_tasks.add_task(process_batch, job_id, files)
    return {"job_id": job_id, "message": "Batch processing started"}

@router.get("/batch/{job_id}")
async def get_batch_status(job_id: str, api_key: str = Depends(get_api_key)):
    """Retrieves the status and results of a batch job."""
    if job_id not in batch_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return batch_jobs[job_id]

async def process_batch(job_id: str, files: List[UploadFile]):
    """Background worker for batch processing."""
    results = []
    temp_dir = "data/temp"
    os.makedirs(temp_dir, exist_ok=True)

    for file in files:
        file_path = f"{temp_dir}/{uuid.uuid4()}_{file.filename}"
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            res = orchestrator.run(file_path=file_path)
            results.append({
                "filename": file.filename,
                "status": "success",
                "data": res.get("normalized_resume")
            })
        except Exception as e:
            results.append({"filename": file.filename, "status": "error", "error": str(e)})
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
    
    batch_jobs[job_id]["status"] = "completed"
    batch_jobs[job_id]["results"] = results
