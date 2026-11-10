from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db, UserModel, WardrobeItemModel

# Asegúrate de mantener este prefijo exacto para que coincida con la llamada del HTML
router = APIRouter(prefix="/api/v1/auth", tags=["Autenticación y Usuarios"])

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class UpdateUsernameRequest(BaseModel):
    new_username: str

# --- ENDPOINT DE LOGIN ---
@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == payload.username).first()
    if not user or user.password != payload.password:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    return {"message": "Login exitoso", "username": user.username}

# --- ENDPOINT DE REGISTRO ---
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(UserModel).filter(UserModel.username == payload.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está registrado")
    
    new_user = UserModel(
        username=payload.username,
        email=payload.email,
        password=payload.password
    )
    db.add(new_user)
    db.commit()
    return {"message": "Usuario registrado correctamente"}

# --- ELIMINAR USUARIO ---
@router.delete("/users/{username}", status_code=status.HTTP_200_OK)
def delete_user(username: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.query(WardrobeItemModel).filter(WardrobeItemModel.username == username).delete()
    db.delete(user)
    db.commit()
    return {"message": f"Usuario '{username}' eliminado"}

# --- CAMBIAR NOMBRE DE USUARIO ---
@router.put("/users/{username}/username", status_code=status.HTTP_200_OK)
def update_username(username: str, payload: UpdateUsernameRequest, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    new_user_check = db.query(UserModel).filter(UserModel.username == payload.new_username).first()
    if new_user_check:
        raise HTTPException(status_code=400, detail="El nuevo nombre ya está ocupado")
    
    wardrobe_items = db.query(WardrobeItemModel).filter(WardrobeItemModel.username == username).all()
    for item in wardrobe_items:
        item.username = payload.new_username
        item.id = f"{payload.new_username}-{item.perfume_id}"
    
    user.username = payload.new_username
    db.commit()
    return {"message": f"Nombre cambiado a '{payload.new_username}'"}