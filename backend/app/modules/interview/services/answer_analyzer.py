import json
import logging
import re
from typing import List, Optional
from pydantic import ValidationError

from app.modules.interview.schemas import AnswerAnalysisResult
from app.modules.interview.services.llm_client import (
    BaseLLMClient,
    get_llm_client,
    LLMClientError,
    LLMTimeoutError,
    LLMResponseError,
)

logger = logging.getLogger(__name__)


class AnswerAnalyzerService:
    """
    AI-powered answer evaluation service.
    Analyzes student interview answers for relevance, technical correctness,
    completeness, clarity, and structure.
    """

    def __init__(self, llm_client: Optional[BaseLLMClient] = None):
        self._llm_client = llm_client

    @property
    def llm_client(self) -> BaseLLMClient:
        return self._llm_client or get_llm_client()

    def build_system_prompt(self) -> str:
        return (
            "You are a principal technical interviewer and senior engineering hiring manager. "
            "Your objective is to evaluate a candidate's answer to an interview question with rigor, objectivity, "
            "and constructive pedagogical feedback.\n\n"
            "Analyze the answer across these 5 key dimensions:\n"
            "1. Relevance: Did the candidate directly and appropriately answer the question asked?\n"
            "2. Technical Correctness: Are the explanations, mechanisms, algorithms, and concepts accurate?\n"
            "3. Completeness: Did the candidate cover the critical concepts, edge cases, and expected points?\n"
            "4. Clarity: Was the articulation concise, coherent, and free of unnecessary rambling?\n"
            "5. Structure: Was the response structured logically (e.g., core concept -> implementation -> trade-offs / STAR method)?\n\n"
            "You MUST respond ONLY with a valid JSON object matching this schema:\n"
            "{\n"
            '  "score": <float 0-100 overall score>,\n'
            '  "technical_score": <float 0-100 correctness score>,\n'
            '  "relevance_score": <float 0-100 relevance score>,\n'
            '  "clarity_score": <float 0-100 clarity and structure score>,\n'
            '  "strengths": ["<specific strength point>", ...],\n'
            '  "weaknesses": ["<specific weakness or omission>", ...],\n'
            '  "feedback": ["<constructive evaluation summary>", ...],\n'
            '  "improvements": ["<actionable recommendation for next time>", ...]\n'
            "}\n\n"
            "Strict requirements:\n"
            "- All numeric scores must be between 0 and 100.\n"
            "- Return ONLY raw JSON without markdown code fences or conversational text."
        )

    def build_user_prompt(
        self,
        question_text: str,
        answer_text: str,
        category: Optional[str] = None,
        topic: Optional[str] = None,
        expected_points: Optional[List[str]] = None,
        difficulty: Optional[str] = None,
        target_role: Optional[str] = None,
    ) -> str:
        prompt_parts = [
            f"Candidate Target Role: {target_role or 'Software Engineer'}",
            f"Question Category: {category or 'Technical'}",
        ]
        if topic:
            prompt_parts.append(f"Topic / Skill Area: {topic}")
        if difficulty:
            prompt_parts.append(f"Question Difficulty: {difficulty}")

        prompt_parts.append(f"\nInterview Question:\n\"{question_text}\"")

        if expected_points and len(expected_points) > 0:
            points_formatted = "\n".join(f"- {pt}" for pt in expected_points)
            prompt_parts.append(f"\nExpected Key Points / Concepts:\n{points_formatted}")

        prompt_parts.append(f"\nCandidate's Submitted Answer:\n\"{answer_text}\"")
        prompt_parts.append(
            "\nPlease evaluate this candidate's answer across relevance, technical correctness, "
            "completeness, clarity, and structure, and return the structured JSON evaluation."
        )

        return "\n".join(prompt_parts)

    def _clean_json_string(self, raw: str) -> str:
        """Strip markdown fences, leading/trailing notes, and isolate the outer JSON object."""
        cleaned = raw.strip()
        # Remove markdown code blocks if present
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
            cleaned = re.sub(r"\s*```$", "", cleaned)
            cleaned = cleaned.strip()

        # If there are surrounding characters, slice between the first '{' and last '}'
        start_idx = cleaned.find("{")
        end_idx = cleaned.rfind("}")
        if start_idx != -1 and end_idx != -1 and end_idx >= start_idx:
            cleaned = cleaned[start_idx : end_idx + 1]

        return cleaned

    async def analyze_answer(
        self,
        question_text: str,
        answer_text: str,
        category: Optional[str] = "Technical",
        topic: Optional[str] = None,
        expected_points: Optional[List[str]] = None,
        difficulty: Optional[str] = "Medium",
        target_role: Optional[str] = None,
    ) -> AnswerAnalysisResult:
        """
        Submits candidate answer to the LLM for multi-dimensional evaluation.
        Validates and parses output into an AnswerAnalysisResult.
        """
        if not question_text or not question_text.strip():
            raise ValueError("Question text cannot be empty for answer analysis.")

        if not answer_text or not answer_text.strip():
            raise ValueError("Answer text cannot be empty for answer analysis.")

        system_prompt = self.build_system_prompt()
        user_prompt = self.build_user_prompt(
            question_text=question_text.strip(),
            answer_text=answer_text.strip(),
            category=category,
            topic=topic,
            expected_points=expected_points or [],
            difficulty=difficulty,
            target_role=target_role,
        )

        try:
            logger.info("Calling LLM provider for answer evaluation...")
            raw_response = await self.llm_client.generate(
                prompt=user_prompt,
                system_prompt=system_prompt,
            )
        except LLMTimeoutError as exc:
            logger.error(f"Answer analysis timed out: {exc}")
            raise
        except LLMClientError as exc:
            logger.error(f"Answer analysis provider error: {exc}")
            raise
        except Exception as exc:
            logger.error(f"Unexpected error calling LLM provider: {exc}")
            raise LLMClientError(f"Failed to communicate with LLM: {str(exc)}") from exc

        if not raw_response or not raw_response.strip():
            raise ValueError("LLM returned an empty response for answer analysis.")

        cleaned_json = self._clean_json_string(raw_response)

        try:
            parsed_data = json.loads(cleaned_json)
        except json.JSONDecodeError as exc:
            logger.error(f"Failed to decode LLM JSON: {exc}. Raw snippet: {raw_response[:200]}")
            raise ValueError(f"LLM returned invalid JSON: {str(exc)}") from exc

        if not isinstance(parsed_data, dict):
            raise ValueError(f"Expected JSON object from LLM, received {type(parsed_data).__name__}")

        try:
            result = AnswerAnalysisResult(**parsed_data)
            return result
        except ValidationError as exc:
            logger.error(f"Pydantic validation failed for answer analysis: {exc}")
            raise ValueError(f"LLM response failed schema validation: {str(exc)}") from exc


answer_analyzer = AnswerAnalyzerService()
