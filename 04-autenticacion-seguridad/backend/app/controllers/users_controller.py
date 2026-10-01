"""
Capa de presentación (Controller) — endpoints del usuario autenticado.
"""

from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.models.user import User, UserRead

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_user)):
    """
    GET /api/users/me — devuelve el usuario autenticado.
    """
    return current_user
