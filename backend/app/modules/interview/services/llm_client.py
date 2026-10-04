import json
import logging
import os
import re
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List

import httpx

logger = logging.getLogger(__name__)


class LLMClientError(Exception):
    """Base exception for LLM provider errors."""
    pass


class LLMTimeoutError(LLMClientError):
    """Raised when an LLM request times out."""
    pass


class LLMResponseError(LLMClientError):
    """Raised when the LLM returns an invalid or empty response."""
    pass


class BaseLLMClient(ABC):
    """Abstract interface for LLM providers."""

    @abstractmethod
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Send prompt to LLM and return generated text."""
        pass


class OpenAILLMClient(BaseLLMClient):
    """OpenAI API implementation using HTTPX."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        timeout_seconds: float = 20.0,
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.timeout_seconds = timeout_seconds
        self.endpoint = "https://api.openai.com/v1/chat/completions"

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        if not self.api_key:
            raise LLMClientError("OPENAI_API_KEY is not configured.")

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "response_format": {"type": "json_object"},
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                response = await client.post(self.endpoint, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                if not content or not content.strip():
                    raise LLMResponseError("OpenAI returned an empty response.")
                return content
        except httpx.TimeoutException as exc:
            raise LLMTimeoutError(f"OpenAI request timed out after {self.timeout_seconds}s") from exc
        except httpx.HTTPStatusError as exc:
            raise LLMClientError(f"OpenAI API returned error: {exc.response.status_code} - {exc.response.text}") from exc
        except Exception as exc:
            if isinstance(exc, LLMClientError):
                raise
            raise LLMClientError(f"Unexpected error communicating with OpenAI: {str(exc)}") from exc


class GeminiLLMClient(BaseLLMClient):
    """Google Gemini API implementation using HTTPX."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        timeout_seconds: float = 20.0,
    ):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        self.timeout_seconds = timeout_seconds

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        if not self.api_key:
            raise LLMClientError("GEMINI_API_KEY is not configured.")

        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"

        contents = []
        full_text = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        contents.append({"parts": [{"text": full_text}]})

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.7,
                "responseMimeType": "application/json",
            },
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                response = await client.post(endpoint, json=payload)
                response.raise_for_status()
                data = response.json()
                candidates = data.get("candidates", [])
                if not candidates:
                    raise LLMResponseError("Gemini returned no candidates.")
                parts = candidates[0].get("content", {}).get("parts", [])
                if not parts or not parts[0].get("text"):
                    raise LLMResponseError("Gemini returned empty content.")
                return parts[0]["text"]
        except httpx.TimeoutException as exc:
            raise LLMTimeoutError(f"Gemini request timed out after {self.timeout_seconds}s") from exc
        except httpx.HTTPStatusError as exc:
            raise LLMClientError(f"Gemini API returned error: {exc.response.status_code} - {exc.response.text}") from exc
        except Exception as exc:
            if isinstance(exc, LLMClientError):
                raise
            raise LLMClientError(f"Unexpected error communicating with Gemini: {str(exc)}") from exc


class MockLLMClient(BaseLLMClient):
    """
    Mock LLM provider generating structured, realistic interview questions
    without external API keys or costs. Used in tests and offline dev.
    """

    def __init__(self, canned_response: Optional[str] = None):
        self.canned_response = canned_response

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        if self.canned_response is not None:
            return self.canned_response

        full_prompt = f"{system_prompt or ''} {prompt}".lower()
        if "evaluate" in full_prompt or "candidate's answer" in full_prompt or "relevance_score" in full_prompt or "technical_score" in full_prompt:
            return self._generate_mock_answer_analysis(prompt)

        # Parse context clues from the prompt to generate tailored mock questions
        return self._generate_mock_questions(prompt)

    def _generate_mock_answer_analysis(self, prompt: str) -> str:
        prompt_lower = prompt.lower()
        if "idk" in prompt_lower or "i don't know" in prompt_lower or len(prompt) < 25:
            return json.dumps({
                "score": 35.0,
                "technical_score": 30.0,
                "relevance_score": 40.0,
                "clarity_score": 45.0,
                "strengths": ["Acknowledged area for development"],
                "weaknesses": ["Answer is too brief and lacks technical depth", "Missing fundamental architectural concepts"],
                "feedback": ["Expand on the foundational principles and provide concrete examples"],
                "improvements": ["Elaborate on real-world use cases and explain trade-offs"]
            }, indent=2)

        return json.dumps({
            "score": 85.0,
            "technical_score": 88.0,
            "relevance_score": 85.0,
            "clarity_score": 82.0,
            "strengths": [
                "Accurately explained core architectural principles",
                "Demonstrated solid understanding of technical trade-offs",
                "Used clear, professional communication"
            ],
            "weaknesses": [
                "Could have touched on scaling and edge case considerations"
            ],
            "feedback": [
                "Strong response overall with clear technical terminology and logical structure.",
                "Good explanation of the primary mechanism."
            ],
            "improvements": [
                "Mention production monitoring and error recovery strategies",
                "Provide a brief code or system architecture example"
            ]
        }, indent=2)

    def _generate_mock_questions(self, prompt: str) -> str:
        prompt_lower = prompt.lower()

        # Detect role
        role = "Software Engineer"
        if "frontend" in prompt_lower:
            role = "Frontend Engineer"
        elif "backend" in prompt_lower:
            role = "Backend Engineer"
        elif "data" in prompt_lower:
            role = "Data Engineer"

        # Detect count
        count = 5
        match = re.search(r"generate\s+(?:exactly\s+)?(\d+)", prompt_lower)
        if match:
            count = int(match.group(1))
        else:
            for num in [15, 10, 5, 3, 2, 1]:
                if f"{num} questions" in prompt_lower or f"count: {num}" in prompt_lower:
                    count = num
                    break

        # Detect difficulty
        difficulty = "Medium"
        if "easy" in prompt_lower:
            difficulty = "Easy"
        elif "hard" in prompt_lower:
            difficulty = "Hard"

        questions: List[Dict[str, Any]] = []

        pool = [
            {
                "category": "Technical",
                "topic": "Core Architecture",
                "question_text": f"How do you design a high-throughput, fault-tolerant service architecture for a {role} system?",
                "expected_points": [
                    "Horizontal scaling and load balancing",
                    "Database read-replicas and caching strategy",
                    "Idempotency and circuit breaker pattern",
                ],
            },
            {
                "category": "Technical",
                "topic": "Data & Performance",
                "question_text": "Explain how database indexing works and when an index might degrade query performance.",
                "expected_points": [
                    "B-tree index structures vs hash indexes",
                    "Index maintenance overhead on writes (INSERT/UPDATE/DELETE)",
                    "Query planner selectivity and index scans",
                ],
            },
            {
                "category": "Behavioral",
                "topic": "Conflict Resolution",
                "question_text": "Describe a situation where you had a strong disagreement with a team member about technical trade-offs. How did you resolve it?",
                "expected_points": [
                    "Clear context and differing perspectives",
                    "Data-driven objective evaluation and benchmarking",
                    "Alignment on the final decision and outcome",
                ],
            },
            {
                "category": "Situational",
                "topic": "Incident Management",
                "question_text": "Suppose a critical production outage occurs right after a Friday evening deployment. What steps do you take?",
                "expected_points": [
                    "Immediate rollback and blast-radius mitigation",
                    "Stakeholder communication and incident triage",
                    "Root-cause analysis and blameless post-mortem",
                ],
            },
            {
                "category": "HR",
                "topic": "Career & Growth",
                "question_text": "Where do you see yourself technically and professionally in the next 3 to 5 years?",
                "expected_points": [
                    "Continuous learning and deepening technical domain mastery",
                    "Mentoring junior teammates and driving system design",
                    "Alignment with organizational engineering goals",
                ],
            },
            {
                "category": "Technical",
                "topic": "Concurrency & Safety",
                "question_text": "How do you detect, handle, and prevent race conditions in concurrent applications?",
                "expected_points": [
                    "Thread synchronization and mutex locks",
                    "Optimistic vs pessimistic locking mechanisms",
                    "Stateless designs and atomic operations",
                ],
            },
            {
                "category": "Behavioral",
                "topic": "Adaptability",
                "question_text": "Tell me about a time when project requirements changed drastically mid-sprint. How did you adapt?",
                "expected_points": [
                    "Agile reprioritization with product managers",
                    "Effective technical refactoring under constraints",
                    "Maintaining team delivery momentum",
                ],
            },
            {
                "category": "Situational",
                "topic": "Technical Debt",
                "question_text": "How do you balance delivering urgent business features against addressing accumulating technical debt?",
                "expected_points": [
                    "Quantifying business impact of technical debt",
                    "Allocating deliberate engineering budget per iteration",
                    "Incremental refactoring alongside new feature delivery",
                ],
            },
            {
                "category": "HR",
                "topic": "Work Values",
                "question_text": "What type of engineering work environment enables you to do your most productive work?",
                "expected_points": [
                    "Autonomy with high accountability",
                    "Open communication and constructive peer code review",
                    "Clear goals and collaborative problem solving",
                ],
            },
            {
                "category": "Technical",
                "topic": "API Design & Resilience",
                "question_text": "What principles do you follow when designing backward-compatible, resilient REST or gRPC APIs?",
                "expected_points": [
                    "Semantic versioning and additive schema evolution",
                    "Proper HTTP status codes and uniform error payloads",
                    "Rate limiting, pagination, and retry policies",
                ],
            },
            {
                "category": "Behavioral",
                "topic": "Ownership",
                "question_text": "Can you give an example of a project where you took ownership outside your defined scope to ensure success?",
                "expected_points": [
                    "Identifying an unaddressed critical gap",
                    "Taking proactive initiative without being asked",
                    "Measurable positive impact on team delivery",
                ],
            },
            {
                "category": "Situational",
                "topic": "Resource Constraints",
                "question_text": "If your team has only half the required engineering time to deliver a mission-critical release, how do you handle it?",
                "expected_points": [
                    "MVP scope pruning and ruthlessly prioritizing core value",
                    "Transparent communication with stakeholders early",
                    "Avoiding quality compromises on security and testing",
                ],
            },
            {
                "category": "HR",
                "topic": "Team Fit",
                "question_text": "How do you handle receiving critical feedback on your code or design proposals?",
                "expected_points": [
                    "Separating personal identity from code quality",
                    "Welcoming objective critique as growth opportunities",
                    "Iterating promptly based on constructive suggestions",
                ],
            },
            {
                "category": "Technical",
                "topic": "Testing Strategy",
                "question_text": "How do you structure an end-to-end automated testing strategy for a mission-critical platform?",
                "expected_points": [
                    "Unit test pyramid foundation",
                    "Contract and integration testing with mocked dependencies",
                    "Continuous integration test automation gates",
                ],
            },
            {
                "category": "Situational",
                "topic": "Security Best Practices",
                "question_text": "What steps do you take to prevent common security vulnerabilities like injection attacks and unauthorized data access?",
                "expected_points": [
                    "Parameterized queries and ORM protections",
                    "Role-based access control and token validation",
                    "Input sanitization and least-privilege security principle",
                ],
            },
        ]

        for i in range(count):
            item = pool[i % len(pool)]
            questions.append({
                "question_order": i + 1,
                "category": item["category"],
                "topic": item["topic"],
                "question_text": item["question_text"],
                "difficulty": difficulty,
                "expected_points": item["expected_points"],
            })

        return json.dumps({"questions": questions}, indent=2)


# ==========================================
# Factory & Registry
# ==========================================
_client_instance: Optional[BaseLLMClient] = None


def get_llm_client() -> BaseLLMClient:
    """
    Factory function returning the configured LLM client.
    Reads provider from LLM_PROVIDER env var ('openai', 'gemini', 'mock').
    Defaults to MockLLMClient if keys are missing or provider is 'mock'.
    """
    global _client_instance
    if _client_instance is not None:
        return _client_instance

    provider = os.getenv("LLM_PROVIDER", "mock").lower().strip()

    if provider == "openai" and os.getenv("OPENAI_API_KEY"):
        return OpenAILLMClient()
    elif provider == "gemini" and os.getenv("GEMINI_API_KEY"):
        return GeminiLLMClient()
    else:
        return MockLLMClient()


def set_llm_client(client: Optional[BaseLLMClient]) -> None:
    """Helper to override LLM client in tests."""
    global _client_instance
    _client_instance = client
