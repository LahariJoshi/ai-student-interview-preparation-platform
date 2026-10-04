import json
import uuid
import pytest
from httpx import AsyncClient

from app.modules.interview.schemas import AnswerAnalysisResult
from app.modules.interview.services.answer_analyzer import AnswerAnalyzerService, answer_analyzer
from app.modules.interview.services.llm_client import (
    MockLLMClient,
    set_llm_client,
    LLMTimeoutError,
    LLMClientError,
)

pytestmark = pytest.mark.asyncio


# ====================================================
# Unit Tests for AnswerAnalyzerService
# ====================================================

async def test_answer_analyzer_success():
    client = MockLLMClient()
    service = AnswerAnalyzerService(llm_client=client)

    result = await service.analyze_answer(
        question_text="Explain the difference between optimistic and pessimistic locking in databases.",
        answer_text="Optimistic locking assumes collisions are rare and verifies with a version column at commit. Pessimistic locking acquires row locks up front preventing concurrent writes.",
        category="Technical",
        topic="Databases",
        expected_points=["Version/timestamp checking", "Exclusive locks / row-level locking", "Concurrency trade-offs"],
        difficulty="Medium",
        target_role="Backend Developer",
    )

    assert isinstance(result, AnswerAnalysisResult)
    assert 0 <= result.score <= 100
    assert 0 <= result.technical_score <= 100
    assert 0 <= result.relevance_score <= 100
    assert 0 <= result.clarity_score <= 100
    assert isinstance(result.strengths, list)
    assert isinstance(result.weaknesses, list)
    assert isinstance(result.feedback, list)
    assert isinstance(result.improvements, list)


async def test_answer_analyzer_markdown_fences():
    canned = """```json
    {
      "score": 92.5,
      "technical_score": 95.0,
      "relevance_score": 90.0,
      "clarity_score": 92.0,
      "strengths": ["Accurate explanation of lexical scoping"],
      "weaknesses": ["Could mention memory leak considerations"],
      "feedback": ["Excellent mastery of JavaScript closures"],
      "improvements": ["Mention how garbage collection interacts with retained references"]
    }
    ```"""
    service = AnswerAnalyzerService(llm_client=MockLLMClient(canned_response=canned))
    result = await service.analyze_answer(
        question_text="What is a closure in JavaScript?",
        answer_text="A closure is the combination of a function bundled together with references to its surrounding lexical environment.",
    )
    assert result.score == 92.5
    assert result.technical_score == 95.0
    assert len(result.strengths) == 1
    assert "Accurate explanation" in result.strengths[0]


async def test_answer_analyzer_empty_inputs():
    service = AnswerAnalyzerService(llm_client=MockLLMClient())

    with pytest.raises(ValueError, match="Question text cannot be empty"):
        await service.analyze_answer(question_text="", answer_text="Valid answer")

    with pytest.raises(ValueError, match="Answer text cannot be empty"):
        await service.analyze_answer(question_text="Valid question", answer_text="   \n  ")


async def test_answer_analyzer_empty_llm_response():
    service = AnswerAnalyzerService(llm_client=MockLLMClient(canned_response=""))
    with pytest.raises(ValueError, match="empty response"):
        await service.analyze_answer(question_text="Question", answer_text="Answer")


async def test_answer_analyzer_malformed_json():
    service = AnswerAnalyzerService(llm_client=MockLLMClient(canned_response="{ not a json string"))
    with pytest.raises(ValueError, match="invalid JSON"):
        await service.analyze_answer(question_text="Question", answer_text="Answer")


async def test_answer_analyzer_schema_validation_failure():
    # Missing required scores
    invalid_data = json.dumps({"strengths": ["Good"]})
    service = AnswerAnalyzerService(llm_client=MockLLMClient(canned_response=invalid_data))
    with pytest.raises(ValueError, match="failed schema validation"):
        await service.analyze_answer(question_text="Question", answer_text="Answer")


async def test_answer_analyzer_timeout():
    class TimeoutClient(MockLLMClient):
        async def generate(self, prompt: str, system_prompt=None) -> str:
            raise LLMTimeoutError("Simulation timeout")

    service = AnswerAnalyzerService(llm_client=TimeoutClient())
    with pytest.raises(LLMTimeoutError):
        await service.analyze_answer(question_text="Question", answer_text="Answer")


async def test_score_clamping():
    data = {
        "score": 150.0,
        "technical_score": -20.0,
        "relevance_score": "88.7",
        "clarity_score": "invalid",
        "strengths": ["Clear communication"],
        "weaknesses": [],
        "feedback": ["Well done"],
        "improvements": []
    }
    result = AnswerAnalysisResult(**data)
    assert result.score == 100.0  # Clamped from 150
    assert result.technical_score == 0.0  # Clamped from -20
    assert result.relevance_score == 88.7  # Parsed from string
    assert result.clarity_score == 50.0  # Fallback for invalid


# ====================================================
# API & Integration Tests
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


async def setup_interview_for_evaluation(client: AsyncClient, cookies):
    set_llm_client(MockLLMClient())

    # 1. Create session
    create_res = await client.post(
        "/api/v1/interview/sessions",
        json={
            "target_role": "Backend Engineer",
            "interview_type": "Technical",
            "experience_level": "Intermediate",
            "difficulty": "Medium",
            "question_count": 2,
            "answer_mode": "Voice + Text",
        },
        cookies=cookies,
    )
    assert create_res.status_code == 201
    session = create_res.json()

    # 2. Generate questions
    q_res = await client.post(
        f"/api/v1/interview/sessions/{session['id']}/generate-questions",
        cookies=cookies,
    )
    assert q_res.status_code == 201
    questions = q_res.json()

    # 3. Submit response for question 0
    resp_res = await client.post(
        f"/api/v1/interview/sessions/{session['id']}/responses",
        json={
            "question_id": questions[0]["id"],
            "answer_text": "Dependency injection passes required dependencies into a class rather than instantiating them directly, improving modularity and testability.",
        },
        cookies=cookies,
    )
    assert resp_res.status_code == 201
    response_data = resp_res.json()

    return session, questions, response_data


async def test_evaluate_response_unauthorized(async_client: AsyncClient):
    fake_session_id = uuid.uuid4()
    fake_response_id = uuid.uuid4()
    res = await async_client.post(
        f"/api/v1/interview/sessions/{fake_session_id}/responses/{fake_response_id}/evaluate"
    )
    assert res.status_code == 401


async def test_evaluate_response_forbidden_other_user(async_client: AsyncClient):
    cookies_owner = await register_and_get_cookies(async_client, "eval_owner@example.com", "Owner")
    cookies_intruder = await register_and_get_cookies(async_client, "eval_intruder@example.com", "Intruder")

    session, questions, response_data = await setup_interview_for_evaluation(async_client, cookies_owner)

    res = await async_client.post(
        f"/api/v1/interview/sessions/{session['id']}/responses/{response_data['id']}/evaluate",
        cookies=cookies_intruder,
    )
    assert res.status_code == 403


async def test_evaluate_response_not_found(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "eval_notfound@example.com")
    session, _, _ = await setup_interview_for_evaluation(async_client, cookies)

    fake_response_id = uuid.uuid4()
    res = await async_client.post(
        f"/api/v1/interview/sessions/{session['id']}/responses/{fake_response_id}/evaluate",
        cookies=cookies,
    )
    assert res.status_code == 404


async def test_evaluate_response_success_and_db_persistence(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "eval_success@example.com")
    session, questions, response_data = await setup_interview_for_evaluation(async_client, cookies)

    # Evaluate the response
    res = await async_client.post(
        f"/api/v1/interview/sessions/{session['id']}/responses/{response_data['id']}/evaluate",
        cookies=cookies,
    )
    assert res.status_code == 200
    data = res.json()

    # Verify return schema
    assert "score" in data
    assert "technical_score" in data
    assert "relevance_score" in data
    assert "clarity_score" in data
    assert "strengths" in data
    assert "weaknesses" in data
    assert "feedback" in data
    assert "improvements" in data
    assert 0 <= data["score"] <= 100

    # Verify database persistence via session detail endpoint
    session_res = await async_client.get(
        f"/api/v1/interview/sessions/{session['id']}",
        cookies=cookies,
    )
    assert session_res.status_code == 200
    session_detail = session_res.json()
    assert session_detail["overall_score"] is not None
    assert session_detail["overall_score"] == data["score"]

    stored_response = session_detail["responses"][0]
    assert stored_response["score"] == data["score"]
    assert stored_response["feedback_text"] is not None
    assert len(stored_response["key_strengths"]) > 0


async def test_evaluate_answer_by_question_endpoint(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "eval_by_q@example.com")
    session, questions, _ = await setup_interview_for_evaluation(async_client, cookies)

    q2 = questions[1]
    res = await async_client.post(
        f"/api/v1/interview/sessions/{session['id']}/evaluate-answer",
        json={
            "question_id": q2["id"],
            "answer_text": "I prioritize automated unit testing and CI pipelines to prevent regressions.",
        },
        cookies=cookies,
    )
    assert res.status_code == 200
    eval_result = res.json()
    assert eval_result["score"] >= 0
    assert len(eval_result["feedback"]) > 0


async def test_evaluate_response_timeout_handling(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "eval_timeout@example.com")
    session, _, response_data = await setup_interview_for_evaluation(async_client, cookies)

    class TimeoutLLMClient(MockLLMClient):
        async def generate(self, prompt: str, system_prompt=None) -> str:
            raise LLMTimeoutError("Simulation timeout")

    set_llm_client(TimeoutLLMClient())

    res = await async_client.post(
        f"/api/v1/interview/sessions/{session['id']}/responses/{response_data['id']}/evaluate",
        cookies=cookies,
    )
    assert res.status_code == 504
    assert "timed out" in res.json()["detail"].lower()
    set_llm_client(MockLLMClient())
