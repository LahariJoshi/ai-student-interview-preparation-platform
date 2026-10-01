import uuid
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.coding import (
    CodingQuestion,
    CodingTestCase,
    CodingSubmission,
    CodingResult,
)

pytestmark = pytest.mark.asyncio


async def register_student(async_client: AsyncClient, email: str = "retrieval_student@example.com") -> dict:
    """Helper to register a student and return session cookies."""
    async_client.cookies.clear()
    payload = {
        "email": email,
        "password": "password123",
        "full_name": "Retrieval Student",
    }
    res = await async_client.post("/api/v1/auth/register", json=payload)
    assert res.status_code == 201
    return dict(res.cookies)


async def seed_test_questions(db: AsyncSession) -> dict:
    """Helper to seed a diverse set of coding questions and test cases."""
    questions_data = [
        {
            "id": uuid.uuid4(),
            "title": "Two Sum",
            "slug": "two-sum",
            "description": "Find two numbers in array that add up to target.",
            "difficulty": "Easy",
            "topic": "Arrays",
            "constraints": "2 <= nums.length <= 10^4",
            "hints": ["Use a hash table."],
            "starter_code": {"python": "def twoSum(nums, target): pass"},
            "test_cases": [
                {"input_data": "[2,7,11,15]\n9", "expected_output": "[0,1]", "is_sample": True},
                {"input_data": "[3,2,4]\n6", "expected_output": "[1,2]", "is_sample": False},
            ],
        },
        {
            "id": uuid.uuid4(),
            "title": "3Sum",
            "slug": "3sum",
            "description": "Find all unique triplets in array that sum to zero.",
            "difficulty": "Medium",
            "topic": "Arrays",
            "constraints": "3 <= nums.length <= 3000",
            "hints": ["Sort array and use two pointers."],
            "starter_code": {"python": "def threeSum(nums): pass"},
            "test_cases": [
                {"input_data": "[-1,0,1,2,-1,-4]", "expected_output": "[[-1,-1,2],[-1,0,1]]", "is_sample": True},
            ],
        },
        {
            "id": uuid.uuid4(),
            "title": "Longest Substring Without Repeating Characters",
            "slug": "longest-substring",
            "description": "Find length of longest substring without repeating characters.",
            "difficulty": "Medium",
            "topic": "Strings",
            "constraints": "0 <= s.length <= 5 * 10^4",
            "hints": ["Sliding window with set."],
            "starter_code": {"python": "def lengthOfLongestSubstring(s): pass"},
            "test_cases": [
                {"input_data": '"abcabcbb"', "expected_output": "3", "is_sample": True},
                {"input_data": '"bbbbb"', "expected_output": "1", "is_sample": True},
            ],
        },
        {
            "id": uuid.uuid4(),
            "title": "Valid Parentheses",
            "slug": "valid-parentheses",
            "description": "Determine if input string brackets are valid.",
            "difficulty": "Easy",
            "topic": "Strings",
            "constraints": "1 <= s.length <= 10^4",
            "hints": ["Use a stack."],
            "starter_code": {"python": "def isValid(s): pass"},
            "test_cases": [
                {"input_data": '"()"', "expected_output": "true", "is_sample": True},
                {"input_data": '"(]"', "expected_output": "false", "is_sample": False},
            ],
        },
        {
            "id": uuid.uuid4(),
            "title": "Median of Two Sorted Arrays",
            "slug": "median-two-sorted-arrays",
            "description": "Find median of two sorted arrays in O(log(m+n)).",
            "difficulty": "Hard",
            "topic": "Arrays",
            "constraints": "0 <= m, n <= 1000",
            "hints": ["Binary search on partition."],
            "starter_code": {"python": "def findMedianSortedArrays(nums1, nums2): pass"},
            "test_cases": [
                {"input_data": "[1,3]\n[2]", "expected_output": "2.0", "is_sample": True},
            ],
        },
    ]

    for qd in questions_data:
        q = CodingQuestion(
            id=qd["id"],
            title=qd["title"],
            slug=qd["slug"],
            description=qd["description"],
            difficulty=qd["difficulty"],
            topic=qd["topic"],
            constraints=qd["constraints"],
            hints=qd["hints"],
            starter_code=qd["starter_code"],
        )
        db.add(q)
        for idx, tc in enumerate(qd["test_cases"]):
            test_case = CodingTestCase(
                id=uuid.uuid4(),
                question_id=q.id,
                input_data=tc["input_data"],
                expected_output=tc["expected_output"],
                is_sample=tc["is_sample"],
                order_index=idx + 1,
            )
            db.add(test_case)

    await db.commit()
    return {qd["slug"]: qd["id"] for qd in questions_data}


async def test_question_filtering_by_topic_and_difficulty(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test filtering questions by topic, difficulty, and both."""
    await seed_test_questions(db_session)

    # 1. Filter by Topic
    res = await async_client.get("/api/v1/coding/questions?topic=Arrays")
    assert res.status_code == 200
    data = res.json()
    assert data["total_count"] == 3
    for q in data["questions"]:
        assert q["topic"] == "Arrays"

    # Case-insensitive topic filter
    res_lower = await async_client.get("/api/v1/coding/questions?topic=arrays")
    assert res_lower.status_code == 200
    assert res_lower.json()["total_count"] == 3

    # 2. Filter by Difficulty
    res_diff = await async_client.get("/api/v1/coding/questions?difficulty=Easy")
    assert res_diff.status_code == 200
    data_diff = res_diff.json()
    assert data_diff["total_count"] == 2
    for q in data_diff["questions"]:
        assert q["difficulty"] == "Easy"

    # Case-insensitive difficulty filter
    res_diff_lower = await async_client.get("/api/v1/coding/questions?difficulty=hard")
    assert res_diff_lower.status_code == 200
    assert res_diff_lower.json()["total_count"] == 1
    assert res_diff_lower.json()["questions"][0]["slug"] == "median-two-sorted-arrays"

    # 3. Combined Filter (Arrays + Medium)
    res_comb = await async_client.get("/api/v1/coding/questions?topic=Arrays&difficulty=Medium")
    assert res_comb.status_code == 200
    data_comb = res_comb.json()
    assert data_comb["total_count"] == 1
    assert data_comb["questions"][0]["slug"] == "3sum"


async def test_question_search_keyword(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test question search across title, description, and topic."""
    await seed_test_questions(db_session)

    # Search in title
    res = await async_client.get("/api/v1/coding/questions?search=Parentheses")
    assert res.status_code == 200
    assert res.json()["total_count"] == 1
    assert res.json()["questions"][0]["title"] == "Valid Parentheses"

    # Search in description
    res_desc = await async_client.get("/api/v1/coding/questions?search=triplets")
    assert res_desc.status_code == 200
    assert res_desc.json()["total_count"] == 1
    assert res_desc.json()["questions"][0]["slug"] == "3sum"

    # Search with no matches
    res_none = await async_client.get("/api/v1/coding/questions?search=NonExistentTerm123")
    assert res_none.status_code == 200
    assert res_none.json()["total_count"] == 0
    assert res_none.json()["questions"] == []


async def test_question_pagination_and_sorting(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test pagination metadata and sorting options."""
    await seed_test_questions(db_session)

    # 1. Page-based pagination (page=1, limit=2)
    p1 = await async_client.get("/api/v1/coding/questions?page=1&limit=2")
    assert p1.status_code == 200
    d1 = p1.json()
    assert d1["total_count"] == 5
    assert d1["page"] == 1
    assert d1["limit"] == 2
    assert d1["total_pages"] == 3
    assert len(d1["questions"]) == 2

    # Page 2
    p2 = await async_client.get("/api/v1/coding/questions?page=2&limit=2")
    assert p2.status_code == 200
    d2 = p2.json()
    assert d2["page"] == 2
    assert len(d2["questions"]) == 2
    # Ensure distinct items
    p1_ids = {q["id"] for q in d1["questions"]}
    p2_ids = {q["id"] for q in d2["questions"]}
    assert p1_ids.isdisjoint(p2_ids)

    # 2. Skip-based pagination offset
    p_skip = await async_client.get("/api/v1/coding/questions?skip=4&limit=2")
    assert p_skip.status_code == 200
    d_skip = p_skip.json()
    assert len(d_skip["questions"]) == 1

    # 3. Sorting by title
    sort_asc = await async_client.get("/api/v1/coding/questions?sort_by=title&sort_order=asc")
    assert sort_asc.status_code == 200
    titles_asc = [q["title"] for q in sort_asc.json()["questions"]]
    assert titles_asc == sorted(titles_asc)

    sort_desc = await async_client.get("/api/v1/coding/questions?sort_by=title&sort_order=desc")
    assert sort_desc.status_code == 200
    titles_desc = [q["title"] for q in sort_desc.json()["questions"]]
    assert titles_desc == sorted(titles_desc, reverse=True)

    # 4. Sorting by difficulty tier (Easy -> Medium -> Hard)
    sort_diff = await async_client.get("/api/v1/coding/questions?sort_by=difficulty&sort_order=asc")
    assert sort_diff.status_code == 200
    diff_order = [q["difficulty"] for q in sort_diff.json()["questions"]]
    # Should start with Easy, then Medium, then Hard
    tier_map = {"Easy": 1, "Medium": 2, "Hard": 3}
    num_tiers = [tier_map[d] for d in diff_order]
    assert num_tiers == sorted(num_tiers)


async def test_question_retrieval_validation_errors(async_client: AsyncClient):
    """Test validation errors for invalid query filters."""
    # Invalid difficulty
    res1 = await async_client.get("/api/v1/coding/questions?difficulty=Expert")
    assert res1.status_code == 400
    assert "Invalid difficulty" in res1.json()["detail"]

    # Invalid status
    res2 = await async_client.get("/api/v1/coding/questions?status=completed")
    assert res2.status_code == 400
    assert "Invalid status filter" in res2.json()["detail"]

    # Invalid sort_by
    res3 = await async_client.get("/api/v1/coding/questions?sort_by=popularity")
    assert res3.status_code == 400
    assert "Invalid sort_by" in res3.json()["detail"]

    # Invalid sort_order
    res4 = await async_client.get("/api/v1/coding/questions?sort_order=sideways")
    assert res4.status_code == 400
    assert "Invalid sort_order" in res4.json()["detail"]

    # Unauthenticated user attempting to filter by solved status
    async_client.cookies.clear()
    res5 = await async_client.get("/api/v1/coding/questions?status=solved")
    assert res5.status_code == 401
    assert "Authentication required" in res5.json()["detail"]


async def test_question_solve_status_filtering(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test solved vs unsolved filtering for an authenticated student."""
    q_map = await seed_test_questions(db_session)
    two_sum_id = q_map["two-sum"]

    # Register student
    cookies = await register_student(async_client, "solver@example.com")

    # Get student user ID
    user_res = await async_client.get("/api/v1/auth/me", cookies=cookies)
    assert user_res.status_code == 200
    student_id = uuid.UUID(user_res.json()["id"])

    # Simulate an Accepted submission for Two Sum
    submission = CodingSubmission(
        id=uuid.uuid4(),
        user_id=student_id,
        question_id=two_sum_id,
        language="python",
        code="def twoSum(nums, target): return [0, 1]",
        status="completed",
    )
    db_session.add(submission)
    await db_session.flush()

    result = CodingResult(
        id=uuid.uuid4(),
        submission_id=submission.id,
        verdict="Accepted",
        score=100.0,
        passed_test_cases=2,
        total_test_cases=2,
        execution_time_ms=25.0,
        memory_kb=14200.0,
    )
    db_session.add(result)
    await db_session.commit()

    # 1. Query with status=solved
    res_solved = await async_client.get("/api/v1/coding/questions?status=solved", cookies=cookies)
    assert res_solved.status_code == 200
    d_solved = res_solved.json()
    assert d_solved["total_count"] == 1
    assert d_solved["questions"][0]["slug"] == "two-sum"
    assert d_solved["questions"][0]["is_solved"] is True

    # 2. Query with status=unsolved
    res_unsolved = await async_client.get("/api/v1/coding/questions?status=unsolved", cookies=cookies)
    assert res_unsolved.status_code == 200
    d_unsolved = res_unsolved.json()
    assert d_unsolved["total_count"] == 4
    unsolved_slugs = [q["slug"] for q in d_unsolved["questions"]]
    assert "two-sum" not in unsolved_slugs
    for q in d_unsolved["questions"]:
        assert q["is_solved"] is False

    # 3. Query details of solved vs unsolved question
    q_solved_res = await async_client.get(f"/api/v1/coding/questions/{two_sum_id}", cookies=cookies)
    assert q_solved_res.status_code == 200
    assert q_solved_res.json()["is_solved"] is True

    three_sum_id = q_map["3sum"]
    q_unsolved_res = await async_client.get(f"/api/v1/coding/questions/{three_sum_id}", cookies=cookies)
    assert q_unsolved_res.status_code == 200
    assert q_unsolved_res.json()["is_solved"] is False


async def test_topic_and_difficulty_summaries(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test topic summary breakdown and difficulty breakdown endpoints."""
    await seed_test_questions(db_session)

    # 1. Topic Summary
    res_topics = await async_client.get("/api/v1/coding/questions/topics/summary")
    assert res_topics.status_code == 200
    summaries = res_topics.json()
    assert isinstance(summaries, list)
    topic_dict = {item["topic"]: item for item in summaries}

    assert "Arrays" in topic_dict
    assert topic_dict["Arrays"]["question_count"] == 3
    assert topic_dict["Arrays"]["easy_count"] == 1  # Two Sum
    assert topic_dict["Arrays"]["medium_count"] == 1  # 3Sum
    assert topic_dict["Arrays"]["hard_count"] == 1  # Median

    assert "Strings" in topic_dict
    assert topic_dict["Strings"]["question_count"] == 2
    assert topic_dict["Strings"]["easy_count"] == 1  # Valid Parentheses
    assert topic_dict["Strings"]["medium_count"] == 1  # Longest Substring

    # 2. Difficulty Summary
    res_diff = await async_client.get("/api/v1/coding/questions/difficulties/summary")
    assert res_diff.status_code == 200
    diff_summaries = res_diff.json()
    diff_dict = {item["difficulty"]: item["question_count"] for item in diff_summaries}
    assert diff_dict["Easy"] == 2
    assert diff_dict["Medium"] == 2
    assert diff_dict["Hard"] == 1


async def test_random_question_selection(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test picking a random question with various filters."""
    await seed_test_questions(db_session)

    # Random question overall
    res = await async_client.get("/api/v1/coding/questions/random")
    assert res.status_code == 200
    data = res.json()
    assert "title" in data
    assert "difficulty" in data
    # Sample test cases are populated
    assert isinstance(data["sample_test_cases"], list)

    # Random question filtered by topic
    res_topic = await async_client.get("/api/v1/coding/questions/random?topic=Strings")
    assert res_topic.status_code == 200
    assert res_topic.json()["topic"] == "Strings"

    # Random question filtered by difficulty
    res_diff = await async_client.get("/api/v1/coding/questions/random?difficulty=Hard")
    assert res_diff.status_code == 200
    assert res_diff.json()["difficulty"] == "Hard"
    assert res_diff.json()["slug"] == "median-two-sorted-arrays"

    # Random question with no match -> 404
    res_404 = await async_client.get("/api/v1/coding/questions/random?topic=GraphTheory")
    assert res_404.status_code == 404
    assert "No questions match" in res_404.json()["detail"]


async def test_get_question_by_id_and_slug_security(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test retrieving questions by ID and slug, ensuring hidden test cases are hidden."""
    q_map = await seed_test_questions(db_session)
    two_sum_id = q_map["two-sum"]

    # 1. Explicit ID endpoint
    res_by_id = await async_client.get(f"/api/v1/coding/questions/id/{two_sum_id}")
    assert res_by_id.status_code == 200
    d_id = res_by_id.json()
    assert d_id["id"] == str(two_sum_id)
    assert d_id["slug"] == "two-sum"
    # Verify hidden test case is not in sample_test_cases
    assert len(d_id["sample_test_cases"]) == 1
    assert d_id["sample_test_cases"][0]["is_sample"] is True
    assert "all_test_cases" not in d_id

    # Non-existent ID
    fake_id = uuid.uuid4()
    res_fake = await async_client.get(f"/api/v1/coding/questions/id/{fake_id}")
    assert res_fake.status_code == 404

    # 2. Slug endpoint
    res_slug = await async_client.get("/api/v1/coding/questions/two-sum")
    assert res_slug.status_code == 200
    assert res_slug.json()["id"] == str(two_sum_id)

    # 3. UUID via /{id_or_slug} route
    res_uuid_slug = await async_client.get(f"/api/v1/coding/questions/{two_sum_id}")
    assert res_uuid_slug.status_code == 200
    assert res_uuid_slug.json()["title"] == "Two Sum"

    # Non-existent slug
    res_slug_404 = await async_client.get("/api/v1/coding/questions/non-existent-problem")
    assert res_slug_404.status_code == 404
