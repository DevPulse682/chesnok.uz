from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from database import db_dep
from models import User
from schemas import (
    UserRegisterRequest,
    UserRegisterResponse,
)
from utils import hash_password

router = APIRouter(prefix="/register", tags=["Auth"])


@router.post("/", response_model=UserRegisterResponse)
async def register_user(db: db_dep, data: UserRegisterRequest):
    stmt = select(User).where(User.email == data.email)
    res = (db.execute(stmt)).scalars().first()

    if res:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(email=data.email, password_hash=hash_password(data.password))

    stmt = select(User)
    existing_user = db.execute(stmt).scalars().first()

    if not existing_user:
        user.is_staff = True
        user.is_superuser = True

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
