from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
import httpx

app = FastAPI(
    title="ScentCraft - Recommendation Service",
    description="Motor de cálculo de similitud olfativa con interfaz visual",
    version="1.2.0"
)

CATALOG_SERVICE_URL = "http://127.0.0.1:8000/api/v1/perfumes"

class RecommendationRequest(BaseModel):
    perfume_id: str
    limit: Optional[int] = 5

def calculate_weighted_similarity(p1: dict, p2: dict):
    weights = {'top_notes': 0.2, 'heart_notes': 0.4, 'base_notes': 0.4}
    total_score = 0.0
    common_notes = set()

    for layer, weight in weights.items():
        set1 = set(p1.get(layer, []))
        set2 = set(p2.get(layer, []))
        if set1 and set2:
            intersection = set1.intersection(set2)
            union = set1.union(set2)
            layer_score = len(intersection) / len(union)
            total_score += layer_score * weight
            common_notes.update(intersection)

    return round(total_score * 100, 1), list(common_notes)

@app.get("/api/v1/recommendations", response_model=dict, tags=["Recommendations"])
@app.post("/api/v1/recommendations", response_model=dict, tags=["Recommendations"])
async def get_recommendations(request: Optional[RecommendationRequest] = None, perfume_id: Optional[str] = None):
    p_id = request.perfume_id if request else perfume_id
    if not p_id:
        raise HTTPException(status_code=400, detail="Debes proporcionar un perfume_id")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(CATALOG_SERVICE_URL)
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Error en catalog-service")
            catalog = response.json()
        except Exception:
            raise HTTPException(status_code=503, detail="catalog-service no disponible en el puerto 8000")

    target = next((p for p in catalog if p["id"] == p_id), None)
    if not target:
        raise HTTPException(status_code=404, detail="Perfume no encontrado")

    results = []
    for item in catalog:
        if item["id"] != p_id:
            score, common = calculate_weighted_similarity(target, item)
            results.append({
                "id": item["id"],
                "name": item["name"],
                "brand": item["brand"],
                "similarity_score": score,
                "common_notes": common,
                "top_notes": item.get("top_notes", []),
                "heart_notes": item.get("heart_notes", []),
                "base_notes": item.get("base_notes", [])
            })

    results.sort(key=lambda x: x["similarity_score"], reverse=True)
    limit = request.limit if request else 5

    return {
        "source_perfume": target,
        "recommendations": results[:limit]
    }

# INTERFAZ WEB (FRONT-END VISUAL)
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def web_ui():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>ScentCraft - Buscador & Recomendador Olfativo</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f6f8; margin: 0; padding: 20px; color: #333; }
            .container { max-width: 900px; margin: auto; background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; margin-bottom: 5px; }
            p.subtitle { text-align: center; color: #7f8c8d; margin-bottom: 25px; }
            .selector-box { text-align: center; margin-bottom: 30px; background: #f8f9fa; padding: 15px; border-radius: 8px; }
            select, button { padding: 10px 15px; font-size: 16px; border-radius: 6px; border: 1px solid #ccc; margin: 5px; }
            button { background: #8e44ad; color: white; border: none; cursor: pointer; transition: 0.3s; }
            button:hover { background: #732d91; }
            .card { border: 1px solid #e1e8ed; border-radius: 8px; padding: 15px; margin-bottom: 15px; background: #fff; display: flex; justify-content: space-between; align-items: center; }
            .card-info { max-width: 70%; }
            .badge { background: #e8f8f5; color: #117a65; padding: 5px 10px; border-radius: 20px; font-weight: bold; font-size: 14px; }
            .notes { font-size: 13px; color: #555; margin-top: 5px; }
            .tag { background: #f0f3f4; padding: 3px 7px; border-radius: 4px; display: inline-block; margin: 2px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>✨ ScentCraft</h1>
            <p class="subtitle">Plataforma de Recomendación Olfativa de Nicho</p>
            
            <div class="selector-box">
                <label for="perfumeSelect"><b>Elige un perfume base:</b></label>
                <select id="perfumeSelect">
                    <option value="khamrah-01">Lattafa - Khamrah</option>
                    <option value="encre-noire-02">Lalique - Encre Noire</option>
                    <option value="angels-share-03">Kilian - Angels' Share</option>
                </select>
                <button onclick="buscarRecomendaciones()">🔍 Buscar Perfumes Similares</button>
            </div>

            <div id="results"></div>
        </div>

        <script>
            async function buscarRecomendaciones() {
                const id = document.getElementById('perfumeSelect').value;
                const container = document.getElementById('results');
                container.innerHTML = "<p style='text-align:center;'>Procesando notas olfativas...</p>";

                try {
                    const res = await fetch(`/api/v1/recommendations?perfume_id=${id}`);
                    const data = await res.json();
                    
                    let html = `<h3>Perfumes parecidos a <b>${data.source_perfume.brand} ${data.source_perfume.name}</b>:</h3>`;
                    
                    data.recommendations.forEach(rec => {
                        html += `
                            <div class="card">
                                <div class="card-info">
                                    <h4 style="margin:0; color:#2c3e50;">${rec.brand} - ${rec.name}</h4>
                                    <div class="notes">
                                        <b>Notas coincidentes:</b> ${rec.common_notes.map(n => `<span class="tag">${n}</span>`).join('') || 'Ninguna directas'}
                                    </div>
                                </div>
                                <div>
                                    <span class="badge">Afinidad: ${rec.similarity_score}%</span>
                                </div>
                            </div>
                        `;
                    });

                    container.innerHTML = html;
                } catch (e) {
                    container.innerHTML = "<p style='color:red; text-align:center;'>Error al conectar con los microservicios.</p>";
                }
            }
        </script>
    </body>
    </html>
    """