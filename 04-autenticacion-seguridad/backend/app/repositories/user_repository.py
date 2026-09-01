"""
Capa de datos (Repository) — acceso a la entidad User.

Usamos el ORM (SQLModel). Pensamos en objetos (`User`), no en filas y
columnas. El repository NO sabe de HTTP ni de reglas de negocio: solo habla
con la base. Devuelve `None` si no encuentra; el que decide qué significa
eso (401, 409) es la capa de arriba.
"""

from sqlmodel import Session, select

from app.models.user import User


class UserRepository:
    """Acceso a datos de la entidad User."""

    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str) -> User | None:
        """Devuelve el usuario con ese email, o None si no existe."""
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()

    def get_by_id(self, user_id: int) -> User | None:
        """Devuelve el usuario por id, o None si no existe."""
        return self.session.get(User, user_id)

    def create(self, email: str, hashed_password: str) -> User:
        """Crea un usuario y devuelve la instancia persistida (con id y fecha)."""
        user = User(email=email, hashed_password=hashed_password)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def count(self) -> int:
        # EJEMPLO resuelto — el health check usa este método.
        statement = select(User)
        return len(self.session.exec(statement).all())
