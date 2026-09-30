

from fastapi import APIRouter, Depends, HTTPException, status

from app import storage
from app.dependencies import get_current_user, require_role
from app.models import Role, RoleChange, User, UserRead

router = APIRouter(prefix="/api", tags=["2 · Usuarios (admin)"])


@router.get("/users", response_model=list[UserRead])
def list_users(
    current_user: User = Depends(require_role(Role.ADMIN)), 
):  
    return storage.list_users(tenant_id=current_user.tenant_id)


@router.get("/users/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    current_user: User = Depends(require_role(Role.ADMIN)),
):
    """Detalle de un usuario. 404 si no existe; 403 si es de otra empresa."""
    user = storage.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    if user.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado para ver este usuario")
    return user


@router.patch("/users/{user_id}/role", response_model=UserRead)
def change_role(
    user_id: int,
    body: RoleChange,
    current_user: User = Depends(require_role(Role.ADMIN))
):
    """Cambia el rol de un usuario (la operación más sensible del sistema).

    Con esto un admin puede crear más admins o degradar a alguien. Por eso
    es la operación MÁS restringida: solo admin, y solo de su empresa.
    """
    user = storage.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    if user.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado para cambiar el rol de este usuario")  
    updated = storage.set_user_role(user_id, body.role)
    return updated  