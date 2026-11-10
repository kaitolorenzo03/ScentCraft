from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(include_in_schema=False)

@router.get("/", response_class=HTMLResponse)
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
            input { width: 100%; padding: 12px; border-radius: 6px; border: 1px solid #ccc; font-size: 15px; margin-bottom: 20px; box-sizing: border-box; }
            .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 15px; }
            .card { border: 1px solid #e1e8ed; border-radius: 8px; padding: 15px; background: #fafbfc; }
            .brand { color: #2980b9; font-weight: bold; font-size: 13px; text-transform: uppercase; }
            .name { margin: 5px 0; font-size: 16px; color: #2c3e50; }
            .notes { font-size: 12px; color: #555; margin-top: 8px; }
            .tag { background: #eef2f5; padding: 2px 6px; border-radius: 4px; display: inline-block; margin: 2px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📚 ScentCraft - Catálogo de Fragancias</h1>
            <p class="subtitle">Explora las 100 fragancias de autor registradas en SQLite</p>
            
            <input type="text" id="search-input" placeholder="🔍 Buscar por nombre, marca o nota (ej: Tom Ford, Vainilla, Oud)..." oninput="filtrarPerfumes()">

            <div id="catalog-grid" class="grid">
                <p>Cargando catálogo...</p>
            </div>
        </div>

        <script>
            let perfumesData = [];

            document.addEventListener("DOMContentLoaded", async () => {
                try {
                    const res = await fetch('/api/v1/perfumes');
                    perfumesData = await res.json();
                    renderPerfumes(perfumesData);
                } catch (e) {
                    document.getElementById('catalog-grid').innerHTML = "<p style='color:red;'>Error al cargar el catálogo de SQLite.</p>";
                }
            });

            function renderPerfumes(list) {
                const container = document.getElementById('catalog-grid');
                if (list.length === 0) {
                    container.innerHTML = "<p>No se encontraron perfumes con ese criterio.</p>";
                    return;
                }

                let html = '';
                list.forEach(p => {
                    html += `
                        <div class="card">
                            <span class="brand">${p.brand}</span>
                            <h3 class="name">${p.name}</h3>
                            <div class="notes">
                                <b>Salida:</b> ${p.top_notes.map(n => `<span class="tag">${n}</span>`).join('')}<br>
                                <b>Corazón:</b> ${p.heart_notes.map(n => `<span class="tag">${n}</span>`).join('')}<br>
                                <b>Fondo:</b> ${p.base_notes.map(n => `<span class="tag">${n}</span>`).join('')}
                            </div>
                        </div>
                    `;
                });
                container.innerHTML = html;
            }

            function filtrarPerfumes() {
                const query = document.getElementById('search-input').value.toLowerCase();
                const filtered = perfumesData.filter(p => 
                    p.name.toLowerCase().includes(query) ||
                    p.brand.toLowerCase().includes(query) ||
                    p.top_notes.some(n => n.toLowerCase().includes(query)) ||
                    p.heart_notes.some(n => n.toLowerCase().includes(query)) ||
                    p.base_notes.some(n => n.toLowerCase().includes(query))
                );
                renderPerfumes(filtered);
            }
        </script>
    </body>
    </html>
    """