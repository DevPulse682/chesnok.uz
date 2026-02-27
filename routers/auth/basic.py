from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import select
from dependencies.dependencies import current_user_basic_dep

from database import db_dep
from models import User
from schemas.auth import UserLoginRequest, UserProfileResponse, UserProfileUpdateRequest
from utils import verify_password

basic = HTTPBasic()

router = APIRouter(prefix="/basic", tags=["Auth"])


@router.post("/login/")
async def login_user(
    db: db_dep,
    data: UserLoginRequest,
    credentials: Annotated[HTTPBasicCredentials, Depends(basic)],
):
    stmt = select(User).where(User.email == data.email)
    user = (db.execute(stmt)).scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return user


@router.put("/profile/", response_model=UserProfileResponse)
async def user_profile_update(
    db: db_dep,
    current_user: current_user_basic_dep,
    update_date: UserProfileUpdateRequest,
):
    for attr, value in update_date.model_dump(exclude_unset=True).items():
        setattr(current_user, attr, value)

    db.commit()
    db.refresh(current_user)
    return current_user


@router.delete("/profile/", status_code=204)
async def profile_delete(db: db_dep, current_user: current_user_basic_dep):
    current_user.is_active = False
    current_user.is_deleted = True
    current_user.deleted_email = current_user.email
    current_user.email = None

    db.commit()
