"""
Capa de datos (Repository) — SQL con el ORM.

Antes (Módulo 02) cada endpoint escribía SQL crudo con psycopg:

    cur.execute("SELECT id, title, completed, created_at FROM tasks ...")

Ahora el ORM traduce Python a SQL. En vez de escribir el SELECT a mano,
escribimos `select(Task)` y SQLModel genera la consulta:

    session.exec(select(Task).order_by(Task.id)).all()

La lección: el ORM escribe el SQL por vos. Vos pensás en OBJETOS
(`Task`), no en filas y columnas.
"""

from sqlalchemy import func
from sqlmodel import Session, select

from app.models.task import Task, TaskUpdate


class TaskRepository:
    """
    Acceso a datos de la entidad Task.

    Recibe una `Session` por el constructor (se la inyecta la capa de
    arriba, ver dependencies.py). No la crea él: así el repository no
    sabe de dónde sale la conexión, solo la usa.
    """

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
        """Crea una tarea nueva y devuelve la instancia persistida."""
        task = Task(title=title)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)  # trae el id y created_at que generó la base
        return task

    def update(self, task: Task, data: TaskUpdate) -> Task:
        """
        Actualiza una tarea con los campos enviados.

        `model_dump(exclude_unset=True)` devuelve SOLO los campos que el
        cliente mandó. Así soportamos actualización parcial: si solo vino
        `completed`, no tocamos el `title`.
        """
        changes = data.model_dump(exclude_unset=True)
        for field, value in changes.items():
            setattr(task, field, value)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        """Borra una tarea de la base."""
        self.session.delete(task)
        self.session.commit()

    def count(self) -> int:
        """Cuenta las tareas (para el health check)."""
        # El conteo lo hace la BASE, no Python: `SELECT count(*) FROM tasks`.
        # Traer todas las filas para contarlas con len() funciona con 10
        # tareas y se cae con 100.000. No escales con los datos al pedo.
        statement = select(func.count()).select_from(Task)
        return self.session.exec(statement).one()
