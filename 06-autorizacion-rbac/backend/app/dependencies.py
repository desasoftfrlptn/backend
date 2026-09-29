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
    if credentials is None:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    try:
        payload = security.decode_token(credentials.credentials)
        user_id = int(payload["sub"])
    except Exception:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    user = storage.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario inexistente")

    request.state.token_payload = payload
    return user


def require_role(required: Role) -> Callable:
    def checker(current_user: Annotated[User, Depends(get_current_user)]) -> User:
        if current_user.role != required:
            raise HTTPException(status_code=403, detail="Rol insuficiente")
        return current_user
    return checker


def require_scope(required: str) -> Callable:
    def checker(
        request: Request,
        current_user: Annotated[User, Depends(get_current_user)],
    ) -> User:
        token_scope = request.state.token_payload.get("scope", "")
        if required not in token_scope.split():
            raise HTTPException(status_code=403, detail="Scope insuficiente")
        return current_user
    return checker