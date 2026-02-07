from typing import Annotated

from fastapi import APIRouter, Header, HTTPException
from sqlalchemy import select

from database import db_dep
from models import User


router = APIRouter(prefix="/lesson", tags=["Lesson"])

SECRET_TOKEN = "shamsiddin"


@router.get("/protected/")
async def protected_api(
    db: db_dep, email: str, X_chesnok_token: Annotated[str | None, Header()] = None
):
    if not X_chesnok_token:
        raise HTTPException(status_code=401, detail="No chesnok token provided.")

    if X_chesnok_token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Incorrect chesnok token.")

    stmt = select(User).where(User.email == email)
    res = db.execute(stmt)
    user = res.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user


@router.get("/protected/adminonly/")
async def protected_admin(
    db: db_dep, email: str, X_chesnok_token: Annotated[str | None, Header()] = None
):
    if not X_chesnok_token:
        raise HTTPException(status_code=401, detail="No chesnok token provided.")

    if X_chesnok_token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Incorrect chesnok token.")

    stmt = select(User).where(User.email == email)
    res = db.execute(stmt)
    user = res.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="San mani adminimmassan karochi!")

    return user


"""
password = A
secret_key = x
salt = c
hashed_password = B

Ax + random() * c = B

1. Symmetric (2 taraflama) password => B/x = A
2. Asymmetric (1 taraflama) password => B/x != A
    > Ax + random() * c == B
"""
