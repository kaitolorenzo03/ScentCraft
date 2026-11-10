import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models import Perfume
from app.database import get_db, PerfumeModel

router = APIRouter(prefix="/api/v1/perfumes", tags=["Perfumes"])

def format_perfume(p: PerfumeModel) -> Perfume:
    return Perfume(
        id=p.id,
        name=p.name,
        brand=p.brand,
        top_notes=json.loads(p.top_notes),
        heart_notes=json.loads(p.heart_notes),
        base_notes=json.loads(p.base_notes)
    )

@router.get("", response_model=List[Perfume])
def get_perfumes(db: Session = Depends(get_db)):
    perfumes = db.query(PerfumeModel).all()
    return [format_perfume(p) for p in perfumes]

@router.get("/{perfume_id}", response_model=Perfume)
def get_perfume_by_id(perfume_id: str, db: Session = Depends(get_db)):
    perfume = db.query(PerfumeModel).filter(PerfumeModel.id == perfume_id).first()
    if not perfume:
        raise HTTPException(status_code=404, detail="Perfume no encontrado")
    return format_perfume(perfume)