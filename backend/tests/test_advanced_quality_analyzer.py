from app.modules.resume.services.quality_analyzer import (
    compute_advanced_quality_score,
)


def test_advanced_quality_score():
    sections = {
        "education": True,
        "skills": True,
        "projects": True,
        "summary": True,
        "certifications": True,
    }

    contact = {
        "email": True,
        "phone": True,
        "linkedin": True,
        "github": True,
    }

    skills = {
        "programming_languages": ["Python", "Java"],
        "web_technologies": ["React", "FastAPI"],
        "databases": ["PostgreSQL"],
    }

    length_analysis = {
        "score": 8.5,
    }

    action_analysis = {
        "score": 8.0,
    }

    metrics_analysis = {
        "score": 6.0,
    }

    project_analysis = {
        "project_quality_score": 12.0,
    }

    skill_quality_analysis = {
        "skill_breadth_score": 3.33,
        "category_diversity_score": 5.0,
    }

    summary_analysis = {
        "summary_quality_score": 8.0,
    }

    result = compute_advanced_quality_score(
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

    assert result["total_score"] > 0
    assert result["total_score"] <= 100

    assert result["length_score"] == 8.5
    assert result["action_verb_score"] == 8.0
    assert result["metrics_score"] == 6.0
    assert result["project_quality_score"] == 12.0
    assert result["summary_quality_score"] == 8.0


def test_advanced_score_empty_resume():
    sections = {}
    contact = {}
    skills = {}

    empty = {"score": 0.0}

    skill_quality = {
        "skill_breadth_score": 0.0,
        "category_diversity_score": 0.0,
    }

    summary = {
        "summary_quality_score": 0.0,
    }

    result = compute_advanced_quality_score(
        sections=sections,
        contact=contact,
        skills=skills,
        length_analysis=empty,
        action_analysis=empty,
        metrics_analysis=empty,
        project_analysis=empty,
        skill_quality_analysis=skill_quality,
        summary_analysis=summary,
    )

    assert result["total_score"] == 0.0