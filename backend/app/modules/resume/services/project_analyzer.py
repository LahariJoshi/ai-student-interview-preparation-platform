import re
from typing import Dict, List


TECHNICAL_TERMS = {
    # Programming languages
    "java",
    "python",
    "c",
    "c++",
    "c#",
    "javascript",
    "typescript",

    # Web technologies
    "html",
    "css",
    "react",
    "angular",
    "vue",
    "next.js",
    "node.js",
    "node",
    "express",

    # Backend / frameworks
    "fastapi",
    "django",
    "flask",
    "spring boot",

    # Databases
    "mysql",
    "postgresql",
    "mongodb",
    "oracle",
    "sqlite",
    "sql",

    # AI / ML
    "machine learning",
    "deep learning",
    "natural language processing",
    "nlp",
    "computer vision",
    "tensorflow",
    "pytorch",
    "scikit-learn",

    # Implementation concepts
    "api",
    "apis",
    "authentication",
    "authorization",
    "backend",
    "database",
    "frontend",
    "full stack",
    "rest",
    "rest api",
    "crud",
    "deployment",
    "testing",
    "algorithm",
    "algorithms",
    "architecture",
    "framework",
    "frameworks",
}


def _count_technical_terms(text: str) -> int:
    """Count technical implementation terms in project content."""

    normalized = text.lower()
    count = 0

    for term in TECHNICAL_TERMS:
        if re.search(rf"\b{re.escape(term)}\b", normalized):
            count += 1

    return count


def _count_action_verbs(text: str) -> int:
    """Count common action verbs used in project descriptions."""

    action_verbs = {
        "built",
        "created",
        "designed",
        "developed",
        "implemented",
        "integrated",
        "optimized",
        "automated",
        "deployed",
        "tested",
        "configured",
        "engineered",
        "developed",
        "analyzed",
        "improved",
    }

    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())

    return sum(1 for word in words if word in action_verbs)


def _count_metrics(text: str) -> int:
    """Count measurable values associated with project content."""

    patterns = [
        r"\b\d+(?:\.\d+)?\s*%",
        r"\b\d+(?:\.\d+)?\s*\+",
        r"\b\d+(?:\.\d+)?\s*(?:users?|projects?|records?|requests?|"
        r"seconds?|minutes?|hours?|days?|months?)\b",
    ]

    count = 0

    for pattern in patterns:
        count += len(re.findall(pattern, text, re.IGNORECASE))

    return count


def analyze_projects(
    project_text: str,
    project_count: int = 0,
) -> Dict[str, object]:
    """
    Analyze the quality of project content.

    Score is out of 15 points.

    Components:
        Section presence          -> 2
        Description quality       -> 3
        Technology mentions       -> 3
        Action verbs              -> 2
        Technical details         -> 3
        Quantifiable impact       -> 2
    """

    if not project_text or not project_text.strip():
        return {
            "project_count": project_count,
            "section_present": False,
            "description_quality": 0.0,
            "technology_score": 0.0,
            "action_verb_score": 0.0,
            "technical_detail_score": 0.0,
            "metrics_score": 0.0,
            "project_quality_score": 0.0,
        }

    text = project_text.strip()
    word_count = len(text.split())

    # 1. Project section presence — 2 points
    section_score = 2.0

    # 2. Description quality — 3 points
    if word_count >= 150:
        description_score = 3.0
    elif word_count >= 80:
        description_score = 2.0
    elif word_count >= 40:
        description_score = 1.0
    else:
        description_score = 0.5

    # 3. Technology mentions — 3 points
    technical_term_count = _count_technical_terms(text)

    if technical_term_count >= 5:
        technology_score = 3.0
    elif technical_term_count >= 3:
        technology_score = 2.0
    elif technical_term_count >= 1:
        technology_score = 1.0
    else:
        technology_score = 0.0

    # 4. Action verbs — 2 points
    action_verb_count = _count_action_verbs(text)

    if action_verb_count >= 4:
        action_verb_score = 2.0
    elif action_verb_count >= 2:
        action_verb_score = 1.5
    elif action_verb_count >= 1:
        action_verb_score = 1.0
    else:
        action_verb_score = 0.0

    # 5. Technical implementation details — 3 points
    technical_detail_count = _count_technical_terms(text)

    if technical_detail_count >= 6:
        technical_detail_score = 3.0
    elif technical_detail_count >= 4:
        technical_detail_score = 2.0
    elif technical_detail_count >= 2:
        technical_detail_score = 1.0
    else:
        technical_detail_score = 0.0

    # 6. Quantifiable impact — 2 points
    metric_count = _count_metrics(text)

    if metric_count >= 2:
        metrics_score = 2.0
    elif metric_count == 1:
        metrics_score = 1.0
    else:
        metrics_score = 0.0

    total_score = round(
        section_score
        + description_score
        + technology_score
        + action_verb_score
        + technical_detail_score
        + metrics_score,
        2,
    )

    return {
        "project_count": project_count,
        "section_present": True,
        "description_quality": description_score,
        "technology_score": technology_score,
        "action_verb_score": action_verb_score,
        "technical_detail_score": technical_detail_score,
        "metrics_score": metrics_score,
        "project_quality_score": total_score,
    }