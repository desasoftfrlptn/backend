"""
Capa de negocio (Service) — los casos de uso de autenticación.

El service aplica las reglas de negocio y delega el acceso a datos en el
repository. Dos decisiones clave:

    1. ¿Dónde se hashea la contraseña? → ACÁ. Hashear es una regla de negocio:
       "todo usuario que se crea, se crea con su contraseña protegida".

    2. ¿El service devuelve un 401/409? → NO. Devuelve `None` para decir "no
       se pudo" y el controller decide el status code. Igual que el 404 del 03.

    3. Timing attack / user enumeration: para que "email inexistente" y
       "contraseña incorrecta" tarden lo MISMO (evitando que un atacante mida
       la diferencia y adivine emails), cuando el usuario no existe igual
       verificamos contra un hash falso. Así el costo de Argon2 siempre corre.
"""

from app.models.user import User, UserCreate
from app.repositories.user_repository import UserRepository
from app.security import hash_password, verify_password

# Un hash falso, calculado UNA vez al importar. Lo usamos en authenticate_user
# para igualar el tiempo de respuesta cuando el usuario no existe (mitigación
# del timing attack / user enumeration).
_DUMMY_HASH = hash_password("dummy-password-for-timing")


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
        if self.repository.get_by_email(email) is not None:
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
            # Mitigación del timing attack: verificamos contra un hash falso
            # para que "email inexistente" tarde lo mismo que "contraseña mal".
            verify_password(password, _DUMMY_HASH)
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def count_users(self) -> int:
        # EJEMPLO resuelto — el health check usa este método.
        return self.repository.count()
