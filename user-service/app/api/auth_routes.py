from fastapi import APIRouter, HTTPException, status
from app.models import UserRegister, UserLogin, TokenResponse
from app.database import USERS_DB

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticación"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserRegister):
    if user.username in USERS_DB:
        raise HTTPException(
            status_code=400, 
            detail="El nombre de usuario ya está registrado"
        )
    USERS_DB[user.username] = {
        "email": user.email,
        "password": user.password  # En producción se aplicaría hash (bcrypt)
    }
    return {"message": f"Usuario '{user.username}' registrado correctamente"}

@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin):
    user = USERS_DB.get(credentials.username)
    if not user or user["password"] != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales incorrectas"
        )
    return TokenResponse(
        access_token=f"fake-jwt-token-{credentials.username}",
        username=credentials.username
    )