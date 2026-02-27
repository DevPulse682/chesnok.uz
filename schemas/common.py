from pydantic import BaseModel


class ProfessionInline(BaseModel):
    id: int
    name: str
