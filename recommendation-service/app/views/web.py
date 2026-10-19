from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(include_in_schema=False)

@router.get("/", response_class=HTMLResponse)
async def recommendation_ui():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>ScentCraft - Motor de Recomendaciones</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f6f8; margin: 0; padding: 20px; color: #333; }
            .container { max-width: 900px; margin: auto; background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; margin-bottom: 5px; }
            p.subtitle { text-align: center; color: #7f8c8d; margin-bottom: 25px; }
            .control-panel { background: #ebf5fb; padding: 20px; border-radius: 8px; margin-bottom: 25px; border: 1px solid #aed6f1; }
            select, button { padding: 10px 15px; border-radius: 6px; border: 1px solid #ccc; font-size: 15px; }
            button { background: #2980b9; color: white; border: none; font-weight: bold; cursor: pointer; }
            button:hover { background: #1f618d; }
            .card { border: 1px solid #e1e8ed; border-radius: 10px; padding: 15px; margin-bottom: 15px; background: #fafbfc; }
            .score-badge { background: #27ae60; color: white; padding: 4px 10px; border-radius: 12px; font-weight: bold; }
            .tag { background: #eef2f5; padding: 4px 8px; border-radius: 4px; display: inline-block; margin: 2px; font-size: 13px; border: 1px solid #dcdfe3; }
            .tag-match { background: #d4efdf; color: #1e8449; border-color: #a9dfbf; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 ScentCraft - Recomendador Olfativo</h1>
            <p class="subtitle">Cómputo de Afinidad y Coincidencia de Notas</p>
            
            <div class="control-panel">
                <label><b>Selecciona tu perfume favorito:</b></label><br><br>
                <select id="perfume-select">
                    <option value="khamrah-01">Lattafa - Khamrah</option>
                    <option value="encre-noire-02">Lalique - Encre Noire</option>
                    <option value="angels-share-03">By Kilian - Angels' Share</option>
                </select>
                <button onclick="obtenerRecomendaciones()">Calcular Similitud</button>
            </div>

            <div id="results-list"></div>
        </div>

        <script>
            async function obtenerRecomendaciones() {
                const selectedId = document.getElementById('perfume-select').value;
                const container = document.getElementById('results-list');
                container.innerHTML = "<p>Calculando afinidades olfativas...</p>";

                try {
                    const res = await fetch('/api/v1/recommendations', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ reference_perfume_id: selectedId })
                    });
                    
                    const data = await res.json();
                    
                    if(!res.ok) {
                        container.innerHTML = `<p style="color:red;">Error: ${data.detail}</p>`;
                        return;
                    }

                    let html = `<h3>Recomendaciones para: <i>${data.reference_perfume_id}</i></h3>`;
                    data.recommendations.forEach(rec => {
                        const matchPercent = (rec.similarity_score * 100).toFixed(0);
                        html += `
                            <div class="card">
                                <div style="display:flex; justify-content:space-between; align-items:center;">
                                    <div>
                                        <b style="color:#8e44ad;">${rec.brand}</b>
                                        <h4 style="margin:2px 0;">${rec.name}</h4>
                                    </div>
                                    <span class="score-badge">${matchPercent}% Afinidad</span>
                                </div>
                                <p style="margin-top:10px; font-size:14px;">
                                    <b>Notas Coincidentes:</b> 
                                    ${rec.matching_notes.length > 0 
                                        ? rec.matching_notes.map(n => `<span class="tag tag-match">✓ ${n}</span>`).join('') 
                                        : '<i>Ninguna coincidencia directa</i>'}
                                </p>
                            </div>
                        `;
                    });
                    container.innerHTML = html;
                } catch (e) {
                    container.innerHTML = "<p style='color:red;'>Asegúrate de que catalog-service está arrancado en el puerto 8000.</p>";
                }
            }
        </script>
    </body>
    </html>
    """