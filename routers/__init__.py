from .posts import router as posts_router
from .tags import router as tags_router
from .category import router as categories_router
from .profession import router as profession_router
from .users import router as users_router
from .lesson import router as lesson_router
from routers.users import router as users_router
from .auth import router as auth_router


__all__ = [
    "posts_router",
    "tags_router",
    "categories_router",
    "profession_router",
    "weather_app",
    "users_router",
    "lesson_router",
    "auth_router",
    "auth_router_one",
]
