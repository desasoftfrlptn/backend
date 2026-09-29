"""
Dependencias de autorización.

- get_current_user: autenticación (401 si el token no sirve). Deja el payload
  del token en request.state para que require_scope lo pueda leer.
- require_role: exige un rol determinado (403 si el usuario tiene otro).
- require_scope: exige un scope en el token (403 si el token no lo trae).

El rol se relee del storage en cada request, así que un cambio de rol se nota
enseguida. El scope, en cambio, lo fija el login y viaja dentro del token.
"""

from typing import Annotated, Callable

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from jwt import InvalidTokenError

from app import security, storage
from app.models import Role, User

bearer_scheme = HTTPBearer(auto_error=False)


# ── 1 · Autenticación ──────────────────────────────────────────────────────


def get_current_user(
    request: Request,
    credentials: Annotated[dict | None, Depends(bearer_scheme)],
) -> User:
    """Quién sos: decodifica el JWT y carga el usuario desde storage.

    - Token ausente / inválido / expirado / usuario inexistente → 401.
    - Usuario cargado → se guarda el payload en `request.state.token_payload`
      para que require_scope (que sí lee del token) lo tenga a mano.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise credentials_exception

    try:
        payload = security.decode_token(credentials.credentials)
        user_id = int(payload["sub"])
    except (InvalidTokenError, KeyError, ValueError):
        raise credentials_exception

    user = storage.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception

    # El payload del token queda accesible para las dependencias que
    # autorizan por SCOPE. El rol, en cambio, se relee del usuario fresco.
    request.state.token_payload = payload
    return user


# ── 2 · Autorización por rol ───────────────────────────────────────────────


def require_role(required: Role) -> Callable:
    """Devuelve una dependencia que exige que el usuario tenga el rol `required`.

    Uso:
        current_user: User = Depends(require_role(Role.ADMIN))
    """
    def checker(
        current_user: Annotated[User, Depends(get_current_user)],
    ) -> User:
        if current_user.role != required:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tenés el rol necesario para esta operación",
            )
        return current_user
    return checker


# ── 3 · Autorización por scope del token ───────────────────────────────────


def require_scope(required: str) -> Callable:
    """Devuelve una dependencia que exige que el token tenga el scope `required`.

    Uso:
        current_user: User = Depends(require_scope("write"))

    Un admin que se logueó con scope "read" no puede escribir: el scope se lee
    del token y no del usuario.
    """
    def checker(
        request: Request,
        current_user: Annotated[User, Depends(get_current_user)],
    ) -> User:
        token_scope = request.state.token_payload.get("scope", "")
        if required not in token_scope.split():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El token no tiene el scope necesario para esta operación",
            )
        return current_user
    return checker
