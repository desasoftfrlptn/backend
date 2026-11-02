---
marp: true
theme: default
paginate: true
backgroundColor: #0f172a
color: #e2e8f0
style: |
  /* ---- Base ---- */
  section {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    padding: 36px 56px;
    background-color: #0f172a;
    color: #e2e8f0;
  }
  h1 { color: #f8fafc; font-size: 1.55em; }
  h2 { color: #f1f5f9; font-size: 1.25em; }
  h3 { color: #94a3b8; font-size: 1em; }
  h4 { color: #93c5fd; }
  strong { color: #f1f5f9; }
  em { color: #cbd5e1; }
  a { color: #93c5fd; }

  /* ---- Slides densas: un escalón SUAVE (0.95, no 0.92) ----
     Ojo: `smaller` se multiplica con pre/table. Antes
     0.92 x 0.82 x 29px = 21.9px de código -> chico en proyector. */
  section.smaller { font-size: 0.95em; }
  section.smaller h1 { font-size: 1.45em; }
  section.smaller h2 { font-size: 1.2em; }

  /* ---- Código ---- */
  code {
    color: #93c5fd;
    background: #1e293b;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.88em;
  }
  pre {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 0.88em;
    line-height: 1.35;
    color: #e2e8f0;
    /* Red de seguridad: si una línea es muy larga se envuelve,
       nunca se recorta (el overflow de Marp corta el texto en silencio). */
    white-space: pre-wrap;
    overflow-wrap: anywhere;
  }
  pre code {
    background: none;
    padding: 0;
    color: #e2e8f0;
  }

  /* ---- Resaltado sintáctico (paleta clara sobre fondo oscuro) ---- */
  pre code :is(.hljs-keyword, .hljs-doctag, .hljs-template-tag, .hljs-template-variable, .hljs-variable.language_, .hljs-selector-tag) { color: #f472b6 !important; }
  pre code :is(.hljs-string, .hljs-regexp, .hljs-meta .hljs-string) { color: #86efac !important; }
  pre code :is(.hljs-title, .hljs-title.function_, .hljs-title.class_, .hljs-name, .hljs-quote, .hljs-selector-pseudo) { color: #7dd3fc !important; }
  pre code :is(.hljs-attr, .hljs-attribute, .hljs-literal, .hljs-meta, .hljs-selector-attr, .hljs-selector-class, .hljs-selector-id, .hljs-variable) { color: #93c5fd !important; }
  pre code :is(.hljs-number, .hljs-symbol) { color: #fcd34d !important; }
  pre code :is(.hljs-operator, .hljs-params, .hljs-subst, .hljs-type) { color: #cbd5e1 !important; }
  pre code :is(.hljs-comment, .hljs-code, .hljs-formula) { color: #94a3b8 !important; font-style: italic; }
  pre code :is(.hljs-section, .hljs-bullet) { color: #f0abfc !important; font-weight: 700; }
  pre code .hljs-built_in { color: #fca5a5 !important; }

  /* ---- Tablas ---- */
  table {
    /* Marp pone display:block + width:max-content: el fondo ocupa 100%
       pero las columnas no se estiran y queda un bloque muerto. */
    display: table;
    font-size: 0.85em;
    background: #1e293b;
    border-radius: 8px;
    overflow: hidden;
    border-collapse: collapse;
    width: 100%;
  }
  thead { background: #334155; }
  th {
    color: #93c5fd;
    padding: 5px 10px;
    text-align: left;
    border-bottom: 2px solid #3b82f6;
    background: #334155;
  }
  td {
    color: #cbd5e1;
    padding: 5px 10px;
    border-bottom: 1px solid #334155;
    background: #1e293b;
  }
  tr:hover td { background: #263348; }

  /* ---- Blockquote ---- */
  blockquote {
    border-left: 4px solid #3b82f6;
    background: #1e293b;
    padding: 8px 14px;
    border-radius: 0 8px 8px 0;
    margin: 8px 0;
  }
  blockquote p {
    color: #94a3b8;
    font-style: italic;
  }

  /* ---- Listas ---- */
  ul { list-style-type: none; padding-left: 0; }
  ul li::before { content: "▸ "; color: #93c5fd; font-weight: bold; }
  ul li { color: #cbd5e1; line-height: 1.5; }
  ol li { color: #cbd5e1; line-height: 1.5; }

  /* ---- Lead slides ---- */
  section.lead h1 { font-size: 2.2em; }
  section.lead p { color: #94a3b8; }

  /* ---- Checkpoint ---- */
  section.checkpoint {
    background-color: #052e16;
  }
  section.checkpoint h1 {
    color: #34d399;
    font-size: 1.7em;
  }
  section.checkpoint p, section.checkpoint li {
    color: #a7f3d0;
  }

  /* ---- Fase ---- */
  section.fase {
    background-color: #1e1b4b;
  }
  section.fase h1 { color: #c4b5fd; font-size: 1.7em; }
  section.fase h2 { color: #ddd6fe; }

  /* ---- Desbloqueo (errores comunes) ---- */
  section.desbloqueo {
    background-color: #2a1a1a;
  }
  section.desbloqueo h1 { color: #fca5a5; font-size: 1.6em; }

  /* ---- Checklists de checkpoint: el bullet ES el checkbox ----
     Marp NO convierte "- [ ]" en checkbox: lo deja como texto "[ ]",
     y encima el ::before de ul le agrega "▸ " -> se ve "▸ [ ]". */
  section.check ul li::before { content: "☐  "; color: #34d399; font-weight: 700; }

  /* ---- Footer ---- */
  footer { color: #64748b; font-size: 0.65em; }
---

<!-- _class: lead -->
<!-- note: |
  Bienvenida a la clase 03. Hoy NO construimos una API nueva: reorganizamos
  la que ya tienen en capas, con ORM y frontend TypeScript.
  Recordar: la lectura previa ya la hicieron en casa. La apertura (quiz +
  repaso) es corta, y después arrancan los 60 min de ACTIVIDAD.
  Timing: apertura 0-1 min
-->

# Arquitectura en Capas + ORM

### Clase 03 — Desarrollo de Software 2026

Hoy no escribimos una API nueva. **La reorganizamos para que crezca sin caerse.**

---

<!-- note: |
  Objetivos medibles. Decirlos en voz alta y dejar la slide visible un momento.
  Son la promesa de la actividad: al final, cada alumno tiene que poder tildar los 3.
  Timing: apertura 1-2 min
-->

## Objetivos de la clase

Al terminar, vas a poder:

1. **Separar** una API en 3 capas — Controller → Service → Repository — y
   explicar **por qué** cada cosa vive donde vive.

2. **Usar un ORM** (SQLModel) para hablar con la base en lugar de escribir
   SQL crudo como en el Módulo 02.

3. **Tipar el frontend** con TypeScript, reflejando el contrato de la API
   como tipos.

> Tres objetivos, 60 minutos de actividad, y los construís vos en grupo.

---

<!-- note: |
  Quiz de 3 preguntas para activar. Que respondan a mano alzada o en voz alta.
  RESPUESTAS (para vos):
  1. Controller (recibe el request/responde HTTP), Service (reglas de negocio),
     Repository (habla con la base).
  2. Porque 404 es HTTP y el service no sabe qué es HTTP: devuelve None y el
     controller lo traduce. "Cada capa solo conoce a la de abajo".
  3. Object-Relational Mapping: mapea objetos a tablas. En el 02 escribías SQL
     a mano (filas/columnas); el ORM lo genera por vos (objetos).
  Si la mayoría no leyó, dale 5 min de lectura rápida en el momento.
  Timing: apertura 2-5 min
-->

## Quiz de apertura (aula invertida)

1. ¿Cuáles son las **3 capas** y qué hace cada una?

2. ¿Por qué el **service** no debería devolver un `404`?

3. ¿Qué es un **ORM** y qué diferencia hay con el SQL del Módulo 02?

> El quiz sale del `MATERIAL_PREVIO.md` (con su bibliografía). Si no lo leíste,
> hoy vas a ver pasar la clase por la ventana.

---

<!-- note: |
  Mostrar el main.py de 298 líneas del Módulo 02 en el proyector (o el repo).
  Preguntar: "¿qué pasa si quiero cambiar el motor de base? ¿cuántas cosas toco?"
  Timing: apertura 5-7 min
-->

<!-- _class: smaller -->

## El problema: el monolito

El `main.py` del Módulo 02, **casi 300 líneas**, mezclaba todo:

```python
# modelos Pydantic
class TaskCreate(BaseModel): ...
class Task(BaseModel): ...
# pool de conexiones
pool = ConnectionPool(...)
# SQL crudo DENTRO de los endpoints
@app.post("/api/tasks")
def create_task(body: TaskCreate):
    with pool.connection() as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute("INSERT INTO tasks ... RETURNING ...", (...))
```

> Cambiar UNA cosa obliga a tocar código que no tiene nada que ver. **Eso es un monolito.**

---

<!-- note: |
  La solución: separar en capas. Dibujar la regla de dependencia.
  Enfatizar: cada capa solo conoce a la de abajo. El 404 es el ejemplo.
  Timing: apertura 7-9 min
-->

<!-- _class: smaller -->

## La solución: capas con regla de dependencia

```
Controller ──► Service ──► Repository ──► Base de datos
  (HTTP)        (negocio)     (ORM/SQL)
```

| Capa | Oficio | NO sabe de… |
|------|--------|-------------|
| **Controller** | rutas, status codes, JSON | SQL, reglas de negocio |
| **Service** | reglas de negocio | HTTP, SQL |
| **Repository** | SQL/ORM, la base | HTTP, negocio |

**Regla de oro**: una capa solo conoce a la de **abajo**. Nunca hacia arriba.

> El `404` es HTTP → vive en el **controller**. El service devuelve `None` y
> **no sabe qué es un status code**. Esa es LA lección de hoy.

---

<!-- note: |
  El mapa FÍSICO: traducir el concepto a carpetas. Los alumnos la van a
  necesitar para orientarse en el setup (fase 0).
  Timing: apertura 9-10 min
-->

<!-- _class: smaller -->

## El mapa de las capas (dónde vive cada cosa)

```
backend/app/
├── main.py               → entrypoint (app + routers + lifespan)
├── database.py           → conexión (engine + session + create_all)
├── dependencies.py       → cableado (Depends: Session → Repo → Service)
│
├── models/task.py        → SQLModel (la tabla + schemas)
├── repositories/         → ORM (select, get, add, update, delete)
├── services/             → reglas de negocio (strip, "no existe")
└── controllers/          → endpoints HTTP (el 404 vive acá)
```

> Cada carpeta = una capa = **una sola responsabilidad**. Ese es el edificio
> que vas a construir hoy.

---

<!-- note: |
  Y el ORM: en el 02 escribían SQL a mano, ahora el ORM lo escribe por ellos.
  Enfatizar que el SQL crudo del 02 no se tira: entenderlo es lo que hace usar bien el ORM.
  Timing: apertura 10-12 min
-->

## Y encima: el ORM

**Módulo 02** — vos escribías el SQL:

```python
cur.execute("SELECT id, title, completed, created_at FROM tasks ORDER BY id")
```

**Módulo 03** — el ORM lo escribe por vos:

```python
statement = select(Task).order_by(Task.id)
tasks = session.exec(statement).all()
```

> Pensás en **objetos** (`Task`), no en filas y columnas. El ORM traduce.
> Y `created_at` ya no se serializa a mano: SQLModel + Pydantic lo resuelven.

---

<!-- note: |
  Consolidar con la tabla antes/después. Es LA tabla que fija la lección:
  cada responsabilidad que estaba mezclada ahora tiene casa.
  Preguntar al aire: "¿dónde creen que vive el strip() del título?"
  Timing: apertura 12-14 min
-->

<!-- _class: smaller -->

## Dónde vive cada cosa (antes → después)

| Responsabilidad | Módulo 02 (monolito) | Módulo 03 (capas) |
|-----------------|---------------------|-------------------|
| Validación (Pydantic) | en el endpoint | `models/task.py` |
| SQL / acceso a datos | dentro de los endpoints | `repositories/` |
| Regla de negocio (`strip`, "no existe") | dentro de los endpoints | `services/` |
| HTTP (rutas, 404, status codes) | mezclado | `controllers/` |
| Conexión a la base | `pool` arriba del main | `database.py` |
| Cableado entre capas | implícito | `dependencies.py` |

> El `strip()` es **negocio** → service. El `404` es **HTTP** → controller.
> El `SELECT` es **datos** → repository. Cada cosa, en su casa.

---

<!-- note: |
  El plan de la actividad. Fijar expectativas: son 60 min de sprint, no un paseo.
  Recordar los roles de los grupos (piloto/navegante/investigador) rotando.
  Timing: apertura 14-15 min (fin de la apertura)
-->

<!-- _class: smaller -->

## El plan — 60 min de actividad

> La lectura previa ya la hiciste en casa. Acá van **60 minutos de construcción**.

| Min | Fase | Qué construyen |
|-----|------|----------------|
| 0-5 | **Setup** | Levantar el scaffold |
| 5-20 | **Repository** | Los 6 métodos del CRUD (ORM) |
| 20-30 | **Service** | Lógica de negocio (el `None`) |
| 30-40 | **Controller** | Endpoints (el `404` acá) |
| 40-50 | **Frontend TS** | Conectar y verificar el CRUD |
| 50-60 | **Cierre** | Reflexión + descubrimientos |

> **Regla del taller**: el docente NO da respuestas. Hace preguntas.
> *"¿Eso es HTTP o es negocio?"* es la pregunta que lo destraba todo.

---

<!-- note: |
  Explicar el flujo de trabajo antes del setup.
  Cada alumno trabaja en SU fork (su copia). La solución NO está en el repo —
  se libera al final de la clase en la rama solucion.
  Timing: actividad 0-1 min (transición)
-->

## El flujo: fork → clonar → desarrollar

1. **Fork** — en GitHub, creás tu copia del repo.
2. **Clonar** — bajás TU fork a tu máquina.
3. **Desarrollar** — completás las 3 capas siguiendo la guía.
4. **Verificar** — Postman + frontend, todo contra TU backend.

```bash
git clone https://github.com/TU_USUARIO/backend.git
cd backend/03-arquitectura-en-capas
```

> Cada uno trabaja en **su fork**. La solución se libera al final de la clase
> (rama `solucion`) para que compares tu código.

---

<!-- _class: fase -->
<!-- note: |
  Fase 0. Guiar el setup. Verificar que todos tengan el server arriba.
  Síntomas: ModuleNotFoundError (corren de otro dir), driver psycopg2 (no uv sync).
  Timing: actividad 0-5 min
-->

## Fase 0 — Setup del scaffold (5 min)

```bash
cd 03-arquitectura-en-capas/backend
cp .env.example .env        # DATABASE_URL del Módulo 02
uv sync                     # instala SQLModel + FastAPI
uv run -m app.main          # server en :8000
```

```bash
curl http://localhost:8000/api/health
```

```json
{ "status": "Funciona", "service": "03-...",
  "db": "conectada", "tasks_count": 0 }
```

> El health **ya funciona** — es el ejemplo vivo que les dejamos en el scaffold.
> La tabla se crea sola (`create_all`). Ya no hay `schema.sql`.

---

<!-- _class: checkpoint check -->
<!-- note: |
  Checkpoint 1: todos con server arriba y health respondiendo.
  Recorrer el aula, desbloquear. No avanzar si alguien no llegó.
  Timing: actividad ~5 min
-->

## ✅ Checkpoint 1 — Scaffold arriba

- `uv sync` sin errores
- `uv run -m app.main` corriendo
- `/api/health` responde `db: "conectada"`
- `/docs` muestra la API

---

<!-- _class: fase -->
<!-- note: |
  Fase 1: repository. Primero los métodos de LECTURA, después los de
  escritura. Pista si se traban: "¿cómo leés una fila por id?
  session.get(Task, id)".
  Timing: actividad 5-12 min
-->

## Fase 1 — Repository: leer (15 min)

Completá `app/repositories/task_repository.py`:

```python
class TaskRepository:
    def __init__(self, session: Session):
        self.session = session
    def list_all(self) -> list[Task]:
        ...                  # select(Task) + order_by
    def get_by_id(self, task_id: int) -> Task | None:
        ...                  # session.get(Task, id)
    def count(self) -> int:
        ...                  # ejemplo resuelto
```

> `select(Task)` reemplaza al `SELECT * FROM tasks` del Módulo 02.
> El `session.get()` reemplaza al `WHERE id = %s`.

---

<!-- _class: fase -->
<!-- note: |
  Fase 1 (2/2): los 3 métodos de escritura. Pista clave:
  "¿cómo aplicás solo los campos que vinieron? model_dump(exclude_unset=True)".
  Timing: actividad 12-20 min
-->

## Fase 1 — Repository: escribir

```python
    def create(self, title: str) -> Task:
        ...                  # add + commit + refresh

    def update(self, task, data) -> Task:
        ...                  # model_dump(exclude_unset=True)

    def delete(self, task: Task) -> None:
        ...                  # delete + commit
```

> `exclude_unset=True` es la clave del PATCH: **solo** pisa los campos
> que vinieron en el body. Sin eso, borrás datos sin querer.

---

<!-- _class: fase -->
<!-- note: |
  Fase 2: service. La lógica. El momento clave: el 404.
  Hacer la pregunta al aire: "si la tarea no existe, ¿el service devuelve
  None o lanza un 404?" Dejar que discutan. La respuesta: None.
  Timing: actividad 20-30 min
-->

## Fase 2 — Service (10 min)

Completá `app/services/task_service.py`:

```python
class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository
    def create_task(self, body: TaskCreate) -> Task:
        return self.repository.create(body.title.strip())   # negocio
    def update_task(self, task_id, body) -> Task | None:
        task = self.repository.get_by_id(task_id)
        if task is None:
            return None              # ⬅️ NO lanza 404 acá
        return self.repository.update(task, body)
```

> **La pregunta del millón**: ¿el service devuelve `None` o lanza un `404`?
> `404` es HTTP, y el service **no sabe qué es HTTP**. Devuelve `None`.

---

<!-- _class: fase -->
<!-- note: |
  Fase 3: controller. Traducir None -> 404. El endpoint POST devuelve 201.
  Referenciar health_controller.py como ejemplo ya dado.
  Timing: actividad 30-40 min
-->

## Fase 3 — Controller (10 min)

Completá `app/controllers/task_controller.py`:

```python
@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, service: TaskService = Depends(get_task_service)):
    task = service.get_task(task_id)
    if task is None:
        raise HTTPException(404, detail=f"Tarea {task_id} no existe")
    return task
```

| Endpoint | Método | Nota |
|----------|--------|------|
| `/api/tasks` | GET | `response_model=list[TaskRead]` |
| `/api/tasks` | POST | `status_code=201` |
| `/api/tasks/{id}` | GET / PATCH / DELETE | `None` → `404` |

> El controller es el único que "habla HTTP": traduce `None` → `404`. Cero SQL acá.

---

<!-- _class: checkpoint check -->
<!-- note: |
  Checkpoint 2: CRUD completo. Pedir que prueben los 6 curls del flujo feliz.
  Verificar el strip del título y el 404.
  Timing: actividad ~40 min
-->

## ✅ Checkpoint 2 — CRUD completo por capas

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"  Probar capas  "}'   # → "Probar capas" (¡strip!)

curl http://localhost:8000/api/tasks
curl http://localhost:8000/api/tasks/1
curl -X PATCH http://localhost:8000/api/tasks/1 \
  -H "Content-Type: application/json" -d '{"completed":true}'
curl -X PATCH http://localhost:8000/api/tasks/1 \
  -H "Content-Type: application/json" -d '{"title":"Editado"}'
curl http://localhost:8000/api/tasks/999    # → 404
curl -X DELETE http://localhost:8000/api/tasks/1
```

- El `strip()` normaliza el título (regla de negocio en el service)
- El `404` funciona (traducción del controller)

---

<!-- _class: fase -->
<!-- note: |
  Fase 4: frontend TS. Ya viene completo. Levantar y verificar CRUD.
  Mostrar types.ts y compararlo con TaskRead del backend.
  Timing: actividad 40-50 min
-->

## Fase 4 — Frontend TypeScript (10 min)

Ya viene **completo**. Levantalo y hacé el CRUD desde la UI:

```bash
cd ../frontend
pnpm install && pnpm dev        # :5173
```

```typescript
// src/types.ts — el contrato de la API, como TIPO
export interface Task {
  id: number;
  title: string;
  completed: boolean;
  created_at: string;
}
```

> Este `interface` es el `TaskRead` del backend, pero en TypeScript.
> El compilador te avisa si escribís mal un campo. Antes, JS callaba.

---

<!-- _class: checkpoint check -->
<!-- note: |
  Checkpoint 3: frontend integrado.
  Timing: actividad ~50 min
-->

## ✅ Checkpoint 3 — Frontend integrado

- CRUD completo desde la UI (crear, editar, toggle, eliminar)
- `types.ts` refleja el contrato del backend
- Errores de tipo los atrapa el compilador, no el navegador

---

<!-- _class: desbloqueo -->
<!-- note: |
  Slide de desbloqueo: proyectala cuando un grupo se traba. No la des de una
  sola vez — es tu "cheat sheet" para responder con pistas sin regalar la
  solución completa.
  Timing: cuando haga falta (no es una fase secuencial)
-->

<!-- _class: smaller -->

## 🔧 Errores comunes (desbloqueo rápido)

| Síntoma | Pista para destrabar |
|---------|----------------------|
| `ModuleNotFoundError: app` | ¿Estás en `backend/`? Ejecutá `uv run -m app.main` |
| `relation "tasks" does not exist` | Revisá `DATABASE_URL` en `.env` |
| No sabés leer una fila por id | `session.get(Task, id)` |
| El update pisa campos que no vinieron | `model_dump(exclude_unset=True)` |
| No sabés dónde va el `404` | *"¿El service sabe qué es un status code?"* |
| Frontend no conecta | El proxy ya está en `vite.config.ts` (scaffold) |

> **Regla**: no des la respuesta. Hacé la pregunta que la destraba.
> *"¿Eso es HTTP o es negocio?"* resuelve la mitad de las dudas.

---

<!-- _class: smaller -->
<!-- note: |
  ESTA slide abre la próxima clase. No la saltees: convierte "aprendí un
  layout" en "entiendo un criterio". Tres tiempos:
  1. Lo que construyeron tiene nombre: Layered Architecture (Fowler, PoEAA).
  2. Capas es UN eje; el otro es por FEATURE (partición vertical).
  3. Screaming = el top-level grita el dominio; Hexagonal = escalón siguiente.
  Cerrá con la pregunta del cambio: "agregá `projects` y contá los archivos
  que tocás en cada layout". Eso se responde en 30 segundos y no se olvida.
  Timing: cierre 50-55 min
-->

## Esto que construyeron tiene nombre

**Layered Architecture** (Fowler, *PoEAA*) — paquete **por capa técnica**.
Es lo que acabás de armar:

```
app/  controllers/  services/  repositories/  models/
```

El **otro eje** posible: paquete **por feature** (partición vertical):

```
app/  tasks/{controller,service,repository}.py
      projects/{...}
      shared/     (db, config — el kernel)
```

| Pregunta | Por capa | Por feature |
|----------|----------|-------------|
| Agregar `projects` | tocás 4 carpetas | tocás 1 carpeta |
| "¿Qué hace el sistema?" | no se ve | grita: tasks, projects |
| Reusar entre features | fácil | cuidado: `shared/` se vuelve basurero |

> **Screaming Architecture**: el árbol grita el **dominio**, no el framework.
> **Hexagonal** es el escalón siguiente: puertos (el service depende de una
> abstracción, no de una clase concreta).
> **No es dogma**: dominio chico → simplificá. Dominio que crece y varios
> equipos → el eje vertical paga solo.

---

<!-- _class: lead -->
<!-- note: |
  Reflexión final. Preguntas al aire (5 min). Cerrar con la frase.
  Anunciar los ejercicios de cierre (en GUIA_DOCENTE/GUIA_ALUMNO).
  Timing: actividad 50-60 min
-->

## Hoy no escribieron una API nueva

### La **reorganizaron** para que el día de mañana, cuando crezca, no se caiga

> *"La Universidad te da el mapa. El recorrido lo hacés vos."*
