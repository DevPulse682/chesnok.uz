from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Integer,
    BigInteger,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    func,
    Table,
    Column,
    relationship,
)
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Profession(BaseModel):
    __tablename__ = "professions"
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    def __repr__(self):
        return f"Profession({self.name})"


class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=True)
    password: Mapped[str] = mapped_column(String(100), nullable=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    profession_id: Mapped[int] = mapped_column(
        ForeignKey("professions.id"), nullable=True
    )
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    post_count: Mapped[int] = mapped_column(BigInteger, default=0)
    post_read_count: Mapped[int] = mapped_column(BigInteger, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    posts: Mapped[list["Post"]] = relationship(
        back_populates="user", lazy="raise_on_sql"
    )

    def __repr__(self):
        return f"User({self.first_name})"


class Category(BaseModel):
    __tablename__ = "categories"
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"Category({self.name})"


class Post(BaseModel):
    __tablename__ = "posts"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    body: Mapped[str] = mapped_column(Text)
    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id"), nullable=True
    )
    views_count: Mapped[int] = mapped_column(BigInteger, default=0)
    likes_count: Mapped[int] = mapped_column(BigInteger, default=0)
    comments_count: Mapped[int] = mapped_column(BigInteger, default=0)
    mins_read: Mapped[int] = mapped_column(BigInteger, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    tags: Mapped[list["Tag"]] = relationship(
        secondary="post_tags", back_populates="posts", lazy="raise_on_sql"
    )

    def __repr__(self):
        return f"<Post(title={self.title})>"


class Comment(BaseModel):
    __tablename__ = "comments"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class Tag(BaseModel):
    __tablename__ = "tags"

    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)


class Media(BaseModel):
    __tablename__ = "media"

    url: Mapped[str] = mapped_column(String(100))


class PostMedia(Base):
    __tablename__ = "post_media"

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), primary_key=True)
    media_id: Mapped[int] = mapped_column(ForeignKey("media.id"), primary_key=True)


class UserSearch(Base):
    __tablename__ = "user_searches"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    term: Mapped[str] = mapped_column(String(50), nullable=False)
    count: Mapped[int] = mapped_column(Integer, default=0)

    def __repr__(self):
        return f"UserSearch{self.term})"


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_agent: Mapped[str] = mapped_column(String(255), nullable=False)
    last_active: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    def __repr__(self):
        return f"Device({self.user_agent})"


class Like(Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    post_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("posts.id"), nullable=False
    )
    device_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("devices.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )

    def __repr__(self):
        return f"Like(post_id={self.post_id}, device_id={self.device_id})"


post_tag_m2m_table = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", BigInteger, ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", BigInteger, ForeignKey("tags.id"), primary_key=True),
)
