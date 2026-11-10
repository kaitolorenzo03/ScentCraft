from app.database import UserModel, WardrobeItemModel, get_db
from app.models import WardrobeItem, WardrobeResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1/users", tags=["Armario Olfativo"])

@router.get("/{username}/wardrobe", response_model=WardrobeResponse)
def get_wardrobe(username: str, db: Session = Depends(get_db)):
    items = db.query(WardrobeItemModel).filter(WardrobeItemModel.username == username).all()
    formatted_items = [
        WardrobeItem(
            perfume_id=i.perfume_id,
            perfume_name=i.perfume_name,
            brand=i.brand,
            category=i.category
        ) for i in items
    ]
    return WardrobeResponse(username=username, items=formatted_items)

@router.post("/{username}/wardrobe", status_code=status.HTTP_201_CREATED)
def add_to_wardrobe(username: str, item: WardrobeItem, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.query(WardrobeItemModel).filter(
        WardrobeItemModel.username == username,
        WardrobeItemModel.perfume_id == item.perfume_id
    ).delete()

    item_id = f"{username}-{item.perfume_id}"
    new_item = WardrobeItemModel(
        id=item_id,
        username=username,
        perfume_id=item.perfume_id,
        perfume_name=item.perfume_name,
        brand=item.brand,
        category=item.category
    )
    db.add(new_item)
    db.commit()
    return {"message": f"Perfume '{item.perfume_name}' añadido al armario de {username}"}