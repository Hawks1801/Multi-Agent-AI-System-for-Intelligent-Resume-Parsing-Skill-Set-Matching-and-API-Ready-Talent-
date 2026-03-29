from fastapi import APIRouter
import json

router = APIRouter()

@router.get("/taxonomy")
async def get_taxonomy():
    """Returns the full hierarchical skill taxonomy."""
    with open("data/taxonomy/skills_large.json", "r") as f:
        return json.load(f)
