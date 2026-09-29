"""
Capa de datos (Repository) — SQL con el ORM.

COMPLETÁ los métodos marcados con TODO. Usá el ORM (SQLModel), no SQL
crudo. Recordá el Módulo 02: antes escribías el SELECT a mano; ahora el
ORM lo genera por vos. Pensás en objetos (`Task`), no en filas y columnas.

Pistas rápidas (desarrollalas — el GUIA_ALaUMNO tiene las consignas):
  - listar todas      → select(Task) + order_by + session.exec(...)
  - leer una por id   → session.get(Task, task_id)
  - crear             → session.add(task) + commit() + refresh(task)
  - actualizar parcial→ data.model_dump(exclude_unset=True) + setattr
  - borrar            → session.delete(task) + commit()
"""

from sqlmodel import Session, select

from app.models.task import Task, TaskUpdate


class TaskRepository:
    """Acceso a datos de la entidad Task."""

    def __init__(self, session: Session):
        self.session = session

    def list_all(self) -> list[Task]:
        """Devuelve todas las tareas ordenadas por id."""
        statement = select(Task).order_by(Task.id)
        return list(self.session.exec(statement).all())

    def get_by_id(self, task_id: int) -> Task | None:
        """Devuelve una tarea por id, o None si no existe."""
        return self.session.get(Task, task_id)

    def create(self, title: str) -> Task:
        """Crea una tarea y devuelve la instancia persistida (con id y fecha)."""
        task = Task(title = title)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def update(self, task: Task, data: TaskUpdate) -> Task:
        """Actualiza SOLO los campos enviados y devuelve la tarea."""
        # exclude_unset → solo los campos que el cliente mandó.
        # exclude_none  → un `null` explícito NO borra el campo. Ninguna
        # columna admite NULL, así que sin esto un {"title": null} rompe
        # la restricción NOT NULL de la base.
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        for key, value in update_data.items():
            setattr(task, key, value)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        """Borra la tarea de la base."""
        self.session.delete(task)
        self.session.commit()

    def count(self) -> int:
        # EJEMPLO resuelto — te sirve de referencia para los demás.
        statement = select(Task)
        return len(self.session.exec(statement).all())
