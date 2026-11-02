# 🧭 Guía del Docente — Arquitectura en Capas + ORM + TypeScript

> **Módulo 03 — Desarrollo de Software 2026**
> **Metodología**: aula invertida + taller por grupos con descubrimiento
> **Duración**: 60 minutos de **actividad** (la lectura previa es aparte — no cuenta en los 60)
> **Tu rol**: no dictás — guiás, desbloqueás y hacés preguntas.

---

## 1. La idea en una frase

Los alumnos **ya saben** el SQL crudo (Módulo 02) y **ya leyeron** los
conceptos (aula invertida). Tu trabajo en el aula es ponerlos a **construir**
la arquitectura en capas por descubrimiento, desbloquearlos cuando se
traben y cerrar con una reflexión que fije los conceptos.

**La regla número uno del taller: no des la respuesta antes de tiempo.**
Ante una duda, respondé con una pregunta: *"¿qué capa creés que debería
conocer eso?"* o *"¿eso es HTTP o es negocio?"*.

---

## 2. Antes de la clase (aula invertida)

1. **Asigná** [`MATERIAL_PREVIO.md`](./MATERIAL_PREVIO.md) con al menos 3-4
   días de anticipación. Dejá claro que la clase es taller y sin lectura
   previa no van a poder construir.
2. **Verificá** la lectura al inicio con un quiz de 3 preguntas (las tenés en
   la presentación, slide 2). No es evaluación: es para activar el cerebro y
   detectar quién no leyó.
3. **Prepará el scaffold**: `main` ya trae la versión **incompleta** (los
   tres archivos con `NotImplementedError`). No hay que "desarmar" nada.
   La versión completa vive en la rama **`solucion`**, que liberás al final.

> ⚠️ **Verificá ANTES de clase** que la rama `solucion` tenga el código:
> ```bash
> git fetch origin
> git diff --stat main..origin/solucion -- 03-arquitectura-en-capas
> ```
> Tiene que mostrar los 3 archivos con cambios. Si da vacío, la rama está
> rota (pasó una vez: el commit que dejó los stubs en `main` se mergeó a
> `solucion`). Restáurala desde `33556ee` antes de entrar al aula — si no,
> los alumnos hacen `git diff main..origin/solucion` y no ven nada.

---

## 3. Los grupos (ya están formados)

Cada grupo trabaja en **una sola máquina** (pair/ensemble programming).
Sugerencia de roles rotativos dentro del grupo:

| Rol | Hace |
|-----|------|
| **Piloto** | Escribe el código (comparte pantalla) |
| **Navegante** | Lee la consigna y las pistas, anticipa errores |
| **Investigador** | Busca en la doc/memorias del Módulo 02 cuando se traban |

Rotá los roles en cada fase (Repository → Service → Controller). Así todos
tocan teclado y todos razonan.

---

## 4. El scaffold: qué se entrega vs qué se construye

**Se entrega ya hecho** (boilerplate, no es la lección):
- `app/models/task.py` — el modelo SQLModel (mucho boilerplate)
- `app/database.py` — engine + session + create_all
- `app/dependencies.py` — el cableado con `Depends()`
- `app/main.py` — el entrypoint
- `app/controllers/health_controller.py` — **ejemplo vivo** de cómo se escribe un controller
- `frontend/` — completo y funcionando (el frontend TS no se construye en el taller)

**Se construye por descubrimiento** (la lección):
- `app/repositories/task_repository.py` — los 6 métodos del CRUD con el ORM
- `app/services/task_service.py` — la lógica de negocio
- `app/controllers/task_controller.py` — los 5 endpoints

Cada uno de estos tres archivos tiene un **esqueleto** en el GUIA_ALUMNO
(firmas con `...` o `raise NotImplementedError`) y consignas que guían sin
regalar la respuesta.

---

## 5. El tiempo en el aula: apertura + 60 minutos de actividad

La **lectura previa** (aula invertida) NO cuenta en los 60 minutos. Los 60
son **solo actividad** (construcción). Antes hay una **apertura** corta para
verificar la lectura y activar conceptos.

### Apertura — verificación de lectura previa (fuera de los 60)

| ~min | Qué hacés |
|------|-----------|
| 0-5 | **Quiz de 3 preguntas** — verificá quién leyó el material previo |
| 5-15 | **Repaso conceptual relámpago**: objetivos → monolito → capas → mapa → ORM → dónde vive cada cosa. Sin profundizar: ya lo leyeron en casa |

### Actividad — 60 minutos

| Min | Fase | Qué hacés vos | Qué hacen los grupos |
|-----|------|---------------|----------------------|
| 0-5 | **Setup** | Entregá el scaffold. Verificá que todos tengan `uv sync` + `.env` + server arriba | Levantan el backend, ven el `/docs`, saludan al health |
| 5-20 | **Repository** | Desbloqueás con preguntas ("¿qué función del ORM lee una fila por id?"). Checkpoint 1 | Completan los 6 métodos del repository |
| 20-30 | **Service** | El momento clave: la pregunta del `404` | Completan la lógica de negocio |
| 30-40 | **Controller** | Guiás la traducción `None` → `404`. Checkpoint 2 | Completan los 5 endpoints, prueban con Postman/Swagger |
| 40-50 | **Frontend TS** | "Levanten `pnpm dev` y hagan el CRUD completo" | Levantan el frontend, editan título, toggle, eliminan |
| 50-60 | **Cierre + reflexión** | Reflexión guiada (sección 7). Anunciás los ejercicios | Comparten un descubrimiento por grupo |

> ⏱️ **No te aferres al reloj con rigidez.** Los checkpoints importan más que
> los minutos. Si un grupo se atrasa, priorizá que lleguen al **Checkpoint 2**
> (backend andando) — el frontend ya viene hecho y se conecta rápido.

---

## 6. Checkpoints (dónde parar y verificar)

**Checkpoint 1 — Repository andando (min ~20 de actividad)**
```bash
curl http://localhost:8000/api/health   # db: conectada, tasks_count: N
```
El grupo tiene el repository completo. Se prueba desde Swagger o Postman.

**Checkpoint 2 — CRUD completo por capas (min ~40 de actividad)**
```bash
# crear → listar → leer una → editar → toggle → eliminar
curl -X POST http://localhost:8000/api/tasks -H "Content-Type: application/json" -d '{"title":"Probar capas"}'
curl http://localhost:8000/api/tasks
curl -X PATCH http://localhost:8000/api/tasks/1 -H "Content-Type: application/json" -d '{"completed":true}'
curl -X PATCH http://localhost:8000/api/tasks/1 -H "Content-Type: application/json" -d '{"title":"Título editado"}'
curl -X DELETE http://localhost:8000/api/tasks/1
```
El 404 ante id inexistente funciona, y el `strip()` del service normaliza el título.

**Checkpoint 3 — Frontend integrado (min ~50 de actividad)**
El frontend TS en `:5173` hace el CRUD completo contra el backend, con
edición de título incluida.

---

## 7. La reflexión final (no la saltees)

Cerrá con estas preguntas al grupo entero (5 min, responden en voz alta):

1. **"¿Qué ganamos separando en capas?"** → esperá: "si cambio la base, toco
   solo el repository", "puedo testear cada capa sola".
2. **"¿Dónde vive el 404 y por qué no en el service?"** → porque 404 es HTTP,
   y el service no sabe de HTTP. Si responden "en el controller", ya
   entendieron la lección.
3. **"¿Qué le pedís al ORM que antes escribías a mano?"** → el SQL. El
   `select(Task)` reemplaza el `SELECT * FROM tasks`.
4. **"¿Qué te da TypeScript que JavaScript no te daba?"** → errores en tiempo
   de compilación, no en runtime.
5. **"¿Cómo se llama el patrón que construyeron?"** → *Layered Architecture*.
   Y la que abre la próxima: **"¿qué otro eje de partición existe?"** →
   por feature (vertical). Pediles el **test del cambio**: "agregá `projects`
   y contá cuántas carpetas tocás en cada layout". Con eso se dan cuenta
   solos de que la arquitectura es una **decisión con costo**, no un dogma.

> La slide "Esto que construyeron tiene nombre" es la bisagra entre esta
> clase y el módulo `03.5` (feature-based / screaming / hexagonal). Si el
> tiempo aprieta, **no la saltees**: es lo único de la clase que enseña a
> elegir, en lugar de repetir.

Terminá con la frase: *"Hoy no escribieron una API nueva — la REORGANIZARON
para que el día de mañana, cuando crezca, no se caiga."*

---

## 8. Síntomas comunes (y cómo desbloquear)

| Síntoma | Causa probable | Desbloqueo |
|---------|----------------|------------|
| `ModuleNotFoundError: app` | Corren desde el directorio equivocado | Están en `backend/` y ejecutan `uv run -m app.main` |
| `relation "tasks" does not exist` | No arrancó el lifespan / base equivocada | Revisar `DATABASE_URL` en `.env`; el `create_all` corre al arrancar |
| `create_all` no crea nada | La tabla ya existe del Módulo 02 (está bien) | Es idempotente: no rompe nada, mapea la tabla existente |
| Error de driver `psycopg2` | No corrieron `uv sync` | `uv sync` instala `psycopg2-binary` |
| No saben cómo leer una fila por id | Buscan el equivalente a `WHERE id = %s` | Pista: `session.get(Task, id)` |
| Devuelven `None` y no saben qué hacer | Confusión de dónde va el 404 | Pregunta guía: "¿el service sabe qué es un status code?" |
| Update pisa campos que no vinieron | Usan `model_dump()` sin `exclude_unset` | Pista: "solo tocá los campos que el cliente mandó" |
| Frontend no conecta | Proxy de Vite no configurado | El proxy ya está en `vite.config.ts` (scaffold) |
| 405 en lugar de 404/422 | Ruta mal definida | Revisar métodos y paths contra la tabla de endpoints del SPEC |

---

## 9. Ejercicios de cierre (para casa)

- 🟢 Explicá con tus palabras la regla de dependencia entre capas.
- 🟡 Agregá `GET /api/tasks?completed=true` (filtro por estado) end-to-end:
  repository → service → controller → frontend.
- 🔴 ¿Qué harías para que el service lance una excepción de dominio
  (`TaskNotFoundError`) en lugar de devolver `None`? ¿Dónde la traducirías a
  404? Investiga `app.add_exception_handler`.
- 🔴 **El test del eje**: reorganizá `app/` en `features/tasks/` +
  `shared/` y agregá una feature `projects` en AMBOS layouts (por capa y por
  feature). Contá archivos tocados, conflictos de merge y tiempo. Escribí
  media carilla con la decisión y el costo. Ese texto vale más que el CRUD.

---

> **Recordá**: el objetivo no es que terminen el CRUD. Es que **entiendan por
> qué** las capas existen. Si se traban y vos les das la respuesta, se llevan
> código. Si los guiás con preguntas, se llevan el criterio.
