"""
Capa de negocio (Service) — los casos de uso de autenticación.
"""
from app.models.user import User, UserCreate
from app.repositories.user_repository import UserRepository
from app.security import hash_password, verify_password

class AuthService:
    """Casos de uso de autenticación: register y login."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register_user(self, body: UserCreate) -> User | None:
        """
        Registra un usuario nuevo. Devuelve el User creado, o None si el
        email ya está en uso.
        """
        email = body.email.lower().strip()
        if self.repository.get_by_email(email):
            return None
        hashed = hash_password(body.password)
        return self.repository.create(email, hashed)

    def authenticate_user(self, email: str, password: str) -> User | None:
        """
        Verifica credenciales. Devuelve el User si son válidas, None si no.
        """
        email = email.lower().strip()
        user = self.repository.get_by_email(email)
        if user is None:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def count_users(self) -> int:
        # EJEMPLO resuelto — el health check usa este método.
        return self.repository.count()