import json
import os

def calculate_overlap(resume_skills, jd_required):
    if not jd_required: return 1.0
    found = [s for s in jd_required if s in resume_skills]
    return len(found) / len(jd_required)

def generate_ground_truth():
    print("--- Generating Ground Truth Match Dataset ---")
    
    with open("data/samples/ground_truth_resumes.json", "r") as f:
        resumes = json.load(f)
        
    with open("data/samples/jds.json", "r") as f:
        jds = json.load(f)
        
    matches = []
    
    # Calculate truth for all pairs (or a subset for large datasets)
    for jd in jds[:20]: # Only first 20 JDs to keep file size manageable
        for res in resumes:
            score = calculate_overlap(res["skills"], jd["required_skills"])
            matches.append({
                "jd_id": jd["id"],
                "resume_id": res["id"],
                "true_score": score
            })
            
    with open("data/samples/ground_truth_matches.json", "w") as f:
        json.dump(matches, f, indent=2)
        
    print(f"Successfully generated {len(matches)} ground truth matches.")

if __name__ == "__main__":
    generate_ground_truth()
