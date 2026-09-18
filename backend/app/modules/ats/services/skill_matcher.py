from typing import Dict, List, Any

from app.modules.ats.services.skill_extractor import extract_skills


# Different names that should be treated as the same skill.
SKILL_ALIASES = {
    "javascript": "javascript",
    "java script": "javascript",

    "typescript": "typescript",
    "type script": "typescript",

    "postgres": "postgresql",
    "postgresql": "postgresql",

    "mysql": "mysql",

    "nodejs": "node.js",
    "node.js": "node.js",

    "reactjs": "react",
    "react.js": "react",

    "nextjs": "next.js",
    "next.js": "next.js",

    "expressjs": "express.js",
    "express.js": "express.js",

    "rest": "rest api",
    "rest api": "rest api",
    "restful api": "rest api",

    "machine learning": "machine learning",
    "ml": "machine learning",

    "artificial intelligence": "artificial intelligence",
    "ai": "artificial intelligence",

    "large language model": "large language models",
    "large language models": "large language models",
    "llm": "large language models",

    "object oriented programming": "object oriented programming",
    "oop": "object oriented programming",

    "database management systems": "database management systems",
    "dbms": "database management systems",
}


def normalize_skill(skill: str) -> str:
    """
    Convert skill names into a common representation.
    """
    normalized = skill.lower().strip()

    return SKILL_ALIASES.get(
        normalized,
        normalized,
    )


def flatten_skills(
    skills_by_category: Dict[str, List[str]],
) -> Dict[str, str]:
    """
    Convert category-wise skills into:
        normalized_skill -> original_skill
    """

    flattened: Dict[str, str] = {}

    for skills in skills_by_category.values():
        for skill in skills:
            normalized = normalize_skill(skill)
            flattened[normalized] = skill

    return flattened


def calculate_skill_match(
    resume_text: str,
    job_description: str,
) -> Dict[str, Any]:
    """
    Compare skills found in a resume against skills
    found in a job description.
    """

    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")

    if not job_description or not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    resume_skills_by_category = extract_skills(resume_text)
    jd_skills_by_category = extract_skills(job_description)

    resume_skills = flatten_skills(resume_skills_by_category)
    jd_skills = flatten_skills(jd_skills_by_category)

    matched_skills: List[str] = []
    missing_skills: List[str] = []

    for normalized_skill, original_skill in jd_skills.items():

        if normalized_skill in resume_skills:
            matched_skills.append(original_skill)
        else:
            missing_skills.append(original_skill)

    total_jd_skills = len(jd_skills)
    matched_count = len(matched_skills)

    if total_jd_skills == 0:
        keyword_match_score = 0.0
    else:
        keyword_match_score = (
            matched_count / total_jd_skills
        ) * 100.0

    return {
        "keyword_match_score": round(
            keyword_match_score,
            2,
        ),
        "matched_skills": sorted(
            set(matched_skills),
            key=str.lower,
        ),
        "missing_skills": sorted(
            set(missing_skills),
            key=str.lower,
        ),
        "resume_skills": sorted(
            set(resume_skills.values()),
            key=str.lower,
        ),
        "jd_skills": sorted(
            set(jd_skills.values()),
            key=str.lower,
        ),
        "matched_count": matched_count,
        "total_jd_skills": total_jd_skills,
    }
