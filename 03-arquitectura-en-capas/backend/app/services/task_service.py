"""
Capa de negocio (Service) — la lógica de la aplicación.

El service orquesta: recibe pedidos "en lenguaje de negocio", aplica
reglas y delega el acceso a datos en el repository.

Una regla importante que se ve acá: el service NO devuelve errores
HTTP. Si una tarea no existe, devuelve `None` (o `False`). Es el
CONTROLLER (la capa de arriba) quien decide cómo comunicarlo al
cliente (404). El service no sabe qué es un status code.
"""

from app.models.task import Task, TaskCreate, TaskUpdate
from app.repositories.task_repository import TaskRepository


class TaskService:
    """Casos de uso de la entidad Task."""

    def __init__(self, repository: TaskRepository):
        # Recibe su repository por el constructor (inyección de
        # dependencias). No lo crea: se lo dan desde afuera.
        self.repository = repository

    def list_tasks(self) -> list[Task]:
        return self.repository.list_all()

    def get_task(self, task_id: int) -> Task | None:
        return self.repository.get_by_id(task_id)

    def create_task(self, body: TaskCreate) -> Task:
        # Regla de negocio: normalizamos el título (sin espacios en los
        # bordes). Esto en el Módulo 02 estaba dentro del endpoint.
        title = body.title.strip()
        return self.repository.create(title)

    def update_task(self, task_id: int, body: TaskUpdate) -> Task | None:
        task = self.repository.get_by_id(task_id)
        if task is None:
            return None  # el controller decidirá que es un 404

        # MISMA regla de negocio que en create: normalizamos el título.
        # Si no la aplicáramos acá, `PATCH {"title": "  x  "}` guardaría
        # los espacios y la regla quedaría a medias según el verbo HTTP.
        # Usamos model_copy para no mutar el DTO que nos pasaron.
        if body.title is not None:
            body = body.model_copy(update={"title": body.title.strip()})

        return self.repository.update(task, body)

    def delete_task(self, task_id: int) -> bool:
        task = self.repository.get_by_id(task_id)
        if task is None:
            return False
        self.repository.delete(task)
        return True

    def count_tasks(self) -> int:
        return self.repository.count()
