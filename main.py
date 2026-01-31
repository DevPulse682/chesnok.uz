from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Post
from schemas import PostCreateRequest, PostListResponse

app = FastAPI(
    title="Chesnokbek sarguzashtlari",
    description="Bu dastur Chesnokbekning sarguzashtlarini boshqarish uchun mo'ljallangan API.",
    version="1.0.0",
)


@app.get("/")
def read_root():
    return {"message": "Salom, Chesnokbek!"}


@app.get("/posts/", response_model=list[PostListResponse])
async def get_posts(session: Session = Depends(get_db)):
    stmt = select(Post).order_by(Post.created_at.desc())
    res = session.execute(stmt)
    posts = res.scalars().all()

    return posts


@app.get("/posts/{slug}/", response_model=PostListResponse)
async def get_post(is_active: bool = None, session: Session = Depends(get_db)):
    stmt = select(Post)

    if is_active is not None:
        stmt = stmt.where(Post.is_active == is_active)

    stmt = stmt.order_by(Post.created_at.desc())
    res = session.execute(stmt)
    post = res.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


@app.post("/posts/create/")
async def create_post(
    create_data: PostCreateRequest, session: Session = Depends(get_db)
):
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


@app.put("/posts/{post_id}/")
async def post_update(
    post_id: int, update_data: PostCreateRequest, session: Session = Depends(get_db)
):
    stmt = select(Post).where(Post.id == post_id)
    result = session.execute(stmt)
    db_post = result.scalars().first()

    if not db_post:
        return {"error": "Post topilmadi!"}

    db_post.title = update_data.title
    db_post.body = update_data.body
    db_post.slug = update_data.slug
    db_post.content = update_data.content
    db_post.is_active = update_data.is_active

    session.commit()
    session.refresh(db_post)

    return db_post


@app.patch("/posts/{post_id}/")
async def post_patch(
    post_id: int, update_data: dict, session: Session = Depends(get_db)
):
    stmt = select(Post).where(Post.id == post_id)
    db_post = session.execute(stmt).scalars().first()

    if not db_post:
        return {"error": "Post topilmadi!"}

    for key, value in update_data.items():
        setattr(db_post, key, value)

    session.commit()
    session.refresh(db_post)
    return db_post


@app.delete("/posts/{post_id}/")
async def post_delete(post_id: int, session: Session = Depends(get_db)):
    stmt = select(Post).where(Post.id == post_id)
    db_post = session.execute(stmt).scalars().first()

    if not db_post:
        return {"error": "your error selection not found sorry!"}

    session.delete(db_post)
    session.commit()

    return {"message": f"ID {post_id} successfully deleted doneeeee !!!."}
