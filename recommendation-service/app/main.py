from app.api.routes import router as api_router
from app.views.web import router as web_router
from fastapi import FastAPI

app = FastAPI(
    title="ScentCraft - Recommendation Service",
    description="Motor de cálculo de similitud olfativa desacoplado",
    version="1.2.0"
)

app.include_router(api_router)
app.include_router(web_router)