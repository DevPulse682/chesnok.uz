from datetime import datetime

from pydantic import BaseModel


class PostCreateRequest(BaseModel):
    title: str
    body: str
    slug: str
    content: str
    is_active: bool = True


class PostListResponse(BaseModel):
    id: int
    title: str
    slug: str
    created_at: datetime


class PostUpdateRequest(BaseModel):
    title: str | None = None
    body: str | None = None
    is_active: bool | None = None
