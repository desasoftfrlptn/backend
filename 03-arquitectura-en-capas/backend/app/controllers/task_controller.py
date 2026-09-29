"""
Capa de presentación (Controller) — los endpoints HTTP.

COMPLETÁ los endpoints marcados con TODO. El controller:
  - recibe el request y delega en el service
  - traduce `None` (o `False`) del service a un `404` con HTTPException
  - NO toca la base ni aplica reglas de negocio

MIRÁ `health_controller.py` (ya viene resuelto): es tu ejemplo de cómo
recibir el service con `Depends(get_task_service)`.

Endpoints a implementar:
  GET    /api/tasks           → list_tasks
  POST   /api/tasks           → create_task (status 201)
  GET    /api/tasks/{task_id} → get_task
  PATCH  /api/tasks/{task_id} → update_task
  DELETE /api/tasks/{task_id} → delete_task
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_task_service
from app.models.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskRead])
def list_tasks(service: TaskService = Depends(get_task_service)):
    return service.list_tasks()


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int , service: TaskService = Depends(get_task_service)):
  task = service.get_task(task_id)
  if task is None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Tarea {task_id} no encontrada",
    )
  return task

@router.post("", response_model = TaskRead, status_code = status.HTTP_201_CREATED)
def create_task(body: TaskCreate, service: TaskService = Depends(get_task_service)):
  try:
    return service.create_task(body)
  except ValueError as error:
    # El service avisó que se violó una regla de negocio. Acá —y solo
    # acá— eso se traduce a HTTP.
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(error),
    )

@router.patch("/{task_id}", response_model = TaskRead)
def update_task(task_id: int, body: TaskUpdate, service: TaskService = Depends(get_task_service)):
  try:
    task = service.update_task(task_id, body)
  except ValueError as error:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(error),
    )
  if task is None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Tarea {task_id} no encontrada",
    )
  return task

@router.delete("/{task_id}")
def delete_task(task_id: int, service: TaskService = Depends(get_task_service)):
  ok = service.delete_task(task_id)
  if not ok:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Tarea {task_id} no encontrada",
    )
  return {"ok": True}