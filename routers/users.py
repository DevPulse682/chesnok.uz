from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from database import db_dep
from models import User
from schemas import UserCreateRequest, UserResponse


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/profile/", response_model=UserResponse)
async def get_profile(db: db_dep, email: str):
    stmt = select(User).where(User.email == email)
    res = db.execute(stmt)
    user = res.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User Not found")

    return user


@router.post("/create/", response_model=UserResponse)
async def users_create(db: db_dep, user_data: UserCreateRequest):
    new_user = User(email=user_data.email, password_hash=user_data.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
