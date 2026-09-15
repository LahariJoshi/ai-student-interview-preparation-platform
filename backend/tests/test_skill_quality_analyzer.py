from app.modules.resume.services.skill_quality_analyzer import (
    analyze_skill_quality,
)


def test_empty_skills():

    result = analyze_skill_quality({})

    assert result["total_skills"] == 0
    assert result["active_categories"] == []
    assert result["category_count"] == 0
    assert result["skill_breadth_score"] == 0.0
    assert result["category_diversity_score"] == 0.0
    assert result["total_skill_quality_score"] == 0.0


def test_skill_breadth():

    skills = {
        "programming_languages": [
            "Python",
            "Java",
            "C++",
            "JavaScript",
            "TypeScript",
        ],
        "web_technologies": [
            "React",
            "FastAPI",
            "HTML",
            "CSS",
        ],
    }

    result = analyze_skill_quality(skills)

    assert result["total_skills"] == 9
    assert result["skill_breadth_score"] == 6.0


def test_category_diversity():

    skills = {
        "programming_languages": ["Python"],
        "web_technologies": ["React"],
        "ai_ml": ["Machine Learning"],
        "databases": ["PostgreSQL"],
        "cloud_devops": ["AWS"],
        "tools_platforms": ["Git"],
    }

    result = analyze_skill_quality(skills)

    assert result["category_count"] == 6
    assert result["category_diversity_score"] == 10.0


def test_duplicate_skills_are_counted_once():

    skills = {
        "programming_languages": [
            "Python",
            "Java",
        ],
        "ai_ml": [
            "Python",
            "TensorFlow",
        ],
    }

    result = analyze_skill_quality(skills)

    assert result["total_skills"] == 3


def test_strong_skill_profile():

    skills = {
        "programming_languages": [
            "Python",
            "Java",
            "JavaScript",
            "C++",
        ],
        "web_technologies": [
            "React",
            "FastAPI",
            "HTML",
        ],
        "ai_ml": [
            "Machine Learning",
            "TensorFlow",
            "PyTorch",
        ],
        "databases": [
            "PostgreSQL",
            "MongoDB",
        ],
        "cloud_devops": [
            "AWS",
            "Docker",
        ],
        "tools_platforms": [
            "Git",
            "GitHub",
        ],
        "core_cs": [
            "Data Structures",
            "Algorithms",
        ],
    }

    result = analyze_skill_quality(skills)

    assert result["total_skills"] == 18
    assert result["skill_breadth_score"] == 10.0
    assert result["category_count"] == 7
    assert result["category_diversity_score"] == 10.0
    assert result["total_skill_quality_score"] == 20.0