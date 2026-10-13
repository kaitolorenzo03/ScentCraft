from fastapi import APIRouter, HTTPException
from typing import List
from app.models import Perfume
from app.database import PERFUMES_DB

router = APIRouter(prefix="/api/v1/perfumes", tags=["Perfumes"])

@router.get("", response_model=List[Perfume])
def get_perfumes():
    return PERFUMES_DB

@router.get("/{perfume_id}", response_model=Perfume)
def get_perfume_by_id(perfume_id: str):
    for perfume in PERFUMES_DB:
        if perfume["id"] == perfume_id:
            return perfume
    raise HTTPException(status_code=404, detail="Perfume no encontrado")