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
