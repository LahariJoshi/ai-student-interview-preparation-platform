from typing import Dict


def analyze_resume_length(text: str) -> Dict[str, object]:
    """
    Analyze resume length and content density.

    Returns:
        word_count:
            Number of words in the extracted resume text.

        character_count:
            Number of non-whitespace characters.

        content_density:
            Human-readable classification of resume length.

        score:
            Resume length/content-density score out of 10.
    """

    if not text or not text.strip():
        return {
            "word_count": 0,
            "character_count": 0,
            "content_density": "very_short",
            "score": 0.0,
        }

    words = text.split()
    word_count = len(words)

    character_count = len("".join(text.split()))

    if word_count < 150:
        content_density = "very_short"
        score = 3.0

    elif word_count < 300:
        content_density = "short"
        score = 6.0

    elif word_count < 500:
        content_density = "good"
        score = 8.5

    elif word_count < 800:
        content_density = "strong"
        score = 10.0

    else:
        content_density = "long"
        score = 8.0

    return {
        "word_count": word_count,
        "character_count": character_count,
        "content_density": content_density,
        "score": score,
    }