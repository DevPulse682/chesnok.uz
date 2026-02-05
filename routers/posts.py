from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from models import Post
from database import db_dep
from schemas import PostCreateRequest, PostListResponse, PostUpdateRequest
from utils import generate_slug


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[PostListResponse])
async def get_post(session: db_dep, slug: str):
    stmt = select(Post)

    if is_active is not None:
        stmt = stmt.where(Post.is_active == is_active)

    stmt = stmt.order_by(Post.created_at.desc())
    result = session.execute(stmt)
    return result.scalars().all()


@router.get("/{slug}/", response_model=list[PostListResponse])
async def get_post_single(slug: str, session: db_dep, is_active: bool = None):
    stmt = select(Post).where(Post.slug == slug)

    if is_active is not None:
        stmt = stmt.where(Post.is_active == is_active)

    stmt = stmt.order_by(Post.created_at.desc())
    res = session.execute(stmt)
    post = res.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


@router.post("/create/")
async def create_post(session: db_dep, create_data: PostCreateRequest):
    new_post = Post(
        title=create_data.title,
        body=create_data.body,
        slug=create_data.slug,
        content=create_data.content,
    )
    session.add(new_post)
    session.commit()
    session.refresh(new_post)

    return new_post


@router.put("/post_id/")
async def post_update(post_id: int, update_data: PostUpdateRequest, session: db_dep):
    stmt = select(Post).where(Post.id == post_id)
    result = session.execute(stmt)
    post = result.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if update_data.title:
        post.title = update_data.title
        post.slug = generate_slug(update_data.title)

    if update_data.body is not None:
        post.body = update_data.body

    if update_data.is_active:
        post.is_active = update_data.is_active

    session.commit()
    session.refresh(post)


@router.patch("/post_id/")
async def post_update_patch(
    session: db_dep, post_id: int, update_data: PostUpdateRequest
):
    stmt = select(Post).where(Post.id == post_id)
    result = session.execute(stmt)
    post = result.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if update_data.title:
        post.title = update_data.title
        post.slug = generate_slug(update_data.title)

    if update_data.body is not None:
        post.body = update_data.body

    if update_data.is_active:
        post.is_active = update_data.is_active

    session.commit()
    session.refresh(post)


@router.delete("/post_id/", status_code=204)
async def post_delete(post_id: int, session: db_dep):
    stmt = select(Post).where(Post.id == post_id)
    result = session.execute(stmt)
    db_post = result.scalars().first()

    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    session.delete(db_post)
    session.commit()

    return {"message": f"ID {post_id} successfully deleted doneeeee !!!."}


@router.get("/weather/")
async def get_weather(lat: float, lon: float):
    # Open-Meteo tekin API manzili
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        if response.status_code != 200:
            raise HTTPException(
                status_code=400, detail="Ob-havo ma'lumotini olib bo'lmadi"
            )

        data = response.json()
        return {
            "shahar_koordinatalari": f"{lat}, {lon}",
            "harorat": data["current_weather"]["temperature"],
            "shamol_tezligi": data["current_weather"]["windspeed"],
            "vaqt": data["current_weather"]["time"],
        }
