from datetime import datetime
from pydantic import BaseModel, EmailStr


class BaseConfigModel(BaseModel):
    model_config = {
        "from_attributes": True,
    }


class PostCreateRequest(BaseConfigModel):
    title: str
    body: str
    slug: str
    content: str
    is_active: bool = True


class PostListResponse(BaseConfigModel):
    id: int
    title: str
    slug: str
    created_at: datetime


class PostUpdateRequest(BaseConfigModel):
    title: str | None = None
    body: str | None = None
    is_active: bool | None = None


class TagCreateRequest(BaseModel):
    name: str
    slug: str


class TagUpdateRequest(BaseModel):
    name: str | None = None


class TagListResponse(BaseModel):
    id: int
    name: str
    slug: str


class CategoryListResonse(BaseModel):
    id: int | None = None
    name: str | None = None


class CategoryCreateRequest(BaseModel):
    name: str | None = None


class ProfessionCreateRequest(BaseModel):
    name: str


class ProfessionListResponse(BaseModel):
    id: int
    name: str


class ProfessionUpdateRequest(BaseModel):
    name: str


class WeatherCoord(BaseModel):
    lon: float
    lat: float


class WeatherInline(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class WeatherMainInline(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    sea_level: int
    grnd_level: int


class WeatherResponse(BaseModel):
    coord: WeatherCoord
    weather: list[WeatherInline]
    # base: str
    # main: WeatherMainInline
    # visibility: int
    # wind: dict[str, float] | None = None
    # rain: dict[str, float] | None = None
    # clouds: dict[str, int] | None = None
    # dt: int
    # sys: dict[str, int | str] | None = None
    # timezone: int
    # id: int
    # name: str
    # cod: int


class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
