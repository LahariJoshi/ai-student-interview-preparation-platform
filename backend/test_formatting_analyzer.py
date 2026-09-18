from app.modules.ats.services.formatting_analyzer import analyze_formatting
from app.modules.resume.services.section_detector import detect_sections
from app.modules.resume.services.contact_detector import detect_contact
from app.modules.resume.services.length_analyzer import analyze_resume_length


sample_resume = """
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

Python, Java, FastAPI, PostgreSQL, Git, Machine Learning

PROJECTS

• Developed an AI-powered student interview preparation platform.
• Built REST APIs using FastAPI and PostgreSQL.
• Implemented resume analysis and ATS matching.

INTERNSHIPS

• Worked on web development and backend API development.

CERTIFICATIONS

• Google Cloud certification
• Python certification
"""


sections = detect_sections(sample_resume)
contact = detect_contact(sample_resume)
length_analysis = analyze_resume_length(sample_resume)

result = analyze_formatting(
    raw_text=sample_resume,
    sections=sections,
    contact=contact,
    length_analysis=length_analysis,
)

print("\\n========== FORMATTING ANALYSIS ==========")
print(f"Formatting Score: {result['score']}/100")

print("\\n--- Details ---")

for component, score in result["details"].items():
    print(f"{component}: {score}")

print("\n--- Missing Core Sections ---")
print(result["missing_sections"])


print("\n--- Strengths ---")

for strength in result["strengths"]:
    print(f"✓ {strength}")


print("\n--- Issues ---")

for issue in result["issues"]:
    print(f"⚠ {issue}")


print("\n--- Resume Information ---")
print(f"Word Count: {result['word_count']}")
print(f"Content Density: {result['content_density']}")