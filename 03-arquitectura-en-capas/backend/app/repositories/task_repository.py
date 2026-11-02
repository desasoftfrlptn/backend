"""
Capa de datos (Repository) — SQL con el ORM.

COMPLETÁ los métodos marcados con TODO. Usá el ORM (SQLModel), no SQL
crudo. Recordá el Módulo 02: antes escribías el SELECT a mano; ahora el
ORM lo genera por vos. Pensás en objetos (`Task`), no en filas y columnas.

Pistas rápidas (desarrollalas — el GUIA_ALUMNO tiene las consignas):
  - listar todas      → select(Task) + order_by + session.exec(...)
  - leer una por id   → session.get(Task, task_id)
  - crear             → session.add(task) + commit() + refresh(task)
  - actualizar parcial→ data.model_dump(exclude_unset=True) + setattr
  - borrar            → session.delete(task) + commit()
"""

from sqlalchemy import func
from sqlmodel import Session, select

from app.models.task import Task, TaskUpdate


class TaskRepository:
    """Acceso a datos de la entidad Task."""

    def __init__(self, session: Session):
        self.session = session

    def list_all(self) -> list[Task]:
        """Devuelve todas las tareas ordenadas por id."""
        raise NotImplementedError("TODO: implementar list_all")

    def get_by_id(self, task_id: int) -> Task | None:
        """Devuelve una tarea por id, o None si no existe."""
        raise NotImplementedError("TODO: implementar get_by_id")

    def create(self, title: str) -> Task:
        """Crea una tarea y devuelve la instancia persistida (con id y fecha)."""
        raise NotImplementedError("TODO: implementar create")

    def update(self, task: Task, data: TaskUpdate) -> Task:
        """Actualiza SOLO los campos enviados y devuelve la tarea."""
        raise NotImplementedError("TODO: implementar update")

    def delete(self, task: Task) -> None:
        """Borra la tarea de la base."""
        raise NotImplementedError("TODO: implementar delete")

    def count(self) -> int:
        # EJEMPLO resuelto — te sirve de referencia para los demás.
        # El conteo lo hace la BASE (`SELECT count(*) FROM tasks`), no
        # Python. Traer todas las filas para contarlas con len() es el
        # error clásico: funciona con 10 tareas y se cae con 100.000.
        statement = select(func.count()).select_from(Task)
        return self.session.exec(statement).one()
