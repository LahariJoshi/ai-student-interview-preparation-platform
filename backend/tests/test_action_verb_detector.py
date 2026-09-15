from app.modules.resume.services.action_verb_detector import detect_action_verbs


def test_detect_action_verbs():
    text = """
    Developed a web application using React.
    Implemented authentication using JWT.
    Designed the database schema.
    Tested the REST APIs.
    """

    result = detect_action_verbs(text)

    assert result["total_action_verbs"] == 4
    assert result["unique_action_verbs"] == 4

    assert "developed" in result["detected_verbs"]
    assert "implemented" in result["detected_verbs"]
    assert "designed" in result["detected_verbs"]
    assert "tested" in result["detected_verbs"]

    assert result["score"] > 0


def test_repeated_action_verbs():
    text = """
    Developed application.
    Developed API.
    Developed frontend.
    Developed backend.
    """

    result = detect_action_verbs(text)

    assert result["total_action_verbs"] == 4
    assert result["unique_action_verbs"] == 1
    assert result["score"] > 0


def test_empty_resume():
    result = detect_action_verbs("")

    assert result["total_action_verbs"] == 0
    assert result["unique_action_verbs"] == 0
    assert result["detected_verbs"] == []
    assert result["score"] == 0.0