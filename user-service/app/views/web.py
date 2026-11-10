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
        <title>ScentCraft - Perfil de Usuario y Armario Olfativo</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f6f8; margin: 0; padding: 20px; color: #333; }
            .container { max-width: 800px; margin: auto; background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; margin-bottom: 5px; }
            p.subtitle { text-align: center; color: #7f8c8d; margin-bottom: 25px; }
            
            /* Paneles */
            .auth-box, .wardrobe-box { background: #fafbfc; border: 1px solid #e1e8ed; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
            .form-group { margin-bottom: 15px; }
            label { display: block; font-weight: bold; margin-bottom: 5px; font-size: 14px; }
            input, select, button { width: 100%; padding: 10px; border-radius: 6px; border: 1px solid #ccc; font-size: 15px; box-sizing: border-box; }
            
            button { background: #8e44ad; color: white; border: none; font-weight: bold; cursor: pointer; transition: background 0.2s; }
            button:hover { background: #732d91; }
            .btn-secondary { background: #7f8c8d; margin-top: 10px; }
            .btn-secondary:hover { background: #626567; }
            
            /* Tarjetas del armario */
            .wardrobe-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 15px; margin-top: 15px; }
            .card { border: 1px solid #dcdfe3; border-radius: 8px; padding: 15px; background: white; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
            .badge { background: #e8daef; color: #8e44ad; padding: 3px 8px; border-radius: 12px; font-size: 12px; font-weight: bold; }
            
            /* Banners de notificación */
            .msg { padding: 10px; border-radius: 6px; margin-bottom: 15px; font-size: 14px; display: none; }
            .msg-success { background: #d4efdf; color: #1e8449; border: 1px solid #a9dfbf; }
            .msg-error { background: #fadbd8; color: #78281f; border: 1px solid #f5b7b1; }
            
            .user-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #f4f6f8; padding-bottom: 10px; margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>👤 ScentCraft - Gestión de Usuario</h1>
            <p class="subtitle">Autenticación y Armario Olfativo Personal</p>
            
            <div id="banner-msg" class="msg"></div>

            <!-- 1. SECCIÓN DE AUTENTICACIÓN (LOGIN / REGISTRO) -->
            <div id="auth-section">
                <!-- FORMULARIO DE LOGIN -->
                <div id="login-box" class="auth-box">
                    <h3>Iniciar Sesión</h3>
                    <div class="form-group">
                        <label>Nombre de Usuario</label>
                        <input type="text" id="login-username" value="kaito">
                    </div>
                    <div class="form-group">
                        <label>Contraseña</label>
                        <input type="password" id="login-password" value="password123">
                    </div>
                    <button onclick="ejecutarLogin()">Entrar a mi Armario</button>
                    <button class="btn-secondary" onclick="mostrarRegistro(true)">¿No tienes cuenta? Regístrate</button>
                </div>

                <!-- FORMULARIO DE REGISTRO -->
                <div id="register-box" class="auth-box" style="display:none;">
                    <h3>Crear Nueva Cuenta</h3>
                    <div class="form-group">
                        <label>Nombre de Usuario</label>
                        <input type="text" id="reg-username" placeholder="Ej: perfume_lover">
                    </div>
                    <div class="form-group">
                        <label>Correo Electrónico</label>
                        <input type="email" id="reg-email" placeholder="usuario@correo.com">
                    </div>
                    <div class="form-group">
                        <label>Contraseña</label>
                        <input type="password" id="reg-password" placeholder="******">
                    </div>
                    <button onclick="ejecutarRegistro()">Registrarme</button>
                    <button class="btn-secondary" onclick="mostrarRegistro(false)">Volver al Login</button>
                </div>
            </div>

            <!-- 2. SECCIÓN DEL ARMARIO OLFATIVO (SOLO TRAS AUTENTICARSE) -->
            <div id="wardrobe-section" style="display:none;">
                <div class="user-header">
                    <h2>Bienvenido, <span id="active-user-display" style="color:#8e44ad;"></span></h2>
                    <div style="display:flex; gap:10px;">
                        <button style="width:auto; padding:8px 12px; background:#e67e22;" onclick="toggleSettings()">⚙️ Ajustes</button>
                        <button style="width:auto; padding:8px 12px;" onclick="cerrarSesion()" class="btn-secondary">Cerrar Sesión</button>
                    </div>
                </div>

                <!-- PANEL DE AJUSTES DE CUENTA (Oculto por defecto) -->
                <div id="settings-box" class="wardrobe-box" style="display:none; background:#fef9e7; border-color:#f5b041;">
                    <h3>⚙️ Configuración de la Cuenta</h3>
                    
                    <!-- Cambiar Nombre -->
                    <div class="form-group">
                        <label>Nuevo Nombre de Usuario</label>
                        <input type="text" id="new-username-input" placeholder="Introduce el nuevo nombre">
                        <button style="margin-top:8px; background:#d35400;" onclick="ejecutarCambioNombre()">Guardar Nuevo Nombre</button>
                    </div>
                    
                    <hr style="margin:20px 0; border:0; border-top:1px solid #f5b041;">
                    
                    <!-- Borrar Cuenta -->
                    <div class="form-group">
                        <label style="color:#c0392b;">Zona de Peligro</label>
                        <button style="background:#c0392b;" onclick="ejecutarBorradoUsuario()">🗑️ Eliminar Mi Cuenta Definitivamente</button>
                    </div>
                </div>

                <!-- FORMULARIO PARA AÑADIR NUEVO PERFUME -->
                <div class="wardrobe-box">
                    <h3>➕ Añadir Fragancia al Armario</h3>
                    <div class="form-group">
                        <label>Seleccionar Perfume del Catálogo</label>
                        <select id="catalog-select">
                            <option value="">Cargando catálogo...</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Uso / Categoría</label>
                        <select id="item-category">
                            <option value="signature">Fragancia Insignia (Signature)</option>
                            <option value="rotation">Rotación Diaria</option>
                            <option value="special">Ocasiones Especiales</option>
                            <option value="wishlist">Lista de Deseos</option>
                        </select>
                    </div>
                    <button onclick="guardarEnArmario()">Añadir al Armario</button>
                </div>

                <!-- LISTADO DE ELEMENTOS DEL ARMARIO -->
                <h3>🖼️ Mi Colección de Fragancias</h3>
                <div id="wardrobe-items" class="wardrobe-grid">
                    <p>Cargando armario...</p>
                </div>
            </div>
        </div>

        <script>
            let currentUser = null;
            let catalogCache = [];

            function showMessage(text, isSuccess = true) {
                const banner = document.getElementById('banner-msg');
                banner.className = `msg ${isSuccess ? 'msg-success' : 'msg-error'}`;
                banner.textContent = text;
                banner.style.display = 'block';
                setTimeout(() => { banner.style.display = 'none'; }, 4000);
            }

            function mostrarRegistro(flag) {
                document.getElementById('login-box').style.display = flag ? 'none' : 'block';
                document.getElementById('register-box').style.display = flag ? 'block' : 'none';
            }

            function toggleSettings() {
                const box = document.getElementById('settings-box');
                box.style.display = box.style.display === 'none' ? 'block' : 'none';
            }

            async function ejecutarLogin() {
                const username = document.getElementById('login-username').value.trim();
                const password = document.getElementById('login-password').value.trim();

                if (!username || !password) {
                    showMessage("Por favor rellena usuario y contraseña", false);
                    return;
                }

                try {
                    const res = await fetch('/api/v1/auth/login', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ username, password })
                    });
                    const data = await res.json();

                    if (!res.ok) {
                        showMessage(data.detail || "Error al iniciar sesión", false);
                        return;
                    }

                    currentUser = username;
                    iniciarVistaArmario();
                    showMessage(`¡Bienvenido de nuevo, ${username}!`);
                } catch (e) {
                    showMessage("Error al conectar con user-service", false);
                }
            }

            async function ejecutarRegistro() {
                const username = document.getElementById('reg-username').value.trim();
                const email = document.getElementById('reg-email').value.trim();
                const password = document.getElementById('reg-password').value.trim();

                if (!username || !email || !password) {
                    showMessage("Todos los campos son obligatorios", false);
                    return;
                }

                try {
                    const res = await fetch('/api/v1/auth/register', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ username, email, password })
                    });
                    const data = await res.json();

                    if (!res.ok) {
                        showMessage(data.detail || "Error al registrar usuario", false);
                        return;
                    }

                    showMessage("Usuario creado correctamente. Ya puedes iniciar sesión.");
                    mostrarRegistro(false);
                    document.getElementById('login-username').value = username;
                } catch (e) {
                    showMessage("Error en el proceso de registro", false);
                }
            }

            async function iniciarVistaArmario() {
                document.getElementById('auth-section').style.display = 'none';
                document.getElementById('wardrobe-section').style.display = 'block';
                document.getElementById('active-user-display').textContent = currentUser;

                await cargarCatalogo();
                await cargarArmario();
            }

            function cerrarSesion() {
                currentUser = null;
                document.getElementById('auth-section').style.display = 'block';
                document.getElementById('wardrobe-section').style.display = 'none';
                document.getElementById('settings-box').style.display = 'none';
                showMessage("Sesión cerrada correctamente.");
            }

            async function cargarCatalogo() {
                const select = document.getElementById('catalog-select');
                try {
                    // ✅ CORREGIDO: Apunta a localhost en vez de 127.0.0.1
                    const res = await fetch('http://localhost:8000/api/v1/perfumes');
                    if (!res.ok) throw new Error("Error al obtener catálogo");
                    catalogCache = await res.json();

                    select.innerHTML = '';
                    catalogCache.forEach(p => {
                        const opt = document.createElement('option');
                        opt.value = p.id;
                        opt.textContent = `${p.brand} - ${p.name}`;
                        select.appendChild(opt);
                    });
                } catch (e) {
                    select.innerHTML = '<option value="">Error cargando perfumes (Verifica catalog-service)</option>';
                }
            }

            async function cargarArmario() {
                const container = document.getElementById('wardrobe-items');
                try {
                    const res = await fetch(`/api/v1/users/${currentUser}/wardrobe`);
                    if (!res.ok) throw new Error("Error al consultar armario");
                    const data = await res.json();

                    if (data.items.length === 0) {
                        container.innerHTML = "<p>Tu armario está vacío. ¡Añade tu primera fragancia arriba!</p>";
                        return;
                    }

                    let html = '';
                    data.items.forEach(item => {
                        html += `
                            <div class="card">
                                <span class="badge">${item.category.toUpperCase()}</span>
                                <h4 style="margin:10px 0 2px 0;">${item.perfume_name}</h4>
                                <p style="margin:0; color:#7f8c8d; font-size:13px;">${item.brand}</p>
                            </div>
                        `;
                    });
                    container.innerHTML = html;
                } catch (e) {
                    container.innerHTML = "<p style='color:red;'>No se pudo recuperar tu armario.</p>";
                }
            }

            async function guardarEnArmario() {
                const perfumeId = document.getElementById('catalog-select').value;
                const category = document.getElementById('item-category').value;

                if (!perfumeId) {
                    showMessage("Selecciona un perfume válido", false);
                    return;
                }

                const selectedPerfume = catalogCache.find(p => p.id === perfumeId);
                if (!selectedPerfume) return;

                const payload = {
                    perfume_id: selectedPerfume.id,
                    perfume_name: selectedPerfume.name,
                    brand: selectedPerfume.brand,
                    category: category
                };

                try {
                    const res = await fetch(`/api/v1/users/${currentUser}/wardrobe`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    });

                    if (!res.ok) {
                        showMessage("Error al añadir la fragancia", false);
                        return;
                    }

                    showMessage(`'${selectedPerfume.name}' añadido a tu armario.`);
                    await cargarArmario();
                } catch (e) {
                    showMessage("Error al comunicar con la API del armario", false);
                }
            }

            async function ejecutarCambioNombre() {
                const newUsername = document.getElementById('new-username-input').value.trim();
                if (!newUsername) {
                    showMessage("Introduce un nuevo nombre válido", false);
                    return;
                }

                try {
                    const res = await fetch(`/api/v1/auth/users/${currentUser}/username`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ new_username: newUsername })
                    });
                    const data = await res.json();

                    if (!res.ok) {
                        showMessage(data.detail || "Error al cambiar nombre", false);
                        return;
                    }

                    currentUser = newUsername;
                    document.getElementById('active-user-display').textContent = currentUser;
                    document.getElementById('new-username-input').value = '';
                    toggleSettings();
                    showMessage(`Nombre actualizado con éxito a '${newUsername}'.`);
                    await cargarArmario();
                } catch (e) {
                    showMessage("Error al procesar el cambio de nombre", false);
                }
            }

            async function ejecutarBorradoUsuario() {
                if (!confirm(`¿Estás seguro de que deseas eliminar la cuenta '${currentUser}'? Esta acción no se puede deshacer.`)) {
                    return;
                }

                try {
                    const res = await fetch(`/api/v1/auth/users/${currentUser}`, {
                        method: 'DELETE'
                    });
                    const data = await res.json();

                    if (!res.ok) {
                        showMessage(data.detail || "Error al borrar usuario", false);
                        return;
                    }

                    cerrarSesion();
                    showMessage("Tu cuenta ha sido eliminada correctamente.");
                } catch (e) {
                    showMessage("Error al intentar eliminar la cuenta", false);
                }
            }
        </script>
    </body>
    </html>
    """