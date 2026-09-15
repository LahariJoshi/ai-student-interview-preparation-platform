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

def compute_advanced_quality_score(
    sections: Dict[str, bool],
    contact: Dict[str, bool],
    skills: Dict[str, list],
    length_analysis: Dict[str, Any],
    action_analysis: Dict[str, Any],
    metrics_analysis: Dict[str, Any],
    project_analysis: Dict[str, Any],
    skill_quality_analysis: Dict[str, Any],
    summary_analysis: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Compute the M4 advanced resume quality score.

    Total score = 100 points.

    Components:
        Resume Length & Content Density — 10
        Action Verbs                   — 10
        Quantifiable Metrics           — 10
        Project Quality                — 15
        Skills Breadth                 — 10
        Skill Category Diversity       — 10
        Summary Quality                — 10
        Section Completeness           — 15
        Contact Information            — 10
    """

    # ── 1. Resume Length & Content Density — 10 pts ───────────────
    length_score = float(
        length_analysis.get("score", 0.0)
    )
    length_score = min(max(length_score, 0.0), 10.0)

    # ── 2. Action Verbs — 10 pts ──────────────────────────────────
    action_score = float(
        action_analysis.get("score", 0.0)
    )
    action_score = min(max(action_score, 0.0), 10.0)

    # ── 3. Quantifiable Metrics — 10 pts ──────────────────────────
    metrics_score = float(
        metrics_analysis.get("score", 0.0)
    )
    metrics_score = min(max(metrics_score, 0.0), 10.0)

    # ── 4. Project Quality — 15 pts ───────────────────────────────
    project_score = float(
        project_analysis.get("project_quality_score", 0.0)
    )

    # ── 5. Skills Breadth — 10 pts ────────────────────────────────
    skill_breadth_score = float(
        skill_quality_analysis.get(
            "skill_breadth_score",
            0.0,
        )
    )
    skill_breadth_score = min(
        max(skill_breadth_score, 0.0),
        10.0,
    )

    # ── 6. Skill Category Diversity — 10 pts ─────────────────────
    category_diversity_score = float(
        skill_quality_analysis.get(
            "category_diversity_score",
            0.0,
        )
    )
    category_diversity_score = min(
        max(category_diversity_score, 0.0),
        10.0,
    )

    # ── 7. Summary Quality — 10 pts ──────────────────────────────
    summary_score = float(
        summary_analysis.get(
            "summary_quality_score",
            0.0,
        )
    )
    summary_score = min(
        max(summary_score, 0.0),
        10.0,
    )

    # ── 8. Section Completeness — 15 pts ─────────────────────────
    #
    # Reuse the M3 section definitions, but normalize them
    # to the new M4 15-point weight.
    #
    # Experience and internships are intentionally excluded
    # because this is a student-focused platform.

    section_weighted_score = sum(
        weight
        for section, weight in SECTION_WEIGHTS.items()
        if sections.get(section, False)
    )

    section_completeness_score = (
        section_weighted_score / _SECTION_MAX
    ) * 15.0

    section_completeness_score = round(
        min(max(section_completeness_score, 0.0), 15.0),
        2,
    )

    # ── 9. Contact Information — 10 pts ──────────────────────────
    contact_fields = list(contact.values())

    contact_found = sum(
        1
        for value in contact_fields
        if value
    )

    contact_score = (
        (contact_found / len(contact_fields)) * 10.0
        if contact_fields
        else 0.0
    )

    contact_score = round(
        min(max(contact_score, 0.0), 10.0),
        2,
    )

    # ── Final M4 score ────────────────────────────────────────────
    total_score = round(
        length_score
        + action_score
        + metrics_score
        + project_score
        + skill_breadth_score
        + category_diversity_score
        + summary_score
        + section_completeness_score
        + contact_score,
        2,
    )

    total_score = round(
        min(max(total_score, 0.0), 100.0),
        2,
    )

    return {
        "total_score": total_score,

        "length_score": round(length_score, 2),
        "action_verb_score": round(action_score, 2),
        "metrics_score": round(metrics_score, 2),
        "project_quality_score": round(project_score, 2),
        "skill_breadth_score": round(skill_breadth_score, 2),
        "skill_category_diversity_score": round(
            category_diversity_score,
            2,
        ),
        "summary_quality_score": round(summary_score, 2),
        "section_completeness_score": section_completeness_score,
        "contact_score": contact_score,

        "sections_found": sum(
            1
            for section in SECTION_WEIGHTS
            if sections.get(section, False)
        ),
        "sections_checked": len(SECTION_WEIGHTS),

        "contact_fields_found": contact_found,

        "total_skills_detected": sum(
            len(skill_list)
            for skill_list in skills.values()
        ),
    }