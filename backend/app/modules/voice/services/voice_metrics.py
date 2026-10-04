import re
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

# ==========================================
# Configurable Default Thresholds & Dictionaries
# ==========================================
DEFAULT_FILLER_WORDS = [
    # Non-lexical fillers / hesitations
    "um",
    "uh",
    "er",
    "ah",
    "eh",
    "hmm",
    # Overused conversational filler words
    "like",
    "basically",
    "actually",
    "literally",
    "honestly",
    "seriously",
    "right",
    "okay",
    "so",
    # Multi-word filler phrases
    "you know",
    "i mean",
    "sort of",
    "kind of",
    "you see",
    "at the end of the day",
    "as a matter of fact",
    "to be honest",
]

DEFAULT_WPM_CONFIG = {
    "slow_threshold": 110.0,
    "optimal_min": 120.0,
    "optimal_max": 160.0,
    "fast_threshold": 170.0,
}

DEFAULT_PAUSE_CONFIG = {
    "min_pause_seconds": 0.4,   # Gaps >= 0.4s qualify as deliberate pauses
    "long_pause_seconds": 2.0,  # Gaps >= 2.0s qualify as hesitation / long pause
}


class VoiceMetricsService:
    """
    Voice analysis service computing:
    1. Filler-word frequency and rate
    2. Speaking rate (WPM)
    3. Pause distribution (when reliable audio timing data is available)
    """

    def __init__(
        self,
        filler_words: Optional[List[str]] = None,
        wpm_config: Optional[Dict[str, float]] = None,
        pause_config: Optional[Dict[str, float]] = None,
    ):
        self.filler_words = sorted(
            [w.strip().lower() for w in (filler_words or DEFAULT_FILLER_WORDS) if w.strip()],
            key=lambda x: -len(x),  # Sort longer phrases first
        )
        self.wpm_config = {**DEFAULT_WPM_CONFIG, **(wpm_config or {})}
        self.pause_config = {**DEFAULT_PAUSE_CONFIG, **(pause_config or {})}

    # ==========================================
    # 1. Filler-Word Analysis
    # ==========================================
    def analyze_filler_words(
        self,
        transcript: str,
        custom_fillers: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Analyzes the transcript for occurrences of filler words and phrases.
        Calculates total count, breakdown by filler, and filler rate per 100 words.

        Return format:
        {
          "filler_word_count": int,
          "filler_words": Dict[str, int],
          "filler_rate": float
        }
        """
        if not transcript or not transcript.strip():
            return {
                "filler_word_count": 0,
                "filler_words": {},
                "filler_rate": 0.0,
            }

        # Tokenize total words
        raw_words = transcript.strip().split()
        total_word_count = len(raw_words)

        fillers_to_check = (
            sorted(
                [w.strip().lower() for w in custom_fillers if w.strip()],
                key=lambda x: -len(x),
            )
            if custom_fillers
            else self.filler_words
        )

        text_lower = f" {transcript.lower()} "
        # Normalize punctuation to spaces for accurate boundary matching while preserving word boundaries
        cleaned_text = re.sub(r"[^\w\s]", " ", text_lower)

        filler_counts: Dict[str, int] = {}
        total_filler_count = 0

        # Replace detected multi-word fillers with placeholder tokens to avoid double-counting overlapping single words
        working_text = cleaned_text
        for filler in fillers_to_check:
            pattern = rf"\b{re.escape(filler)}\b"
            matches = re.findall(pattern, working_text)
            count = len(matches)
            if count > 0:
                filler_counts[filler] = count
                total_filler_count += count
                # Replace with placeholder token of distinct words to keep word spacing intact
                working_text = re.sub(pattern, " __filler_matched__ ", working_text)

        # Filler rate = filler words per 100 spoken words
        filler_rate = round((total_filler_count / total_word_count) * 100, 2) if total_word_count > 0 else 0.0

        return {
            "filler_word_count": total_filler_count,
            "filler_words": filler_counts,
            "filler_rate": filler_rate,
        }

    # ==========================================
    # 2. Speaking-Rate Analysis
    # ==========================================
    def analyze_speaking_rate(
        self,
        transcript: str,
        duration_seconds: float,
        custom_wpm_config: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        """
        Calculates candidate speaking pace in words per minute (WPM).
        speech_rate = spoken_words / speaking_duration_minutes

        Return format:
        {
          "word_count": int,
          "duration_seconds": float,
          "speech_rate_wpm": float
        }
        """
        if not transcript or not transcript.strip():
            return {
                "word_count": 0,
                "duration_seconds": max(0.0, round(float(duration_seconds), 2)),
                "speech_rate_wpm": 0.0,
            }

        word_count = len(transcript.strip().split())
        clean_duration = max(0.0, float(duration_seconds))

        if clean_duration <= 0.0:
            speech_rate_wpm = 0.0
        else:
            speaking_duration_minutes = clean_duration / 60.0
            speech_rate_wpm = round(word_count / speaking_duration_minutes, 1)

        return {
            "word_count": word_count,
            "duration_seconds": round(clean_duration, 2),
            "speech_rate_wpm": speech_rate_wpm,
        }

    def evaluate_pace_category(self, wpm: float) -> str:
        """Categorizes speaking pace against configured thresholds."""
        if wpm < self.wpm_config["slow_threshold"]:
            return "slow"
        elif wpm > self.wpm_config["fast_threshold"]:
            return "fast"
        return "optimal"

    # ==========================================
    # 3. Pause Analysis
    # ==========================================
    def analyze_pauses(
        self,
        timing_data: Optional[List[Dict[str, float]]] = None,
    ) -> Dict[str, Any]:
        """
        Analyzes silence / pause intervals when reliable timing data is available.

        If precise pause information is unavailable, does not invent precision;
        clearly marks the metric as unavailable / estimated.

        Return format:
        {
          "pause_count": int,
          "total_pause_seconds": float,
          "average_pause_seconds": float,
          "longest_pause_seconds": float,
          "data_availability": "precise" | "unavailable",
          "is_estimated": bool
        }
        """
        min_pause = self.pause_config.get("min_pause_seconds", 0.4)

        # When reliable timing data is not provided, do NOT invent numbers
        if not timing_data or len(timing_data) < 2:
            return {
                "pause_count": 0,
                "total_pause_seconds": 0.0,
                "average_pause_seconds": 0.0,
                "longest_pause_seconds": 0.0,
                "data_availability": "unavailable",
                "is_estimated": True,
            }

        # Check if input is a list of pause gaps directly: [{"duration": 1.2}, ...]
        if "duration" in timing_data[0]:
            pause_durations = [
                float(item["duration"])
                for item in timing_data
                if float(item.get("duration", 0.0)) >= min_pause
            ]
        # Or word timestamps: [{"word": "...", "start": 0.0, "end": 0.5}, ...]
        elif "start" in timing_data[0] and "end" in timing_data[0]:
            sorted_words = sorted(timing_data, key=lambda x: x.get("start", 0.0))
            pause_durations = []
            for i in range(len(sorted_words) - 1):
                curr_end = sorted_words[i].get("end", 0.0)
                next_start = sorted_words[i + 1].get("start", 0.0)
                gap = next_start - curr_end
                if gap >= min_pause:
                    pause_durations.append(round(gap, 2))
        else:
            return {
                "pause_count": 0,
                "total_pause_seconds": 0.0,
                "average_pause_seconds": 0.0,
                "longest_pause_seconds": 0.0,
                "data_availability": "unavailable",
                "is_estimated": True,
            }

        pause_count = len(pause_durations)
        total_pause_seconds = round(sum(pause_durations), 2)
        average_pause_seconds = (
            round(total_pause_seconds / pause_count, 2) if pause_count > 0 else 0.0
        )
        longest_pause_seconds = (
            round(max(pause_durations), 2) if pause_count > 0 else 0.0
        )

        return {
            "pause_count": pause_count,
            "total_pause_seconds": total_pause_seconds,
            "average_pause_seconds": average_pause_seconds,
            "longest_pause_seconds": longest_pause_seconds,
            "data_availability": "precise",
            "is_estimated": False,
        }

    # ==========================================
    # Unified Analysis Pipeline
    # ==========================================
    def analyze_metrics(
        self,
        transcript: str,
        duration_seconds: float,
        timing_data: Optional[List[Dict[str, float]]] = None,
    ) -> Dict[str, Any]:
        """
        Unified method running filler, speaking rate, and pause analysis.
        """
        filler_res = self.analyze_filler_words(transcript)
        speaking_res = self.analyze_speaking_rate(transcript, duration_seconds)
        pause_res = self.analyze_pauses(timing_data)

        return {
            "filler_analysis": filler_res,
            "speaking_rate": speaking_res,
            "pause_analysis": pause_res,
        }


voice_metrics_service = VoiceMetricsService()
