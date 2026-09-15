import re
from typing import Dict, List


ACTION_VERBS = {
    "achieved",
    "analyzed",
    "architected",
    "automated",
    "built",
    "collaborated",
    "configured",
    "created",
    "debugged",
    "deployed",
    "designed",
    "developed",
    "engineered",
    "enhanced",
    "evaluated",
    "implemented",
    "improved",
    "integrated",
    "led",
    "managed",
    "optimized",
    "programmed",
    "refactored",
    "researched",
    "resolved",
    "tested",
    "trained",
    "transformed",
    "validated",
}


def _normalise_text(text: str) -> str:
    """Convert text to lowercase for reliable matching."""
    return text.lower()


def detect_action_verbs(text: str) -> Dict[str, object]:
    """
    Detect action verbs in resume text.

    Returns:
        total_action_verbs:
            Total number of detected action-verb occurrences.

        unique_action_verbs:
            Number of distinct action verbs found.

        detected_verbs:
            Sorted list of detected unique verbs.

        action_verb_ratio:
            Number of action-verb occurrences relative to
            the total number of words.

        score:
            Action-verb quality score out of 10.
    """

    if not text or not text.strip():
        return {
            "total_action_verbs": 0,
            "unique_action_verbs": 0,
            "detected_verbs": [],
            "action_verb_ratio": 0.0,
            "score": 0.0,
        }

    normalised_text = _normalise_text(text)

    words = re.findall(r"\b[a-zA-Z]+\b", normalised_text)
    total_words = len(words)

    detected_verbs: List[str] = []

    for verb in ACTION_VERBS:
        pattern = rf"\b{re.escape(verb)}\b"
        matches = re.findall(pattern, normalised_text)

        if matches:
            detected_verbs.extend(matches)

    total_action_verbs = len(detected_verbs)
    unique_action_verbs = len(set(detected_verbs))

    if total_words > 0:
        action_verb_ratio = total_action_verbs / total_words
    else:
        action_verb_ratio = 0.0

    # Score out of 10.
    #
    # The score considers both:
    # 1. Number of action verbs
    # 2. Diversity of action verbs
    #
    # This prevents a resume from receiving a high score
    # merely by repeating the same verb many times.

    occurrence_score = min(total_action_verbs / 15, 1.0) * 6
    diversity_score = min(unique_action_verbs / 8, 1.0) * 4

    score = round(occurrence_score + diversity_score, 2)

    return {
        "total_action_verbs": total_action_verbs,
        "unique_action_verbs": unique_action_verbs,
        "detected_verbs": sorted(set(detected_verbs)),
        "action_verb_ratio": round(action_verb_ratio, 4),
        "score": score,
    }