import json
import pytest
import uuid
from httpx import AsyncClient

from app.modules.interview.services.llm_client import (
    MockLLMClient,
    set_llm_client,
    get_llm_client,
    LLMTimeoutError,
    LLMClientError,
)
from app.modules.interview.services.question_generator import (
    QuestionGeneratorService,
    GeneratedQuestionSchema,
)

pytestmark = pytest.mark.asyncio


async def register_and_get_cookies(client: AsyncClient, email: str, name: str = "Test User"):
    reg_payload = {
        "email": email,
        "password": "Password123!",
        "full_name": name,
    }
    res = await client.post("/api/v1/auth/register", json=reg_payload)
    assert res.status_code == 201
    return res.cookies


# ====================================================
# Unit Tests for QuestionGeneratorService & LLMClient
# ====================================================

async def test_llm_client_mock_generation():
    client = MockLLMClient()
    prompt = "Generate 5 questions for a Frontend Engineer with Easy difficulty"
    raw_response = await client.generate(prompt)
    assert raw_response is not None
    data = json.loads(raw_response)
    assert "questions" in data
    assert len(data["questions"]) == 5
    for q in data["questions"]:
        assert "question_text" in q
        assert "category" in q
        assert "difficulty" in q
        assert "question_order" in q


async def test_question_generator_parsing_valid():
    service = QuestionGeneratorService(llm_client=MockLLMClient())
    questions = await service.generate_questions(
        interview_type="Technical",
        target_role="Fullstack Developer",
        experience_level="Fresher",
        difficulty="Medium",
        question_count=5,
        target_company="Google",
    )
    assert len(questions) == 5
    for idx, q in enumerate(questions, start=1):
        assert isinstance(q, GeneratedQuestionSchema)
        assert q.question_order == idx
        assert q.category in ["Technical", "Behavioral", "HR", "Situational"]
        assert q.difficulty in ["Easy", "Medium", "Hard"]
        assert len(q.question_text) >= 10


async def test_question_generator_handles_markdown_fence():
    canned_json = """```json
    {
      "questions": [
        {
          "question_order": 1,
          "category": "technical",
          "topic": "Closures",
          "question_text": "What is a closure in JavaScript and how does lexical scoping work?",
          "difficulty": "medium",
          "expected_points": ["Inner function access", "Lexical scope"]
        }
      ]
    }
    ```"""
    service = QuestionGeneratorService(llm_client=MockLLMClient(canned_response=canned_json))
    questions = await service.generate_questions("Technical", "Web Developer", "Fresher", "Easy", 1)
    assert len(questions) == 1
    assert questions[0].topic == "Closures"
    assert questions[0].category == "Technical"


async def test_question_generator_handles_empty_response():
    service = QuestionGeneratorService(llm_client=MockLLMClient(canned_response=""))
    with pytest.raises(ValueError, match="empty response"):
        await service.generate_questions("Technical", "Engineer", "Fresher", "Easy", 3)


async def test_question_generator_handles_malformed_json():
    service = QuestionGeneratorService(llm_client=MockLLMClient(canned_response="{ not valid json"))
    with pytest.raises(ValueError, match="invalid JSON"):
        await service.generate_questions("Technical", "Engineer", "Fresher", "Easy", 3)


async def test_question_generator_handles_missing_questions_root():
    service = QuestionGeneratorService(llm_client=MockLLMClient(canned_response='{"wrong_key": []}'))
    with pytest.raises(ValueError, match="missing 'questions' array"):
        await service.generate_questions("Technical", "Engineer", "Fresher", "Easy", 3)


class TimeoutMockClient(MockLLMClient):
    async def generate(self, prompt: str, system_prompt=None) -> str:
        raise LLMTimeoutError("Request timed out")


class ErrorMockClient(MockLLMClient):
    async def generate(self, prompt: str, system_prompt=None) -> str:
        raise LLMClientError("Provider internal server error")


async def test_question_generator_handles_timeout():
    service = QuestionGeneratorService(llm_client=TimeoutMockClient())
    with pytest.raises(LLMTimeoutError):
        await service.generate_questions("Technical", "Engineer", "Fresher", "Easy", 3)


# ====================================================
# API Integration Tests for /generate-questions
# ====================================================

async def test_api_generate_questions_success(async_client: AsyncClient):
    # Set mock client
    set_llm_client(MockLLMClient())

    cookies = await register_and_get_cookies(async_client, "gen_success@example.com", "Gen Tester")

    # 1. Create session
    create_res = await async_client.post(
        "/api/v1/interview/sessions",
        json={
            "target_role": "Backend Engineer",
            "interview_type": "Mixed",
            "difficulty": "Medium",
            "question_count": 5,
        },
        cookies=cookies,
    )
    assert create_res.status_code == 201
    session_id = create_res.json()["id"]

    # 2. Generate questions
    gen_res = await async_client.post(
        f"/api/v1/interview/sessions/{session_id}/generate-questions",
        cookies=cookies,
    )
    assert gen_res.status_code == 201
    questions = gen_res.json()
    assert len(questions) == 5

    categories = set()
    for idx, q in enumerate(questions, start=1):
        assert q["session_id"] == session_id
        assert q["question_order"] == idx
        assert len(q["question_text"]) >= 10
        categories.add(q["category"])

    # Verify categories generated
    assert any(cat in ["Technical", "Behavioral", "HR", "Situational"] for cat in categories)


async def test_api_prevent_duplicate_question_generation(async_client: AsyncClient):
    set_llm_client(MockLLMClient())
    cookies = await register_and_get_cookies(async_client, "dup_gen@example.com")

    create_res = await async_client.post(
        "/api/v1/interview/sessions",
        json={"target_role": "Data Analyst", "question_count": 3},
        cookies=cookies,
    )
    session_id = create_res.json()["id"]

    # First generation -> 201
    gen1 = await async_client.post(f"/api/v1/interview/sessions/{session_id}/generate-questions", cookies=cookies)
    assert gen1.status_code == 201

    # Second generation -> 400 Bad Request
    gen2 = await async_client.post(f"/api/v1/interview/sessions/{session_id}/generate-questions", cookies=cookies)
    assert gen2.status_code == 400
    assert "already been generated" in gen2.json()["detail"]


async def test_api_generate_questions_ownership_isolation(async_client: AsyncClient):
    set_llm_client(MockLLMClient())
    cookies_owner = await register_and_get_cookies(async_client, "owner_gen@example.com")
    cookies_other = await register_and_get_cookies(async_client, "other_gen@example.com")

    # Owner creates session
    create_res = await async_client.post(
        "/api/v1/interview/sessions",
        json={"target_role": "Security Engineer"},
        cookies=cookies_owner,
    )
    session_id = create_res.json()["id"]

    # Other user attempts to generate questions for owner's session -> 403 Forbidden
    other_gen = await async_client.post(
        f"/api/v1/interview/sessions/{session_id}/generate-questions",
        cookies=cookies_other,
    )
    assert other_gen.status_code == 403

    # Non-existent session -> 404 Not Found
    random_id = uuid.uuid4()
    not_found_res = await async_client.post(
        f"/api/v1/interview/sessions/{random_id}/generate-questions",
        cookies=cookies_owner,
    )
    assert not_found_res.status_code == 404


async def test_api_generate_questions_provider_timeout(async_client: AsyncClient):
    # Set timeout client
    set_llm_client(TimeoutMockClient())
    cookies = await register_and_get_cookies(async_client, "timeout_test@example.com")

    create_res = await async_client.post(
        "/api/v1/interview/sessions",
        json={"target_role": "Cloud Architect"},
        cookies=cookies,
    )
    session_id = create_res.json()["id"]

    res = await async_client.post(
        f"/api/v1/interview/sessions/{session_id}/generate-questions",
        cookies=cookies,
    )
    assert res.status_code == 504
    assert "timed out" in res.json()["detail"]

    # Reset client
    set_llm_client(None)


async def test_api_generate_questions_provider_error(async_client: AsyncClient):
    # Set error client
    set_llm_client(ErrorMockClient())
    cookies = await register_and_get_cookies(async_client, "error_test@example.com")

    create_res = await async_client.post(
        "/api/v1/interview/sessions",
        json={"target_role": "Site Reliability Engineer"},
        cookies=cookies,
    )
    session_id = create_res.json()["id"]

    res = await async_client.post(
        f"/api/v1/interview/sessions/{session_id}/generate-questions",
        cookies=cookies,
    )
    assert res.status_code == 502
    assert "failed" in res.json()["detail"]

    # Reset client
    set_llm_client(None)
