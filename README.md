# ScentCraft - Plataforma de Perfumería de Nicho y Recomendación Olfativa

## 1. Descripción del Dominio y Problema de Negocio
ScentCraft es una Aplicación Nativa de la Nube (Cloud-Native Application) orientada a la catalogación y procesamiento de recomendaciones para perfumería de autor. En este sector, la búsqueda tradicional basada en marcas o nombres resulta insuficiente. La afinidad de una fragancia depende de la composición química de su pirámide olfativa (notas de salida, corazón y fondo). 

El sistema resuelve la necesidad de calcular coincidencias entre perfiles olfativos complejos sin ralentizar las operaciones de lectura habituales del catálogo, mediante una arquitectura distribuida y desacoplada basada en microservicios.

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

## 4. Diagrama de Arquitectura de Referencia

```mermaid
graph TD
    Client[Cliente / Swagger UI / Postman] -->|HTTP REST| Catalog[catalog-service REST API]
    Client -->|HTTP REST| Rec[recommendation-service]
    Catalog -->|Consultas SQL/NoSQL| DB[(PostgreSQL / MongoDB)]
    Catalog -->|Guarda/Lee Caché| Redis[(Redis Cache)]
    Rec -->|Lee datos catálogo| Catalog
    Rec -->|Caché recomendaciones| Redis


## 5. Especificación Sintética de la API REST

A continuación se detallan los endpoints principales de la arquitectura de microservicios, definiendo las rutas, verbos HTTP y los payloads JSON esperados para las peticiones y respuestas:

| Verbo HTTP | Ruta / Endpoint | Descripción | Request Payload (Entrada) | Response Payload (Salida) |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/perfumes` | Obtiene el catálogo paginado de perfumes y sus pirámides olfativas | *Ninguno* | `200 OK`<br>```json<br>[<br>  {<br>    "id": "perfume-01",<br>    "name": "Khamrah",<br>    "brand": "Lattafa",<br>    "top_notes": ["Canela", "Nuez moscada"],<br>    "heart_notes": ["Praliné", "Tuberosa"],<br>    "base_notes": ["Vainilla", "Haba tonka"]<br>  }<br>]<br>``` |
| `GET` | `/api/v1/perfumes/{id}` | Consulta el detalle específico de un perfume por su identificador | *Ninguno* | `200 OK` (Objeto JSON del perfume) / `404 Not Found` (`{"detail": "Perfume not found"}`) |
| `POST` | `/api/v1/recommendations` | Solicita el cálculo de recomendaciones olfativas basadas en un perfume o notas | ```json<br>{<br>  "perfume_id": "perfume-01",<br>  "limit": 5<br>}<br>``` | `200 OK`<br>```json<br>{<br>  "source_perfume": "perfume-01",<br>  "recommendations": [<br>    {<br>      "id": "perfume-08",<br>      "name": "Angels' Share",<br>      "similarity_score": 0.89<br>    }<br>  ],<br>  "cached": true<br>}<br>``` |
