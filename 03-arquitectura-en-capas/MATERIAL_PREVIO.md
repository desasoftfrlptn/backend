# 📖 Material Previo — Arquitectura en Capas + ORM (aula invertida)

> **Módulo 03 — Desarrollo de Software 2026**
> **Leé esto ANTES de la clase.** La clase es un taller: si no venís con esto
> leído, no vas a poder construir. El aula es para HACER, no para enterarte.

---

## La promesa

En el Módulo 02 escribiste la API de tareas con **SQL crudo** dentro de los
endpoints. Funcionaba… pero, ¿te acordás cómo quedó `main.py`? Casi 300
líneas donde se mezclaba todo: los modelos Pydantic, el pool, el SQL, los
endpoints, el health check. **Un solo archivo hacía demasiadas cosas.**

Hoy vas a aprender a separar ese caos en **capas** con responsabilidades
claras, y vas a conocer una herramienta que te escribe el SQL: un **ORM**.

---

## 1. El problema: el monolito

Imaginá una obra en construcción donde el plomero, el electricista y el
albañil trabajan todos juntos en el mismo ambiente, compartiendo las mismas
herramientas y hablándose por encima del otro. Cualquier arreglo de cañerías
obliga a mover los cables y romper una pared. **Eso es un monolito.**

En código, "monolito" no significa "archivo grande": significa **muchas
responsabilidades mezcladas**. El `main.py` del Módulo 02 tenía (al menos)
cuatro oficios distintos:

1. **Validar** lo que llega del cliente (Pydantic)
2. **Hablar con la base** (SQL, pool, `dict_row`)
3. **Decidir reglas** (qué hacer si no existe, normalizar el título)
4. **Responder HTTP** (rutas, status codes, JSON)

El síntoma clásico: para cambiar UNA cosa (por ejemplo, cómo se guarda una
tarea), tenés que tocar código que no tiene nada que ver. Y para testear una
regla de negocio, necesitás levantar el servidor entero.

> 🧠 **El principio**: *"Separation of Concerns"* (separación de
> responsabilidades). Cada parte del sistema debería ocuparse de UNA sola
> cosa, y hacerla bien.

### 📚 Para profundizar en este tema

- 📖 **Robert C. Martin — *Clean Architecture***: fundamenta por qué mezclar responsabilidades te condena. El [artículo introductorio](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) resume la idea en 10 minutos.
- 🔗 **[Separation of Concerns](https://en.wikipedia.org/wiki/Separation_of_concerns)** — el principio formal detrás de "cada parte hace una sola cosa".
- 🎬 **Uncle Bob (Robert C. Martin)** — sus charlas sobre arquitectura están en el canal de [NDC Conferences](https://www.youtube.com/@NDC). Buscá *"Clean Architecture"*.

---

## 2. La solución: capas

Separamos el sistema en capas, como los pisos de un edificio. Cada piso
tiene su oficio y **solo se comunica con el piso de abajo**:

```
Controller ──► Service ──► Repository ──► Base de datos
  (HTTP)        (negocio)     (ORM/SQL)
```

| Capa | Oficio | Pregunta que responde |
|------|--------|-----------------------|
| **Controller** | Recibir el request y devolver una respuesta HTTP | "¿Qué ruta, qué método, qué status code?" |
| **Service** | Aplicar las reglas de negocio | "¿Qué se puede hacer y cómo?" |
| **Repository** | Hablar con la base de datos | "¿Cómo se guarda/lee esto?" |

**La regla de oro**: una capa solo conoce a la de abajo. El controller sabe
que existe un service; el service NO sabe que existe un controller. El
service sabe que existe un repository; el repository NO sabe de HTTP.

¿Por qué importa? Porque así cada capa se puede **cambiar y testear por
separado**. Si mañana cambiás la base de datos por otra, solo tocás el
repository. Si cambiás el framework HTTP, solo tocás el controller.

> 🧠 **Inversión de Control (IoC)**: cada capa recibe lo que necesita **desde
> afuera** (se lo "inyectan"), no lo construye ella misma. En FastAPI eso se
> hace con `Depends()`.

### 📚 Para profundizar en este tema

- 📖 **Robert C. Martin — *Clean Architecture***: la "regla de dependencia" que estás viendo acá (una capa solo conoce a la de abajo) es el corazón del libro.
- 🔗 **[FastAPI — Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)** — la inyección de dependencias (`Depends`) que conecta las capas en FastAPI.
- 🎬 **ArjanCodes — [canal](https://www.youtube.com/@ArjanCodes)**: arquitectura de software en Python con ejemplos prácticos. Buscá *"dependency injection"* y *"clean architecture"*.

---

## 3. ¿Qué es un ORM?

**ORM** = *Object-Relational Mapping*. Es una capa que te permite trabajar
con la base de datos usando **objetos de Python**, sin escribir SQL a mano.

### El contraste que es la lección de hoy

**Módulo 02 — SQL crudo** (vos escribías cada consulta):

```python
cur.execute("SELECT id, title, completed, created_at FROM tasks ORDER BY id")
rows = cur.fetchall()
```

**Módulo 03 — ORM** (el ORM escribe el SQL por vos):

```python
statement = select(Task).order_by(Task.id)
tasks = session.exec(statement).all()
```

La diferencia: en el Módulo 02 pensabas en **filas y columnas** (strings SQL).
Ahora pensás en **objetos** (`Task`). El ORM traduce tu intención a SQL.

**¿Por qué usar un ORM?**
- Menos código repetitivo (no escribís el SQL de cada consulta a mano)
- Menos errores (el ORM parametriza solo — protege de inyección SQL)
- Portabilidad (cambiás de base y el ORM se adapta)
- Refleja el modelo de tu dominio como objetos

**¿Y el SQL crudo que aprendiste en el 02?** No se tira a la basura. Entender
el SQL que hay debajo es lo que te hace **usar el ORM bien** y no a ciegas.
El ORM es una herramienta, no magia: si no sabés qué SQL genera, vas a tener
problemas de performance y no vas a saber por qué.

### 📚 Para profundizar en este tema

- 🔗 **[SQLAlchemy 2.0 — Documentación](https://docs.sqlalchemy.org/en/20/)** — el ORM que está debajo de SQLModel. El tutorial oficial cubre el patrón `select()`.
- 🔗 **[psycopg — Documentación](https://www.psycopg.org/psycopg3/docs/)** — el driver que usaste en el Módulo 02. El ORM genera SQL que este driver ejecuta por vos.
- 🎬 **ArjanCodes — [canal](https://www.youtube.com/@ArjanCodes)**: videos sobre ORMs y SQLAlchemy en Python, explicando el SQL que generan por debajo.

---

## 4. SQLModel en 3 minutos

**SQLModel** es un ORM creado por el autor de FastAPI. Une dos cosas:

- **SQLAlchemy** (el ORM más usado de Python) → para hablar con la base
- **Pydantic** (que ya usaste) → para validar y serializar JSON

Una clase puede ser **la tabla** (con `table=True`):

```python
class Task(TaskBase, table=True):
    __tablename__ = "tasks"
    id: int | None = Field(default=None, primary_key=True)
    completed: bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
```

Y de esa misma base, **heredando**, definimos qué entra y qué sale por la API:

```python
class TaskCreate(TaskBase):      # lo que manda el cliente al crear
    pass

class TaskRead(TaskBase):        # lo que devuelve la API
    id: int
    completed: bool
    created_at: datetime
```

Fijate que **ya no existe `schema.sql`**: el ORM genera la tabla desde la
clase. `SQLModel.metadata.create_all(engine)` crea las tablas al arrancar.

### 📚 Para profundizar en este tema

- 🔗 **[SQLModel — Documentación](https://sqlmodel.tiangolo.com/)** — la doc oficial del ORM que usamos hoy. El [tutorial](https://sqlmodel.tiangolo.com/tutorial/) cubre exactamente lo que vas a construir.
- 🎬 **tiangolo (Sebastián Ramírez)** — creador de FastAPI y SQLModel. Sus charlas están en el canal de [PyCon US](https://www.youtube.com/@PyConUS). Buscá *"FastAPI"*.

---

## 5. TypeScript: el frontend deja de adivinar

En los módulos 01 y 02, el frontend era **JavaScript**. Cada vez que leías
`task.completed`, confiabas en que el backend te mandara ese campo bien
escrito. JavaScript no te avisa si te equivocás de nombre de campo: falla en
silencio, en runtime.

**TypeScript** agrega **tipos estáticos** a JavaScript. Definís la forma de
los datos y el compilador te avisa ANTES de ejecutar si la usás mal.

```typescript
export interface Task {
  id: number;
  title: string;
  completed: boolean;
  created_at: string;
}
```

Este `interface` **es el contrato de la API, escrito como tipo**. Si el
backend cambia `created_at` por `createdAt`, el frontend TypeScript **no
compila** y te lo dice en el editor. Eso es seguridad que JavaScript no te da.

> 🧠 La lección: el contrato de la API vive en **dos lugares** — el schema
> Pydantic (backend) y las interfaces TypeScript (frontend). Tienen que
> coincidir, y ahora ambos lados están tipados.

### 📚 Para profundizar en este tema

- 📖 **Dan Vanderkam — *Effective TypeScript***: 62 consejos para usar TypeScript bien, no solo "que compile".
- 🔗 **[TypeScript Handbook](https://www.typescriptlang.org/docs/)** — la referencia oficial del lenguaje.
- 🔗 **[React + TypeScript](https://react.dev/learn/typescript)** — cómo tipar componentes React (lo que usamos en el frontend).
- 🎬 **Matt Pocock — [canal](https://www.youtube.com/@mattpocockuk)**: el referente de TypeScript en YouTube. Tutoriales claros y directos.

---

## 6. Esto tiene nombre: *Layered Architecture* (y el eje que no usamos)

> Esta sección es **mapa, no taller**. No la vas a construir hoy. La leés
> para saber **cómo se llama** lo que sí vas a construir, y para saber que
> hay más de una forma de organizar el mismo sistema.

Lo que vas a armar en clase es **Layered Architecture**: el patrón que
divide el sistema en capas horizontales donde cada una solo habla con la
de abajo. Martin Fowler lo formalizó en *Patterns of Enterprise Application
Architecture* como "Layered Architecture" (también se lo llama N-tier).

### 6.1 Capas es UN eje, no EL eje

Hay dos formas de partir el mismo sistema:

**Partición HORIZONTAL — por capa técnica** (lo que construís hoy):

```
app/
├── controllers/   ← TODO lo HTTP del sistema
├── services/      ← TODO el negocio del sistema
├── repositories/  ← TODO el acceso a datos
└── models/        ← TODO el vocabulario compartido
```

**Partición VERTICAL — por feature** (package by feature):

```
app/
├── tasks/
│   ├── controller.py
│   ├── service.py
│   ├── repository.py
│   └── schemas.py
├── projects/
│   └── ...
└── shared/          ← db, config: el kernel compartido
```

Fijate que **por feature no desaparecen las capas**: cada feature tiene
adentro su controller, su service y su repository. Cambia **el eje de
agrupación**, no la cantidad de capas.

### 6.2 El test del cambio (la forma de decidir sin religión)

El mejor argumento no es teórico, es medible:

> **Agregá una segunda feature (`projects`) y contá cuántos archivos y
> carpetas tocás en cada layout.**

| Pregunta | Por capa (horizontal) | Por feature (vertical) |
|----------|----------------------|------------------------|
| Agregar `projects` | tocás 4 carpetas (una por capa) | tocás 1 carpeta |
| "¿Qué hace el sistema?" | hay que leer todo | el árbol lo grita |
| Reusar algo entre features | fácil (ya está separado) | cuidado: `shared/` se vuelve basurero |
| Un equipo por feature | pisa archivos ajenos | cada equipo en su carpeta |
| App CRUD chica, 2 personas | simple y directo | ceremonia innecesaria |

**Ninguna gana siempre.** Con un dominio chico y un solo equipo, por capa
es más simple. Con un dominio que crece, varias features y varios equipos,
el eje vertical paga solo (menos conflictos de merge, mejor localidad del
cambio, camino natural a microservicios).

### 6.3 Screaming Architecture

Es un **criterio de nombres**, no otra estructura. La pregunta es: cuando
alguien abre la carpeta raíz, ¿qué grita?

```
# Grita FRAMEWORK (mal)
app/  routers/  models/  utils/

# Grita DOMINIO (bien)
app/  tasks/  projects/  billing/  shared/
```

Robert C. Martin lo llama *Screaming Architecture*: la estructura tiene
que gritar **los casos de uso del negocio**, no el framework con el que lo
implementaste. Si mañana cambiás FastAPI por Django, el árbol del dominio
no debería moverse.

### 6.4 ¿Y el escalón siguiente?

**Hexagonal (Ports & Adapters)** y **Clean Architecture** son el paso
siguiente: ahí la regla deja de ser "conozco la capa de abajo" y pasa a ser
"el negocio **no conoce** la base ni el framework". El service depende de
una **interfaz** (puerto) y el repositorio es un **adaptador** que la
implementa. Eso es lo que permite testear el negocio sin base de datos.

Hoy usás Inyección de Dependencias con `Depends()`, pero el service sigue
dependiendo de una **clase concreta** (`TaskRepository`), no de una
abstracción. Esa es la diferencia exacta entre "capas" y "hexagonal".

> 🧠 **La lección de esta sección**: aprender un layout no es aprender
> arquitectura. Aprender arquitectura es saber **qué eje elegir, por qué, y
> qué costo tiene**. El día que defiendas una decisión en una entrevista,
> no vas a decir "usé capas porque es mejor": vas a decir "usé capas porque
> el dominio era chico y el equipo era uno; si crecía, pasaba a features".

### 📚 Para profundizar en este tema

- 📖 **Martin Fowler — *Patterns of Enterprise Application Architecture***: el capítulo de Layered Architecture. La definición canónica del patrón que usás hoy.
- 🔗 **[Package by feature, not by layer](https://phauer.com/2021/package-by-feature/)** — el artículo que mejor explica el eje vertical con ejemplos.
- 🔗 **[Screaming Architecture (Uncle Bob)](https://blog.cleancoder.com/uncle-bob/2011/09/30/Screaming-Architecture.html)** — por qué el árbol tiene que gritar el dominio.
- 🔗 **[Hexagonal Architecture (Alistair Cockburn)](https://alistair.cockburn.us/hexagonal-architecture/)** — puertos y adaptadores, el escalón siguiente.
- 🎬 **ArjanCodes — [canal](https://www.youtube.com/@ArjanCodes)**: comparaciones prácticas entre "por capa" y "por feature" en Python.

---

## Autoevaluación (hacela antes de venir)

Respondé mentalmente. Si dudás, releé la sección:

1. ¿Cuáles son las 3 capas y qué hace cada una?
2. ¿Por qué el controller NO debería escribir SQL?
3. ¿Por qué el service NO debería devolver un `404` directamente?
4. ¿Qué es un ORM y cuál es la diferencia con el SQL crudo del Módulo 02?
5. En SQLModel, ¿qué significa `table=True`?
6. ¿Qué ventaja te da TypeScript frente a JavaScript?
7. ¿Cómo se llama el patrón que vas a construir y qué otro eje de partición existe?
8. ¿Qué preguntarías para decidir entre "por capa" y "por feature"?

---

## Bibliografía

> 🎯 **El quiz de la clase sale de acá.** Las 3 preguntas del quiz de apertura
> se responden con las secciones 2, 3 y 4 de arriba + la lectura previa de
> esta sección. Si podés responder la autoevaluación, venís listo.

### 📚 Lectura previa (obligatoria — responde el quiz)

| Pregunta del quiz | Dónde está la respuesta |
|-------------------|-------------------------|
| ¿Cuáles son las **3 capas** y qué hace cada una? | Sección 2 (la solución: capas) + tutorial de FastAPI abajo |
| ¿Por qué el **service** no devuelve un `404`? | Sección 2, "la regla de oro" (cada capa solo conoce a la de abajo) |
| ¿Qué es un **ORM** y qué lo diferencia del SQL crudo? | Secciones 3 y 4 + intro de SQLModel abajo |

- **[SQLModel — Introducción y tutorial](https://sqlmodel.tiangolo.com/tutorial/)** — qué es y cómo define tablas. Responde la pregunta del ORM.
- **[FastAPI — SQL (Relational) Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)** — cómo se organiza un backend FastAPI con base de datos. Responde la pregunta de las capas.
- **[Separation of Concerns (Wikipedia)](https://en.wikipedia.org/wiki/Separation_of_concerns)** — el principio detrás de la pregunta "¿por qué el service no devuelve 404?".

### 🔖 Referencia (para profundizar después de clase)

- [SQLAlchemy 2.0 — Documentación](https://docs.sqlalchemy.org/en/20/) — el motor que está debajo de SQLModel. Entenderlo es lo que separa "usar el ORM" de "usarlo bien".
- [FastAPI — Dependencias](https://fastapi.tiangolo.com/tutorial/dependencies/) — la inyección de dependencias (`Depends`) que conecta las capas.
- [TypeScript — Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) — la referencia oficial del lenguaje.
- [React + TypeScript](https://react.dev/learn/typescript) — cómo tipar componentes React.
- [Vite — Documentación](https://vite.dev/) — el dev server que usamos en el frontend.
- **Robert C. Martin — *Clean Architecture*** ([artículo](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) | [libro](https://www.oreilly.com/library/view/clean-architecture-a/9780134494272/)) — la filosofía profunda de las capas y la regla de dependencia. Para quien quiera ir más allá.
- **Eric Evans — *Domain-Driven Design*** ([libro](https://www.oreilly.com/library/view/domain-driven-design-tackling/0321125215/)) — de dónde sale el concepto de "Service" como capa de dominio.

---

## Qué vas a necesitar en clase

- El proyecto del Módulo 02 (la base `tasks` ya creada — la reutilizamos)
- Tu `DATABASE_URL` (Docker o Supabase, la misma del Módulo 02)
- `uv` y `pnpm` instalados (ya los usaste)
- **Actitud de taller**: vas a construir en grupo, no a copiar.

> *"La Universidad te da el mapa. El recorrido lo hacés vos."*
