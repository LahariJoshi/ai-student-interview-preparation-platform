from app.modules.resume.services.project_analyzer import analyze_projects


def test_empty_project_content():
    result = analyze_projects("", 0)

    assert result["project_count"] == 0
    assert result["section_present"] is False
    assert result["project_quality_score"] == 0.0


def test_basic_project():
    text = """
    Developed a student management application using Java and MySQL.
    """

    result = analyze_projects(text, 1)

    assert result["project_count"] == 1
    assert result["section_present"] is True
    assert result["technology_score"] > 0
    assert result["action_verb_score"] > 0
    assert result["project_quality_score"] > 0


def test_strong_project():
    text = """
    Developed a full-stack student management application using React,
    FastAPI and PostgreSQL. Implemented REST APIs, authentication,
    authorization and CRUD operations. Designed the database architecture,
    tested the application and deployed the backend. The system supported
    500+ users and improved processing time by 30%.
    """

    result = analyze_projects(text, 1)

    assert result["project_count"] == 1
    assert result["section_present"] is True
    assert result["technology_score"] == 3.0
    assert result["action_verb_score"] >= 1.5
    assert result["technical_detail_score"] == 3.0
    assert result["metrics_score"] == 2.0
    assert result["project_quality_score"] > 10


def test_project_without_metrics():
    text = """
    Developed a machine learning application using Python and Scikit-learn.
    Implemented data preprocessing and model training. Tested multiple
    classification algorithms and evaluated the model performance.
    """

    result = analyze_projects(text, 1)

    assert result["section_present"] is True
    assert result["metrics_score"] == 0.0
    assert result["project_quality_score"] > 0


def test_multiple_projects():
    text = """
    Developed a web application using React and Node.js.
    Implemented REST APIs and authentication.

    Built a machine learning model using Python and Scikit-learn.
    Tested classification algorithms and evaluated performance.
    """

    result = analyze_projects(text, 2)

    assert result["project_count"] == 2
    assert result["section_present"] is True
    assert result["project_quality_score"] > 0