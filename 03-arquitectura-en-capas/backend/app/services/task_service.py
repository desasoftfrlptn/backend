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
        raise NotImplementedError("TODO: implementar list_tasks")

    def get_task(self, task_id: int) -> Task | None:
        raise NotImplementedError("TODO: implementar get_task")

    def create_task(self, body: TaskCreate) -> Task:
        # Pista: normalizá el título con .strip() antes de crear.
        # Esa es una REGLA DE NEGOCIO, por eso vive acá (no en el controller).
        raise NotImplementedError("TODO: implementar create_task")

    def update_task(self, task_id: int, body: TaskUpdate) -> Task | None:
        # Pista: si no existe, devolvé None. Si existe, actualizá.
        # OJO: el PATCH también normaliza el título (la MISMA regla que
        # create). Si no lo hacés, `PATCH {"title": "  x  "}` guarda los
        # espacios y la regla de negocio queda a medias.
        raise NotImplementedError("TODO: implementar update_task")

    def delete_task(self, task_id: int) -> bool:
        # Pista: devolvé True si existía y se borró, False si no.
        raise NotImplementedError("TODO: implementar delete_task")

    def count_tasks(self) -> int:
        # EJEMPLO resuelto — el health check usa este método.
        # Mirá cómo delega en el repository: así se hace en TODOS los métodos.
        return self.repository.count()
