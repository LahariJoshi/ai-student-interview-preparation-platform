import re
from typing import Dict

from app.modules.resume.services.skill_detector import detect_skills


SUMMARY_ACTION_VERBS = {
    "develop",
    "developed",
    "developing",
    "build",
    "built",
    "building",
    "design",
    "designed",
    "designing",
    "implement",
    "implemented",
    "implementing",
    "create",
    "created",
    "creating",
    "engineer",
    "engineered",
    "engineering",
    "analyze",
    "analyzed",
    "analyzing",
    "optimize",
    "optimized",
    "optimizing",
    "integrate",
    "integrated",
    "integrating",
    "deploy",
    "deployed",
    "deploying",
    "work",
    "worked",
    "working",
    "specialize",
    "specialized",
    "specializing",
    "focus",
    "focused",
    "focusing",
    "experience",
    "experienced",
    "experiencing",
}


def _count_action_verbs(text: str) -> int:
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())
    return sum(1 for word in words if word in SUMMARY_ACTION_VERBS)


def analyze_summary(summary_text: str) -> Dict[str, object]:
    """
    Analyze the quality of a resume summary.

    Maximum score: 10 points.

    Components:
        Summary presence       -> 2
        Appropriate length     -> 2
        Technical skills       -> 2
        Action-oriented text   -> 2
        Meaningful content     -> 2
    """

    if not summary_text or not summary_text.strip():
        return {
            "summary_present": False,
            "word_count": 0,
            "skill_mentions": 0,
            "action_verb_count": 0,
            "meaningful_content": False,
            "summary_quality_score": 0.0,
        }

    text = summary_text.strip()
    word_count = len(text.split())

    # ---------------------------------------------------------
    # 1. Summary presence — 2 points
    # ---------------------------------------------------------

    presence_score = 2.0

    # ---------------------------------------------------------
    # 2. Appropriate length — 2 points
    #
    # 30–80 words is considered a strong student summary.
    # ---------------------------------------------------------

    if 30 <= word_count <= 80:
        length_score = 2.0
    elif 20 <= word_count < 30 or 80 < word_count <= 120:
        length_score = 1.0
    else:
        length_score = 0.0

    # ---------------------------------------------------------
    # 3. Technical skill mentions — 2 points
    # ---------------------------------------------------------

    detected_skills = detect_skills(text)

    skill_mentions = sum(
        len(skill_list)
        for skill_list in detected_skills.values()
    )

    if skill_mentions >= 3:
        skill_score = 2.0
    elif skill_mentions >= 1:
        skill_score = 1.0
    else:
        skill_score = 0.0

    # ---------------------------------------------------------
    # 4. Action-oriented language — 2 points
    # ---------------------------------------------------------

    action_verb_count = _count_action_verbs(text)

    if action_verb_count >= 2:
        action_score = 2.0
    elif action_verb_count == 1:
        action_score = 1.0
    else:
        action_score = 0.0

    # ---------------------------------------------------------
    # 5. Meaningful content — 2 points
    #
    # A meaningful summary should communicate more than
    # generic statements such as "hardworking student".
    # ---------------------------------------------------------

    generic_phrases = {
        "hardworking",
        "hard working",
        "motivated",
        "quick learner",
        "team player",
        "seeking a job",
        "looking for a job",
    }

    normalized = text.lower()

    generic_count = sum(
        1
        for phrase in generic_phrases
        if phrase in normalized
    )

    meaningful_content = (
        word_count >= 20
        and (
            skill_mentions >= 1
            or action_verb_count >= 1
        )
    )

    if meaningful_content and generic_count < 3:
        meaningful_score = 2.0
    elif meaningful_content:
        meaningful_score = 1.0
    else:
        meaningful_score = 0.0

    total_score = round(
        presence_score
        + length_score
        + skill_score
        + action_score
        + meaningful_score,
        2,
    )

    return {
        "summary_present": True,
        "word_count": word_count,
        "skill_mentions": skill_mentions,
        "action_verb_count": action_verb_count,
        "meaningful_content": meaningful_content,
        "summary_quality_score": total_score,
    }