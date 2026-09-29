"""
Capa de negocio (Service) — la lógica de la aplicación.

COMPLETÁ los métodos marcados con TODO. El service delega el acceso a
datos en el repository y aplica las reglas de negocio.

LA DECISIÓN CLAVE DE HOY:
    Cuando la tarea no existe, el service devuelve `None` (o `False`).
    NO lanza un error 404. ¿Por qué? Porque 404 es HTTP, y el service
    NO sabe qué es HTTP. El controller (la capa de arriba) lo traduce.
"""

from app.models.task import Task, TaskCreate, TaskUpdate
from app.repositories.task_repository import TaskRepository


class TaskService:
    """Casos de uso de la entidad Task."""

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def list_tasks(self) -> list[Task]:
        return self.repository.list_all()

    def get_task(self, task_id: int) -> Task | None:
        return self.repository.get_by_id(task_id)

    def create_task(self, body: TaskCreate) -> Task:
        # Normalizar el título es una REGLA DE NEGOCIO: vive acá, no en
        # el controller. Un título que queda vacío tras el .strip() no es
        # una tarea válida, así que lo rechazamos con un ValueError.
        # Ojo: ValueError es Python puro, NO es HTTP. El service sigue sin
        # saber qué es un 400 — eso lo traduce el controller.
        return self.repository.create(self._normalize_title(body.title))

    def update_task(self, task_id: int, body: TaskUpdate) -> Task | None:
        task = self.repository.get_by_id(task_id)
        if task is None:
            return None
        # Misma regla que en create: si mandan título, se normaliza igual.
        if body.title is not None:
            body.title = self._normalize_title(body.title)
        return self.repository.update(task, body)

    def delete_task(self, task_id: int) -> bool:
        task = self.repository.get_by_id(task_id)
        if task is None:
            return False
        self.repository.delete(task)
        return True
        # Pista: devolvé True si existía y se borró, False si no.

    @staticmethod
    def _normalize_title(title: str) -> str:
        """Recorta espacios y exige que quede algo. Regla de negocio."""
        normalized = title.strip()
        if not normalized:
            raise ValueError("El título no puede estar vacío")
        return normalized

    def count_tasks(self) -> int:
        # EJEMPLO resuelto — el health check usa este método.
        # Mirá cómo delega en el repository: así se hace en TODOS los métodos.
        return self.repository.count()
