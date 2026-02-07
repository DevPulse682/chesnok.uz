from .posts import router as posts_router
from .tags import router as tags_router
from .category import router as categories_router
from .profession import router as profession_router


__all__ = ["posts_router", "tags_router", "categories_router", "profession_router"]
