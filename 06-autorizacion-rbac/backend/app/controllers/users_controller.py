"""
Controller de usuarios: gestión de usuarios y roles (solo admin).

  GET   /api/users            → lista los usuarios de tu empresa
  GET   /api/users/{id}       → detalle de un usuario
  PATCH /api/users/{id}/role  → cambia el rol de un usuario

Las tres operaciones son solo para admin y siempre dentro de su propia empresa.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app import storage
from app.dependencies import require_role
from app.models import Role, RoleChange, User, UserRead

router = APIRouter(prefix="/api", tags=["2 · Usuarios (admin)"])


def _verificar_misma_empresa(user: User, current_user: User) -> None:
    if user.tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ese usuario pertenece a otra empresa",
        )


@router.get("/users", response_model=list[UserRead])
def list_users(
    current_user: User = Depends(require_role(Role.ADMIN)),
):
    """Lista los usuarios de tu empresa (el storage filtra por tenant)."""
    return storage.list_users(tenant_id=current_user.tenant_id)


@router.get("/users/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    current_user: User = Depends(require_role(Role.ADMIN)),
):
    """Detalle de un usuario. 404 si no existe, 403 si es de otra empresa."""
    user = storage.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    _verificar_misma_empresa(user, current_user)
    return user


@router.patch("/users/{user_id}/role", response_model=UserRead)
def change_role(
    user_id: int,
    body: RoleChange,
    current_user: User = Depends(require_role(Role.ADMIN)),
):
    """Cambia el rol de un usuario. Solo admin y solo dentro de su empresa."""
    user = storage.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    _verificar_misma_empresa(user, current_user)
    return storage.set_user_role(user_id, body.role)
