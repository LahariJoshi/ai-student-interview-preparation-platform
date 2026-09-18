from uuid import UUID
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user

from app.db.models.user import User
from app.db.models.job_description import JobDescription
from app.db.models.resume import Resume
from app.db.models.ats_analysis import ATSAnalysis

from app.modules.ats.schemas import (
    JobDescriptionCreate,
    JobDescriptionOut,
    JobDescriptionListOut,
    MessageResponse,
    SemanticAnalysisRequest,
)

from app.modules.ats.services.skill_extractor import extract_skills
from app.modules.ats.services.semantic_analyzer import (
    calculate_semantic_similarity,
)
from app.modules.ats.services.ats_analyzer import (
    calculate_ats_score,
)

router = APIRouter(
    prefix="/ats",
    tags=["ATS"],
)


@router.post(
    "/job-descriptions",
    response_model=JobDescriptionOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_job_description(
    data: JobDescriptionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    job_description = JobDescription(
        user_id=current_user.id,
        title=data.title,
        company_name=data.company_name,
        description_text=data.description_text,
    )

    db.add(job_description)

    await db.commit()
    await db.refresh(job_description)

    return job_description

@router.get(
    "/job-descriptions",
    response_model=JobDescriptionListOut,
)
async def get_my_job_descriptions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(JobDescription)
        .where(JobDescription.user_id == current_user.id)
        .order_by(JobDescription.created_at.desc())
    )

    job_descriptions = result.scalars().all()

    return {
        "job_descriptions": job_descriptions,
        "total_count": len(job_descriptions),
    }

@router.get(
    "/job-descriptions/{job_description_id}",
    response_model=JobDescriptionOut,
)
async def get_job_description(
    job_description_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(JobDescription).where(
            JobDescription.id == job_description_id,
            JobDescription.user_id == current_user.id,
        )
    )

    job_description = result.scalar_one_or_none()

    if not job_description:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found or access unauthorized.",
        )

    return job_description

@router.delete(
    "/job-descriptions/{job_description_id}",
    response_model=MessageResponse,
)
async def delete_job_description(
    job_description_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(JobDescription).where(
            JobDescription.id == job_description_id,
            JobDescription.user_id == current_user.id,
        )
    )

    job_description = result.scalar_one_or_none()

    if not job_description:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found or access unauthorized.",
        )

    await db.delete(job_description)
    await db.commit()

    return {
        "message": "Job description deleted successfully."
    }

@router.get(
    "/job-descriptions/{job_description_id}/skills"
)
async def extract_job_description_skills(
    job_description_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(JobDescription).where(
            JobDescription.id == job_description_id,
            JobDescription.user_id == current_user.id,
        )
    )

    job_description = result.scalar_one_or_none()

    if not job_description:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found or access unauthorized.",
        )

    skills = extract_skills(job_description.description_text)

    return {
        "job_description_id": job_description.id,
        "skills": skills,
    }

@router.post("/semantic-analysis")
async def analyze_semantic_similarity(
    request: SemanticAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Get the selected resume
    resume_result = await db.execute(
        select(Resume).where(
            Resume.id == request.resume_id,
            Resume.user_id == current_user.id,
        )
    )

    resume = resume_result.scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found or access unauthorized.",
        )

    # Make sure resume text is available
    if not resume.raw_text:
        raise HTTPException(
            status_code=400,
            detail="Resume text has not been extracted yet.",
        )

    # Get the selected job description
    jd_result = await db.execute(
        select(JobDescription).where(
            JobDescription.id == request.job_description_id,
            JobDescription.user_id == current_user.id,
        )
    )

    job_description = jd_result.scalar_one_or_none()

    if not job_description:
        raise HTTPException(
            status_code=404,
            detail="Job description not found or access unauthorized.",
        )

    # Calculate semantic similarity
    result = calculate_semantic_similarity(
        resume_text=resume.raw_text,
        job_description=job_description.description_text,
    )

    return {
        "resume_id": resume.id,
        "job_description_id": job_description.id,
        "cosine_similarity": result["cosine_similarity"],
        "semantic_score": result["semantic_score"],
    }

@router.post("/analyze")
async def analyze_ats(
    request: SemanticAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # 1. Get the selected resume
    resume_result = await db.execute(
        select(Resume).where(
            Resume.id == request.resume_id,
            Resume.user_id == current_user.id,
        )
    )

    resume = resume_result.scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found or access unauthorized.",
        )

    # 2. Make sure resume text exists
    if (
        resume.extraction_status != "completed"
        or not resume.raw_text
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Resume text has not been extracted yet. "
                "Please extract the resume text first."
            ),
        )

    # 3. Get the selected job description
    jd_result = await db.execute(
        select(JobDescription).where(
            JobDescription.id == request.job_description_id,
            JobDescription.user_id == current_user.id,
        )
    )

    job_description = jd_result.scalar_one_or_none()

    if not job_description:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found or access unauthorized.",
        )

    # 4. Run complete ATS analysis
    try:
        result = calculate_ats_score(
            resume_text=resume.raw_text,
            job_description=job_description.description_text,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    # 5. Save ATS analysis
    analysis = ATSAnalysis(
        user_id=current_user.id,
        resume_id=resume.id,
        job_description_id=job_description.id,
        analysis_status="completed",

        ats_score=result["ats_score"],

        formatting_score=result[
            "component_scores"
        ]["formatting_score"],

        keyword_match_score=result[
            "component_scores"
        ]["keyword_match_score"],

        semantic_similarity_score=result[
            "component_scores"
        ]["semantic_score"],

        action_impact_score=result[
            "component_scores"
        ]["action_impact_score"],

        matched_skills_json=result[
            "matched_skills"
        ],

        missing_skills_json=result[
            "missing_skills"
        ],

        jd_requirements_json={
            "skills": result["jd_skills"],
        },

        analysis_details_json=result,

        analyzed_at=datetime.now(timezone.utc),
    )

    db.add(analysis)

    await db.commit()
    await db.refresh(analysis)

    # 6. Return ATS result
    return {
        "analysis_id": analysis.id,
        "resume_id": resume.id,         
        "job_description_id": job_description.id,
        "analysis_status": analysis.analysis_status,

        "ats_score": analysis.ats_score,

        "formatting_score": analysis.formatting_score,
        "keyword_match_score": analysis.keyword_match_score,
        "semantic_similarity_score": (
            analysis.semantic_similarity_score
        ),
        "action_impact_score": analysis.action_impact_score,

        "matched_skills": analysis.matched_skills_json,
        "missing_skills": analysis.missing_skills_json,
        "jd_requirements": analysis.jd_requirements_json,

        "analyzed_at": analysis.analyzed_at,
    }