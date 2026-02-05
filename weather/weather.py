from fastapi import APIRouter
import httpx

router = APIRouter()


@router.get("/weather/")
async def get_weather(lat: float, lon: float):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
