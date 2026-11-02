# 📘 SPEC — Módulo 03: Arquitectura en Capas + ORM

> **Este documento es TU recurso de aprendizaje.**
> No es un contrato frío: es el mapa de lo que vas a construir, **por qué** lo
> construimos así, y **qué vas a descubrir** en el camino. Leelo antes de
> tocar código, y volvé a él cuando te trabes.

---

## 1. Qué vas a construir

La **misma API de Tareas** de los módulos 01 y 02, pero **reorganizada**:

- En **3 capas** con responsabilidades separadas (Controller → Service → Repository)
- Con un **ORM** (SQLModel) en lugar del SQL crudo que escribiste en el 02
- Con un **frontend TypeScript** que refleja el contrato como tipos

Y lo más importante: **el contrato de la API no cambia**. Mismo JSON, mismos
campos, mismos endpoints (y algunos nuevos).

> 🤔 **¿Qué descubriste en el Módulo 02?** Que el `main.py` de casi 300 líneas
> mezclaba todo: validación, SQL, reglas y HTTP. Hoy vas a separar ese caos.

---

## 2. Por qué lo construimos así (la idea de fondo)

Cuando todo vive en un solo archivo, **cambiar una cosa obliga a tocar cosas
que no tienen nada que ver**. La solución es separar por **responsabilidades**:

```
Controller ──► Service ──► Repository ──► Base de datos
  (HTTP)        (negocio)     (ORM/SQL)
```

**La regla de oro**: una capa solo conoce a la que está **debajo**. Nunca hacia
arriba ni en diagonal.

> 💡 **Pista para el taller**: cuando no sepas dónde va algo, preguntate *"¿esto
> es HTTP, es negocio, o es datos?"*. El `404` es HTTP → controller. El `strip()`
> del título es negocio → service. El `SELECT` es datos → repository.

---

## 3. Qué tenés que completar (tu misión)

El repo te entrega el backend **casi listo**. Solo tenés que escribir **3
archivos**, que son justamente las 3 capas:

| Archivo | Capa | Qué hacés |
|---------|------|-----------|
| `backend/app/repositories/task_repository.py` | Repository | Los 6 métodos del CRUD con el ORM |
| `backend/app/services/task_service.py` | Service | La lógica de negocio |
| `backend/app/controllers/task_controller.py` | Controller | Los 5 endpoints HTTP |

Todo lo demás ya viene **dado** (el modelo, la conexión, el cableado, el
entrypoint y un controller de ejemplo). La guía `GUIA_ALUMNO.md` te lleva
paso a paso.

> 🎯 **Tu meta**: que al final el CRUD completo funcione por las 3 capas, y el
> frontend TypeScript haga todo desde la UI.

---

## 4. La arquitectura

### 4.1 Las capas y sus responsabilidades

| Capa | Carpeta | Sabe de… | NO sabe de… |
|------|---------|----------|-------------|
| Controller | `controllers/` | HTTP (rutas, status codes, JSON) | SQL, reglas de negocio |
| Service | `services/` | Reglas de negocio | HTTP, SQL |
| Repository | `repositories/` | SQL/ORM, la base | HTTP, negocio |

### 4.2 Dónde vive cada responsabilidad

| Responsabilidad | Antes (módulo 02) | Ahora (módulo 03) |
|-----------------|-------------------|-------------------|
| Validación (Pydantic) | en el endpoint | `models/task.py` |
| SQL / acceso a datos | dentro de los endpoints | `repositories/` |
| Regla de negocio (`strip`, "no existe") | dentro de los endpoints | `services/` |
| HTTP (rutas, 404, status codes) | mezclado | `controllers/` |
| Conexión a la base | `pool` arriba del main | `database.py` |
| Cableado entre capas | implícito | `dependencies.py` |

> 🤔 **¿Qué descubriste acá?** La decisión clave: el `404` NO vive en el
> service. El service devuelve `None` (o `False`) y **no sabe qué es un status
> code**. Es el controller quien lo traduce a `404`. ¿Por qué? Porque `404` es
> una preocupación **HTTP**, y el service no conoce HTTP.

### 4.3 El ORM en la capa de datos

En el módulo 02 escribías el SQL a mano. Ahora el ORM lo escribe por vos:

```python
# Módulo 02 — SQL crudo
cur.execute("SELECT id, title, completed, created_at FROM tasks ORDER BY id")

# Módulo 03 — ORM
statement = select(Task).order_by(Task.id)
tasks = session.exec(statement).all()
```

> 💡 **Pista para el taller**: `session.get(Task, id)` es el atajo para "leer
> una fila por id" (reemplaza al `WHERE id = %s` del módulo 02).

---

### 4.4 Cómo se llama esto (y el otro eje)

Lo que construís tiene nombre: **Layered Architecture** (Fowler, *PoEAA*).
Es una partición **horizontal**: `controllers/`, `services/`, `repositories/`
agrupan TODO lo HTTP, TODO el negocio y TODO el acceso a datos del sistema.

Dos precisiones que el diagrama lineal no muestra:

1. **`models/` no es una capa del flujo**: lo importan las tres capas. Es un
   **kernel compartido** (el vocabulario del dominio), no un piso del
   edificio. La regla "solo conozco la de abajo" aplica al flujo, no a él.
2. **Capas es UN eje, no EL eje.** El otro es la partición **vertical por
   feature** (`tasks/`, `projects/`, cada una con sus 3 capas adentro) —
   *package by feature*. Y **Screaming Architecture** es el criterio de
   nombres: el árbol de arriba tiene que gritar el **dominio**, no el
   framework.

> 🧠 Hoy construís **un** eje, a propósito: es el que mejor cuenta el
> "antes → después" contra el monolito del 02. Saber que existe el otro,
> y **cuándo** conviene cada uno, es el objetivo conceptual de la clase.
> El detalle está en `MATERIAL_PREVIO.md` §6.

---

## 5. El modelo de datos (SQLModel)

Una clase de Python define la tabla (con `table=True`):

```python
class Task(TaskBase, table=True):
    __tablename__ = "tasks"
    id: int | None = Field(default=None, primary_key=True)
    completed: bool = Field(default=False)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
```

Y heredando, definimos qué entra y qué sale por la API:

| Clase | Rol | Uso |
|-------|-----|-----|
| `Task` | La TABLA (`table=True`) | Persistencia |
| `TaskCreate` | Entrada al crear (solo title) | `POST` |
| `TaskUpdate` | Entrada al actualizar (campos opcionales) | `PATCH` |
| `TaskRead` | Salida (tarea completa) | `response_model` |

> 🤔 **¿Qué descubriste acá?** Ya no existe `schema.sql`. El ORM genera la
> tabla desde la clase (`SQLModel.metadata.create_all`). Y `created_at` lo
> sigue generando **la base** (`server_default=func.now()`), como en el 02.

---

## 6. Los endpoints (el CRUD completo)

| Método | Ruta | Qué hace |
|--------|------|----------|
| `GET` | `/api/health` | Verifica que la base responde |
| `GET` | `/api/tasks` | Lista todas las tareas |
| `POST` | `/api/tasks` | Crea una tarea (`201`) |
| `GET` | `/api/tasks/{id}` | Lee UNA tarea |
| `PATCH` | `/api/tasks/{id}` | Actualiza título y/o estado |
| `DELETE` | `/api/tasks/{id}` | Elimina una tarea |

**Errores que tenés que respetar:**

| Caso | Código |
|------|--------|
| `title` vacío / > 200 / no string / faltante | `422` |
| GET/PATCH/DELETE de id inexistente | `404` `{"detail": "Tarea {id} no encontrada"}` |

> 💡 **Pista para el taller**: el `POST` devuelve `201`, no `200`. Y el `PATCH`
> es parcial: podés mandar solo `completed`, solo `title`, o ambos.

---

## 7. Cómo verificar tu trabajo

```bash
cd backend
uv sync
cp .env.example .env        # DATABASE_URL (podés reusar la del módulo 02)
uv run -m app.main          # http://localhost:8000
```

**Checkpoints** (si los pasás, vas bien):

1. `/api/health` responde `db: "conectada"`.
2. `POST` crea una tarea y el `title` sale **sin espacios** (el `strip()` del service).
3. `PATCH` con solo `completed` no pisa el `title`, y viceversa.
4. `GET/PATCH/DELETE` de un id inexistente devuelven `404`.
5. El frontend (`pnpm dev` en `../frontend`) hace el CRUD completo desde la UI.

> 🎯 **Tu meta final**: el CRUD funciona por las 3 capas, y el frontend
> TypeScript lo hace todo desde la interfaz.

---

## 8. Dónde seguir aprendiendo

- `MATERIAL_PREVIO.md` → los conceptos + referencias (bibliografía, docs, videos).
- `GUIA_ALUMNO.md` → la guía paso a paso con consignas y pistas.
- `README.md` → instalación y estructura del repo.
- La **collection Postman** (`postman/`) → para verificar el flujo feliz y los casos límite.
