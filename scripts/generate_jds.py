import json
import random
import os

def generate_jds():
    print("--- Generating 100+ Synthetic Job Descriptions ---")
    
    roles = [
        "Software Engineer", "Frontend Developer", "Backend Engineer", "Full Stack Developer",
        "Data Scientist", "Machine Learning Engineer", "DevOps Engineer", "Cloud Architect",
        "Product Manager", "UI/UX Designer", "Cybersecurity Analyst", "Data Engineer",
        "System Administrator", "Quality Assurance Engineer", "Mobile App Developer"
    ]
    
    levels = ["Junior", "Senior", "Lead", "Principal", "Staff"]
    
    # Load base skills for relevance
    with open("data/taxonomy/skills_large.json", "r") as f:
        taxonomy = json.load(f)
    
    all_tech_skills = []
    def get_skills(data):
        if isinstance(data, list): all_tech_skills.extend(data)
        elif isinstance(data, dict):
            for v in data.values(): get_skills(v)
    
    get_skills(taxonomy["Technology"])
    
    jds = []
    for i in range(110):
        role = random.choice(roles)
        level = random.choice(levels)
        title = f"{level} {role}"
        
        # Pick 4-7 required skills and 2-4 nice-to-have
        req = random.sample(all_tech_skills if 'tech' in role.lower() else all_tech_skills, random.randint(4, 7))
        nice = random.sample([s for s in all_tech_skills if s not in req], random.randint(2, 4))
        
        jd = {
            "id": f"jd_{i+1}",
            "title": title,
            "description": f"We are looking for a {title} to join our growing team. You will be responsible for building scalable systems and collaborating with cross-functional teams using {', '.join(req)}.",
            "required_skills": req,
            "nice_to_have_skills": nice,
            "experience_level": level
        }
        jds.append(jd)
        
    os.makedirs("data/samples", exist_ok=True)
    with open("data/samples/jds.json", "w") as f:
        json.dump(jds, f, indent=2)
        
    print(f"Successfully generated {len(jds)} job descriptions in data/samples/jds.json")

if __name__ == "__main__":
    # Fix for variable name in script
    import sys
    content = open(__file__).read().replace("all_tech_skills", "all_tech_skills")
    with open(__file__, "w") as f: f.write(content)
    
    generate_jds()
