import pytest
from httpx import AsyncClient

from app.modules.voice.services.voice_metrics import (
    VoiceMetricsService,
    voice_metrics_service,
    DEFAULT_FILLER_WORDS,
)


# ====================================================
# Unit Tests: Filler-Word Analysis
# ====================================================

def test_filler_analysis_single_and_multi_word():
    service = VoiceMetricsService()
    text = "Um, so basically, I was, like, writing tests, you know, at the end of the day."
    res = service.analyze_filler_words(text)

    assert "filler_word_count" in res
    assert "filler_words" in res
    assert "filler_rate" in res

    # Check detected fillers
    fillers = res["filler_words"]
    assert "um" in fillers
    assert "basically" in fillers
    assert "like" in fillers
    assert "you know" in fillers
    assert "at the end of the day" in fillers

    assert res["filler_word_count"] >= 5
    assert res["filler_rate"] > 0.0


def test_filler_analysis_clean_text_no_fillers():
    service = VoiceMetricsService()
    clean_text = "I architected the database schema using relational constraints and foreign keys."
    res = service.analyze_filler_words(clean_text)

    assert res["filler_word_count"] == 0
    assert res["filler_words"] == {}
    assert res["filler_rate"] == 0.0


def test_filler_analysis_empty_text():
    service = VoiceMetricsService()
    res = service.analyze_filler_words("")
    assert res["filler_word_count"] == 0
    assert res["filler_words"] == {}
    assert res["filler_rate"] == 0.0


def test_filler_analysis_custom_configurable_fillers():
    # Configure custom filler words
    custom_service = VoiceMetricsService(filler_words=["foo", "bar buzz", "whatever"])
    text = "The system foo was totally whatever and had bar buzz in it."

    res = custom_service.analyze_filler_words(text)
    assert "foo" in res["filler_words"]
    assert "whatever" in res["filler_words"]
    assert "bar buzz" in res["filler_words"]
    assert "um" not in res["filler_words"]  # Default "um" not in custom list


# ====================================================
# Unit Tests: Speaking-Rate Analysis
# ====================================================

def test_speaking_rate_exact_math():
    service = VoiceMetricsService()
    # Exactly 150 words in 60 seconds -> 150.0 WPM
    words = "word " * 150
    res = service.analyze_speaking_rate(words, duration_seconds=60.0)

    assert res["word_count"] == 150
    assert res["duration_seconds"] == 60.0
    assert res["speech_rate_wpm"] == 150.0


def test_speaking_rate_half_minute():
    service = VoiceMetricsService()
    # 70 words in 30 seconds -> (70 / 0.5) = 140.0 WPM
    words = "test " * 70
    res = service.analyze_speaking_rate(words, duration_seconds=30.0)

    assert res["word_count"] == 70
    assert res["duration_seconds"] == 30.0
    assert res["speech_rate_wpm"] == 140.0


def test_speaking_rate_zero_duration_guard():
    service = VoiceMetricsService()
    words = "Some candidate response words."
    res = service.analyze_speaking_rate(words, duration_seconds=0.0)

    assert res["speech_rate_wpm"] == 0.0
    assert res["duration_seconds"] == 0.0


def test_speaking_rate_configurable_thresholds():
    custom_wpm = {
        "slow_threshold": 100.0,
        "optimal_min": 110.0,
        "optimal_max": 150.0,
        "fast_threshold": 160.0,
    }
    service = VoiceMetricsService(wpm_config=custom_wpm)

    assert service.evaluate_pace_category(80.0) == "slow"
    assert service.evaluate_pace_category(130.0) == "optimal"
    assert service.evaluate_pace_category(180.0) == "fast"


# ====================================================
# Unit Tests: Pause Analysis
# ====================================================

def test_pause_analysis_with_precise_timing_data():
    service = VoiceMetricsService()

    # Timing data with 3 pauses:
    # word 1: 0.0 -> 0.5 (pause 0.5s until 1.0)
    # word 2: 1.0 -> 1.5 (pause 1.0s until 2.5)
    # word 3: 2.5 -> 3.0 (pause 0.2s until 3.2 - under 0.4s threshold, not counted)
    # word 4: 3.2 -> 3.6 (pause 0.8s until 4.4)
    # word 5: 4.4 -> 5.0
    timing_data = [
        {"word": "First", "start": 0.0, "end": 0.5},
        {"word": "second", "start": 1.0, "end": 1.5},
        {"word": "third", "start": 2.5, "end": 3.0},
        {"word": "fourth", "start": 3.2, "end": 3.6},
        {"word": "fifth", "start": 4.4, "end": 5.0},
    ]

    res = service.analyze_pauses(timing_data)

    assert res["data_availability"] == "precise"
    assert res["is_estimated"] is False
    assert res["pause_count"] == 3  # 0.5s, 1.0s, 0.8s
    assert res["total_pause_seconds"] == 2.3
    assert res["longest_pause_seconds"] == 1.0
    assert res["average_pause_seconds"] == round(2.3 / 3, 2)


def test_pause_analysis_when_timing_data_unavailable():
    service = VoiceMetricsService()

    # When no timing data is available, do NOT invent precision
    res = service.analyze_pauses(timing_data=None)

    assert res["data_availability"] == "unavailable"
    assert res["is_estimated"] is True
    assert res["pause_count"] == 0
    assert res["total_pause_seconds"] == 0.0
    assert res["average_pause_seconds"] == 0.0
    assert res["longest_pause_seconds"] == 0.0


def test_unified_analyze_metrics():
    service = VoiceMetricsService()
    transcript = "Um, I basically designed our database with indexing, you know."
    res = service.analyze_metrics(transcript, duration_seconds=12.0)

    assert "filler_analysis" in res
    assert "speaking_rate" in res
    assert "pause_analysis" in res

    assert res["filler_analysis"]["filler_word_count"] > 0
    assert res["speaking_rate"]["word_count"] > 0
    assert res["pause_analysis"]["data_availability"] == "unavailable"


# ====================================================
# API Integration Tests
# ====================================================

async def register_and_get_cookies(client: AsyncClient, email: str, name: str = "Test User"):
    reg_payload = {
        "email": email,
        "password": "Password123!",
        "full_name": name,
    }
    res = await client.post("/api/v1/auth/register", json=reg_payload)
    assert res.status_code == 201
    return res.cookies


@pytest.mark.asyncio
async def test_calculate_metrics_unauthorized(async_client: AsyncClient):
    payload = {
        "transcribed_text": "Um, well, this is a response.",
        "duration_seconds": 15.0,
    }
    res = await async_client.post("/api/v1/voice/metrics", json=payload)
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_calculate_metrics_success(async_client: AsyncClient):

    cookies = await register_and_get_cookies(async_client, "voice_metrics_user@example.com")

    payload = {
        "transcribed_text": "Um, like, basically I built an event-driven architecture, you know.",
        "duration_seconds": 20.0,
    }
    res = await async_client.post("/api/v1/voice/metrics", json=payload, cookies=cookies)
    assert res.status_code == 200

    data = res.json()
    assert "filler_analysis" in data
    assert "speaking_rate" in data
    assert "pause_analysis" in data

    assert data["filler_analysis"]["filler_word_count"] >= 3
    assert data["speaking_rate"]["duration_seconds"] == 20.0
    assert data["speaking_rate"]["speech_rate_wpm"] > 0
    assert data["pause_analysis"]["data_availability"] == "unavailable"
