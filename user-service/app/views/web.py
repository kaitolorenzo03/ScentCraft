from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(include_in_schema=False)

@router.get("/", response_class=HTMLResponse)
async def user_ui():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>ScentCraft - Perfil y Armario Olfativo</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f6f8; margin: 0; padding: 20px; color: #333; }
            .container { max-width: 900px; margin: auto; background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; margin-bottom: 5px; }
            p.subtitle { text-align: center; color: #7f8c8d; margin-bottom: 25px; }
            .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 25px; }
            .section { background: #fafbfc; border: 1px solid #e1e8ed; padding: 20px; border-radius: 10px; }
            input, select, button { width: 100%; padding: 10px; margin: 6px 0; border-radius: 6px; border: 1px solid #ccc; font-size: 14px; box-sizing: border-box; }
            button { background: #8e44ad; color: white; border: none; font-weight: bold; cursor: pointer; margin-top: 10px; }
            button:hover { background: #71368a; }
            .badge { padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; color: white; display: inline-block; }
            .badge-signature { background: #f1c40f; color: #7d6608; }
            .badge-owned { background: #2ecc71; }
            .badge-wishlist { background: #9b59b6; }
            .msg { margin-top: 8px; font-size: 13px; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>👤 ScentCraft - Gestión de Usuarios y Armario</h1>
            <p class="subtitle">Crea tu cuenta, gestiona tu sesión y organiza tu colección olfativa</p>
            
            <div class="grid">
                <!-- FORMULARIO 1: REGISTRO DE USUARIO -->
                <div class="section">
                    <h3>1. Crear Nueva Cuenta</h3>
                    <input type="text" id="reg-username" placeholder="Nombre de usuario">
                    <input type="email" id="reg-email" placeholder="Correo electrónico">
                    <input type="password" id="reg-password" placeholder="Contraseña">
                    <button onclick="registrarUsuario()">Registrarse</button>
                    <div id="reg-msg" class="msg"></div>
                </div>

                <!-- FORMULARIO 2: GESTIÓN DE ARMARIO -->
                <div class="section">
                    <h3>2. Añadir Perfume al Armario</h3>
                    <input type="text" id="add-username" value="kaito" placeholder="Usuario de destino">
                    <input type="text" id="perfume-id" placeholder="ID (ej: khamrah-01)">
                    <input type="text" id="perfume-name" placeholder="Nombre (ej: Khamrah)">
                    <input type="text" id="perfume-brand" placeholder="Marca (ej: Lattafa)">
                    <select id="perfume-category">
                        <option value="signature">⭐ Perfume de Firma</option>
                        <option value="owned">🟢 En Colección</option>
                        <option value="wishlist">💜 Lista de Deseos</option>
                    </select>
                    <button onclick="agregarPerfume()">Guardar en Armario</button>
                    <div id="add-msg" class="msg"></div>
                </div>
            </div>

            <!-- BUSCADOR / CONSULTA DE ARMARIO -->
            <div class="section">
                <h3>3. Consultar Armario de un Usuario</h3>
                <div style="display:flex; gap:10px;">
                    <input type="text" id="search-username" value="kaito" placeholder="Ver armario de...">
                    <button style="width: auto; padding: 0 25px;" onclick="cargarArmario()">Cargar</button>
                </div>
                <div id="wardrobe-results" style="margin-top:15px;"></div>
            </div>
        </div>

        <script>
            async function registrarUsuario() {
                const username = document.getElementById('reg-username').value;
                const email = document.getElementById('reg-email').value;
                const password = document.getElementById('reg-password').value;
                const msg = document.getElementById('reg-msg');

                try {
                    const res = await fetch('/api/v1/auth/register', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ username, email, password })
                    });
                    const data = await res.json();
                    if(res.ok) {
                        msg.style.color = "green";
                        msg.innerText = "✓ Usuario creado. ¡Ahora puedes consultar o añadir a su armario!";
                        document.getElementById('search-username').value = username;
                        document.getElementById('add-username').value = username;
                    } else {
                        msg.style.color = "red";
                        msg.innerText = data.detail || "Error al registrar";
                    }
                } catch(e) { msg.style.color = "red"; msg.innerText = "Error de conexión"; }
            }

            async function agregarPerfume() {
                const username = document.getElementById('add-username').value;
                const item = {
                    perfume_id: document.getElementById('perfume-id').value,
                    perfume_name: document.getElementById('perfume-name').value,
                    brand: document.getElementById('perfume-brand').value,
                    category: document.getElementById('perfume-category').value
                };
                const msg = document.getElementById('add-msg');

                try {
                    const res = await fetch(`/api/v1/users/${username}/wardrobe`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(item)
                    });
                    const data = await res.json();
                    if(res.ok) {
                        msg.style.color = "green";
                        msg.innerText = "✓ Perfume guardado correctamente";
                        document.getElementById('search-username').value = username;
                        cargarArmario();
                    } else {
                        msg.style.color = "red";
                        msg.innerText = "Error al guardar el perfume";
                    }
                } catch(e) { msg.style.color = "red"; msg.innerText = "Error de conexión"; }
            }

            async function cargarArmario() {
                const username = document.getElementById('search-username').value;
                const container = document.getElementById('wardrobe-results');
                
                try {
                    const res = await fetch(`/api/v1/users/${username}/wardrobe`);
                    const data = await res.json();
                    
                    if (!data.items || data.items.length === 0) {
                        container.innerHTML = `<p>El usuario <b>${username}</b> no tiene perfumes en su armario aún.</p>`;
                        return;
                    }

                    let html = `<p><b>Armario de <i>${data.username}</i> (${data.items.length} perfumes):</b></p><ul>`;
                    data.items.forEach(item => {
                        let badgeClass = 'badge-owned';
                        let label = 'En Colección';
                        if (item.category === 'signature') { badgeClass = 'badge-signature'; label = 'Perfume de Firma ⭐'; }
                        if (item.category === 'wishlist') { badgeClass = 'badge-wishlist'; label = 'Lista de Deseos 💜'; }

                        html += `
                            <li style="margin-bottom: 8px;">
                                <b>${item.brand}</b> - ${item.perfume_name} 
                                <span class="badge ${badgeClass}">${label}</span>
                            </li>
                        `;
                    });
                    html += '</ul>';
                    container.innerHTML = html;
                } catch (e) {
                    container.innerHTML = "<p style='color:red;'>Error al cargar el armario.</p>";
                }
            }
            cargarArmario();
        </script>
    </body>
    </html>
    """