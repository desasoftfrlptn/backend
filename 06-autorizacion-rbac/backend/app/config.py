"""
Configuración del módulo 06 — Autorización RBAC.

Misma filosofía que el módulo 05: defaults de DESARROLLO para correr sin .env,
y fail-loud en producción (SECRET_KEY obligatoria; sin ella la app NO arranca).

Este archivo NO se modifica en la entrega.
"""

import os

# ──────────────────────────────────────────────────────────────────────────
# Entorno
# ──────────────────────────────────────────────────────────────────────────
# "development" (default) | "production" | "testing"
ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development").lower()
IS_PRODUCTION: bool = ENVIRONMENT == "production"

# ──────────────────────────────────────────────────────────────────────────
# JWT
# ──────────────────────────────────────────────────────────────────────────
_SECRET_KEY = os.getenv("SECRET_KEY")
if not _SECRET_KEY:
    if IS_PRODUCTION:
        # Fail-loud: sin SECRET_KEY no hay firma segura → no se puede arrancar.
        raise RuntimeError(
            "SECRET_KEY es OBLIGATORIA en producción. Generala con: "
            "openssl rand -hex 32   y pasala por variable de entorno o "
            "secret manager. NUNCA hardcodeada en el código."
        )
    # Solo para desarrollo local. Generá la tuya con `openssl rand -hex 32`.
    _SECRET_KEY = "dev-only-6f5e4d3c2b1a0987-no-usar-en-produccion-cambiar-ya"
SECRET_KEY: str = _SECRET_KEY

ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# ──────────────────────────────────────────────────────────────────────────
# Tenancy
# ──────────────────────────────────────────────────────────────────────────
DEFAULT_TENANT_ID: int = 1

# ──────────────────────────────────────────────────────────────────────────
# Usuarios demo con los que arranca el storage
# ──────────────────────────────────────────────────────────────────────────
DEMO_PASSWORD: str = os.getenv("DEMO_PASSWORD", "demo12345")