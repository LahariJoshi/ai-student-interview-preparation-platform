"""
Quality Analyzer — computes a 0–100 quality score and detailed breakdown.

Score components:
  Section Completeness  — 40 pts
  Contact Information   — 15 pts
  Content Quality       — 45 pts

Student-focused rules:
  - Education, Skills, Projects, Summary and Certifications contribute
    to section completeness.
  - Experience and Internships are not penalized when missing because
    students may not have professional experience.
  - Contact information is scored separately and is not included
    in section completeness.
  - All scores are clamped to their valid ranges.
"""

from typing import Dict, Any


# Sections that contribute to the 40-point completeness score.
#
# Contact is intentionally excluded because it has its own
# separate 15-point score.
#
# Experience and Internships are intentionally excluded because
# the platform is student-focused and students may not have
# professional experience.
SECTION_WEIGHTS = {
    "education": 10.0,
    "skills": 10.0,
    "projects": 10.0,
    "summary": 5.0,
    "certifications": 5.0,
}

_SECTION_MAX = 40.0
_CONTACT_MAX = 15.0
_CONTENT_MAX = 45.0


def compute_quality_score(
    sections: Dict[str, bool],
    contact: Dict[str, bool],
    word_count: int,
    character_count: int,
    skills: Dict[str, list],
) -> Dict[str, Any]:
    """
    Compute the resume quality score and detailed breakdown.

    Returns:
        {
            "total_score": float,          # 0.0–100.0
            "section_score": float,        # 0.0–40.0
            "contact_score": float,        # 0.0–15.0
            "content_score": float,        # 0.0–45.0
            "sections_found": int,
            "sections_checked": int,
            "contact_fields_found": int,
            "total_skills_detected": int,
        }
    """

    # ── 1. Section completeness (40 pts) ──────────────────────────────────
    #
    # Each section has a defined weight.
    # Missing Experience/Internships do not affect this score.

    section_score = sum(
        weight
        for section, weight in SECTION_WEIGHTS.items()
        if sections.get(section, False)
    )

    section_score = round(
        min(section_score, _SECTION_MAX),
        2,
    )

    sections_found = sum(
        1
        for section in SECTION_WEIGHTS
        if sections.get(section, False)
    )

    # ── 2. Contact information (15 pts) ───────────────────────────────────
    #
    # Four contact fields are currently detected:
    # email, phone, LinkedIn and GitHub.
    #
    # Each contributes equally: 15 / 4 = 3.75 points.

    contact_fields = list(contact.values())

    contact_found = sum(
        1
        for value in contact_fields
        if value
    )

    contact_score = (
        round(
            (contact_found / len(contact_fields)) * _CONTACT_MAX,
            2,
        )
        if contact_fields
        else 0.0
    )

    contact_score = min(
        contact_score,
        _CONTACT_MAX,
    )

    # ── 3. Content quality (45 pts) ───────────────────────────────────────
    content_score = 0.0

    # a) Word count adequacy (up to 20 pts)
    if word_count >= 300:
        content_score += 20.0
    elif word_count >= 150:
        content_score += 12.0
    elif word_count >= 50:
        content_score += 6.0

    # b) Skills breadth (up to 15 pts)
    total_skills = sum(
        len(skill_list)
        for skill_list in skills.values()
    )

    if total_skills >= 15:
        content_score += 15.0
    elif total_skills >= 8:
        content_score += 10.0
    elif total_skills >= 3:
        content_score += 5.0

    # c) Skill category diversity (up to 10 pts)
    categories_with_skills = sum(
        1
        for skill_list in skills.values()
        if skill_list
    )

    if categories_with_skills >= 4:
        content_score += 10.0
    elif categories_with_skills >= 2:
        content_score += 5.0

    content_score = min(
        round(content_score, 2),
        _CONTENT_MAX,
    )

    # ── 4. Final score ────────────────────────────────────────────────────
    total_score = round(
        section_score
        + contact_score
        + content_score,
        2,
    )

    total_score = max(
        0.0,
        min(100.0, total_score),
    )

    return {
        "total_score": total_score,
        "section_score": section_score,
        "contact_score": contact_score,
        "content_score": content_score,
        "sections_found": sections_found,
        "sections_checked": len(SECTION_WEIGHTS),
        "contact_fields_found": contact_found,
        "total_skills_detected": total_skills,
    }