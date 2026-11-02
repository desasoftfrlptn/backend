"""
Capa de presentación (Controller) — endpoints de /api/tasks.

Fijate qué HACE y qué NO hace el controller:
  - SÍ: define rutas, métodos, status codes, valida el body (Pydantic).
  - SÍ: traduce "no existe" (None del service) a un 404.
  - NO: toca la base (no hay SQL acá).
  - NO: aplica reglas de negocio (eso es del service).

En el Módulo 02 todo esto estaba mezclado en un solo main.py. Ahora
cada endpoint delega y queda chiquito.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_task_service
from app.models.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskRead])
def list_tasks(service: TaskService = Depends(get_task_service)):
    """GET /api/tasks — listar todas las tareas."""
    return service.list_tasks()


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, service: TaskService = Depends(get_task_service)):
    """GET /api/tasks/{id} — obtener UNA tarea."""
    task = service.get_task(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea {task_id} no encontrada",
        )
    return task


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(body: TaskCreate, service: TaskService = Depends(get_task_service)):
    """POST /api/tasks — crear una tarea."""
    return service.create_task(body)


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    body: TaskUpdate,
    service: TaskService = Depends(get_task_service),
):
    """
    PATCH /api/tasks/{id} — actualizar título y/o estado.

    Es PATCH (no PUT) porque es una actualización PARCIAL: podés mandar
    solo `{"completed": true}` o solo `{"title": "nuevo"}` o ambos.
    """
    task = service.update_task(task_id, body)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea {task_id} no encontrada",
        )
    return task


@router.delete("/{task_id}")
def delete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    """DELETE /api/tasks/{id} — eliminar una tarea."""
    if not service.delete_task(task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea {task_id} no encontrada",
        )
    return {"ok": True}
