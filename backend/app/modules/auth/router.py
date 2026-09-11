from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, get_current_user
from app.db.models.user import User
from app.db.models.profile import Profile
from app.modules.auth.schemas import UserRegister, UserLogin, UserOut, MessageResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


def set_auth_cookie(response: Response, token: str):
    response.set_cookie(
        key=settings.COOKIE_NAME,
        value=token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite=settings.COOKIE_SAMESITE,
        secure=settings.COOKIE_SECURE,
        domain=settings.COOKIE_DOMAIN,
    )


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_student(
    payload: UserRegister,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    # Check if email exists
    existing = await db.execute(select(User).where(User.email == payload.email.lower()))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists."
        )

    # Create User
    new_user = User(
        email=payload.email.lower(),
        password_hash=hash_password(payload.password),
        full_name=payload.full_name,
        role="student",
    )
    db.add(new_user)
    await db.flush()  # populate new_user.id

    # Create associated default Profile
    new_profile = Profile(
        user_id=new_user.id,
        target_role=None,
        experience_level=None,
        target_companies=[],
        tech_skills=[],
    )
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_user)

    # Issue JWT token inside HTTP-only cookie
    token = create_access_token(user_id=str(new_user.id))
    set_auth_cookie(response, token)

    return new_user


@router.post("/login", response_model=UserOut)
async def login_student(
    payload: UserLogin,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.email == payload.email.lower()))
    user = result.scalar_one_or_none()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    # Issue JWT token inside HTTP-only cookie
    token = create_access_token(user_id=str(user.id))
    set_auth_cookie(response, token)

    return user


@router.post("/logout", response_model=MessageResponse)
async def logout_student(response: Response):
    response.delete_cookie(
        key=settings.COOKIE_NAME,
        samesite=settings.COOKIE_SAMESITE,
        secure=settings.COOKIE_SECURE,
        domain=settings.COOKIE_DOMAIN,
    )
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserOut)
async def get_current_student(current_user: User = Depends(get_current_user)):
    return current_user
