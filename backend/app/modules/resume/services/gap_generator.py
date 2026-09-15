"""
Gap Generator — produces evidence-based improvement gaps from analysis results.

Rules:
  - Every gap must be directly supported by the detected data.
  - Never generate vague or presumptuous gaps (e.g. "You have no experience").
  - Each gap has a 'message' (human-readable) and a 'category' (machine tag).
"""

from typing import Dict, List, Any


def generate_gaps(
    sections: Dict[str, bool],
    contact: Dict[str, bool],
    word_count: int,
    skills: Dict[str, List[str]],
) -> List[Dict[str, str]]:
    """
    Return a list of gap dicts, each with 'message' and 'category'.

    Args:
        sections: output of detect_sections()
        contact:  output of detect_contact()
        word_count: total word count of the extracted text
        skills:   output of detect_skills()

    Returns:
        List[{"message": str, "category": str}]
    """
    gaps: List[Dict[str, str]] = []

    # ── Section gaps ──────────────────────────────────────────────────────────
    if not sections.get("summary"):
        gaps.append({
            "message": "Summary/Objective section not detected. Adding a professional summary helps recruiters quickly understand your profile.",
            "category": "sections",
        })

    if not sections.get("education"):
        gaps.append({
            "message": "Education section not detected. Including your educational background is essential for student resumes.",
            "category": "sections",
        })

    if not sections.get("skills"):
        gaps.append({
            "message": "Skills section not detected. A dedicated skills section makes your technical competencies easy to find.",
            "category": "sections",
        })

    if not sections.get("projects"):
        gaps.append({
            "message": "Projects section not detected. Showcasing projects is especially important for students without extensive work experience.",
            "category": "sections",
        })

    # ── Contact gaps ──────────────────────────────────────────────────────────
    if not contact.get("has_email"):
        gaps.append({
            "message": "Email address not detected. Ensure your contact email is clearly visible.",
            "category": "contact",
        })

    if not contact.get("has_phone"):
        gaps.append({
            "message": "Phone number not detected. Adding a contact number improves recruiter reachability.",
            "category": "contact",
        })

    if not contact.get("has_linkedin"):
        gaps.append({
            "message": "LinkedIn profile URL not detected. Adding a LinkedIn link (linkedin.com/in/...) strengthens your professional presence.",
            "category": "contact",
        })

    if not contact.get("has_github"):
        gaps.append({
            "message": "GitHub profile URL not detected. For technical roles, a GitHub link (github.com/...) demonstrates your coding activity.",
            "category": "contact",
        })

    # ── Content quality gaps ──────────────────────────────────────────────────
    if word_count < 150:
        gaps.append({
            "message": f"Resume appears short ({word_count} words detected). A strong resume typically contains at least 150–300 words.",
            "category": "content",
        })

    total_skills = sum(len(v) for v in skills.values())
    if total_skills < 3:
        gaps.append({
            "message": "Very few or no recognisable technical skills detected. Ensure technical skills are listed clearly using standard terminology.",
            "category": "skills",
        })

    categories_with_skills = sum(1 for v in skills.values() if v)
    if total_skills >= 3 and categories_with_skills < 2:
        gaps.append({
            "message": "Skills detected in only one category. Demonstrating breadth across multiple skill areas (e.g. languages + tools + databases) is beneficial.",
            "category": "skills",
        })

    return gaps
