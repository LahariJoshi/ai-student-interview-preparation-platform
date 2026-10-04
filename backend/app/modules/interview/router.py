from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.db.models.user import User
from app.modules.interview.schemas import (
    InterviewSessionCreate,
    InterviewSessionOut,
    InterviewSessionDetailOut,
    InterviewQuestionOut,
    InterviewResponseOut,
    InterviewResponseCreateRequest,
    AnswerSubmitRequest,
    AnswerAnalysisResult,
    EvaluateAnswerRequest,
    InterviewResultOut,
    InterviewHistoryPaginationOut,
)
from app.modules.interview.services.interview_service import interview_service

router = APIRouter(
    prefix="/interview",
    tags=["Interview"],
)


@router.post(
    "/sessions",
    response_model=InterviewSessionOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new interview session",
)
async def create_session(
    data: InterviewSessionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await interview_service.create_session(
        db=db,
        user_id=current_user.id,
        data=data,
    )


@router.get(
    "/sessions",
    response_model=List[InterviewSessionOut],
    status_code=status.HTTP_200_OK,
    summary="List all interview sessions for the current user",
)
async def list_user_sessions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await interview_service.get_user_sessions(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/sessions/{session_id}",
    response_model=InterviewSessionDetailOut,
    status_code=status.HTTP_200_OK,
    summary="Get details of a specific interview session",
)
async def get_session(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await interview_service.get_session_by_id(
        db=db,
        session_id=session_id,
        user_id=current_user.id,
    )


@router.post(
    "/sessions/{session_id}/start",
    response_model=InterviewSessionOut,
    status_code=status.HTTP_200_OK,
    summary="Start an interview session",
)
async def start_session(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await interview_service.start_session(
        db=db,
        session_id=session_id,
        user_id=current_user.id,
    )


@router.post(
    "/sessions/{session_id}/complete",
    response_model=InterviewSessionOut,
    status_code=status.HTTP_200_OK,
    summary="Complete an interview session",
)
async def complete_session(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await interview_service.complete_session(
        db=db,
        session_id=session_id,
        user_id=current_user.id,
    )


@router.post(
    "/sessions/{session_id}/generate-questions",
    response_model=List[InterviewQuestionOut],
    status_code=status.HTTP_201_CREATED,
    summary="Generate AI interview questions for a session",
)
async def generate_questions(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await interview_service.generate_session_questions(
        db=db,
        session_id=session_id,
        user_id=current_user.id,
    )


@router.get(
    "/sessions/{session_id}/questions",
    response_model=List[InterviewQuestionOut],
    status_code=status.HTTP_200_OK,
    summary="Get all questions for an interview session",
)
async def get_session_questions(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    session = await interview_service.get_session_by_id(
        db=db,
        session_id=session_id,
        user_id=current_user.id,
    )
    return session.questions


@router.post(
    "/sessions/{session_id}/responses",
    response_model=InterviewResponseOut,
    summary="Submit an answer for a question in this interview session",
)
async def submit_response(
    session_id: UUID,
    payload: InterviewResponseCreateRequest,
    response: Response,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    resp_obj, is_created = await interview_service.submit_answer(
        db=db,
        session_id=session_id,
        user_id=current_user.id,
        question_id=payload.question_id,
        answer_text=payload.answer_text,
        allow_retry=payload.allow_retry,
    )
    response.status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
    return resp_obj


@router.post(
    "/sessions/{session_id}/answer",
    response_model=InterviewResponseOut,
    status_code=status.HTTP_200_OK,
    summary="Submit answer for a question in this interview session (compatibility)",
)
async def submit_answer(
    session_id: UUID,
    payload: AnswerSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    resp_obj, _ = await interview_service.submit_answer(
        db=db,
        session_id=session_id,
        user_id=current_user.id,
        question_id=payload.question_id,
        answer_text=payload.get_text(),
        allow_retry=True,
    )
    return resp_obj


@router.post(
    "/sessions/{session_id}/responses/{response_id}/evaluate",
    response_model=AnswerAnalysisResult,
    status_code=status.HTTP_200_OK,
    summary="Evaluate a recorded interview answer using AI",
)
async def evaluate_response(
    session_id: UUID,
    response_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await interview_service.evaluate_response(
        db=db,
        session_id=session_id,
        user_id=current_user.id,
        response_id=response_id,
    )


@router.post(
    "/sessions/{session_id}/evaluate-answer",
    response_model=AnswerAnalysisResult,
    status_code=status.HTTP_200_OK,
    summary="Evaluate an answer by question or response ID using AI",
)
async def evaluate_answer(
    session_id: UUID,
    payload: EvaluateAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await interview_service.evaluate_response(
        db=db,
        session_id=session_id,
        user_id=current_user.id,
        response_id=payload.response_id,
        question_id=payload.question_id,
        answer_text=payload.answer_text,
    )


@router.get(
    "/sessions/{session_id}/result",
    response_model=InterviewResultOut,
    status_code=status.HTTP_200_OK,
    summary="Get aggregated final interview result, scores, metrics, and recommendations",
)
async def get_interview_result(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await interview_service.get_interview_result(
        db=db,
        session_id=session_id,
        user_id=current_user.id,
    )


@router.get(
    "/history",
    response_model=InterviewHistoryPaginationOut,
    status_code=status.HTTP_200_OK,
    summary="Get paginated interview history for the current user",
)
async def get_interview_history(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items per page"),
    page: Optional[int] = Query(None, ge=1, description="Page number (1-indexed)"),
    page_size: Optional[int] = Query(None, ge=1, le=100, description="Items per page"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if page is not None and page_size is not None:
        effective_skip = (page - 1) * page_size
        effective_limit = page_size
    elif page_size is not None:
        effective_skip = skip
        effective_limit = page_size
    else:
        effective_skip = skip
        effective_limit = limit

    return await interview_service.get_interview_history(
        db=db,
        user_id=current_user.id,
        skip=effective_skip,
        limit=effective_limit,
    )





