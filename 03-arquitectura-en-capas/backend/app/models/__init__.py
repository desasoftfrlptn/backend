"""
Modelos compartidos (SQLModel) — el mapa entre Python y las tablas.

OJO, ESTO NO ES UNA CAPA DEL FLUJO.

El diagrama Controller → Service → Repository muestra el FLUJO de una
petición. `models/` no está en ese flujo: lo importan las TRES capas.
Es un **kernel compartido** (shared kernel): el vocabulario común
(`Task`, `TaskCreate`, `TaskUpdate`, `TaskRead`).

Por eso la regla "solo se conoce la capa de abajo" aplica al flujo,
no a este paquete. Si algún día `models/` empieza a importar capas,
ahí sí tenés un problema de dependencias circulares.

En el Módulo 02 esto no existía: el "modelo" era la tabla SQL escrita
a mano en `schema.sql`. Ahora una clase de Python define la tabla.
"""
