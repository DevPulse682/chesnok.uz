from fastapi import APIRouter
import httpx


from schemas import WeatherResponse


router = APIRouter(prefix="/weather", tags=["Weather"])

API_KEY = "b89d55fa0d0b58e75f3fa5c6a3a61632"


@router.get("/weather/today/", response_model=WeatherResponse)
async def get_weather(city: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        )

        if resp.status_code == 404:
            return {"error": "Shahar topilmadi! "}
        return resp.json()
