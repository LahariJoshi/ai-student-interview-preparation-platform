import re
from typing import Dict, List


# Patterns that represent measurable evidence in a resume.
METRIC_PATTERNS = [
    # Percentages: 30%, 95.5%
    re.compile(r"\b\d+(?:\.\d+)?\s*%"),

    # Numbers with +: 50+, 1000+
    re.compile(r"\b\d+(?:\.\d+)?\s*\+"),

    # Numbers followed by common units.
    re.compile(
        r"\b\d+(?:\.\d+)?\s*"
        r"(?:users?|clients?|customers?|projects?|"
        r"applications?|records?|employees?|"
        r"requests?|transactions?|features?|"
        r"modules?|teams?|members?|"
        r"hours?|days?|weeks?|months?|years?|"
        r"seconds?|minutes?|ms|"
        r"GB|MB|TB)\b",
        re.IGNORECASE,
    ),

    # Currency amounts: ₹50,000, $500, €100, £250
    re.compile(
        r"(?:₹|\$|€|£)\s*\d+(?:,\d{3})*(?:\.\d+)?"
    ),

    # Decimal measurements commonly used for performance.
    # Examples: 8.7 CGPA, 95.5 accuracy
    re.compile(
        r"\b\d+(?:\.\d+)?\s*"
        r"(?:CGPA|GPA|accuracy|score|precision|recall|F1)\b",
        re.IGNORECASE,
    ),
]


# Academic / resume numbers that should not automatically
# be treated as impact metrics.
EXCLUDED_CONTEXT_PATTERNS = [
    re.compile(r"\b(?:19|20)\d{2}\b"),  # Years such as 2024, 2025
]


def _is_excluded_match(text: str, start: int, end: int) -> bool:
    """
    Determine whether a numeric match is likely to be a
    non-impact value such as a year.
    """

    matched_text = text[start:end].strip()

    for pattern in EXCLUDED_CONTEXT_PATTERNS:
        if pattern.fullmatch(matched_text):
            return True

    return False


def detect_metrics(text: str) -> Dict[str, object]:
    """
    Detect measurable evidence in resume text.

    Returns:
        metric_count:
            Number of detected measurable values.

        metrics:
            Unique detected metric strings.

        score:
            Quantifiable-impact score out of 10.
    """

    if not text or not text.strip():
        return {
            "metric_count": 0,
            "metrics": [],
            "score": 0.0,
        }

    detected_metrics: List[str] = []

    for pattern in METRIC_PATTERNS:
        for match in pattern.finditer(text):
            if not _is_excluded_match(text, match.start(), match.end()):
                detected_metrics.append(match.group(0).strip())

    # Remove duplicates while preserving order.
    unique_metrics = list(dict.fromkeys(detected_metrics))

    metric_count = len(unique_metrics)

    # Score out of 10.
    #
    # 5 or more meaningful metrics receives the maximum score.
    score = min(metric_count / 5, 1.0) * 10

    return {
        "metric_count": metric_count,
        "metrics": unique_metrics,
        "score": round(score, 2),
    }