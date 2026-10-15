"""Service responsible for generating and assembling mock interview questions.

Supports:
- Role & experience level filtering
- Interview type filtering (Technical, HR, Behavioral, Mixed)
- Personalized question synthesis from student's parsed resume
- Fallback to curated dataset questions
"""

from typing import List, Dict, Any, Optional
import random

from app.modules.interview.services.provider import get_llm_provider
from datasets.interview_questions import INTERVIEW_QUESTION_DATASET


async def generate_interview_questions(
    role: str,
    interview_type: str,
    experience_level: str,
    skills: List[str],
    resume_skills: Optional[List[str]] = None,
    resume_projects: Optional[List[str]] = None,
    total_questions: int = 5,
) -> List[Dict[str, Any]]:
    """Generate or retrieve structured interview questions customized to candidate specs."""
    provider = get_llm_provider()

    # 1. Fetch base questions from provider
    base_questions = await provider.generate_questions(
        role=role,
        interview_type=interview_type,
        experience_level=experience_level,
        skills=skills,
        count=total_questions,
    )

    questions_out: List[Dict[str, Any]] = []

    # 2. If student provided resume with projects and requested mixed/technical, insert a personalized project question
    if resume_projects and len(resume_projects) > 0 and interview_type in ("technical", "mixed"):
        proj_name = resume_projects[0]
        project_q = {
            "question_text": f"In your resume, you highlighted your project '{proj_name}'. Can you walk me through the overall system architecture, your individual technical contributions, and a key engineering trade-off you solved during its implementation?",
            "category": "project_based",
            "difficulty": experience_level,
            "topic_or_skill": f"Project: {proj_name}",
            "expected_key_points": [
                "Problem statement and context of the project",
                "Technology stack selection rationale",
                "Component architecture and data flow",
                "Technical challenge faced and solution implemented",
                "Learnings or quantifiable project outcomes",
            ],
            "reference_answer": f"A comprehensive response starts with the core problem '{proj_name}' addressed, outlines the frontend/backend/database stack, describes the specific feature or pipeline the candidate built, and details how a performance, data integrity, or latency issue was resolved.",
            "evaluation_rubric": {
                "relevance_weight": 0.20,
                "technical_weight": 0.35,
                "clarity_weight": 0.25,
                "completeness_weight": 0.20,
            },
        }
        questions_out.append(project_q)

    # 3. If student has resume skills not covered yet, inject a skill-targeted question
    active_skills = list(set((skills or []) + (resume_skills or [])))
    if active_skills and len(questions_out) < total_questions and interview_type in ("technical", "mixed"):
        top_skill = active_skills[0]
        skill_q = {
            "question_text": f"You mentioned proficiency with {top_skill}. How do you ensure high performance, maintainability, and error handling when building production features with {top_skill}?",
            "category": "technical",
            "difficulty": experience_level,
            "topic_or_skill": top_skill,
            "expected_key_points": [
                f"Core best practices and design patterns in {top_skill}",
                "Structured exception handling and logging",
                "Performance optimization or memory considerations",
                "Testing and code validation strategies",
            ],
            "reference_answer": f"When developing with {top_skill}, emphasize clean modular code structure, defensive error handling with meaningful exceptions, proper resource management (e.g. connection pooling or memory cleanup), and automated unit/integration tests.",
            "evaluation_rubric": {
                "relevance_weight": 0.25,
                "technical_weight": 0.35,
                "clarity_weight": 0.20,
                "completeness_weight": 0.20,
            },
        }
        questions_out.append(skill_q)

    # 4. Fill remaining slots from base_questions without duplicates
    for bq in base_questions:
        if len(questions_out) >= total_questions:
            break
        # Avoid duplicate questions
        if not any(bq["question_text"] == q["question_text"] for q in questions_out):
            questions_out.append(bq)

    # In case we still need more, fallback to general dataset
    if len(questions_out) < total_questions:
        for ds_item in INTERVIEW_QUESTION_DATASET:
            if len(questions_out) >= total_questions:
                break
            if not any(ds_item["question"] == q["question_text"] for q in questions_out):
                questions_out.append({
                    "question_text": ds_item["question"],
                    "category": ds_item["category"],
                    "difficulty": ds_item["difficulty"],
                    "topic_or_skill": ds_item.get("topic", role),
                    "expected_key_points": ds_item["expected_key_points"],
                    "reference_answer": ds_item["reference_answer"],
                    "evaluation_rubric": ds_item["rubric"],
                })

    return questions_out[:total_questions]
