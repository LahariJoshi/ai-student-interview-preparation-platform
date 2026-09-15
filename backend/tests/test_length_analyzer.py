from app.modules.resume.services.length_analyzer import analyze_resume_length


def test_empty_resume():
    result = analyze_resume_length("")

    assert result["word_count"] == 0
    assert result["character_count"] == 0
    assert result["content_density"] == "very_short"
    assert result["score"] == 0.0


def test_very_short_resume():
    text = " ".join(["resume"] * 100)

    result = analyze_resume_length(text)

    assert result["word_count"] == 100
    assert result["content_density"] == "very_short"
    assert result["score"] == 3.0


def test_short_resume():
    text = " ".join(["resume"] * 200)

    result = analyze_resume_length(text)

    assert result["word_count"] == 200
    assert result["content_density"] == "short"
    assert result["score"] == 6.0


def test_good_resume_length():
    text = " ".join(["resume"] * 400)

    result = analyze_resume_length(text)

    assert result["word_count"] == 400
    assert result["content_density"] == "good"
    assert result["score"] == 8.5


def test_strong_resume_length():
    text = " ".join(["resume"] * 600)

    result = analyze_resume_length(text)

    assert result["word_count"] == 600
    assert result["content_density"] == "strong"
    assert result["score"] == 10.0


def test_long_resume():
    text = " ".join(["resume"] * 900)

    result = analyze_resume_length(text)

    assert result["word_count"] == 900
    assert result["content_density"] == "long"
    assert result["score"] == 8.0