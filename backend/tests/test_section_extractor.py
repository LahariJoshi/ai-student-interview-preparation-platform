from app.modules.resume.services.section_extractor import extract_sections


def test_extract_basic_sections():
    text = """
    Summary
    Computer Science student interested in AI and software development.

    Education
    B.Tech in Computer Science.

    Projects
    AI Interview Preparation Platform using Python and React.
    """

    sections = extract_sections(text)

    assert "summary" in sections
    assert "education" in sections
    assert "projects" in sections

    assert "Computer Science student" in sections["summary"]
    assert "B.Tech" in sections["education"]
    assert "AI Interview Preparation Platform" in sections["projects"]


def test_extract_heading_variations():
    text = """
    ### PROFESSIONAL SUMMARY:
    Motivated Computer Science student.

    TECHNICAL SKILLS:
    Python, Java, SQL

    ACADEMIC PROJECTS:
    Student Management System
    """

    sections = extract_sections(text)

    assert "summary" in sections
    assert "skills" in sections
    assert "projects" in sections


def test_section_content_does_not_include_next_heading():
    text = """
    Summary
    Motivated student with Python skills.

    Education
    B.Tech Computer Science.

    Projects
    Resume Analyzer.
    """

    sections = extract_sections(text)

    assert "Education" not in sections["summary"]
    assert "Projects" not in sections["education"]


def test_empty_text():
    sections = extract_sections("")

    assert sections == {}


def test_unknown_heading_is_not_used_as_boundary():
    text = """
    Summary
    Motivated Computer Science student.

    My Background
    This is some additional information.

    Education
    B.Tech Computer Science.
    """

    sections = extract_sections(text)

    assert "summary" in sections
    assert "education" in sections

    assert "My Background" in sections["summary"]