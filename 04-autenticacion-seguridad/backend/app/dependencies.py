"""
Inyección de dependencias — el "cableado" entre capas + AUTENTICACIÓN.

    get_session          → crea una Session por request
    get_user_repository  → recibe la Session, devuelve un repository
    get_auth_service     → recibe el repository, devuelve un service
    get_current_user     → recibe el token + el repository, devuelve el User

`get_current_user` es LA lección de hoy: cómo un endpoint sabe QUIÉN está
hablando. Es una dependencia: cualquier endpoint que la pida en `Depends()`
queda protegido (si falla, el endpoint nunca se ejecuta).

El 401 vive acá, que es la capa HTTP. `decode_token` solo deja propagar la
excepción del JWT; la traducción a status code la hacemos acá. Es EXACTAMENTE
el mismo criterio que el 404 del Módulo 03.
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

# El "extractor" de tokens: busca el token en el header `Authorization: Bearer
# <token>`. El `tokenUrl` es la ruta del login (aparece en "Authorize" del Swagger).
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

    - Decodifica el token; si falla (firma inválida, expirado) → 401.
    - Extrae el `sub` (el user id) y busca el usuario.
    - Si el usuario no existe (token válido pero usuario borrado) → 401.
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
