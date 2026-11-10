
from pydantic import BaseModel


class RecommendationRequest(BaseModel):
    reference_perfume_id: str

class RecommendationItem(BaseModel):
    perfume_id: str
    name: str
    brand: str
    similarity_score: float
    matching_notes: list[str]

class RecommendationResponse(BaseModel):
    reference_perfume_id: str
    recommendations: list[RecommendationItem]