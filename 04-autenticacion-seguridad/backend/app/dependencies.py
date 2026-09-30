"""
Inyección de dependencias — el "cableado" entre capas + AUTENTICACIÓN.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlmodel import Session
from app.database import engine
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.security import decode_token
from app.services.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_session():
    """Una Session nueva por cada request."""
    with Session(engine) as session:
        yield session


def get_user_repository(session: Session = Depends(get_session)) -> UserRepository:
    """Construye el repository con la Session del request."""
    return UserRepository(session)


def get_auth_service(
    repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    """Construye el service con su repository."""
    return AuthService(repository)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    repository: UserRepository = Depends(get_user_repository),
) -> User:
    """
    Protege una ruta: resuelve QUIÉN es el usuario a partir del token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        user_id = int(payload["sub"])
    except InvalidTokenError:
        raise credentials_exception

    user = repository.get_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user