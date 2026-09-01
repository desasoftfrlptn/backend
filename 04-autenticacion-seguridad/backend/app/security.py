"""
Capa de seguridad — hash de contraseñas + tokens JWT.

Acá viven las dos operaciones más importantes de la seguridad de usuarios:

    1. HASH de contraseñas (Argon2, vía pwdlib).
       NUNCA guardamos la contraseña en texto plano. Guardamos un hash:
       una función irreversible que nos deja VERIFICAR ("esta contraseña
       coincide con este hash?") pero no RECUPERAR la contraseña original.

    2. JWT: crear y decodificar tokens FIRMADOS.
       El token es un string que el server firma con el SECRET_KEY. Quien
       no tenga la clave no puede fabricar ni alterar un token válido.
"""

from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

# pwdlib configura el hashing con el algoritmo RECOMENDADO (Argon2id).
# Argon2 es el ganador del Password Hashing Competition: diseñado para ser
# lento y costoso, lo que hace inviable el brute-force con GPUs.
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Convierte una contraseña en texto plano en un hash irreversible."""
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con un hash.

    Devuelve True/False — NUNCA lanza si no coincide.
    """
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(subject: str, expires_minutes: int | None = None) -> str:
    """
    Crea un JWT firmado para el usuario identificado por `subject`.

    Lleva dos claims importantes:
      - "sub" → el subject (identificador del usuario)
      - "exp" → la expiración (momento en que el token deja de valer)

    ⚠️ Usamos `datetime.now(timezone.utc)`. Sin timezone, el cálculo de
    expiración es frágil y rompe en distintos husos horarios.
    """
    expires = expires_minutes if expires_minutes is not None else ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    """
    Decodifica y VERIFICA la firma de un JWT.

    ⚠️ CRÍTICO: `algorithms=[ALGORITHM]` va EXPLÍCITO. Sin esto, permitís el
    "algorithm confusion attack". Siempre declarás qué algoritmos son válidos.

    Si el token expiró o la firma es inválida, `jwt.decode` lanza una
    excepción (`jwt.ExpiredSignatureError`, `jwt.InvalidTokenError`...).
    NO la capturamos acá: la dejamos propagar. El que la traduce a 401 es
    `get_current_user` (la capa HTTP). Igual que el 404 del Módulo 03.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
