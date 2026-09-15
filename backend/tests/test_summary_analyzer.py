from app.modules.resume.services.summary_analyzer import (
    analyze_summary,
)


def test_empty_summary():

    result = analyze_summary("")

    assert result["summary_present"] is False
    assert result["word_count"] == 0
    assert result["summary_quality_score"] == 0.0


def test_strong_summary():

    text = """
    Computer Science student skilled in Python, Java and React with
    experience developing full-stack applications and implementing REST
    APIs. Built academic projects using PostgreSQL and machine learning,
    and interested in developing scalable software solutions.
    """

    result = analyze_summary(text)

    assert result["summary_present"] is True
    assert result["word_count"] >= 30
    assert result["skill_mentions"] >= 3
    assert result["action_verb_count"] >= 2
    assert result["meaningful_content"] is True
    assert result["summary_quality_score"] >= 8.0


def test_summary_with_no_technical_skills():

    text = """
    Motivated student looking for opportunities to learn new things
    and contribute to a professional organization.
    """

    result = analyze_summary(text)

    assert result["summary_present"] is True
    assert result["skill_mentions"] == 0
    assert result["summary_quality_score"] < 8.0


def test_short_summary():

    text = "Computer Science student skilled in Python."

    result = analyze_summary(text)

    assert result["summary_present"] is True
    assert result["word_count"] < 20
    assert result["summary_quality_score"] < 8.0


def test_generic_summary():

    text = """
    Hardworking motivated student and quick learner who is a team player
    looking for a job and seeking a job opportunity.
    """

    result = analyze_summary(text)

    assert result["summary_present"] is True
    assert result["meaningful_content"] is False
    assert result["summary_quality_score"] < 6.0