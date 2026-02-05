from fastapi import FastAPI

from routers import posts_router
from database import engine
import models
from weather.weather import router as weather_app


models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Chesnokbek sarguzashtlari",
    description="Bu dastur Chesnokbekning sarguzashtlarini boshqarish uchun mo'ljallangan API.",
    version="1.0.0",
)


app.include_router(weather_app, prefix="/info", tags=["weather"])
app.include_router(posts_router)
