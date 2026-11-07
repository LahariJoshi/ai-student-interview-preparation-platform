from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")
    full_name: str = Field(..., min_length=2, description="Full name of student")


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    message: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str = Field(..., min_length=16, description="Single-use password reset token")
    new_password: str = Field(..., min_length=6, description="Password must be at least 6 characters")


class VerifyResetTokenResponse(BaseModel):
    valid: bool
    message: Optional[str] = None


class RecoveryStatusResponse(BaseModel):
    smtp_configured: bool
    environment: str
    dev_recovery_available: bool


class DevResetPasswordRequest(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, description="Full name registered on the student account")
    dev_recovery_key: str = Field(..., min_length=4, description="Development recovery authorization key")
    new_password: str = Field(..., min_length=6, description="New password must be at least 6 characters")


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=1, description="Current student password")
    new_password: str = Field(..., min_length=6, description="New password must be at least 6 characters")
