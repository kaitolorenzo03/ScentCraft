# --- ETAPA 1: BUILDER ---
FROM python:3.11-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# --- ETAPA 2: RUNNER (Final) ---
FROM python:3.11-slim AS runner

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear usuario no root por seguridad
RUN adduser --disabled-password --gecos "" appuser

# Copiar dependencias de la etapa builder y código fuente
COPY --from=builder /root/.local /home/appuser/.local
COPY . /app

# ✅ Crear carpeta de volumen de datos y asignar permisos explícitos a appuser
RUN mkdir -p /app/data && chown -R appuser:appuser /app /home/appuser

USER appuser

ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]