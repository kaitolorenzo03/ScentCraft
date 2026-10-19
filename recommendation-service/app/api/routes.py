from fastapi import APIRouter
from app.models import RecommendationRequest, RecommendationResponse
from app.services import generate_recommendations

router = APIRouter(prefix="/api/v1/recommendations", tags=["Recommendations"])

@router.post("", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    results = await generate_recommendations(request.reference_perfume_id)
    return RecommendationResponse(
        reference_perfume_id=request.reference_perfume_id,
        recommendations=results
    )