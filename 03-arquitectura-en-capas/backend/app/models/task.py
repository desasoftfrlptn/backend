"""
Modelo de la entidad Task — SQLModel.

SQLModel une dos mundos en una sola clase:
  - el MODELO DE TABLA (mapea la tabla `tasks` en PostgreSQL)
  - el SCHEMA de validación (Pydantic: valida y serializa JSON)

En el Módulo 02 teníamos dos cosas separadas y a mano:
  1. `schema.sql`  → la tabla (SQL crudo)
  2. clases Pydantic → la validación de la API

Ahora UNA clase describe la tabla, y heredando definimos qué entra y
qué sale por la API. Menos código, más claridad.

OJO CON ESTO (vale oro):
    Los modelos con `table=True` NO validan al instanciar. `Task(title="")`
    no explota: SQLModel lo permite. La validación real vive en los SCHEMAS
    (`TaskCreate`, `TaskUpdate`), que son modelos Pydantic "puros". Por eso
    los validadores de abajo van en los schemas y NO en `TaskBase`.
"""

from datetime import datetime

from pydantic import field_validator
from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel


class TaskBase(SQLModel):
    """
    Los campos comunes a todas las "vistas" de una tarea.

    Acá vive lo mínimo que define a una tarea: su título. Las demás
    clases heredan de acá para no repetir campos.
    """

    title: str = Field(min_length=1, max_length=200, index=True)


class Task(TaskBase, table=True):
    """
    La TABLA. `table=True` le dice a SQLModel: "esta clase es una tabla".

    Mapea (casi) 1 a 1 la tabla `tasks` del Módulo 02:
      - id          → primary key
      - completed   → boolean, false por defecto
      - created_at  → timestamp que genera LA BASE (server_default)

    Fijate la diferencia clave con el Módulo 02: ya no hay `schema.sql`.
    El ORM genera el `CREATE TABLE` desde esta clase.
    """

    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True)

    completed: bool = Field(default=False)

    # server_default=func.now() → la BASE genera la fecha (como el
    # `DEFAULT NOW()` del módulo 02). El código Python no la inventa.
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    )


class TaskCreate(TaskBase):
    """Lo que el cliente envía para CREAR: solo el título."""

    @field_validator("title")
    @classmethod
    def title_no_puede_quedar_vacio(cls, value: str) -> str:
        """
        `min_length=1` rechaza `""`... pero NO rechaza `"   "` (tres
        espacios miden 3). Sin esto, el `strip()` del service dejaría el
        título en `""` y se guardaría una tarea sin título.

        Fijate que acá NO normalizamos: solo RECHAZAMOS. El `strip()` es
        una regla de negocio y vive en el service. Si normalizáramos acá,
        le robaríamos la lección al service.
        """
        if not value.strip():
            raise ValueError("El título no puede estar vacío")
        return value


class TaskUpdate(SQLModel):
    """
    Lo que el cliente envía para ACTUALIZAR: campos OPCIONALES.

    Al ser todo opcional, permitimos actualizaciones parciales:
      - solo el título
      - solo el estado `completed`
      - ambos
    """

    title: str | None = Field(default=None, min_length=1, max_length=200)
    completed: bool | None = None

    @field_validator("title")
    @classmethod
    def title_no_puede_quedar_vacio(cls, value: str | None) -> str:
        """
        Este validador SOLO se ejecuta si `title` vino en el body (Pydantic
        no valida campos ausentes). Así el PATCH parcial sigue funcionando:
        `{"completed": true}` no pasa por acá.

        Rechazamos dos casos que antes terminaban en un 500:
          - `{"title": null}`  → la columna es NOT NULL (IntegrityError)
          - `{"title": "   "}` → el strip() lo dejaría vacío
        """
        if value is None:
            raise ValueError("El título no puede ser nulo")
        if not value.strip():
            raise ValueError("El título no puede estar vacío")
        return value


class TaskRead(TaskBase):
    """Lo que la API devuelve: la tarea completa (id + estado + fecha)."""

    id: int
    completed: bool
    created_at: datetime
