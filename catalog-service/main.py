from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="ScentCraft - Catalog Service",
    description="API de lectura y gestión del catálogo con vista visual",
    version="1.2.0"
)

class Perfume(BaseModel):
    id: str
    name: str
    brand: str
    top_notes: List[str]
    heart_notes: List[str]
    base_notes: List[str]

PERFUMES_DB = [
    {
        "id": "khamrah-01",
        "name": "Khamrah",
        "brand": "Lattafa",
        "top_notes": ["Canela", "Nuez moscada", "Bergamota"],
        "heart_notes": ["Praliné", "Tuberosa", "Feijoa"],
        "base_notes": ["Vainilla", "Haba tonka", "Mirra", "Ámbar"]
    },
    {
        "id": "encre-noire-02",
        "name": "Encre Noire",
        "brand": "Lalique",
        "top_notes": ["Ciprés"],
        "heart_notes": ["Vetiver de Borbón", "Vetiver de Haití"],
        "base_notes": ["Madera de cachemira", "Almizcle"]
    },
    {
        "id": "angels-share-03",
        "name": "Angels' Share",
        "brand": "By Kilian",
        "top_notes": ["Cognac"],
        "heart_notes": ["Canela", "Habas tonka", "Roble"],
        "base_notes": ["Praliné", "Vainilla", "Sándalo"]
    }
]

@app.get("/api/v1/perfumes", response_model=List[Perfume], tags=["Perfumes"])
def get_perfumes():
    return PERFUMES_DB

@app.get("/api/v1/perfumes/{perfume_id}", response_model=Perfume, tags=["Perfumes"])
def get_perfume_by_id(perfume_id: str):
    for perfume in PERFUMES_DB:
        if perfume["id"] == perfume_id:
            return perfume
    raise HTTPException(status_code=404, detail="Perfume no encontrado")

# INTERFAZ WEB (FRONT-END VISUAL DEL CATÁLOGO)
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def catalog_ui():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>ScentCraft - Catálogo de Perfumería</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f6f8; margin: 0; padding: 20px; color: #333; }
            .container { max-width: 900px; margin: auto; background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; margin-bottom: 5px; }
            p.subtitle { text-align: center; color: #7f8c8d; margin-bottom: 25px; }
            .card { border: 1px solid #e1e8ed; border-radius: 10px; padding: 20px; margin-bottom: 20px; background: #fafbfc; }
            .card-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eaeaea; padding-bottom: 10px; margin-bottom: 15px; }
            .brand { color: #8e44ad; font-weight: bold; font-size: 14px; text-transform: uppercase; }
            .title { margin: 0; color: #2c3e50; font-size: 20px; }
            .pyramid-section { margin-top: 8px; font-size: 14px; }
            .pyramid-label { font-weight: bold; width: 80px; display: inline-block; color: #555; }
            .tag { background: #eef2f5; padding: 4px 8px; border-radius: 4px; display: inline-block; margin: 2px; font-size: 13px; border: 1px solid #dcdfe3; }
            .tag-top { background: #fef9e7; color: #7d6608; border-color: #f9e79f; }
            .tag-heart { background: #fbeee6; color: #7e5109; border-color: #f5cba7; }
            .tag-base { background: #eaeded; color: #2e4053; border-color: #d5dbdb; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📚 ScentCraft - Catálogo</h1>
            <p class="subtitle">Colección de Perfumería de Autor y Pirámides Olfativas</p>
            <div id="catalog-list"></div>
        </div>

        <script>
            async function cargarCatalogo() {
                const container = document.getElementById('catalog-list');
                try {
                    const res = await fetch('/api/v1/perfumes');
                    const perfumes = await res.json();
                    
                    let html = '';
                    perfumes.forEach(p => {
                        html += `
                            <div class="card">
                                <div class="card-header">
                                    <div>
                                        <span class="brand">${p.brand}</span>
                                        <h3 class="title">${p.name}</h3>
                                    </div>
                                    <span style="color:#aaa; font-size:12px;">ID: ${p.id}</span>
                                </div>
                                <div class="pyramid-section">
                                    <span class="pyramid-label">Salida:</span>
                                    ${p.top_notes.map(n => `<span class="tag tag-top">${n}</span>`).join('')}
                                </div>
                                <div class="pyramid-section">
                                    <span class="pyramid-label">Corazón:</span>
                                    ${p.heart_notes.map(n => `<span class="tag tag-heart">${n}</span>`).join('')}
                                </div>
                                <div class="pyramid-section">
                                    <span class="pyramid-label">Fondo:</span>
                                    ${p.base_notes.map(n => `<span class="tag tag-base">${n}</span>`).join('')}
                                </div>
                            </div>
                        `;
                    });
                    container.innerHTML = html;
                } catch (e) {
                    container.innerHTML = "<p style='color:red; text-align:center;'>Error al cargar el catálogo.</p>";
                }
            }
            cargarCatalogo();
        </script>
    </body>
    </html>
    """