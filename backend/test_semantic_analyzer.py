from app.modules.ats.services.semantic_analyzer import (
    calculate_semantic_similarity,
)


resume = """
Computer Science student with experience in Python,
FastAPI, PostgreSQL, Machine Learning and backend API development.
Developed AI-powered applications and REST APIs.
"""


relevant_jd = """
Looking for a Python developer with experience in FastAPI,
PostgreSQL, Machine Learning and backend API development.
"""


unrelated_jd = """
Looking for a graphic designer with experience in Photoshop,
Illustrator, Figma, typography, branding and visual design.
"""


print("\n========== RELEVANT JD ==========")

result = calculate_semantic_similarity(
    resume,
    relevant_jd,
)

print("Cosine Similarity:", result["cosine_similarity"])
print("Semantic Score:", result["semantic_score"])


print("\n========== UNRELATED JD ==========")

result = calculate_semantic_similarity(
    resume,
    unrelated_jd,
)

print("Cosine Similarity:", result["cosine_similarity"])
print("Semantic Score:", result["semantic_score"])