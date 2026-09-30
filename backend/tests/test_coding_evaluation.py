import uuid
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.coding import (
    CodingQuestion,
    CodingTestCase,
    CodingSubmission,
    CodingResult,
)

pytestmark = pytest.mark.asyncio


async def register_student(async_client: AsyncClient, email: str = "coder@example.com") -> dict:
    """Helper to register a student and return session cookies."""
    async_client.cookies.clear()
    payload = {
        "email": email,
        "password": "password123",
        "full_name": "Test Coder",
    }
    res = await async_client.post("/api/v1/auth/register", json=payload)
    assert res.status_code == 201
    return dict(res.cookies)


async def create_question_with_test_cases(
    db: AsyncSession,
    title: str = "Reverse String",
    slug: str = "reverse-string",
) -> CodingQuestion:
    """Helper to create a question with both sample and hidden test cases."""
    q = CodingQuestion(
        id=uuid.uuid4(),
        title=title,
        slug=slug,
        description="Write a function reverse_str(s) that reverses a given string.",
        difficulty="Easy",
        topic="Strings",
        starter_code={
            "python": "def reverse_str(s):\n    return s[::-1]",
            "javascript": "const fs = require('fs');\nconst input = fs.readFileSync(0, 'utf-8').trim();\nconsole.log(input.split('').reverse().join(''));",
        },
    )
    db.add(q)
    await db.flush()

    tc1 = CodingTestCase(
        id=uuid.uuid4(),
        question_id=q.id,
        input_data="hello",
        expected_output="olleh",
        is_sample=True,
        explanation="hello reversed is olleh",
        order_index=0,
    )
    tc2 = CodingTestCase(
        id=uuid.uuid4(),
        question_id=q.id,
        input_data="world",
        expected_output="dlrow",
        is_sample=True,
        explanation="world reversed is dlrow",
        order_index=1,
    )
    tc_hidden = CodingTestCase(
        id=uuid.uuid4(),
        question_id=q.id,
        input_data="secret_hidden_string",
        expected_output="gnirts_neddih_terces",
        is_sample=False,
        explanation=None,
        order_index=2,
    )
    db.add_all([tc1, tc2, tc_hidden])
    await db.commit()
    await db.refresh(q)
    return q


async def test_evaluate_submission_accepted_python(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test evaluating a valid Python submission that passes all sample and hidden test cases."""
    question = await create_question_with_test_cases(db_session, "Reverse Str Accepted", "rev-accepted")
    cookies = await register_student(async_client, "accepted_coder@example.com")

    # Correct solution handling stdin or reverse_str function
    code = (
        "import sys\n"
        "s = sys.stdin.read().strip()\n"
        "print(s[::-1])\n"
    )

    create_res = await async_client.post(
        "/api/v1/coding/submissions",
        json={"question_id": str(question.id), "language": "python", "code": code},
        cookies=cookies,
    )
    assert create_res.status_code == 201
    sub_id = create_res.json()["id"]

    eval_res = await async_client.post(
        f"/api/v1/coding/submissions/{sub_id}/evaluate",
        cookies=cookies,
    )
    assert eval_res.status_code == 200
    data = eval_res.json()

    assert data["status"] == "completed"
    assert data["result"] is not None
    result = data["result"]
    assert result["verdict"] == "Accepted"
    assert result["score"] == 100.0
    assert result["passed_test_cases"] == 3
    assert result["total_test_cases"] == 3
    assert result["error_message"] is None

    # Check test case details - hidden test cases must have I/O redacted
    tc_results = result["test_case_results"]
    assert len(tc_results) == 3

    for tc in tc_results:
        assert tc["passed"] is True
        assert tc["verdict"] == "Passed"
        if tc["is_sample"]:
            assert tc["input_data"] is not None
            assert tc["expected_output"] is not None
            assert tc["actual_output"] is not None
        else:
            # Privacy & anti-cheat: hidden test case input/output must be None
            assert tc["input_data"] is None
            assert tc["expected_output"] is None
            assert tc["actual_output"] is None


async def test_evaluate_submission_wrong_answer(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test evaluating a submission that produces wrong answers."""
    question = await create_question_with_test_cases(db_session, "Reverse Str WA", "rev-wa")
    cookies = await register_student(async_client, "wa_coder@example.com")

    # Code produces constant wrong answer
    code = "print('incorrect_output')"

    create_res = await async_client.post(
        "/api/v1/coding/submissions",
        json={"question_id": str(question.id), "language": "python", "code": code},
        cookies=cookies,
    )
    sub_id = create_res.json()["id"]

    eval_res = await async_client.post(
        f"/api/v1/coding/submissions/{sub_id}/evaluate",
        cookies=cookies,
    )
    assert eval_res.status_code == 200
    data = eval_res.json()

    assert data["status"] == "completed"
    assert data["result"]["verdict"] == "Wrong Answer"
    assert data["result"]["score"] == 0.0
    assert data["result"]["passed_test_cases"] == 0
    assert data["result"]["total_test_cases"] == 3


async def test_evaluate_submission_syntax_compilation_error(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test evaluating a submission with syntax/compilation error."""
    question = await create_question_with_test_cases(db_session, "Reverse Str Syntax", "rev-syntax")
    cookies = await register_student(async_client, "syntax_coder@example.com")

    # Code has syntax error
    code = "def invalid_syntax(: pass"

    create_res = await async_client.post(
        "/api/v1/coding/submissions",
        json={"question_id": str(question.id), "language": "python", "code": code},
        cookies=cookies,
    )
    sub_id = create_res.json()["id"]

    eval_res = await async_client.post(
        f"/api/v1/coding/submissions/{sub_id}/evaluate",
        cookies=cookies,
    )
    assert eval_res.status_code == 200
    data = eval_res.json()

    assert data["status"] == "completed"
    assert data["result"]["verdict"] == "Compilation Error"
    assert data["result"]["score"] == 0.0
    assert "SyntaxError" in data["result"]["error_message"]


async def test_evaluate_submission_runtime_error(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test evaluating a submission that throws runtime exception."""
    question = await create_question_with_test_cases(db_session, "Reverse Str Runtime", "rev-runtime")
    cookies = await register_student(async_client, "runtime_coder@example.com")

    # Code raises ZeroDivisionError
    code = "x = 1 / 0"

    create_res = await async_client.post(
        "/api/v1/coding/submissions",
        json={"question_id": str(question.id), "language": "python", "code": code},
        cookies=cookies,
    )
    sub_id = create_res.json()["id"]

    eval_res = await async_client.post(
        f"/api/v1/coding/submissions/{sub_id}/evaluate",
        cookies=cookies,
    )
    assert eval_res.status_code == 200
    data = eval_res.json()

    assert data["status"] == "completed"
    assert data["result"]["verdict"] == "Runtime Error"
    assert data["result"]["score"] == 0.0
    assert "ZeroDivisionError" in data["result"]["error_message"]


async def test_evaluate_submission_timeout(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test evaluating code with an infinite loop triggers Time Limit Exceeded."""
    question = await create_question_with_test_cases(db_session, "Reverse Str Timeout", "rev-timeout")
    cookies = await register_student(async_client, "timeout_coder@example.com")

    # Code runs infinite loop
    code = "while True:\n    pass"

    create_res = await async_client.post(
        "/api/v1/coding/submissions",
        json={"question_id": str(question.id), "language": "python", "code": code},
        cookies=cookies,
    )
    sub_id = create_res.json()["id"]

    eval_res = await async_client.post(
        f"/api/v1/coding/submissions/{sub_id}/evaluate",
        cookies=cookies,
    )
    assert eval_res.status_code == 200
    data = eval_res.json()

    assert data["status"] == "completed"
    assert data["result"]["verdict"] == "Time Limit Exceeded"
    assert data["result"]["score"] == 0.0
    assert "Time limit exceeded" in data["result"]["error_message"]


async def test_evaluate_submission_security_os_blocked(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test security validation blocks forbidden modules (e.g. os)."""
    question = await create_question_with_test_cases(db_session, "Reverse Str Security OS", "rev-sec-os")
    cookies = await register_student(async_client, "hacker_os@example.com")

    # Attempting to import os
    code = "import os\nprint(os.listdir('.'))"

    create_res = await async_client.post(
        "/api/v1/coding/submissions",
        json={"question_id": str(question.id), "language": "python", "code": code},
        cookies=cookies,
    )
    sub_id = create_res.json()["id"]

    eval_res = await async_client.post(
        f"/api/v1/coding/submissions/{sub_id}/evaluate",
        cookies=cookies,
    )
    assert eval_res.status_code == 200
    data = eval_res.json()

    assert data["status"] == "completed"
    assert data["result"]["verdict"] == "Compilation Error"
    assert "Module 'os' is not permitted" in data["result"]["error_message"]


async def test_evaluate_submission_security_open_blocked(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test security validation blocks forbidden built-in functions (e.g. open)."""
    question = await create_question_with_test_cases(db_session, "Reverse Str Security Open", "rev-sec-open")
    cookies = await register_student(async_client, "hacker_open@example.com")

    code = "f = open('config.py', 'r')\nprint(f.read())"

    create_res = await async_client.post(
        "/api/v1/coding/submissions",
        json={"question_id": str(question.id), "language": "python", "code": code},
        cookies=cookies,
    )
    sub_id = create_res.json()["id"]

    eval_res = await async_client.post(
        f"/api/v1/coding/submissions/{sub_id}/evaluate",
        cookies=cookies,
    )
    assert eval_res.status_code == 200
    data = eval_res.json()

    assert data["status"] == "completed"
    assert data["result"]["verdict"] == "Compilation Error"
    assert "Function 'open' is not permitted" in data["result"]["error_message"]


async def test_evaluate_submission_security_dunder_blocked(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test security validation blocks forbidden dunder access (e.g. __subclasses__)."""
    question = await create_question_with_test_cases(db_session, "Reverse Str Security Dunder", "rev-sec-dunder")
    cookies = await register_student(async_client, "hacker_dunder@example.com")

    code = "classes = ().__class__.__bases__[0].__subclasses__()\nprint(classes)"

    create_res = await async_client.post(
        "/api/v1/coding/submissions",
        json={"question_id": str(question.id), "language": "python", "code": code},
        cookies=cookies,
    )
    sub_id = create_res.json()["id"]

    eval_res = await async_client.post(
        f"/api/v1/coding/submissions/{sub_id}/evaluate",
        cookies=cookies,
    )
    assert eval_res.status_code == 200
    data = eval_res.json()

    assert data["status"] == "completed"
    assert data["result"]["verdict"] == "Compilation Error"
    assert "Attribute '__subclasses__' is not permitted" in data["result"]["error_message"]


async def test_evaluate_immediate_query_param(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test POST /submissions?evaluate=true evaluates immediately in single request."""
    question = await create_question_with_test_cases(db_session, "Immediate Eval Q", "imm-eval-q")
    cookies = await register_student(async_client, "immediate_eval@example.com")

    code = "import sys\nprint(sys.stdin.read().strip()[::-1])"

    res = await async_client.post(
        "/api/v1/coding/submissions?evaluate=true",
        json={"question_id": str(question.id), "language": "python", "code": code},
        cookies=cookies,
    )
    assert res.status_code == 201
    data = res.json()

    assert data["status"] == "completed"
    assert data["result"] is not None
    assert data["result"]["verdict"] == "Accepted"
    assert data["result"]["score"] == 100.0


async def test_run_sample_code_interactive(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test POST /questions/{id}/run executes code against sample test cases without persisting submission."""
    question = await create_question_with_test_cases(db_session, "Run Sample Q", "run-sample-q")
    cookies = await register_student(async_client, "sample_runner@example.com")

    code = "import sys\nprint(sys.stdin.read().strip()[::-1])"

    run_res = await async_client.post(
        f"/api/v1/coding/questions/{question.id}/run",
        json={"language": "python", "code": code},
        cookies=cookies,
    )
    assert run_res.status_code == 200
    data = run_res.json()

    assert data["verdict"] == "Accepted"
    assert data["passed_test_cases"] == 2  # Only the 2 sample test cases
    assert data["total_test_cases"] == 2
    assert len(data["test_cases"]) == 2

    # Verify no persistent submission was created
    sub_count_res = await async_client.get(
        f"/api/v1/coding/questions/{question.id}/submissions",
        cookies=cookies,
    )
    assert sub_count_res.status_code == 200
    assert sub_count_res.json()["total_count"] == 0


async def test_evaluate_submission_user_isolation(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test that student B cannot trigger evaluation of student A's submission."""
    question = await create_question_with_test_cases(db_session, "Eval Isolation Q", "eval-iso-q")

    # Student A creates submission
    cookies_a = await register_student(async_client, "student_a_eval@example.com")
    sub_res = await async_client.post(
        "/api/v1/coding/submissions",
        json={"question_id": str(question.id), "language": "python", "code": "print('hello')"},
        cookies=cookies_a,
    )
    sub_id = sub_res.json()["id"]

    # Student B attempts to evaluate Student A's submission
    cookies_b = await register_student(async_client, "student_b_eval@example.com")
    eval_res = await async_client.post(
        f"/api/v1/coding/submissions/{sub_id}/evaluate",
        cookies=cookies_b,
    )
    assert eval_res.status_code == 403
    assert "You can only evaluate your own submissions" in eval_res.json()["detail"]


async def test_evaluate_submission_javascript_accepted(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test evaluating a valid JavaScript submission with Node.js."""
    question = await create_question_with_test_cases(db_session, "Reverse Str JS", "rev-js")
    cookies = await register_student(async_client, "js_coder@example.com")

    js_code = (
        "let input = '';\n"
        "process.stdin.setEncoding('utf-8');\n"
        "process.stdin.on('data', chunk => { input += chunk; });\n"
        "process.stdin.on('end', () => {\n"
        "    console.log(input.trim().split('').reverse().join(''));\n"
        "});\n"
    )

    create_res = await async_client.post(
        "/api/v1/coding/submissions",
        json={"question_id": str(question.id), "language": "javascript", "code": js_code},
        cookies=cookies,
    )
    assert create_res.status_code == 201
    sub_id = create_res.json()["id"]

    eval_res = await async_client.post(
        f"/api/v1/coding/submissions/{sub_id}/evaluate",
        cookies=cookies,
    )
    assert eval_res.status_code == 200
    data = eval_res.json()

    assert data["status"] == "completed"
    assert data["result"]["verdict"] == "Accepted"
    assert data["result"]["score"] == 100.0
    assert data["result"]["passed_test_cases"] == 3
