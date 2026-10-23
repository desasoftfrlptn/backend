# Guía del Alumno — Arquitectura en Capas + ORM (taller por grupos)

> **Módulo 03 — Desarrollo de Software 2026**
> **Modalidad**: taller por grupos con descubrimiento. **60 minutos.**
> Ya leíste el `MATERIAL_PREVIO.md`. Ahora a construir.

---

## Cómo funciona este taller

1. Tu **fork** ya trae el **esqueleto** del backend (todo lo demás viene hecho).
2. Tu grupo completa **tres archivos** siguiendo las consignas.
3. Después de cada fase, **verificás** que funcione antes de avanzar.
4. Si te trabás: preguntale al docente. Pero él no te da la respuesta — te
   hace una pregunta que te ayuda a encontrarla vos.

**Roles dentro del grupo** (rotan en cada fase): **Piloto** (escribe),
**Navegante** (lee consignas y anticipa errores), **Investigador** (busca en
la doc o en el código del Módulo 02).

---

## Qué ya viene hecho en tu fork (NO se modifica)

```
03-arquitectura-en-capas/backend/
├── app/
│   ├── main.py                    # entrypoint (dado)
│   ├── database.py                # engine + session (dado)
│   ├── dependencies.py            # cableado Depends() (dado)
│   ├── models/task.py             # modelo SQLModel (dado)
│   ├── controllers/
│   │   └── health_controller.py   # EJEMPLO de controller (dado)
│   ├── repositories/
│   │   └── task_repository.py     # ⬅️ VOS LO COMPLETÁS
│   ├── services/
│   │   └── task_service.py        # ⬅️ VOS LO COMPLETÁS
│   └── controllers/
│       └── task_controller.py     # ⬅️ VOS LO COMPLETÁS
└── ...
```

El frontend (`../frontend/`) ya viene **completo y funcionando**. No se
construye en el taller: se conecta al final.

---

## Fase 0 — Setup (5 min)

```bash
cd 03-arquitectura-en-capas/backend
cp .env.example .env      # completá DATABASE_URL (la del Módulo 02)
uv sync                   # instala SQLModel + FastAPI
uv run -m app.main        # levanta el server en :8000
```

Verificá:

```bash
curl http://localhost:8000/api/health
# → {"status":"Funciona","service":"03-...","db":"conectada","tasks_count":0}
```

> El health **ya funciona** porque usa el `health_controller` (dado) y el
> `count()` del repository. Espera… ¿el repository no estaba incompleto?
> Fijate: el `count()` ya viene escrito como EJEMPLO. Los otros métodos son
> los tuyos.

---

## Fase 1 — Repository: la capa de datos (15 min)

**Objetivo**: completar `app/repositories/task_repository.py`.

### El esqueleto

```python
from sqlmodel import Session, select
from app.models.task import Task, TaskUpdate


class TaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def list_all(self) -> list[Task]:
        # TODO: devolver todas las tareas ordenadas por id
        ...

    def get_by_id(self, task_id: int) -> Task | None:
        # TODO: devolver una tarea por id, o None si no existe
        ...

    def create(self, title: str) -> Task:
        # TODO: crear una tarea y devolverla (con id y created_at)
        ...

    def update(self, task: Task, data: TaskUpdate) -> Task:
        # TODO: aplicar SOLO los campos enviados y devolver la tarea
        ...

    def delete(self, task: Task) -> None:
        # TODO: borrar la tarea
        ...

    def count(self) -> int:
        # (ya viene hecho — es tu ejemplo)
        statement = select(Task)
        return len(self.session.exec(statement).all())
```

### Consignas (descubrimiento)

1. **`list_all`**: en el Módulo 02 escribías
   `SELECT ... FROM tasks ORDER BY id`. Ahora usás `select(Task)` + `order_by`.
   ¿Cómo ejecutás un `select` en una sesión? (pista: `session.exec(...)`).
2. **`get_by_id`**: no hace falta un `select` con `WHERE`. El ORM tiene un
   atajo: `session.get(Task, task_id)`. ¿Qué devuelve si no existe?
3. **`create`**: creás el objeto `Task(title=...)`, lo agregás con
   `session.add(...)`, hacés `commit()`. Después de commitear, ¿cómo traés el
   `id` y el `created_at` que generó la base? (pista: `refresh`).
4. **`update`**: el `data` es un `TaskUpdate` con campos opcionales. Tenés que
   aplicar **solo los que vinieron**. `data.model_dump(exclude_unset=True)` te
   da un dict con solo los campos enviados. Recorrelo y usá `setattr`.
5. **`delete`**: `session.delete(...)` + `commit()`.

> 🔎 **Pregunta de la fase**: ¿por qué el repository NO devuelve un error 404
> ni un mensaje HTTP? (respuesta al final de la fase 2).

**Verificá** con Swagger (`http://localhost:8000/docs`) o Postman: creá una
tarea desde el endpoint de `POST`… esperá, el controller tampoco está. **Usá
el checkpoint del docente** para probar el repository: mientras tanto,
ejecutá el health (usa `count`) para confirmar que el repository compila.

---

## Fase 2 — Service: la capa de negocio (10 min)

**Objetivo**: completar `app/services/task_service.py`.

### El esqueleto

```python
from app.models.task import Task, TaskCreate, TaskUpdate
from app.repositories.task_repository import TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def list_tasks(self) -> list[Task]:
        # TODO
        ...

    def get_task(self, task_id: int) -> Task | None:
        # TODO
        ...

    def create_task(self, body: TaskCreate) -> Task:
        # TODO: normalizar el título (strip) y crear
        ...

    def update_task(self, task_id: int, body: TaskUpdate) -> Task | None:
        # TODO: si no existe, devolver None; si existe, actualizar
        ...

    def delete_task(self, task_id: int) -> bool:
        # TODO: devolver True si existía y se borró, False si no
        ...

    def count_tasks(self) -> int:
        # TODO
        ...
```

### Consignas (descubrimiento)

1. **El service delega**: casi todos los métodos son "llamar al repository y
   devolver". La gracia está en dos detalles.
2. **`create_task`**: el `strip()` del título. En el Módulo 02 eso estaba
   DENTRO del endpoint. Ahora es una **regla de negocio**, por eso vive acá.
3. **`update_task` / `delete_task`**: si la tarea no existe, ¿devolvés `None`
   (o `False`) o lanzás un error? **RESPUESTA CLAVE**: el service **no sabe de
   HTTP**, así que no puede decir "404". Devuelve `None`/`False` y que la capa
   de arriba decida. Esa es la lección de hoy.

> 🧠 **La pregunta de la fase 1, respondida**: el repository (ni el service)
> devuelven 404 porque **404 es una preocupación HTTP**, y ellos no saben qué
> es HTTP. Eso lo decide el controller.

**Verificá** cuando completes el controller (fase 3).

---

## Fase 3 — Controller: la capa HTTP (15 min)

**Objetivo**: completar `app/controllers/task_controller.py`.

### El esqueleto

```python
from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_task_service
from app.models.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskRead])
def list_tasks(service: TaskService = Depends(get_task_service)):
    # TODO: delegar en el service
    ...

# ... y también: GET /{task_id}, POST, PATCH /{task_id}, DELETE /{task_id}
```

### Consignas (descubrimiento)

1. **Fijate en `health_controller.py`** (el ejemplo dado): cómo recibe el
   service con `Depends(get_task_service)`. Copiá ese patrón.
2. **Los 5 endpoints**: GET lista, GET una, POST, PATCH, DELETE. Las rutas y
   `response_model` están en la tabla del SPEC. Mirá `health_controller.py` y
   completá.
3. **El 404 vive acá**: cuando el service te devuelve `None` (o `False`),
   `raise HTTPException(status_code=404, detail=f"Tarea {task_id} no encontrada")`.
4. **POST devuelve 201**: `status_code=status.HTTP_201_CREATED`.

> 🧠 **La lección se cierra**: el controller es el único que "habla HTTP".
> Traduce `None` → 404, y `Task` → JSON (vía `response_model`). No hay una
> sola línea de SQL ni de regla de negocio acá.

**Verificá** el CRUD completo:

```bash
curl -X POST http://localhost:8000/api/tasks -H "Content-Type: application/json" -d '{"title":"  Probar capas  "}'
# → title normalizado: "Probar capas" (¡el strip del service!)

curl http://localhost:8000/api/tasks
curl http://localhost:8000/api/tasks/1
curl -X PATCH http://localhost:8000/api/tasks/1 -H "Content-Type: application/json" -d '{"completed":true}'
curl -X PATCH http://localhost:8000/api/tasks/1 -H "Content-Type: application/json" -d '{"title":"Título editado"}'
curl http://localhost:8000/api/tasks/999   # → 404
curl -X DELETE http://localhost:8000/api/tasks/1
```

---

## Fase 4 — Frontend TypeScript (10 min)

El frontend ya viene **completo**. Tu trabajo es conectarlo y verificar el
CRUD de punta a punta.

```bash
cd ../frontend
pnpm install
pnpm dev        # levanta en :5173
```

Abrí `http://localhost:5173` y hacé el CRUD completo desde la UI:
crear, editar título, tachar (toggle), eliminar.

**Descubrí los tipos**: abrí `src/types.ts`. Ese `interface Task` **es el
contrato de la API, escrito como tipo**. Compáralo con el `TaskRead` del
backend (`app/models/task.py`). ¿Ves cómo coinciden campo por campo?

> 🧠 **Pregunta de cierre**: en el Módulo 01/02 el frontend era JS. ¿Qué
> error te habría avisado el compilador ahora que antes no? (ej: escribir mal
> `completed` como `completado`).

---

## Fase 5 — Verificación final y reflexión (5 min)

Completá la collection de Postman (`postman/03-arquitectura-en-capas...`)
con el flujo feliz + casos límite, y preparate para responder en voz alta:

1. ¿Qué ganamos separando en capas?
Cada capa cambia por una sola razón, si tegno que cambiar la base de datos, solo tocás el repository, si una regla de negocio cambia solo tocas el service, si cambia el http solo toco el controller.
2. ¿Dónde vive el 404 y por qué no en el service?
El 404 esta en el controller, ya que, el 404 es un codigo de estado http.
3. ¿Qué SQL que escribías a mano en el 02 ahora escribe el ORM?
4. ¿Qué te da TypeScript que JavaScript no te daba?
Verificacion de tipos en tiempo de compilacion, si escribo mal un campo TypeScript lo marca como error antes de correr el codigo.
---

## 🔐 La solución

> La solución completa **NO está en este repo**. El docente la libera al
> final de la clase en la rama `solucion`. Cuando se anuncie, hacé:
>
> ```bash
> git fetch origin
> git diff main..origin/solucion
> ```
>
> Y compará tu código con la solución.
>
> **La gracia del taller está en descubrirlo vos.** Si la solución estuviera
> acá desde el principio, no aprenderías nada.
