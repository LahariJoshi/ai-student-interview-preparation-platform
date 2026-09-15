"""
Resume Analyzer — orchestrates all sub-services to produce a complete
deterministic resume analysis. No LLMs, no external APIs.
"""

from datetime import datetime, timezone
from typing import Any, Dict

from app.modules.resume.services.section_detector import detect_sections
from app.modules.resume.services.contact_detector import detect_contact
from app.modules.resume.services.skill_detector import detect_skills
from app.modules.resume.services.quality_analyzer import compute_quality_score
from app.modules.resume.services.gap_generator import generate_gaps


def analyze_resume(raw_text: str, word_count: int, character_count: int) -> Dict[str, Any]:
    """
    Run all sub-services on the raw resume text and return a structured
    analysis result dict that can be persisted directly into ResumeAnalysis.

    Args:
        raw_text:        Extracted plain text from the resume file.
        word_count:      Pre-computed word count (from Resume.word_count).
        character_count: Pre-computed character count (from Resume.character_count).

    Returns:
        {
            "sections": Dict[str, bool],
            "contact": Dict[str, bool],
            "skills": Dict[str, List[str]],
            "quality_details": Dict[str, Any],
            "quality_score": float,
            "gaps": List[Dict[str, str]],
            "analyzed_at": datetime,
        }
    """
    # 1. Detect sections
    sections = detect_sections(raw_text)

    # 2. Detect contact info (boolean flags only)
    contact = detect_contact(raw_text)

    # 3. Detect skills by category
    skills = detect_skills(raw_text)

    # 4. Compute quality score + breakdown
    quality_details = compute_quality_score(
        sections=sections,
        contact=contact,
        word_count=word_count,
        character_count=character_count,
        skills=skills,
    )
    quality_score: float = quality_details["total_score"]

    # 5. Generate evidence-based improvement gaps
    gaps = generate_gaps(
        sections=sections,
        contact=contact,
        word_count=word_count,
        skills=skills,
    )

    return {
        "sections": sections,
        "contact": contact,
        "skills": skills,
        "quality_details": quality_details,
        "quality_score": quality_score,
        "gaps": gaps,
        "analyzed_at": datetime.now(timezone.utc),
    }
