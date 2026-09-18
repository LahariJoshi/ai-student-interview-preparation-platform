from app.modules.ats.services.ats_analyzer import (
    calculate_ats_score,
)


resume = """
Lahari Joshi
lahari@example.com
+91 9876543210
linkedin.com/in/lahari
github.com/lahari

SUMMARY

Computer Science student interested in Artificial Intelligence
and Machine Learning.

EDUCATION

B.Tech in Computer Science and Engineering
CMR College of Engineering and Technology

SKILLS

Python, Java, FastAPI, PostgreSQL, Git, Machine Learning, Docker

PROJECTS

• Developed an AI-powered student interview preparation platform.
• Built REST APIs using FastAPI and PostgreSQL.
• Implemented resume analysis and ATS matching.
• Improved backend processing by 30%.

EXPERIENCE

• Developed backend applications using Python and FastAPI.
• Automated API testing and deployment workflows.

CERTIFICATIONS

• Google Cloud certification
• Python certification
"""


job_description = """
We are looking for a Python developer with experience in
FastAPI, PostgreSQL, Docker, Git, Machine Learning and AWS.

The candidate should have experience developing backend APIs,
building scalable applications and working with REST APIs.

Knowledge of React and cloud technologies is preferred.
"""


result = calculate_ats_score(
    resume_text=resume,
    job_description=job_description,
)


print("\n========== FINAL ATS ANALYSIS ==========")

print(
    "Final ATS Score:",
    result["ats_score"],
    "/100",
)

print("\n========== COMPONENT SCORES ==========")

for name, score in result["component_scores"].items():
    print(f"{name}: {score}")

print("\n========== ACTION / IMPACT ==========")

print(
    "Action Verb Score:",
    result["action_impact_details"]["action_verb_score"],
)

print(
    "Metrics Score:",
    result["action_impact_details"]["metrics_score"],
)

print(
    "Action/Impact Score:",
    result["component_scores"]["action_impact_score"],
)

print("\n========== SKILL MATCHING ==========")

print(
    "Matched Skills:",
    result["matched_skills"],
)

print(
    "Missing Skills:",
    result["missing_skills"],
)

print(
    "JD Skills:",
    result["jd_skills"],
)