"""
test_seeded_api_verification.py - End-to-end API verification against seeded question bank.
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from seed_coding_questions import seed_questions_to_session

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture(autouse=True)
async def seed_test_database(db_session: AsyncSession):
    """Seed test SQLite in-memory database with the full question bank."""
    await seed_questions_to_session(db_session)


async def test_api_questions_list_seeded(async_client: AsyncClient):
    """Verify that GET /api/v1/coding/questions returns the seeded question bank."""
    res = await async_client.get("/api/v1/coding/questions?limit=50")
    assert res.status_code == 200
    data = res.json()
    assert data["total_count"] >= 150
    assert len(data["questions"]) == 50
    assert "id" in data["questions"][0]
    assert "slug" in data["questions"][0]
    assert "title" in data["questions"][0]
    assert "difficulty" in data["questions"][0]
    assert "topic" in data["questions"][0]


async def test_api_topics_summary_seeded(async_client: AsyncClient):
    """Verify that GET /api/v1/coding/questions/topics/summary returns all DSA topics with counts."""
    res = await async_client.get("/api/v1/coding/questions/topics/summary")
    assert res.status_code == 200
    topics = res.json()
    assert len(topics) >= 10
    topic_names = {t["topic"] for t in topics}
    assert "Array" in topic_names
    assert "String" in topic_names
    assert "Dynamic Programming" in topic_names
    for t in topics:
        assert t["question_count"] > 0


async def test_api_difficulties_summary_seeded(async_client: AsyncClient):
    """Verify that GET /api/v1/coding/questions/difficulties/summary returns Easy, Medium, Hard counts."""
    res = await async_client.get("/api/v1/coding/questions/difficulties/summary")
    assert res.status_code == 200
    diffs = res.json()
    diff_dict = {d["difficulty"]: d["question_count"] for d in diffs}
    assert diff_dict.get("Easy", 0) >= 50
    assert diff_dict.get("Medium", 0) >= 70
    assert diff_dict.get("Hard", 0) >= 30


async def test_api_question_detail_by_slug(async_client: AsyncClient):
    """Verify that GET /api/v1/coding/questions/{id_or_slug} returns full question details and sample test cases."""
    res = await async_client.get("/api/v1/coding/questions/two-sum")
    assert res.status_code == 200
    q = res.json()
    assert q["title"] == "Two Sum"
    assert q["difficulty"] == "Easy"
    assert q["topic"] == "Array"
    assert "python" in q["starter_code"]
    assert len(q["sample_test_cases"]) >= 2
    for stc in q["sample_test_cases"]:
        assert stc["is_sample"] is True
        assert stc["input_data"] is not None
        assert stc["expected_output"] is not None


async def test_api_question_random_seeded(async_client: AsyncClient):
    """Verify that GET /api/v1/coding/questions/random selects a real question."""
    res = await async_client.get("/api/v1/coding/questions/random?difficulty=Easy")
    assert res.status_code == 200
    q = res.json()
    assert q["difficulty"] == "Easy"
    assert q["slug"] is not None
