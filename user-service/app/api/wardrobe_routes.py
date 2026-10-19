from fastapi import APIRouter, HTTPException, status
from app.models import WardrobeItem, WardrobeResponse
from app.database import WARDROBE_DB

router = APIRouter(prefix="/api/v1/users", tags=["Armario Olfativo"])

@router.get("/{username}/wardrobe", response_model=WardrobeResponse)
def get_wardrobe(username: str):
    items = WARDROBE_DB.get(username, [])
    return WardrobeResponse(username=username, items=items)

@router.post("/{username}/wardrobe", status_code=status.HTTP_201_CREATED)
def add_to_wardrobe(username: str, item: WardrobeItem):
    if username not in WARDROBE_DB:
        WARDROBE_DB[username] = []
    
    # Evitar duplicados del mismo perfume
    WARDROBE_DB[username] = [i for i in WARDROBE_DB[username] if i["perfume_id"] != item.perfume_id]
    WARDROBE_DB[username].append(item.dict())
    
    return {"message": f"Perfume '{item.perfume_name}' añadido al armario de {username}"}