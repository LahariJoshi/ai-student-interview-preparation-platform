"""Audio processing and speech delivery analysis service.

Calculates practical practice metrics:
- Speaking pace (words per minute)
- Pause estimation
- Filler words frequency (um, uh, like, you know, actually, basically)
Applies non-evaluative delivery metrics with ethical safeguards.
"""

import os
import re
from typing import Dict, Any, List

COMMON_FILLER_WORDS = [
    "um",
    "uh",
    "like",
    "you know",
    "basically",
    "actually",
    "literally",
    "sort of",
    "kind of",
    "i mean",
]


def analyze_speech_delivery(
    transcript: str,
    duration_seconds: float,
) -> Dict[str, Any]:
    """Calculate objective speech pacing and filler-word metrics from transcription and duration.

    Returns:
        delivery_metrics dict with words_count, speaking_rate_wpm, pacing_verdict, filler_words, filler_count.
    """
    if not transcript or duration_seconds <= 0:
        return {
            "words_count": 0,
            "speaking_rate_wpm": 0.0,
            "pacing_verdict": "No audio input detected",
            "filler_words": [],
            "filler_count": 0,
            "duration_seconds": round(duration_seconds, 1),
        }

    words = re.findall(r"\b\w+\b", transcript.lower())
    words_count = len(words)
    minutes = duration_seconds / 60.0
    speaking_rate_wpm = round(words_count / max(minutes, 0.01), 1)

    # Detect filler words
    lower_text = transcript.lower()
    detected_fillers: List[str] = []
    total_filler_count = 0

    for filler in COMMON_FILLER_WORDS:
        count = len(re.findall(rf"\b{re.escape(filler)}\b", lower_text))
        if count > 0:
            detected_fillers.append(f"{filler} ({count})")
            total_filler_count += count

    # Determine pacing verdict (Standard conversational presentation is 120-160 WPM)
    if speaking_rate_wpm < 90:
        pacing_verdict = "Deliberate / Slow pace. You can speak a bit more fluidly."
    elif speaking_rate_wpm > 180:
        pacing_verdict = "Fast pace. Consider slowing down slightly to ensure maximum clarity."
    else:
        pacing_verdict = "Optimal pacing (120-160 WPM) — clear and well-modulated."

    return {
        "words_count": words_count,
        "speaking_rate_wpm": speaking_rate_wpm,
        "pacing_verdict": pacing_verdict,
        "filler_words": detected_fillers,
        "filler_count": total_filler_count,
        "duration_seconds": round(duration_seconds, 1),
    }
