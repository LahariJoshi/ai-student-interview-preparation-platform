"""Evaluation service for scoring answers and generating comprehensive interview feedback.

Applies:
- Multi-criteria transparent rubric
- Overall session score calculation
- Strengths and weaknesses aggregation
- Actionable recommendations linking to coding and resume practice
"""

from typing import List, Dict, Any, Optional
from app.modules.interview.services.provider import get_llm_provider
from app.db.models.interview import InterviewSession, InterviewQuestion, InterviewAnswer


async def evaluate_single_answer(
    question: InterviewQuestion,
    answer_text: str,
) -> Dict[str, Any]:
    """Score a single question answer using the active provider."""
    provider = get_llm_provider()

    result = await provider.evaluate_answer(
        question=question.question_text,
        category=question.category,
        expected_key_points=question.expected_key_points or [],
        reference_answer=question.reference_answer,
        student_answer=answer_text,
    )
    return result


def aggregate_session_feedback(
    session: InterviewSession,
    questions: List[InterviewQuestion],
    answers: List[InterviewAnswer],
) -> Dict[str, Any]:
    """Calculate overall scores, strengths, weaknesses, and next-step practice recommendations."""
    if not answers:
        return {
            "overall_score": 0.0,
            "technical_score": 0.0,
            "communication_score": 0.0,
            "strengths": ["Completed setup"],
            "weaknesses": ["No answers submitted"],
            "recommendations": [
                {
                    "title": "Attempt Interview Questions",
                    "description": "Start an interview and provide structured responses to receive personalized feedback.",
                    "action_type": "interview",
                    "link": "/interview",
                }
            ],
        }

    total_score = 0.0
    tech_scores = []
    comm_scores = []
    strengths: List[str] = []
    weaknesses: List[str] = []
    concepts_to_revise = set()

    for ans in answers:
        s = ans.score or 0.0
        total_score += s

        if ans.technical_accuracy_score is not None:
            tech_scores.append(ans.technical_accuracy_score)
        if ans.clarity_score is not None:
            comm_scores.append(ans.clarity_score)

        if s >= 75.0:
            strengths.append(f"Demonstrated solid grasp on question #{ans.question.order_index + 1 if ans.question else 'technical topic'}")
        elif s < 60.0:
            weaknesses.append(f"Need to elaborate on technical depth for #{ans.question.order_index + 1 if ans.question else 'topic'}")

        if ans.concepts_to_revise:
            for c in ans.concepts_to_revise:
                concepts_to_revise.add(c)

    overall_avg = round(total_score / len(answers), 1)
    tech_avg = round(sum(tech_scores) / max(len(tech_scores), 1), 1)
    comm_avg = round(sum(comm_scores) / max(len(comm_scores), 1), 1)

    if not strengths:
        strengths.append("Willingness to practice and engage in structured mock interviews under timed conditions.")
    if not weaknesses:
        weaknesses.append("Continue practicing concise delivery and introducing quantifiable real-world metrics into answers.")

    # Actionable recommendations
    recommendations = []

    # 1. Coding recommendation
    if tech_avg < 75.0:
        recommendations.append({
            "title": "Algorithmic Problem-Solving Practice",
            "description": "Strengthen technical data structures and core algorithm patterns in the Coding Assessment Sandbox.",
            "action_type": "coding",
            "link": "/coding",
        })

    # 2. Resume / ATS recommendation
    recommendations.append({
        "title": "Refine Project Details in Resume",
        "description": "Ensure your resume clearly highlights project architecture and quantifiable engineering impact to answer STAR questions with ease.",
        "action_type": "resume",
        "link": "/resume",
    })

    # 3. Topic specific recommendation
    if concepts_to_revise:
        top_concepts = list(concepts_to_revise)[:3]
        recommendations.append({
            "title": f"Revise Core Concepts: {', '.join(top_concepts)}",
            "description": "Review technical documentation and trade-offs for these frequently asked interview topics.",
            "action_type": "study",
            "link": "/coding",
        })

    return {
        "overall_score": overall_avg,
        "technical_score": tech_avg,
        "communication_score": comm_avg,
        "strengths": strengths[:4],
        "weaknesses": weaknesses[:4],
        "recommendations": recommendations,
    }
