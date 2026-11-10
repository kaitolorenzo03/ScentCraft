from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth_routes import router as auth_router
from app.api.wardrobe_routes import router as wardrobe_router
from app.views.web import router as web_router
from app.database import init_db

# Inicializar la base de datos user.db en /app/data al arrancar
init_db()

app = FastAPI(
    title="ScentCraft - User Service",
    description="Gestión de autenticación de usuarios y Armario Olfativo",
    version="1.2.0"
)

# --- PERMITIR PETICIONES CROSS-ORIGIN (CORS) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth_router)
app.include_router(wardrobe_router)
app.include_router(web_router)