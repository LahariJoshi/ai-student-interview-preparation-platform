from app.modules.resume.services.metrics_detector import detect_metrics


def test_detect_percentages_and_counts():
    text = """
    Developed an application used by 500+ students.
    Improved performance by 30%.
    Achieved 95% accuracy.
    """

    result = detect_metrics(text)

    assert result["metric_count"] == 3
    assert "500+" in result["metrics"]
    assert "30%" in result["metrics"]
    assert "95%" in result["metrics"]
    assert result["score"] > 0


def test_detect_units_and_currency():
    text = """
    Reduced processing time by 2 seconds.
    Managed 1000 users.
    Reduced infrastructure cost by ₹50,000.
    """

    result = detect_metrics(text)

    assert result["metric_count"] == 3
    assert result["score"] > 0


def test_ignore_years():
    text = """
    B.Tech Computer Science
    2023 - 2027
    Developed projects during 2025.
    """

    result = detect_metrics(text)

    assert result["metric_count"] == 0
    assert result["metrics"] == []
    assert result["score"] == 0.0


def test_empty_resume():
    result = detect_metrics("")

    assert result["metric_count"] == 0
    assert result["metrics"] == []
    assert result["score"] == 0.0


def test_multiple_metrics():
    text = """
    Developed a platform used by 1000+ users.
    Improved response time by 40%.
    Reduced processing time to 2 seconds.
    Achieved 95% accuracy.
    Managed 5 projects.
    """

    result = detect_metrics(text)

    assert result["metric_count"] >= 5
    assert result["score"] == 10.0