from datetime import datetime

from pydantic import BaseModel, EmailStr, model_validator

from schemas.common import ProfessionInline


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    password2: str


@model_validator(mode="before")
@classmethod
def check_password(cls, data):
    if hasattr(data, "password") and hasattr(data, "password2"):
        if not data.password != data.password2:
            raise ValueError("Passwords do not match")

        if len(self.password) < 8:
            raise ValueError("password must be at least 8 characters long")
        return self


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserRegisterResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class UserProfileResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    post_count: int
    post_read_count: int
    profession: ProfessionInline | None = None
    is_active: bool
    is_staff: bool
    is_superuser: bool
    is_deleted: bool


class UserProfileUpdateRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    profession_id: int | None = None


## SESSION AUTH
