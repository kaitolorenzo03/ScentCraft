import httpx
from typing import List, Dict
from fastapi import HTTPException
from app.models import RecommendationItem

# URL base del microservicio de catálogo (en local corre en el puerto 8000)
CATALOG_SERVICE_URL = "http://127.0.0.1:8000/api/v1/perfumes"

async def fetch_catalog() -> List[Dict]:
    """Consulta de forma asíncrona el microservicio de catálogo."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(CATALOG_SERVICE_URL, timeout=5.0)
            if response.status_code == 200:
                return response.json()
            return []
        except httpx.RequestError:
            raise HTTPException(
                status_code=503, 
                detail="El servicio de catálogo (catalog-service) no está disponible"
            )

def calculate_similarity(target: Dict, candidate: Dict) -> RecommendationItem:
    """Calcula la coincidencia de notas olfativas entre dos perfumes."""
    target_notes = set(target["top_notes"] + target["heart_notes"] + target["base_notes"])
    candidate_notes = set(candidate["top_notes"] + candidate["heart_notes"] + candidate["base_notes"])
    
    intersection = target_notes.intersection(candidate_notes)
    union = target_notes.union(candidate_notes)
    
    score = round(len(intersection) / len(union), 2) if union else 0.0
    
    return RecommendationItem(
        perfume_id=candidate["id"],
        name=candidate["name"],
        brand=candidate["brand"],
        similarity_score=score,
        matching_notes=list(intersection)
    )

async def generate_recommendations(reference_id: str) -> List[RecommendationItem]:
    """Genera el ranking de recomendaciones filtrado y ordenado."""
    catalog = await fetch_catalog()
    
    target_perfume = next((p for p in catalog if p["id"] == reference_id), None)
    if not target_perfume:
        raise HTTPException(status_code=404, detail="Perfume de referencia no encontrado en el catálogo")
    
    recommendations = []
    for candidate in catalog:
        if candidate["id"] != reference_id:
            rec_item = calculate_similarity(target_perfume, candidate)
            recommendations.append(rec_item)
            
    # Ordenar de mayor a menor similitud
    recommendations.sort(key=lambda x: x.similarity_score, reverse=True)
    return recommendations