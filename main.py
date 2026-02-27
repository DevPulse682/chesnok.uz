from fastapi import FastAPI
from database import engine
import models

# Routerlarni import qilish
from routers.posts import router as posts_router
from routers.tags import router as tags_router
from routers.category import router as categories_router
from routers.profession import router as profession_router
from weather.weather import router as weather_app
from routers.lesson import router as lesson_router
from routers.users import router as users_router
from routers.auth import router as auth_router


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Chesnokbek sarguzashtlari",
    description="Bu dastur Chesnokbekning sarguzashtlarini boshqarish uchun mo'ljallangan API.",
    version="1.0.0",
)

# Routerlarni ulash
app.include_router(weather_app, prefix="/info", tags=["weather"])
app.include_router(posts_router)
app.include_router(tags_router)
app.include_router(categories_router)
app.include_router(profession_router)
app.include_router(users_router)
app.include_router(lesson_router)
app.include_router(auth_router)
