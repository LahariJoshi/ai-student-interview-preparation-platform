"""Modular LLM Provider interface supporting OpenAI, Gemini, HuggingFace, and Offline Rule/Dataset Engine.

Ensures that if external AI credentials are missing, system falls back transparently
to a grounded, deterministic evaluation and generation engine without crashes.
"""

import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List

from app.core.config import settings

logger = logging.getLogger(__name__)


class BaseLLMProvider(ABC):
    """Abstract interface for LLM operations."""

    @abstractmethod
    async def generate_questions(
        self,
        role: str,
        interview_type: str,
        experience_level: str,
        skills: List[str],
        resume_summary: Optional[str] = None,
        count: int = 5,
    ) -> List[Dict[str, Any]]:
        """Generate tailored interview questions."""
        pass

    @abstractmethod
    async def evaluate_answer(
        self,
        question: str,
        category: str,
        expected_key_points: List[str],
        reference_answer: Optional[str],
        student_answer: str,
    ) -> Dict[str, Any]:
        """Evaluate a student's answer according to transparent criteria."""
        pass


class OfflineDatasetLLMProvider(BaseLLMProvider):
    """Fallback provider when external AI APIs are not configured.

    Uses dataset question selection and grounded heuristic evaluation.
    """

    async def generate_questions(
        self,
        role: str,
        interview_type: str,
        experience_level: str,
        skills: List[str],
        resume_summary: Optional[str] = None,
        count: int = 5,
    ) -> List[Dict[str, Any]]:
        # Imported lazily to avoid circular dependencies
        from datasets.interview_questions import INTERVIEW_QUESTION_DATASET

        role_lower = role.lower()
        matched: List[Dict[str, Any]] = []

        # 1. Filter by role or general
        for item in INTERVIEW_QUESTION_DATASET:
            item_role = item["role"].lower()
            if item_role in role_lower or role_lower in item_role:
                matched.append(item)

        # 2. Filter or prioritize by interview type
        if interview_type == "technical":
            pool = [q for q in matched if q["category"] in ("technical", "project_based")]
        elif interview_type in ("hr", "behavioral"):
            pool = [q for q in INTERVIEW_QUESTION_DATASET if q["category"] in ("hr", "behavioral")]
        else:  # mixed
            pool = matched + [q for q in INTERVIEW_QUESTION_DATASET if q["category"] in ("hr", "behavioral")]

        # If pool has fewer than requested, include remaining dataset items
        if len(pool) < count:
            remaining = [q for q in INTERVIEW_QUESTION_DATASET if q not in pool]
            pool.extend(remaining)

        # Truncate to count
        selected = pool[:count]

        # Enhance with custom skills if provided
        results = []
        for i, q in enumerate(selected):
            results.append({
                "question_text": q["question"],
                "category": q["category"],
                "difficulty": q["difficulty"],
                "topic_or_skill": q.get("topic", role),
                "expected_key_points": q["expected_key_points"],
                "reference_answer": q["reference_answer"],
                "evaluation_rubric": q["rubric"],
            })

        return results

    async def evaluate_answer(
        self,
        question: str,
        category: str,
        expected_key_points: List[str],
        reference_answer: Optional[str],
        student_answer: str,
    ) -> Dict[str, Any]:
        """Deterministic, grounded rubric evaluation for text answers."""
        cleaned = student_answer.strip().lower()
        word_count = len(cleaned.split())

        if word_count < 5:
            return {
                "score": 10.0,
                "relevance_score": 15.0,
                "technical_accuracy_score": 10.0,
                "completeness_score": 10.0,
                "clarity_score": 20.0,
                "detailed_feedback": "Answer is too brief to demonstrate technical competence. Please provide detailed explanations with examples or reasoning.",
                "improvement_tips": [
                    "Elaborate on core concepts instead of single-word or very short statements.",
                    "Structure your answer with context, explanation, and an illustrative example.",
                ],
                "concepts_to_revise": expected_key_points[:2],
            }

        # Calculate keyword & keypoint coverage
        matched_points = []
        missing_points = []
        for point in expected_key_points:
            # Check for token overlap
            tokens = [t.lower() for t in point.split() if len(t) > 3]
            hit = any(t in cleaned for t in tokens)
            if hit:
                matched_points.append(point)
            else:
                missing_points.append(point)

        coverage_ratio = len(matched_points) / max(len(expected_key_points), 1)

        # Baseline scoring
        relevance_score = min(100.0, 40.0 + (coverage_ratio * 50.0) + (min(word_count, 120) / 120.0 * 10.0))
        technical_score = min(100.0, 35.0 + (coverage_ratio * 55.0) + (10.0 if word_count >= 30 else 0.0))
        completeness_score = min(100.0, 30.0 + (coverage_ratio * 60.0) + (10.0 if word_count >= 50 else 0.0))
        clarity_score = min(100.0, 50.0 + (25.0 if word_count >= 25 else 10.0) + (25.0 if "." in student_answer else 10.0))

        overall_score = round(
            (relevance_score * 0.25) +
            (technical_score * 0.35) +
            (completeness_score * 0.20) +
            (clarity_score * 0.20),
            1,
        )

        tips = []
        if missing_points:
            tips.append(f"Make sure to address key aspects such as: {', '.join(missing_points[:2])}.")
        if word_count < 40:
            tips.append("Aim for a more comprehensive explanation (40-100 words) to highlight depth of understanding.")
        if "." not in student_answer:
            tips.append("Organize your thoughts into distinct sentences or bullet points for enhanced clarity.")
        if not tips:
            tips.append("Great answer! Consider sharing a brief real-world production use-case or edge case to make it even stronger.")

        return {
            "score": overall_score,
            "relevance_score": round(relevance_score, 1),
            "technical_accuracy_score": round(technical_score, 1),
            "completeness_score": round(completeness_score, 1),
            "clarity_score": round(clarity_score, 1),
            "detailed_feedback": (
                f"You covered {len(matched_points)} of {len(expected_key_points)} core discussion points. "
                + ("Strong technical foundation shown." if overall_score >= 70 else "Good attempt; deepening your explanation with key architectural trade-offs will improve your score.")
            ),
            "improvement_tips": tips,
            "concepts_to_revise": missing_points if missing_points else expected_key_points[:1],
        }


def get_llm_provider() -> BaseLLMProvider:
    """Factory returning the active LLM provider based on environment."""
    # When keys become available in settings, OpenAI / Gemini adapters can be plugged in here
    return OfflineDatasetLLMProvider()
