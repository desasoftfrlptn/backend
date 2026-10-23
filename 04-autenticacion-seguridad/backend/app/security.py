"""
Capa de seguridad — hash de contraseñas + tokens JWT.

COMPLETÁ las funciones marcadas con TODO. Este es EL archivo de la clase:
acá vivís las dos operaciones más importantes de la seguridad de usuarios.

Hay dos responsabilidades separadas (y no mezclarlas es la lección):

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

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

# pwdlib configura el hashing con el algoritmo RECOMENDADO (Argon2id).
# Argon2 es el ganador del Password Hashing Competition: diseñado para ser
# lento y costoso, lo que hace inviable el brute-force con GPUs.
# Es la misma librería y API que recomienda la doc oficial de FastAPI hoy.
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Convierte una contraseña en texto plano en un hash irreversible.
    """
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
      Verifica si una contraseña en texto plano coincide con un hash
    """
    return password_hash.verify(plain_password, hashed_password)

def create_access_token(subject: str, expires_minutes: int | None = None) -> str:
    """
    Crea un JWT con subject y fecha de expiración.

    La expiración usa UTC para evitar problemas de uso horario.
    """
    payload = {"sub": subject}
    minutes = (
        expires_minutes
        if expires_minutes is not None
        else ACCESS_TOKEN_EXPIRE_MINUTES
    )
    expire = datetime.now(timezone.utc) + timedelta(minutes=minutes)

    payload["exp"] = expire
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    """ Decodifica y verifica la firma de un JWT. """
    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )
    
    