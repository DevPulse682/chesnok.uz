from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from database import db_dep
from models import Category
from schemas import CategoryCreateRequest, CategoryListResonse
from utils import generate_slug

router = APIRouter(prefix="/category", tags=["Category"])


@router.get("/list/", response_model=list[CategoryListResonse])
async def get_categories(session: db_dep):
    stmt = select(Category)
    res = session.execute(stmt)
    category = res.scalars().all()

    if not category:
        HTTPException(status_code=404, detail="List of tag is empty")
    return category


@router.post("/create/", response_model=CategoryListResonse)
async def tag_create(session: db_dep, data: CategoryCreateRequest):
    categorya = Category(name=data.name, slug=generate_slug(data.name))
    session.add(categorya)
    session.commit()
    session.refresh(categorya)

    return categorya


@router.put("/update/")
async def update_category(
    session: db_dep, category_id: int, update_d: CategoryCreateRequest
):
    stmt = select(Category).where(Category.id == category_id)
    res = session.execute(stmt)
    categorya = res.scalars().first()
    if categorya is None:
        HTTPException(status_code=404, detail="Not Found")

    categorya.name = update_d.name
    categorya.slug = generate_slug(update_d.name)
    session.commit()
    session.refresh(categorya)

    return categorya


@router.delete("/delete/", status_code=204)
async def delete_category(session: db_dep, id: int):
    stmt = select(Category).where(Category.id == id)
    res = session.execute(stmt)
    category = res.scalars().first()

    if not category:
        raise HTTPException(status_code=404, detail="NOT FOUND")
    session.delete(category)

    session.refresh(category)
    session.commit()
