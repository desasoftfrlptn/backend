"""
Capa de presentación (Controller) — endpoints de AUTENTICACIÓN.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_auth_service
from app.models.user import Token, UserCreate, UserLogin, UserRead
from app.security import create_access_token
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(body: UserCreate, service: AuthService = Depends(get_auth_service)):
    """
    POST /api/auth/register — crea un usuario.
    """
    user = service.register_user(body)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El email ya está registrado",
        )
    return user


@router.post("/login", response_model=Token)
def login(body: UserLogin, service: AuthService = Depends(get_auth_service)):
    """
    POST /api/auth/login — verifica credenciales y emite un JWT.
    """
    user = service.authenticate_user(body.email, body.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(subject=str(user.id))
    return {"access_token": access_token, "token_type": "bearer"}