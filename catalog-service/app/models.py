
from pydantic import BaseModel


class Perfume(BaseModel):
    id: str
    name: str
    brand: str
    top_notes: list[str]
    heart_notes: list[str]
    base_notes: list[str]