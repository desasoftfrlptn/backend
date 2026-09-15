# ──────────────────────────────────────────────────────────────────────────
# Módulo 06 — Autorización RBAC · Imagen del frontend (React + Vite)
#
# La herramienta visual de prueba. Corre Vite DEV con --host 0.0.0.0 para ser
# alcanzable desde el host. El proxy hacia la API se configura con la
# variable VITE_PROXY_TARGET (la define docker-compose.yml → backend:8000).
#
# No toqués este archivo en la entrega: es infraestructura de la cátedra.
# ──────────────────────────────────────────────────────────────────────────

FROM node:22-alpine

WORKDIR /app

# pnpm se instala global con npm (viene con la imagen node).
RUN npm install -g pnpm@9

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .

EXPOSE 5173

# --host 0.0.0.0: dentro del contenedor, escuchar en todas las interfaces.
CMD ["pnpm", "dev", "--host", "0.0.0.0"]