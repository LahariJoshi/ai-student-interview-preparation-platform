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
