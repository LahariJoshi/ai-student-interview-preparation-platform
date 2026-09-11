from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.db.models.user import User
from app.db.models.profile import Profile
from app.modules.profile.schemas import ProfileOut, ProfileUpdate

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("", response_model=ProfileOut)
async def get_student_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Profile).where(Profile.user_id == current_user.id))
    profile = result.scalar_one_or_none()

    if not profile:
        # Create default profile if missing
        profile = Profile(user_id=current_user.id)
        db.add(profile)
        await db.commit()
        await db.refresh(profile)

    return profile


@router.put("", response_model=ProfileOut)
async def update_student_profile(
    payload: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Profile).where(Profile.user_id == current_user.id))
    profile = result.scalar_one_or_none()

    if not profile:
        profile = Profile(user_id=current_user.id)
        db.add(profile)

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)

    await db.commit()
    await db.refresh(profile)
    return profile
