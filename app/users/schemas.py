from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional


class UserRegisterSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=6)
    confirm_password: str = Field(..., min_length=6)

    @field_validator("confirm_password")
    def check_password_match(cls, confirm_password, validation):
        if not (confirm_password == validation.data.get("password")):
            raise ValueError("passwords dont match")
        return confirm_password


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    id: int
    username: str = Field(..., min_length=3, max_length=150)
    email: EmailStr
    is_active: bool
    created_at: datetime = Field(..., description="Time of creation")
    updated_at: datetime = Field(..., description="Time of update")


class TokenSchema(BaseModel):
    token: str = Field(..., description="user refresh token")
