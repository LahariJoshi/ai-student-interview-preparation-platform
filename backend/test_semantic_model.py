
from sentence_transformers import SentenceTransformer, util


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


print("Loading model...")

model = SentenceTransformer(MODEL_NAME)

print("Model loaded successfully!")


resume_text = """
Computer Science student with experience in Python,
FastAPI, PostgreSQL, machine learning and web development.
Developed backend APIs and AI-powered applications.
"""

job_description = """
Looking for a Python developer with experience in FastAPI,
PostgreSQL, machine learning and backend API development.
"""

unrelated_job_description = """
Looking for a graphic designer with experience in Adobe Photoshop,
Illustrator, Figma, UI design, branding, typography and visual design.
The candidate should have strong creativity and experience creating
marketing materials and social media graphics.
"""

resume_embedding = model.encode(resume_text)
jd_embedding = model.encode(job_description)
similarity = util.cos_sim(
    resume_embedding,
    jd_embedding
).item()

semantic_score = max(0.0, min(100.0, similarity * 100))

print("\n========== SEMANTIC SIMILARITY ==========")
print(f"Cosine similarity: {similarity:.4f}")
print(f"Semantic score: {semantic_score:.2f}/100")


print("\nEmbedding test successful!")

print("Resume embedding dimensions:", len(resume_embedding))
print("JD embedding dimensions:", len(jd_embedding))

unrelated_jd_embedding = model.encode(unrelated_job_description)

unrelated_similarity = util.cos_sim(
    resume_embedding,
    unrelated_jd_embedding
).item()

unrelated_score = max(0.0, min(100.0, unrelated_similarity * 100))

print("\n========== COMPARISON TEST ==========")
print(f"Relevant JD similarity:   {similarity:.4f}")
print(f"Relevant JD score:         {semantic_score:.2f}/100")

print(f"Unrelated JD similarity:   {unrelated_similarity:.4f}")
print(f"Unrelated JD score:       {unrelated_score:.2f}/100")
