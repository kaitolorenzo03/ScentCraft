# ScentCraft - Plataforma de Perfumería de Nicho y Recomendación Olfativa
# 1. Descripción del Dominio, Arquitectura Modular y Casos de Uso Principales

## Descripción del Dominio y Problema de Negocio
**ScentCraft** es una Aplicación Nativa de la Nube (*Cloud-Native Application*) orientada a la catalogación avanzada, gestión de comunidades y procesamiento de recomendaciones para la perfumería de autor y de nicho. En este sector, la búsqueda basada únicamente en nombres comerciales o marcas resulta insuficiente, ya que la afinidad entre fragancias depende de la composición química y la estructura de su **pirámide olfativa** (notas de salida, corazón y fondo).

El sistema resuelve la necesidad de calcular coincidencias complejas entre perfiles olfativos, gestionar armarios digitales de fragancias personales y mantener catálogos extensos sin bloquear las operaciones de lectura o cálculo, mediante una arquitectura distribuida, desacoplada y modular basada en microservicios.

---

## Arquitectura de Microservicios Modularizada

Cada microservicio sigue el principio de **separación de responsabilidades** (SoC) mediante un patrón de diseño en capas (`app/models.py`, `app/api/`, `app/services.py`, `app/views/`), garantizando que la lógica de negocio, la persistencia, los endpoints REST y la capa de presentación no estén acoplados.

### Componentes del Sistema:

1. **`catalog-service` (Puerto 8000):**
   * **Responsabilidad:** Gestión y consulta del catálogo de perfumería de nicho y sus pirámides olfativas.
   * **Estructura Interna:** Routers dedicados a las rutas REST (`/api/v1/perfumes`), esquemas de datos Pydantic para la estructura olfativa y vistas HTML independientes.

2. **`recommendation-service` (Puerto 8001):**
   * **Responsabilidad:** Motor de cómputo e inteligencia de afinidad olfativa.
   * **Estructura Interna:** Capa de servicios (`services.py`) con clientes HTTP asíncronos (`httpx`) para consultar `catalog-service`, algoritmos de similitud ponderada por capas de notas y panel gráfico interactivo.

3. **`user-service` (Puerto 8002 / 8003):**
   * **Responsabilidad:** Autenticación de usuarios, gestión de sesiones desacoplada y administración del Armario Olfativo ("Scent Wardrobe").
   * **Estructura Interna:** Módulos de API separados para la autenticación (`auth_routes.py`) y la gestión de la colección personal (`wardrobe_routes.py`).

4. **`Redis Cache` (Capa de Caché y Persistencia Cloud):**
   * **Responsabilidad:** Optimización del rendimiento y reducción de latencia en peticiones concurrentes.
   * **Función:** Almacena en memoria las recomendaciones calculadas con alta frecuencia para evitar recomputaciones innecesarias de CPU.

---

## Casos de Uso Principales (CU)

A continuación se detallan los flujos de uso fundamentales del sistema:

* **`CU01: Consulta de Catálogo y Pirámides Olfativas`**
  * **Actor:** Cliente externo / Usuario final.
  * **Descripción:** El usuario consulta la lista global de fragancias o la ficha técnica individual de un perfume, obteniendo el desglose de sus notas de salida, corazón y fondo.
  * **Servicio involucrado:** `catalog-service`.

* **`CU02: Cálculo y Solicitud de Recomendación Olfativa`**
  * **Actor:** Cliente externo / Usuario final.
  * **Descripción:** El usuario selecciona un perfume de referencia para obtener recomendaciones. El servicio analiza la intersección de notas olfativas y devuelve un ranking ordenado por porcentaje de similitud (`similarity_score`) y notas coincidentes.
  * **Servicios involucrados:** `recommendation-service` y `catalog-service`.

* **`CU03: Registro, Login y Autenticación de Usuario`**
  * **Actor:** Cliente externo / Usuario final.
  * **Descripción:** Permite a los usuarios crear una cuenta en la plataforma e iniciar sesión para obtener credenciales/tokens de acceso para gestionar sus datos privados.
  * **Servicio involucrado:** `user-service`.

* **`CU04: Gestión del Armario Olfativo Personal ("Scent Wardrobe")`**
  * **Actor:** Usuario autenticado.
  * **Descripción:** El usuario organiza su colección privada catalogando perfumes como *"Perfume de Firma"*, *"En Colección"* o *"Lista de Deseos"*.
  * **Servicio involucrado:** `user-service`.

* **`CU05: Optimización de Recomendaciones mediante Caché`**
  * **Actor:** Sistema / `recommendation-service`.
  * **Descripción:** Ante una solicitud de recomendación, el motor comprueba primero en Redis si el resultado ya fue calculado previamente, sirviendo la respuesta inmediatamente si existe en caché.
  * **Servicios involucrados:** `recommendation-service` y `Redis Cache`.

## 2. Justificación según NIST SP 800-145 (5 Características Clave del Cloud)
1. **Autoservicio bajo demanda (On-demand self-service):** Aprovisionamiento automático de contenedores e infraestructura sin requerir intervención humana directa con el proveedor de la nube.
2. **Acceso amplio a la red (Broad network access):** Exposición de capacidades a través de protocolos estándar HTTP/REST e interfaces JSON accesibles desde cualquier plataforma cliente.
3. **Asignación común de recursos (Resource pooling):** Los microservicios comparten la infraestructura de cómputo y bases de datos asignando recursos dinámicamente según la carga.
4. **Rápida elasticidad (Rapid elasticity):** Escalado independiente del microservicio de recomendaciones (`recommendation-service`) para asimilar picos de demanda durante lanzamientos de fragancias o campañas promocionales.
5. **Servicio medido (Measured service):** Control y monitorización continua del consumo de recursos, latencia de respuestas y tasa de peticiones.

## 3. Mapeo de Actores NIST SP 500-292 e Impacto Económico
* **Cloud Consumer:** Clientes externos, aplicaciones cliente o herramientas de prueba de API (Swagger UI / Postman).
* **Cloud Provider:** Plataforma de infraestructura en la nube encargada de alojar los contenedores.
* **Cloud Broker:** Capa de orquestación y despliegue de infraestructura que gestiona la provisión del entorno.
* **Cloud Auditor:** Herramientas de telemetría y supervisión del rendimiento y seguridad del sistema.
* **Cloud Carrier:** Proveedores de red y telecomunicaciones que garantizan el transporte seguro del tráfico HTTP/S.
* **Impacto Económico:** La adopción del modelo *Pay-as-you-go* evita el sobredimensionamiento de servidores dedicados tradicionales, optimizando los costes operativos al escalar la infraestructura de forma elástica en función de la demanda real.


## 4. Especificación Sintética de la API REST

A continuación se detallan los endpoints principales de la arquitectura de microservicios, definiendo las rutas, verbos HTTP y los payloads JSON esperados para las peticiones y respuestas:

| Verbo HTTP | Ruta / Endpoint | Descripción | Request Payload (Entrada) | Response Payload (Salida) |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/perfumes` | Obtiene el catálogo paginado de perfumes y sus pirámides olfativas | *Ninguno* | `200 OK` — `[{"id": "perfume-01", "name": "Khamrah", "brand": "Lattafa", "top_notes": ["Canela"], "heart_notes": ["Praliné"], "base_notes": ["Vainilla"]}]` |
| `GET` | `/api/v1/perfumes/{id}` | Consulta el detalle específico de un perfume por su identificador | *Ninguno* | `200 OK` (Objeto JSON del perfume) / `404 Not Found` (`{"detail": "Perfume not found"}`) |
| `POST` | `/api/v1/recommendations` | Solicita el cálculo de recomendaciones olfativas basadas en un perfume o notas | `{"perfume_id": "perfume-01", "limit": 5}` | `200 OK` — `{"source_perfume": "perfume-01", "recommendations": [{"id": "perfume-08", "name": "Angels' Share", "similarity_score": 0.89}], "cached": true}` |

## 5. Diagrama de Arquitectura de Referencia
## 🏗️ Arquitectura del Sistema

ScentCraft sigue una arquitectura orientada a **microservicios desacoplados** bajo el principio *Database per Service*. Cada servicio mantiene su propia responsabilidad y capa de datos independiente.

```mermaid
graph TD
    subgraph Client Layer [Capa de Presentación Web]
        UI_Cat[Web UI / View <br/> catalog-service:8000]
        UI_Rec[Web UI / View <br/> recommendation-service:8001]
        UI_Usr[Web UI / View <br/> user-service:8002]
    end

    subgraph Service Layer [Capa de Microservicios - FastAPI]
        CS[catalog-service <br/> Port 8000]
        RS[recommendation-service <br/> Port 8001]
        US[user-service <br/> Port 8002]
    end

    subgraph Persistence Layer [Capa de Persistencia e Infraestructura]
        DB_Cat[(SQLite DB <br/> catalog.db)]
        DB_Usr[(SQLite DB <br/> user.db)]
        RedisCache[(Redis Cache <br/> Port 6379)]
    end

    %% Interacciones de Interfaz Web a API
    UI_Cat -->|Local Route| CS
    UI_Rec -->|Local Route| RS
    UI_Usr -->|Local Route| US

    %% Comunicación Inter-Servicio (HTTP Asíncrono / httpx)
    RS -->|HTTP Async GET /api/v1/perfumes| CS

    %% Acceso a Persistencia
    CS -->|SQLAlchemy ORM| DB_Cat
    US -->|SQLAlchemy ORM| DB_Usr
    RS -.->|Caché de recomendaciones| RedisCache
