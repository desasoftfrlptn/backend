from typing import Annotated, Callable

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from jwt import InvalidTokenError

from app import security, storage
from app.models import Role, User

bearer_scheme = HTTPBearer(auto_error=False)

def get_current_user(
    request: Request,
    credentials: Annotated[dict | None, Depends(bearer_scheme)],
) -> User:
    """Quién sos: decodifica el JWT y carga el usuario desde storage."""
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

    request.state.token_payload = payload
    return user

def require_role(required: Role) -> Callable:
    """Exige que el usuario tenga el rol `required` (o 403)."""

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

def require_scope(required: str) -> Callable:
    """Exige que el TOKEN tenga `required` en su scope (o 403)."""

    def checker(
        request: Request,
        current_user: Annotated[User, Depends(get_current_user)],
    ) -> User:
        payload = request.state.token_payload
        token_scope = payload.get("scope", "")
        if required not in token_scope.split():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El token no tiene el scope necesario para esta operación",
            )
        return current_user

    return checker
