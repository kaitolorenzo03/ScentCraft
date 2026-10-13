from pydantic import BaseModel
from typing import List

class Perfume(BaseModel):
    id: str
    name: str
    brand: str
    top_notes: List[str]
    heart_notes: List[str]
    base_notes: List[str]