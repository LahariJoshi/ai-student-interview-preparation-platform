from typing import Any, Dict

from app.modules.ats.services.formatting_analyzer import analyze_formatting
from app.modules.ats.services.skill_matcher import calculate_skill_match
from app.modules.ats.services.semantic_analyzer import calculate_semantic_similarity

from app.modules.resume.services.section_detector import detect_sections
from app.modules.resume.services.contact_detector import detect_contact
from app.modules.resume.services.length_analyzer import analyze_resume_length
from app.modules.resume.services.action_verb_detector import detect_action_verbs
from app.modules.resume.services.metrics_detector import detect_metrics


def calculate_ats_score(
    resume_text: str,
    job_description: str,
) -> Dict[str, Any]:
    """
    Calculate the combined ATS score using:

    - Formatting: 25%
    - Keyword Match: 35%
    - Semantic Similarity: 25%
    - Action/Impact: 15%
    """

    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")

    if not job_description or not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    # --------------------------------------------------
    # 1. Resume structural information
    # --------------------------------------------------

    sections = detect_sections(resume_text)
    contact = detect_contact(resume_text)
    length_analysis = analyze_resume_length(resume_text)

    # --------------------------------------------------
    # 2. Formatting analysis
    # --------------------------------------------------

    formatting_result = analyze_formatting(
        raw_text=resume_text,
        sections=sections,
        contact=contact,
        length_analysis=length_analysis,
    )

    formatting_score = float(
        formatting_result.get("score", 0.0)
    )

    # --------------------------------------------------
    # 3. Keyword / skill matching
    # --------------------------------------------------

    skill_match_result = calculate_skill_match(
        resume_text=resume_text,
        job_description=job_description,
    )

    keyword_match_score = float(
        skill_match_result.get(
            "keyword_match_score",
            0.0,
        )
    )

    # --------------------------------------------------
    # 4. Semantic similarity
    # --------------------------------------------------

    semantic_result = calculate_semantic_similarity(
        resume_text=resume_text,
        job_description=job_description,
    )

    semantic_score = float(
        semantic_result.get(
            "semantic_score",
            0.0,
        )
    )

    # --------------------------------------------------
    # 5. Action / Impact analysis
    # --------------------------------------------------

    action_result = detect_action_verbs(resume_text)
    metrics_result = detect_metrics(resume_text)

    action_score = float(
        action_result.get("score", 0.0)
    )

    metrics_score = float(
        metrics_result.get("score", 0.0)
    )

    # Both existing analyzers return scores out of 10.
    # Their average becomes the Action/Impact score out of 10.
    action_impact_score = (
        action_score + metrics_score
    ) / 2.0

    # Convert from /10 to /100.
    action_impact_score_100 = (
        action_impact_score / 10.0
    ) * 100.0

    # --------------------------------------------------
    # 6. Final ATS score
    # --------------------------------------------------

    final_score = (
        (formatting_score * 0.25)
        + (keyword_match_score * 0.35)
        + (semantic_score * 0.25)
        + (action_impact_score_100 * 0.15)
    )

    final_score = max(
        0.0,
        min(100.0, final_score),
    )

    return {
        "ats_score": round(final_score, 2),

        "component_scores": {
            "formatting_score": round(
                formatting_score,
                2,
            ),
            "keyword_match_score": round(
                keyword_match_score,
                2,
            ),
            "semantic_score": round(
                semantic_score,
                2,
            ),
            "action_impact_score": round(
                action_impact_score_100,
                2,
            ),
        },

        "action_impact_details": {
            "action_verb_score": round(
                action_score,
                2,
            ),
            "metrics_score": round(
                metrics_score,
                2,
            ),
        },

        "matched_skills": skill_match_result.get(
            "matched_skills",
            [],
        ),

        "missing_skills": skill_match_result.get(
            "missing_skills",
            [],
        ),

        "jd_skills": skill_match_result.get(
            "jd_skills",
            [],
        ),

        "resume_skills": skill_match_result.get(
            "resume_skills",
            [],
        ),

        "semantic_details": semantic_result,

        "formatting_details": formatting_result,

        "action_verb_details": action_result,

        "metrics_details": metrics_result,
    }