from app.api.routes import router as api_router
from app.database import init_db
from app.views.web import router as web_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

init_db()

app = FastAPI(
    title="ScentCraft - Catalog Service",
    description="API de lectura y gestión del catálogo de perfumería de nicho",
    version="1.2.0"
)

# --- PERMITIR PETICIONES CROSS-ORIGIN (CORS) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite peticiones desde el recomendador y otros orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.include_router(web_router)