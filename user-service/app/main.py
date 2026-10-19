from fastapi import FastAPI
from app.api.auth_routes import router as auth_router
from app.api.wardrobe_routes import router as wardrobe_router
from app.views.web import router as web_router

app = FastAPI(
    title="ScentCraft - User Service",
    description="Gestión de autenticación de usuarios y Armario Olfativo",
    version="1.2.0"
)

app.include_router(auth_router)
app.include_router(wardrobe_router)
app.include_router(web_router)