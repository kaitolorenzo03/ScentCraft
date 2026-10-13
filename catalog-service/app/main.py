from fastapi import FastAPI
from app.api.routes import router as api_router
from app.views.web import router as web_router

app = FastAPI(
    title="ScentCraft - Catalog Service",
    description="API de lectura y gestión del catálogo de perfumería de nicho",
    version="1.2.0"
)

app.include_router(api_router)
app.include_router(web_router)