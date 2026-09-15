# ──────────────────────────────────────────────────────────────────────────
# Módulo 06 — Autorización RBAC · Imagen del backend (FastAPI)
#
# La app corre en memoria (seed automático al arrancar) → imagen sin estado.
# El entrypoint usa uvicorn con --host 0.0.0.0 para que el contenedor sea
# alcanzable desde el host (y desde el frontend en la red de Compose).
#
# No toqués este archivo en la entrega: es infraestructura de la cátedra.
# ──────────────────────────────────────────────────────────────────────────

FROM python:3.12-slim

WORKDIR /app

# Primero las dependencias (capa cacheable), después el código.
# El pyproject (hatchling) instala el paquete `app` completo.
COPY pyproject.toml ./
COPY app ./app

RUN pip install --no-cache-dir .

EXPOSE 8000

# host 0.0.0.0: dentro del contenedor el service no vive en "localhost" del host.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]