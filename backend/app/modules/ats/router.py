from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user

from app.db.models.user import User
from app.db.models.job_description import JobDescription

from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException, status

from app.modules.ats.schemas import (
    JobDescriptionCreate,
    JobDescriptionOut,
    JobDescriptionListOut,
    MessageResponse,
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