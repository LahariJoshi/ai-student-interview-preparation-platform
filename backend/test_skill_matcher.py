from app.modules.ats.services.skill_matcher import (
    calculate_skill_match,
)


resume = """
Computer Science student with experience in Python,
FastAPI, PostgreSQL, Machine Learning, Git and Docker.
Developed backend APIs using FastAPI and REST APIs.
"""


job_description = """
We are looking for a Python developer with experience in
FastAPI, PostgreSQL, Docker, Git, Machine Learning and AWS.
Knowledge of React is preferred.
"""


result = calculate_skill_match(
    resume_text=resume,
    job_description=job_description,
)


print("\n========== KEYWORD MATCH ANALYSIS ==========")

print(
    "Keyword Match Score:",
    result["keyword_match_score"],
)

print(
    "Matched Skills:",
    result["matched_skills"],
)

print(
    "Missing Skills:",
    result["missing_skills"],
)

print(
    "Matched Count:",
    result["matched_count"],
)

print(
    "Total JD Skills:",
    result["total_jd_skills"],
)