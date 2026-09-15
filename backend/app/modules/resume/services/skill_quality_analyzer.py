from typing import Dict, List


def analyze_skill_quality(
    skills: Dict[str, List[str]],
) -> Dict[str, object]:
    """
    Analyze skill breadth and category diversity.

    Skill breadth contributes up to 10 points.
    Category diversity contributes up to 10 points.

    Returns:
        total_skills:
            Total number of unique detected skills.

        active_categories:
            Categories containing at least one skill.

        category_count:
            Number of categories containing skills.

        skill_breadth_score:
            Score out of 10.

        category_diversity_score:
            Score out of 10.

        total_skill_quality_score:
            Combined score out of 20.
    """

    if not skills:
        return {
            "total_skills": 0,
            "active_categories": [],
            "category_count": 0,
            "skill_breadth_score": 0.0,
            "category_diversity_score": 0.0,
            "total_skill_quality_score": 0.0,
        }

    # Collect unique skills across all categories.
    all_skills = set()

    active_categories = []

    for category, skill_list in skills.items():
        if skill_list:
            active_categories.append(category)

            for skill in skill_list:
                all_skills.add(skill.lower())

    total_skills = len(all_skills)
    category_count = len(active_categories)

    # ---------------------------------------------------------
    # Skill Breadth — 10 points
    #
    # 15+ distinct skills receives the maximum score.
    # ---------------------------------------------------------

    skill_breadth_score = min(total_skills / 15, 1.0) * 10

    # ---------------------------------------------------------
    # Category Diversity — 10 points
    #
    # There are 8 categories in the current M3 dictionary.
    # 6+ active categories receives the maximum score.
    # ---------------------------------------------------------

    category_diversity_score = min(category_count / 6, 1.0) * 10

    total_skill_quality_score = (
        skill_breadth_score + category_diversity_score
    )

    return {
        "total_skills": total_skills,
        "active_categories": sorted(active_categories),
        "category_count": category_count,
        "skill_breadth_score": round(skill_breadth_score, 2),
        "category_diversity_score": round(category_diversity_score, 2),
        "total_skill_quality_score": round(total_skill_quality_score, 2),
    }