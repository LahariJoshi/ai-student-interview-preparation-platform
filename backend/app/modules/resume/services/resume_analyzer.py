"""
Resume Analyzer — orchestrates all sub-services to produce a complete
deterministic resume analysis. No LLMs, no external APIs.
"""

from datetime import datetime, timezone
from typing import Any, Dict

from app.modules.resume.services.section_detector import detect_sections
from app.modules.resume.services.contact_detector import detect_contact
from app.modules.resume.services.skill_detector import detect_skills

from app.modules.resume.services.quality_analyzer import (
    compute_quality_score,
    compute_advanced_quality_score,
)

from app.modules.resume.services.gap_generator import generate_gaps

# M4 advanced analysis services
from app.modules.resume.services.section_extractor import extract_sections
from app.modules.resume.services.length_analyzer import analyze_resume_length
from app.modules.resume.services.action_verb_detector import detect_action_verbs
from app.modules.resume.services.metrics_detector import detect_metrics
from app.modules.resume.services.project_analyzer import analyze_projects
from app.modules.resume.services.skill_quality_analyzer import analyze_skill_quality
from app.modules.resume.services.summary_analyzer import analyze_summary


def analyze_resume(
    raw_text: str,
    word_count: int,
    character_count: int,
) -> Dict[str, Any]:
    """
    Run all M3 and M4 sub-services on the raw resume text.

    Returns a structured analysis result that can be persisted
    into ResumeAnalysis.
    """

    # ================================================================
    # M3 — STRUCTURAL ANALYSIS
    # ================================================================

    # 1. Detect resume sections
    sections = detect_sections(raw_text)

    # 2. Detect contact information
    contact = detect_contact(raw_text)

    # 3. Detect categorized skills
    skills = detect_skills(raw_text)

    # 4. Compute the original M3 quality score
    #
    # This is retained for backward compatibility and comparison.
    quality_details = compute_quality_score(
        sections=sections,
        contact=contact,
        word_count=word_count,
        character_count=character_count,
        skills=skills,
    )

    # ================================================================
    # M4 — ADVANCED QUALITY ANALYSIS
    # ================================================================

    # 5. Extract the actual text belonging to each section
    section_texts = extract_sections(raw_text)

    # 6. Analyze resume length and content density
    length_analysis = analyze_resume_length(raw_text)

    # 7. Analyze action verbs
    action_analysis = detect_action_verbs(raw_text)

    # 8. Detect quantifiable achievements / metrics
    metrics_analysis = detect_metrics(raw_text)

    # 9. Analyze project quality
    project_text = section_texts.get("projects", "")

    project_analysis = analyze_projects(
        project_text=project_text,
        project_count=1 if project_text.strip() else 0,
    )

    # 10. Analyze skill breadth and category diversity
    skill_quality_analysis = analyze_skill_quality(skills)

    # 11. Analyze summary quality
    summary_text = section_texts.get("summary", "")

    summary_analysis = analyze_summary(summary_text)

    # 12. Compute the final M4 quality score
    advanced_quality_details = compute_advanced_quality_score(
        sections=sections,
        contact=contact,
        skills=skills,
        length_analysis=length_analysis,
        action_analysis=action_analysis,
        metrics_analysis=metrics_analysis,
        project_analysis=project_analysis,
        skill_quality_analysis=skill_quality_analysis,
        summary_analysis=summary_analysis,
    )

    # The M4 score becomes the final resume quality score.
    quality_score = advanced_quality_details["total_score"]

    # ================================================================
    # M3 — GAP GENERATION
    # ================================================================

    # 13. Generate evidence-based improvement gaps
    gaps = generate_gaps(
        sections=sections,
        contact=contact,
        word_count=word_count,
        skills=skills,
    )

    # ================================================================
    # FINAL RESULT
    # ================================================================

    return {
        "sections": sections,
        "contact": contact,
        "skills": skills,

        # Original M3 structural analysis
        "quality_details": quality_details,

        # New M4 advanced analysis
        "advanced_quality_details": advanced_quality_details,

        # Final score = M4 score
        "quality_score": quality_score,

        "gaps": gaps,

        "analyzed_at": datetime.now(timezone.utc),
    }