import hashlib
import secrets
import time
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.email import is_email_configured, send_password_reset_email
from app.core.security import create_access_token, get_current_user, hash_password, verify_password
from app.db.models.password_reset import PasswordResetToken
from app.db.models.profile import Profile
from app.db.models.user import User
from app.modules.auth.schemas import (
    ChangePasswordRequest,
    DevResetPasswordRequest,
    ForgotPasswordRequest,
    MessageResponse,
    RecoveryStatusResponse,
    ResetPasswordRequest,
    UserLogin,
    UserOut,
    UserRegister,
    VerifyResetTokenResponse,
)

router = APIRouter(prefix="/auth", tags=["Auth"])

# In-memory rate limiting tracker: IP/key -> list of request timestamps
_rate_limit_records: Dict[str, List[float]] = defaultdict(list)
RATE_LIMIT_WINDOW_SECONDS = 900  # 15 minutes
MAX_REQUESTS_PER_WINDOW = 5


def check_rate_limit(key: str) -> None:
    """
    Enforce rate limits on sensitive authentication recovery actions.
    Limits requests to MAX_REQUESTS_PER_WINDOW within RATE_LIMIT_WINDOW_SECONDS.
    """
    now = time.time()
    # Prune old timestamps
    recent = [t for t in _rate_limit_records[key] if now - t < RATE_LIMIT_WINDOW_SECONDS]
    _rate_limit_records[key] = recent

    if len(recent) >= MAX_REQUESTS_PER_WINDOW:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many password reset requests. Please wait a few minutes before trying again.",
        )
    _rate_limit_records[key].append(now)


def is_token_expired(expires_at: datetime) -> bool:
    """
    Safely compare token expiration across SQLite (naive) and PostgreSQL (tz-aware).
    """
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    return expires_at < datetime.now(timezone.utc)


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


@router.get("/recovery-status", response_model=RecoveryStatusResponse)
async def get_recovery_status():
    """
    Check the current server recovery capabilities (SMTP configured vs Dev Recovery).
    Used by the frontend to dynamically display the appropriate recovery option.
    """
    return {
        "smtp_configured": is_email_configured(),
        "environment": settings.ENVIRONMENT,
        "dev_recovery_available": settings.is_development(),
    }


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_student(
    payload: UserRegister,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    # Check if email exists
    existing = await db.execute(select(User).where(User.email == payload.email.lower()))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists.",
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
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.email == payload.email.lower()))
    user = result.scalar_one_or_none()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
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


@router.post("/change-password", response_model=MessageResponse)
async def change_student_password(
    payload: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Authenticated account-management flow to change the user's password.
    Requires verifying the existing password before updating.
    """
    if not verify_password(payload.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password. Please verify and try again.",
        )

    current_user.password_hash = hash_password(payload.new_password)

    # Invalidate any pending password reset tokens for this user
    await db.execute(
        update(PasswordResetToken)
        .where(PasswordResetToken.user_id == current_user.id)
        .values(used=True)
    )

    await db.commit()

    return {"message": "Your password has been changed successfully."}


@router.post("/forgot-password", response_model=MessageResponse)
async def request_password_reset(
    payload: ForgotPasswordRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Initiate the email-based password recovery process (Production & SMTP Mode).
    Generates a secure, time-limited, single-use reset token and emails it to the user.
    Generic response is returned to avoid email enumeration.
    """
    client_ip = request.client.host if request.client else "unknown"
    rate_limit_key = f"{client_ip}:{payload.email.lower()}"
    check_rate_limit(rate_limit_key)

    # Do not simulate success if email delivery is not configured
    if not is_email_configured():
        if settings.is_development():
            detail_msg = (
                "Email delivery (SMTP) is not configured on this server. "
                "In local development, please use the Local Development Recovery option with identity verification."
            )
        else:
            detail_msg = (
                "Email delivery service is not configured on the server. "
                "Please configure SMTP credentials (SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD) in .env to enable password recovery."
            )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail_msg,
        )

    # Check if user exists
    user_query = await db.execute(select(User).where(User.email == payload.email.lower()))
    user = user_query.scalar_one_or_none()

    if user:
        # Invalidate any existing active tokens for this user
        await db.execute(
            update(PasswordResetToken)
            .where(PasswordResetToken.user_id == user.id, PasswordResetToken.used == False)  # noqa: E712
            .values(used=True)
        )

        # Generate single-use unguessable token
        raw_token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=settings.RESET_TOKEN_EXPIRE_MINUTES
        )

        reset_token_record = PasswordResetToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at,
            used=False,
        )
        db.add(reset_token_record)
        await db.commit()

        # Build reset link pointing to the frontend reset password page
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={raw_token}"

        # Dispatch reset email
        await send_password_reset_email(
            to_email=user.email,
            recipient_name=user.full_name,
            reset_link=reset_link,
            expires_in_minutes=settings.RESET_TOKEN_EXPIRE_MINUTES,
        )

    # Uniform response to prevent account enumeration
    return {
        "message": "If an account is associated with this email address, a password reset link has been sent to your inbox."
    }


@router.post("/dev-reset-password", response_model=MessageResponse)
async def dev_reset_password(
    payload: DevResetPasswordRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Safe local-development recovery mechanism that works without SMTP.
    Requires identity verification (account holder's registered full name)
    AND the server's development recovery authorization key.
    Strictly forbidden in production environments.
    """
    if not settings.is_development():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Development password recovery is strictly forbidden in non-development environments.",
        )

    client_ip = request.client.host if request.client else "unknown"
    check_rate_limit(f"dev_reset:{client_ip}:{payload.email.lower()}")

    # Verify development recovery key
    if not payload.dev_recovery_key or payload.dev_recovery_key.strip() != settings.DEV_RECOVERY_KEY.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid development recovery authorization key. Please check DEV_RECOVERY_KEY in your server configuration.",
        )

    # Look up user by email
    user_query = await db.execute(select(User).where(User.email == payload.email.lower()))
    user = user_query.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No registered student account found with the provided email address.",
        )

    # Enforce identity verification: full name must match registered account holder
    if user.full_name.strip().lower() != payload.full_name.strip().lower():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identity verification failed: The provided full name does not match the registered account details.",
        )

    # Securely hash and update user password
    user.password_hash = hash_password(payload.new_password)

    # Invalidate all pending tokens for this user
    await db.execute(
        update(PasswordResetToken)
        .where(PasswordResetToken.user_id == user.id)
        .values(used=True)
    )

    await db.commit()

    return {
        "message": "Password successfully updated via development recovery. You can now log in with your new password."
    }


@router.get("/verify-reset-token", response_model=VerifyResetTokenResponse)
async def verify_reset_token(
    token: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Validate whether a password reset token is active, unexpired, and unused.
    Used by frontend reset page before displaying the new password input form.
    """
    if not token or len(token) < 16:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password reset token format.",
        )

    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    query = await db.execute(
        select(PasswordResetToken).where(PasswordResetToken.token_hash == token_hash)
    )
    token_record = query.scalar_one_or_none()

    if not token_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password reset token is invalid or does not exist.",
        )

    if token_record.used:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This password reset token has already been used.",
        )

    if is_token_expired(token_record.expires_at):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This password reset token has expired. Please request a new link.",
        )

    return {"valid": True, "message": "Token is valid"}


@router.post("/reset-password", response_model=MessageResponse)
async def complete_password_reset(
    payload: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Reset user password using a verified single-use token.
    Securely hashes the new password, updates the database, and marks the token used.
    """
    token_hash = hashlib.sha256(payload.token.encode("utf-8")).hexdigest()
    query = await db.execute(
        select(PasswordResetToken).where(PasswordResetToken.token_hash == token_hash)
    )
    token_record = query.scalar_one_or_none()

    if not token_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or unrecognized password reset token.",
        )

    if token_record.used:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This password reset token has already been used. Please request a new reset link.",
        )

    if is_token_expired(token_record.expires_at):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This password reset token has expired. Please request a new reset link.",
        )

    # Fetch User
    user_query = await db.execute(select(User).where(User.id == token_record.user_id))
    user = user_query.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user account associated with this token was not found.",
        )

    # Securely hash and update user password
    user.password_hash = hash_password(payload.new_password)

    # Mark this token and any other pending tokens for this user as used
    token_record.used = True
    await db.execute(
        update(PasswordResetToken)
        .where(PasswordResetToken.user_id == user.id)
        .values(used=True)
    )

    await db.commit()

    return {
        "message": "Password successfully reset. You can now sign in with your new password."
    }
