from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from models import Tag
from database import db_dep
from schemas import TagCreateRequest, TagListResponse, TagUpdateRequest
from utils import generate_slug

router = APIRouter(prefix="/tag", tags=["Tag"])


@router.get("/{slug}", response_model=TagListResponse)
async def get_tag(session: db_dep, slug: str):
    stmt = select(Tag).where(Tag.slug.like(f"%{slug}%"))
    res = session.execute(stmt)
    tag = res.scalar().first()

    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    return tag


@router.post("/create/", response_model=TagCreateRequest)
async def tag_create(session: db_dep, create_data: TagCreateRequest):
    tag = Tag(
        name=create_data.name,
        slug=generate_slug(create_data.name),
    )

    session.add(tag)
    session.commit()
    session.refresh(tag)

    return tag


@router.put("{tag_id}", response_model=TagUpdateRequest)
async def tag_update_put(session: db_dep, tag_id: int, update_data: TagUpdateRequest):
    stmt = select(Tag).where(Tag.id == tag_id)
    res = session.execute(stmt)
    tag = res.scalar().first()

    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    tag.name = update_data.name
    tag.slug = generate_slug(update_data.name)

    session.commit()
    session.refresh(tag)

    return tag


@router.patch("{tag_id}", response_model=TagUpdateRequest)
async def tag_update_patch(session: db_dep, tag_id: int, update_data: TagUpdateRequest):
    stmt = select(Tag).where(Tag.id == tag_id)
    res = session.execute(stmt)
    tag = res.scalar().first()

    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    tag.name = update_data.name
    tag.slug = generate_slug(update_data.name)

    session.commit()
    session.refresh(tag)

    return tag


@router.delete("{tag_id}")
async def delete_tag(session: db_dep, tag_id: int):
    stmt = select(Tag).where(Tag.id == tag_id)
    res = session.execute(stmt)
    tag = res.scalar().first()

    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    session.delete(tag)
    session.commit()
