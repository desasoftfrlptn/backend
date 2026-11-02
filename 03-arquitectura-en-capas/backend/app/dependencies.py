"""
Inyección de dependencias — el "cableado" entre capas.

Acá CONECTAMOS las capas. Le decimos a FastAPI cómo construir cada
pieza cuando un endpoint la pide:

    Controller ──► Service ──► Repository ──► Session ──► PostgreSQL

Cada función de acá es una dependencia que FastAPI resuelve con
`Depends()`. La cadena es explícita y en cascada:

    get_session         → crea una Session por request (vive en database.py)
    get_task_repository → recibe la Session, devuelve un repository
    get_task_service    → recibe el repository, devuelve un service

Acá solo RE-EXPORTAMOS `get_session`: la fuente de verdad es `database.py`.
Tener dos copias de la misma dependencia es una bomba de tiempo (cambiás
una y la otra sigue con el comportamiento viejo).

La regla de oro: cada capa recibe lo que necesita DESDE AFUERA, nunca
lo construye por su cuenta. Eso es Inversión de Control (IoC), y es lo
que hace que las capas sean intercambiables y testeables.
"""

from fastapi import Depends
from sqlmodel import Session

from app.database import get_session
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService


def get_task_repository(session: Session = Depends(get_session)) -> TaskRepository:
    """Construye el repository con la Session del request."""
    return TaskRepository(session)


def get_task_service(
    repository: TaskRepository = Depends(get_task_repository),
) -> TaskService:
    """Construye el service con su repository."""
    return TaskService(repository)
