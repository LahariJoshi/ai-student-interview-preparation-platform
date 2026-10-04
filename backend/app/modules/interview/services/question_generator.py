import json
import logging
import re
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

from app.modules.interview.services.llm_client import (
    BaseLLMClient,
    get_llm_client,
    LLMClientError,
    LLMTimeoutError,
    LLMResponseError,
)

logger = logging.getLogger(__name__)


class GeneratedQuestionSchema(BaseModel):
    question_order: int = Field(..., ge=1, description="Sequential question number")
    category: str = Field(..., description="Technical, Behavioral, HR, or Situational")
    topic: Optional[str] = Field(None, description="Topic or skill tested")
    question_text: str = Field(..., min_length=10, description="The interview question")
    difficulty: str = Field(..., description="Easy, Medium, or Hard")
    expected_points: List[str] = Field(default_factory=list, description="Key concepts expected in good answers")

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        valid = {"technical", "behavioral", "hr", "situational"}
        cleaned = v.strip().lower()
        if cleaned not in valid:
            # Map or fallback
            if "tech" in cleaned or "code" in cleaned:
                return "Technical"
            elif "behav" in cleaned:
                return "Behavioral"
            elif "hr" in cleaned:
                return "HR"
            elif "situa" in cleaned:
                return "Situational"
            return "Technical"
        # Return Title Case
        return "HR" if cleaned == "hr" else cleaned.capitalize()

    @field_validator("difficulty")
    @classmethod
    def validate_difficulty(cls, v: str) -> str:
        valid = {"easy", "medium", "hard"}
        cleaned = v.strip().lower()
        if cleaned not in valid:
            return "Medium"
        return cleaned.capitalize()


class GeneratedQuestionsResponse(BaseModel):
    questions: List[GeneratedQuestionSchema]


class QuestionGeneratorService:
    def __init__(self, llm_client: Optional[BaseLLMClient] = None):
        self._llm_client = llm_client

    @property
    def llm_client(self) -> BaseLLMClient:
        return self._llm_client or get_llm_client()

    def build_system_prompt(self) -> str:
        return (
            "You are an expert technical recruiter and senior engineering interviewer. "
            "Your task is to generate realistic, industry-standard interview questions tailored "
            "to the student's target role, experience level, and difficulty. "
            "You must return your output strictly as a JSON object adhering to this schema:\n"
            "{\n"
            '  "questions": [\n'
            "    {\n"
            '      "question_order": 1,\n'
            '      "category": "Technical" | "Behavioral" | "HR" | "Situational",\n'
            '      "topic": "string",\n'
            '      "question_text": "string",\n'
            '      "difficulty": "Easy" | "Medium" | "Hard",\n'
            '      "expected_points": ["string", "string"]\n'
            "    }\n"
            "  ]\n"
            "}\n"
            "Do not output markdown explanations outside the JSON."
        )

    def build_user_prompt(
        self,
        interview_type: str,
        target_role: str,
        experience_level: str,
        difficulty: str,
        question_count: int,
        target_company: Optional[str] = None,
    ) -> str:
        company_clause = f"Target Company: {target_company}\n" if target_company else ""
        return (
            f"Generate exactly {question_count} interview questions for the following candidate profile:\n"
            f"Target Role: {target_role}\n"
            f"{company_clause}"
            f"Interview Type: {interview_type}\n"
            f"Experience Level: {experience_level}\n"
            f"Difficulty: {difficulty}\n\n"
            f"Requirements:\n"
            f"1. Generate questions spanning the categories appropriate for '{interview_type}'. "
            f"Include Technical, Behavioral, HR, and Situational questions where relevant.\n"
            f"2. Calibrate depth according to experience level '{experience_level}' and difficulty '{difficulty}'.\n"
            f"3. Include 2-4 concise expected_points for each question summarizing what a strong answer should demonstrate.\n"
            f"4. Ensure question_order starts at 1 and increases sequentially up to {question_count}.\n"
        )

    def parse_and_validate_response(self, raw_text: str, expected_count: int) -> List[GeneratedQuestionSchema]:
        if not raw_text or not raw_text.strip():
            raise ValueError("LLM returned an empty response.")

        # Strip markdown fences if present
        text = raw_text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text)
        text = text.strip()

        try:
            parsed_json = json.loads(text)
        except json.JSONDecodeError as exc:
            logger.error(f"Malformed LLM response (invalid JSON): {text[:200]}")
            raise ValueError("Malformed LLM response: invalid JSON format.") from exc

        if not isinstance(parsed_json, dict) or "questions" not in parsed_json:
            raise ValueError("Malformed LLM response: missing 'questions' array in JSON root.")

        try:
            validated = GeneratedQuestionsResponse.model_validate(parsed_json)
        except Exception as exc:
            logger.error(f"Schema validation error on LLM response: {exc}")
            raise ValueError(f"Malformed LLM response: {str(exc)}") from exc

        if not validated.questions:
            raise ValueError("LLM response contained an empty questions list.")

        # Ensure question_order is strictly 1..N
        for idx, q in enumerate(validated.questions, start=1):
            q.question_order = idx

        return validated.questions

    async def generate_questions(
        self,
        interview_type: str,
        target_role: str,
        experience_level: str,
        difficulty: str,
        question_count: int,
        target_company: Optional[str] = None,
    ) -> List[GeneratedQuestionSchema]:
        system_prompt = self.build_system_prompt()
        user_prompt = self.build_user_prompt(
            interview_type=interview_type,
            target_role=target_role,
            experience_level=experience_level,
            difficulty=difficulty,
            question_count=question_count,
            target_company=target_company,
        )

        try:
            raw_response = await self.llm_client.generate(
                prompt=user_prompt,
                system_prompt=system_prompt,
            )
        except LLMTimeoutError as exc:
            logger.error(f"Timeout while contacting LLM provider: {exc}")
            raise
        except LLMClientError as exc:
            logger.error(f"LLM provider error: {exc}")
            raise

        return self.parse_and_validate_response(raw_response, expected_count=question_count)


question_generator = QuestionGeneratorService()
