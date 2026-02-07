from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from database import db_dep
from models import Profession
from schemas import (
    ProfessionCreateRequest,
    ProfessionListResponse,
    ProfessionUpdateRequest,
)

router = APIRouter(prefix="/profession", tags=["Profession"])


@router.post("/create/", response_model=ProfessionListResponse)
async def create_profession(session: db_dep, create_data: ProfessionCreateRequest):
    profession = Profession(name=create_data.name)
    session.add(profession)
    session.commit()
    session.refresh(profession)
    return profession


@router.get("/list/", response_model=list[ProfessionListResponse])
async def profession_list(session: db_dep):
    stmt = select(Profession)
    res = session.execute(stmt).scalars().all()

    return res


@router.put("/update/", response_model=ProfessionListResponse)
async def profession_update(
    session: db_dep, profession_id: int, update_data: ProfessionUpdateRequest
):
    p = session.get(Profession, profession_id)

    if not p:
        raise HTTPException(status_code=404, detail="Not found")

    p.name = update_data.name
    session.commit()
    session.refresh(p)
    return p


@router.delete("/delete/", status_code=204)
async def profession_delete(session: db_dep, profession_id: int):
    p = session.get(Profession, profession_id)

    if not p:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(p)
    session.commit()
    return
