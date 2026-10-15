import pytest
import uuid
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user import User
from app.core.security import hash_password, create_access_token
from app.core.config import settings
from app.modules.interview.services.voice_service import analyze_speech_delivery
from app.modules.interview.services.question_service import generate_interview_questions
from app.modules.interview.services.provider import OfflineDatasetLLMProvider


@pytest.mark.asyncio
async def test_speech_delivery_metrics():
    # 1. Normal delivery
    transcript = "In this project we used React on the frontend and FastAPI for our REST endpoints. We also implemented database connection pooling."
    metrics = analyze_speech_delivery(transcript, duration_seconds=60.0)
    assert metrics["words_count"] > 15
    assert metrics["speaking_rate_wpm"] > 0
    assert "Optimal" in metrics["pacing_verdict"] or "Deliberate" in metrics["pacing_verdict"]

    # 2. Filler words detection
    filler_transcript = "Um basically we like decided to actually use Python uh you know because of like fast development."
    metrics2 = analyze_speech_delivery(filler_transcript, duration_seconds=30.0)
    assert metrics2["filler_count"] >= 3
    assert len(metrics2["filler_words"]) >= 2


@pytest.mark.asyncio
async def test_offline_question_generation():
    questions = await generate_interview_questions(
        role="Software Developer",
        interview_type="mixed",
        experience_level="Intermediate",
        skills=["Python", "PostgreSQL"],
        resume_projects=["E-Commerce Platform"],
        total_questions=4,
    )
    assert len(questions) == 4
    # Check that personalized project or skill questions are integrated
    has_project_q = any("E-Commerce Platform" in q["question_text"] for q in questions)
    assert has_project_q is True


@pytest.mark.asyncio
async def test_offline_answer_evaluation():
    provider = OfflineDatasetLLMProvider()
    question = "Can you explain the difference between an Array and a Linked List?"
    key_points = [
        "Contiguous vs non-contiguous memory allocation",
        "O(1) random access for arrays vs O(n) traversal for linked lists",
    ]
    student_answer = "An array uses contiguous memory allowing O(1) random access with an index. In contrast, a linked list uses non-contiguous nodes linked by pointers, which requires O(n) sequential traversal to find an element."

    result = await provider.evaluate_answer(
        question=question,
        category="technical",
        expected_key_points=key_points,
        reference_answer=None,
        student_answer=student_answer,
    )
    assert result["score"] >= 70.0
    assert result["relevance_score"] >= 60.0
    assert "detailed_feedback" in result
    assert isinstance(result["improvement_tips"], list)


@pytest.mark.asyncio
async def test_interview_full_api_lifecycle(async_client: AsyncClient, db_session: AsyncSession):
    # 1. Create student user
    student = User(
        email="interview_student@example.com",
        password_hash=hash_password("StudentPass123!"),
        full_name="Interview Candidate",
        role="student",
    )
    db_session.add(student)
    await db_session.commit()
    await db_session.refresh(student)

    token = create_access_token(str(student.id))
    cookies = {settings.COOKIE_NAME: token}

    # 2. Create interview session
    create_payload = {
        "interview_type": "technical",
        "target_role": "Python Developer",
        "experience_level": "Beginner",
        "duration_minutes": 15,
        "custom_skills": ["FastAPI", "Docker"],
    }
    res = await async_client.post("/api/v1/interviews/sessions", json=create_payload, cookies=cookies)
    assert res.status_code == 201, res.text
    session_data = res.json()
    session_id = session_data["id"]
    assert session_data["status"] == "in_progress"
    assert len(session_data["questions"]) > 0

    first_question = session_data["questions"][0]

    # 3. Get current question
    q_res = await async_client.get(f"/api/v1/interviews/sessions/{session_id}/current-question", cookies=cookies)
    assert q_res.status_code == 200
    assert q_res.json()["id"] == first_question["id"]

    # 4. Submit answer
    answer_payload = {
        "question_id": first_question["id"],
        "answer_text": "Mutable objects can be modified in place such as lists and dictionaries, whereas immutable objects like integers and strings cannot. Python passes arguments by object reference.",
        "is_voice_response": False,
        "duration_seconds": 45.0,
    }
    ans_res = await async_client.post(f"/api/v1/interviews/sessions/{session_id}/answers", json=answer_payload, cookies=cookies)
    assert ans_res.status_code == 200
    ans_data = ans_res.json()
    assert ans_data["score"] is not None
    assert ans_data["score"] >= 40.0

    # 5. Prevent duplicate submission
    dup_res = await async_client.post(f"/api/v1/interviews/sessions/{session_id}/answers", json=answer_payload, cookies=cookies)
    assert dup_res.status_code == 409

    # 6. End interview session
    end_res = await async_client.post(f"/api/v1/interviews/sessions/{session_id}/end", cookies=cookies)
    assert end_res.status_code == 200
    assert end_res.json()["status"] == "completed"

    # 7. Get results
    results_res = await async_client.get(f"/api/v1/interviews/sessions/{session_id}/results", cookies=cookies)
    assert results_res.status_code == 200
    res_data = results_res.json()
    assert res_data["overall_score"] is not None
    assert len(res_data["strengths"]) > 0
    assert len(res_data["recommendations"]) > 0

    # 8. Check interview history
    hist_res = await async_client.get("/api/v1/interviews/history", cookies=cookies)
    assert hist_res.status_code == 200
    hist_data = hist_res.json()
    assert hist_data["total_interviews"] >= 1
    assert hist_data["completed_interviews"] >= 1


@pytest.mark.asyncio
async def test_interview_security_isolation(async_client: AsyncClient, db_session: AsyncSession):
    # User 1
    u1 = User(
        email="student1@example.com",
        password_hash=hash_password("Pass1!"),
        full_name="Student One",
        role="student",
    )
    # User 2
    u2 = User(
        email="student2@example.com",
        password_hash=hash_password("Pass2!"),
        full_name="Student Two",
        role="student",
    )
    db_session.add_all([u1, u2])
    await db_session.commit()
    await db_session.refresh(u1)
    await db_session.refresh(u2)

    token1 = create_access_token(str(u1.id))
    token2 = create_access_token(str(u2.id))

    # User 1 creates session
    res = await async_client.post(
        "/api/v1/interviews/sessions",
        json={"interview_type": "technical", "target_role": "Software Developer", "experience_level": "Beginner"},
        cookies={settings.COOKIE_NAME: token1},
    )
    session_id = res.json()["id"]

    # User 2 tries to access User 1's session -> must return 404/unauthorized
    tamper_res = await async_client.get(
        f"/api/v1/interviews/sessions/{session_id}",
        cookies={settings.COOKIE_NAME: token2},
    )
    assert tamper_res.status_code == 404
