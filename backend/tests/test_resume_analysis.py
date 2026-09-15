"""
Tests for Milestone 3: Deterministic Resume Analysis Engine.

Covers:
- Unit tests for section_detector, contact_detector, skill_detector,
  quality_analyzer, gap_generator, resume_analyzer
- Integration tests for POST /api/v1/resume/{id}/analyze
- Integration tests for GET /api/v1/resume/{id}/analysis
- Upsert behaviour (re-running analysis updates existing record)
- Auth / ownership enforcement
- Requires extraction before analysis (400 guard)
"""

import io
import uuid
import pytest

from httpx import AsyncClient
from sqlalchemy import update

from app.db.models.resume import Resume as ResumeModel
from app.modules.resume.services.section_detector import detect_sections
from app.modules.resume.services.contact_detector import detect_contact
from app.modules.resume.services.skill_detector import detect_skills
from app.modules.resume.services.quality_analyzer import compute_quality_score
from app.modules.resume.services.gap_generator import generate_gaps
from app.modules.resume.services.resume_analyzer import analyze_resume


# ── Shared test fixtures ──────────────────────────────────────────────────────

VALID_PDF_BYTES = (
    b"%PDF-1.4\n"
    b"1 0 obj\n"
    b"<< /Type /Catalog >>\n"
    b"endobj\n"
    b"trailer\n"
    b"<< /Root 1 0 R >>\n"
    b"%%EOF"
)


RICH_RESUME_TEXT = """
John Doe
john.doe@email.com | +91-9876543210
linkedin.com/in/johndoe | github.com/johndoe

Summary
Motivated Computer Science student with strong programming background seeking software engineering roles.

Education
B.Tech Computer Science, XYZ University, 2021–2025. CGPA: 8.5

Skills
Programming Languages: Python, Java, JavaScript
Web Technologies: React, FastAPI, HTML, CSS
Databases: PostgreSQL, MongoDB
Tools: Git, GitHub, Docker
Cloud: AWS

Projects
Student Interview Prep Platform
- Built a full-stack web application using React and FastAPI
- Integrated PostgreSQL database with SQLAlchemy ORM
- Deployed on AWS using Docker containers

Certifications
AWS Certified Cloud Practitioner

Achievements
Winner, National Hackathon 2024
"""


MINIMAL_RESUME_TEXT = "John Doe. Python developer."

EXTRACTION_MOCK_TEXT = RICH_RESUME_TEXT


async def register_and_login(
    client: AsyncClient,
    email: str = "analyst@example.com",
):
    payload = {
        "email": email,
        "password": "password123",
        "full_name": "Test User",
    }

    res = await client.post(
        "/api/v1/auth/register",
        json=payload,
    )

    assert res.status_code in (200, 201)

    return res.cookies


async def upload_resume(
    client: AsyncClient,
    cookies,
    *,
    text: str = "",
):
    """
    Upload a minimal PDF.

    The actual extracted text is injected directly into the database
    in integration tests because the test PDF is intentionally minimal.
    """

    files = {
        "file": (
            "resume.pdf",
            io.BytesIO(VALID_PDF_BYTES),
            "application/pdf",
        )
    }

    res = await client.post(
        "/api/v1/resume/upload",
        files=files,
        cookies=cookies,
    )

    assert res.status_code == 201

    return res.json()["id"]


# ── Unit tests: section_detector ─────────────────────────────────────────────


def test_section_detector_rich_resume():
    sections = detect_sections(RICH_RESUME_TEXT)

    assert sections["summary"] is True
    assert sections["education"] is True
    assert sections["skills"] is True
    assert sections["projects"] is True
    assert sections["certifications"] is True
    assert sections["achievements"] is True


def test_section_detector_missing_sections():
    sections = detect_sections(MINIMAL_RESUME_TEXT)

    assert sections["summary"] is False
    assert sections["education"] is False
    assert sections["projects"] is False


def test_section_detector_case_insensitive():
    text = (
        "EDUCATION\n"
        "B.Tech from XYZ\n\n"
        "PROFESSIONAL SUMMARY\n"
        "Experienced developer."
    )

    sections = detect_sections(text)

    assert sections["education"] is True
    assert sections["summary"] is True


# ── Unit tests: contact_detector ─────────────────────────────────────────────


def test_contact_detector_rich_resume():
    contact = detect_contact(RICH_RESUME_TEXT)

    assert contact["has_email"] is True
    assert contact["has_phone"] is True
    assert contact["has_linkedin"] is True
    assert contact["has_github"] is True


def test_contact_detector_minimal_resume():
    contact = detect_contact(MINIMAL_RESUME_TEXT)

    assert contact["has_email"] is False
    assert contact["has_phone"] is False
    assert contact["has_linkedin"] is False
    assert contact["has_github"] is False


def test_contact_detector_no_actual_values_stored():
    """
    Verify the detector returns only booleans,
    never actual contact strings.
    """

    contact = detect_contact(RICH_RESUME_TEXT)

    for key, value in contact.items():
        assert isinstance(
            value,
            bool,
        ), f"{key} should be bool, got {type(value)}"


# ── Unit tests: skill_detector ───────────────────────────────────────────────


def test_skill_detector_detects_known_skills():
    skills = detect_skills(RICH_RESUME_TEXT)

    assert "Python" in skills["programming_languages"]
    assert "Java" in skills["programming_languages"]
    assert "React" in skills["web_technologies"]
    assert "FastAPI" in skills["web_technologies"]
    assert "PostgreSQL" in skills["databases"]
    assert "Docker" in skills["cloud_devops"]
    assert "AWS" in skills["cloud_devops"]
    assert "Git" in skills["tools_platforms"]


def test_skill_detector_no_false_positives_in_empty_text():
    skills = detect_skills("")

    for category, skill_list in skills.items():
        assert skill_list == [], (
            f"Category '{category}' should be empty for empty text"
        )


def test_skill_detector_case_insensitive():
    text = "proficient in python, java and react framework"

    skills = detect_skills(text)

    assert "Python" in skills["programming_languages"]
    assert "Java" in skills["programming_languages"]
    assert "React" in skills["web_technologies"]


# ── Unit tests: quality_analyzer ─────────────────────────────────────────────


def test_quality_score_rich_resume():
    sections = detect_sections(RICH_RESUME_TEXT)
    contact = detect_contact(RICH_RESUME_TEXT)
    skills = detect_skills(RICH_RESUME_TEXT)

    word_count = len(RICH_RESUME_TEXT.split())

    details = compute_quality_score(
        sections,
        contact,
        word_count,
        len(RICH_RESUME_TEXT),
        skills,
    )

    assert 0.0 <= details["total_score"] <= 100.0
    assert details["total_score"] > 50.0
    assert details["section_score"] >= 0.0
    assert details["contact_score"] >= 0.0
    assert details["content_score"] >= 0.0


def test_quality_score_minimal_resume():
    sections = detect_sections(MINIMAL_RESUME_TEXT)
    contact = detect_contact(MINIMAL_RESUME_TEXT)
    skills = detect_skills(MINIMAL_RESUME_TEXT)

    word_count = len(MINIMAL_RESUME_TEXT.split())

    details = compute_quality_score(
        sections,
        contact,
        word_count,
        len(MINIMAL_RESUME_TEXT),
        skills,
    )

    assert 0.0 <= details["total_score"] <= 100.0
    assert details["total_score"] < 30.0


def test_quality_score_clamped_to_100():
    """
    Quality score must never exceed 100.
    """

    sections = {
        key: True
        for key in [
            "summary",
            "education",
            "skills",
            "projects",
            "contact",
        ]
    }

    contact = {
        "has_email": True,
        "has_phone": True,
        "has_linkedin": True,
        "has_github": True,
    }

    skills = {
        category: ["A", "B", "C", "D", "E"]
        for category in [
            "programming_languages",
            "web_technologies",
            "ai_ml",
            "databases",
            "cloud_devops",
        ]
    }

    details = compute_quality_score(
        sections,
        contact,
        500,
        3000,
        skills,
    )

    assert details["total_score"] <= 100.0


# ── Unit tests: gap_generator ────────────────────────────────────────────────


def test_gap_generator_minimal_resume():
    sections = detect_sections(MINIMAL_RESUME_TEXT)
    contact = detect_contact(MINIMAL_RESUME_TEXT)
    skills = detect_skills(MINIMAL_RESUME_TEXT)

    gaps = generate_gaps(
        sections,
        contact,
        len(MINIMAL_RESUME_TEXT.split()),
        skills,
    )

    assert len(gaps) > 0

    categories = [
        gap["category"]
        for gap in gaps
    ]

    assert "sections" in categories
    assert "contact" in categories


def test_gap_generator_no_vague_experience_gap():
    """
    Gap generator must NOT emit gaps presuming lack of experience.
    """

    sections = detect_sections(MINIMAL_RESUME_TEXT)
    contact = detect_contact(MINIMAL_RESUME_TEXT)
    skills = detect_skills(MINIMAL_RESUME_TEXT)

    gaps = generate_gaps(
        sections,
        contact,
        10,
        skills,
    )

    gap_messages = [
        gap["message"].lower()
        for gap in gaps
    ]

    for message in gap_messages:
        assert "no experience" not in message
        assert "you have no" not in message


def test_gap_generator_rich_resume_fewer_gaps():
    sections_rich = detect_sections(RICH_RESUME_TEXT)
    contact_rich = detect_contact(RICH_RESUME_TEXT)
    skills_rich = detect_skills(RICH_RESUME_TEXT)

    word_count_rich = len(RICH_RESUME_TEXT.split())

    gaps_rich = generate_gaps(
        sections_rich,
        contact_rich,
        word_count_rich,
        skills_rich,
    )

    sections_min = detect_sections(MINIMAL_RESUME_TEXT)
    contact_min = detect_contact(MINIMAL_RESUME_TEXT)
    skills_min = detect_skills(MINIMAL_RESUME_TEXT)

    gaps_min = generate_gaps(
        sections_min,
        contact_min,
        len(MINIMAL_RESUME_TEXT.split()),
        skills_min,
    )

    assert len(gaps_rich) < len(gaps_min)


# ── Unit tests: resume_analyzer orchestrator ──────────────────────────────────


def test_analyze_resume_returns_complete_structure():
    word_count = len(RICH_RESUME_TEXT.split())

    result = analyze_resume(
        RICH_RESUME_TEXT,
        word_count,
        len(RICH_RESUME_TEXT),
    )

    assert "sections" in result
    assert "contact" in result
    assert "skills" in result
    assert "quality_details" in result
    assert "quality_score" in result
    assert "gaps" in result
    assert "analyzed_at" in result

    assert isinstance(
        result["quality_score"],
        float,
    )

    assert 0.0 <= result["quality_score"] <= 100.0


# ── Integration tests ────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_analyze_requires_extraction_first(
    async_client: AsyncClient,
):
    """
    POST /analyze on a resume with status 'pending'
    must return 400.
    """

    cookies = await register_and_login(
        async_client,
        "noextract@example.com",
    )

    resume_id = await upload_resume(
        async_client,
        cookies,
    )

    res = await async_client.post(
        f"/api/v1/resume/{resume_id}/analyze",
        cookies=cookies,
    )

    assert res.status_code == 400
    assert "extract-text" in res.json()["detail"]


@pytest.mark.asyncio
async def test_analyze_resume_unauthenticated(
    async_client: AsyncClient,
):
    """
    POST /analyze without authentication must return 401.
    """

    fake_id = str(uuid.uuid4())

    res = await async_client.post(
        f"/api/v1/resume/{fake_id}/analyze"
    )

    assert res.status_code == 401


@pytest.mark.asyncio
async def test_get_analysis_not_found(
    async_client: AsyncClient,
):
    """
    GET /analysis on a resume with no analysis record
    must return 404.
    """

    cookies = await register_and_login(
        async_client,
        "noanalysis@example.com",
    )

    resume_id = await upload_resume(
        async_client,
        cookies,
    )

    res = await async_client.get(
        f"/api/v1/resume/{resume_id}/analysis",
        cookies=cookies,
    )

    assert res.status_code == 404


@pytest.mark.asyncio
async def test_analyze_and_get_analysis_full_flow(
    async_client: AsyncClient,
    db_session,
):
    """
    Full integration flow:

    1. Register + upload resume
    2. Inject extracted text directly into DB
    3. POST /analyze
    4. GET /analysis
    5. Re-run POST /analyze
    """

    cookies = await register_and_login(
        async_client,
        "fullflow@example.com",
    )

    resume_id = await upload_resume(
        async_client,
        cookies,
    )

    # Inject extracted text directly into the test database.
    await db_session.execute(
        update(ResumeModel)
        .where(
            ResumeModel.id == uuid.UUID(resume_id)
        )
        .values(
            raw_text=RICH_RESUME_TEXT,
            extraction_status="completed",
            word_count=len(RICH_RESUME_TEXT.split()),
            character_count=len(RICH_RESUME_TEXT),
        )
    )

    await db_session.commit()

    # POST /analyze
    res = await async_client.post(
        f"/api/v1/resume/{resume_id}/analyze",
        cookies=cookies,
    )

    assert res.status_code == 200, res.text

    data = res.json()

    assert data["analysis_status"] == "completed"
    assert data["quality_score"] is not None
    assert 0.0 <= data["quality_score"] <= 100.0
    assert data["sections_json"] is not None
    assert data["skills_json"] is not None
    assert data["gaps_json"] is not None
    assert data["quality_details_json"] is not None
    assert data["resume_id"] == resume_id

    # GET /analysis
    get_res = await async_client.get(
        f"/api/v1/resume/{resume_id}/analysis",
        cookies=cookies,
    )

    assert get_res.status_code == 200

    get_data = get_res.json()

    assert get_data["resume_id"] == resume_id
    assert get_data["quality_score"] == data["quality_score"]

    # Re-run POST /analyze.
    # Existing analysis should be updated rather than duplicated.
    re_run = await async_client.post(
        f"/api/v1/resume/{resume_id}/analyze",
        cookies=cookies,
    )

    assert re_run.status_code == 200
    assert re_run.json()["analysis_status"] == "completed"


@pytest.mark.asyncio
async def test_analysis_user_isolation(
    async_client: AsyncClient,
    db_session,
):
    """
    User B cannot see User A's analysis.
    """

    # User A registers and uploads a resume.
    cookies_a = await register_and_login(
        async_client,
        "isolation_a@example.com",
    )

    resume_id = await upload_resume(
        async_client,
        cookies_a,
    )

    # Inject extracted text.
    await db_session.execute(
        update(ResumeModel)
        .where(
            ResumeModel.id == uuid.UUID(resume_id)
        )
        .values(
            raw_text=RICH_RESUME_TEXT,
            extraction_status="completed",
            word_count=len(RICH_RESUME_TEXT.split()),
            character_count=len(RICH_RESUME_TEXT),
        )
    )

    await db_session.commit()

    # User A runs analysis.
    res = await async_client.post(
        f"/api/v1/resume/{resume_id}/analyze",
        cookies=cookies_a,
    )

    assert res.status_code == 200

    # User B registers.
    cookies_b = await register_and_login(
        async_client,
        "isolation_b@example.com",
    )

    # User B tries to access User A's analysis.
    res_b = await async_client.get(
        f"/api/v1/resume/{resume_id}/analysis",
        cookies=cookies_b,
    )

    assert res_b.status_code == 404

def test_section_detector_avoids_body_text_false_positives():
    text = """
    I completed my degree from CMR College of Engineering and Technology.
    During my project, I demonstrated strong leadership and teamwork.
    I conducted research on machine learning techniques.
    """

    sections = detect_sections(text)

    assert sections["education"] is False
    assert sections["extracurricular"] is False
    assert sections["publications"] is False


def test_section_detector_accepts_heading_variations():
    text = """
    ### EDUCATION:
    CMR College of Engineering and Technology

    TECHNICAL SKILLS:
    Java, Python, SQL

    PROJECTS
    AI Interview Preparation Platform

    CERTIFICATIONS:
    Google Cloud Certification
    """

    sections = detect_sections(text)

    assert sections["education"] is True
    assert sections["skills"] is True
    assert sections["projects"] is True
    assert sections["certifications"] is True