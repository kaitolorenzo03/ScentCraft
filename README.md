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
* **Cloud Provider:** Plataforma de infraestructura en la nube (ej. AWS / Render / Railway) encargada de alojar los contenedores.
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
