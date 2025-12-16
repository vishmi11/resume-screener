import json
import os

# Get the absolute path to the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SKILLS_FILE = os.path.join(BASE_DIR, "skills.json")

with open(SKILLS_FILE, "r") as f:
    SKILLS_DICT = json.load(f)

def match_skills(text: str, role_key: str):
    """
    text: resume text (cleaned)
    role_key: one of the keys in skills.json e.g. "data_analyst"
    returns: matched skills, missing skills, match score %
    """
    text = text.lower()
    role_skills = SKILLS_DICT.get(role_key, [])
    matched = [skill for skill in role_skills if skill.lower() in text]
    missing = [skill for skill in role_skills if skill.lower() not in text]
    score = round(len(matched) / len(role_skills) * 100, 2) if role_skills else 0
    return matched, missing, score
