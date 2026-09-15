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

  /* ---- Slides densas: reducimos todo un escalón ---- */
  section.smaller { font-size: 0.92em; }
  section.smaller h1 { font-size: 1.4em; }
  section.smaller h2 { font-size: 1.15em; }

  /* ---- Código ---- */
  code {
    color: #93c5fd;
    background: #1e293b;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.85em;
  }
  pre {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 0.82em;
    line-height: 1.35;
    color: #e2e8f0;
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
    font-size: 0.8em;
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

  /* ---- Fase ---- */
  section.fase {
    background-color: #1e1b4b;
  }
  section.fase h1 { color: #c4b5fd; font-size: 1.7em; }
  section.fase h2 { color: #ddd6fe; }

  /* ---- Brecha (la lección central) ---- */
  section.brecha {
    background-color: #2a1a1a;
  }
  section.brecha h1 { color: #fca5a5; font-size: 1.7em; }
  section.brecha h2 { color: #fecaca; }
  section.brecha li, section.brecha p { color: #fecaca; }

  /* ---- Entrega (la parte de evaluación) ---- */
  section.entrega {
    background-color: #052e16;
  }
  section.entrega h1 { color: #34d399; font-size: 1.7em; }
  section.entrega p, section.entrega li { color: #a7f3d0; }

  /* ---- Bibliografía ---- */
  section.biblio {
    background-color: #0b1220;
  }
  section.biblio h1 { color: #93c5fd; font-size: 1.6em; }
  section.biblio h2 { color: #c4b5fd; font-size: 1.05em; }
  section.biblio li { font-size: 0.82em; line-height: 1.45; }

  /* ---- Footer ---- */
  footer { color: #64748b; font-size: 0.6em; }
---

<!-- _class: lead -->
<!-- note: |
  Bienvenida a la clase 06. Hoy NO hay API nueva: cerramos el contrato de
  seguridad. En el 04 le pusimos identidad (authN), en el 05 vimos los
  vehículos (sesión/token), y HOY decidimos qué PODÉS hacer (authZ).
  Esta apertura es breve (10-12 min): repaso 04-05, la brecha A01, y el
  plan de la entrega OBLIGATORIA. Después, 60 min de trabajo individual.
  Timing: apertura 0-1 min
-->

# Autorización RBAC

### Clase 06 — Desarrollo de Software 2026 · 🚦 ENTREGA OBLIGATORIA

En el 04 la API aprendió **quién sos**. Hoy la API aprende **qué podés hacer**.

---

<!-- note: |
  La agenda de hoy. Dejar claro desde el minuto 1 que hay ENTREGA OBLIGATORIA
  (22/09) y que el ritmo de la clase es individual, no grupal.
  Timing: apertura 1-2 min
-->

## La clase de hoy

| # | Momento | Qué pasa |
|---|---------|----------|
| 1 | **Repaso 04-05** (5 min) | AuthN: identidad, JWT, los 7 vehículos |
| 2 | **La brecha A01** (3 min) | Estás logueado ≠ podés hacerlo. OWASP lo confirma |
| 3 | **El módulo 06** (4 min) | RBAC + object-level + scopes + tenancy + la matriz |
| 4 | **Actividad** (60 min) | Leé la SPEC y completá los 4 archivos 🔓 |
| 5 | **Entrega obligatoria** | Rollo: fork + PR antes del **22/09 23:59** |

> La lectura previa (`MATERIAL_PREVIO.md`) ya la hiciste en casa. Si no, hoy
> vas a ver pasar la clase por la ventana y la fecha límite no se corre.

---

<!-- note: |
  REPASO 04. Rápido: la API pasó de "recibe cualquier request" a "sabe quién
  sos". 4 hitos, 30 segundos cada uno. Preguntar al aire quién se acuerda
  del hash que usamos (Argon2) y si el JWT se firma o se encripta (se firma).
  Timing: apertura 2-4 min
-->

<!-- _class: smaller -->

## Repaso · Clase 04 — Autenticación

En el Módulo 04 la API pasó de recibir **cualquier request** a saber **quién sos**:

1. **Hash Argon2** — la contraseña NUNCA se guarda en texto plano.
   Guardamos un hash *irreversible y lento*. (¿Alguno se acuerda de pwdlib?)

2. **JWT firmado** — al loguear, el server emite un token **firmado**:
   `header.payload.firma`. Ojo: se **firma**, no se encripta →
   el payload es legible sin el secreto.

```python
# security.py (04/05/06) — el payload del JWT es legible SIN el secreto
{"sub": "1", "iat": 1717..., "exp": 1718...}
```

3. **Sesión server-side vs JWT** — estado en el server (revocación
   inmediata) vs token autocontenido (stateless, escala).

4. **OWASP** — las amenazas de la autenticación (A07/A02 de aquel momento).

> La lección del 04: *"sin saber quién sos, no podés decidir qué podés hacer"*
> — y esa última parte es EXACTAMENTE la clase de hoy.

---

<!-- note: |
  REPASO 05. 7 métodos + rate limit. No los repasamos uno por uno: la tabla
  con la LECCIÓN de cada uno alcanza. El puente: todos resuelven "cómo
  demuestro quién soy" — ninguno decide "qué puedo hacer". Ese es el hueco.
  Timing: apertura 4-6 min
-->

<!-- _class: smaller -->

## Repaso · Clase 05 — Los 7 vehículos de identidad

| Método | Cómo demuestra quién sos | La lección |
|--------|--------------------------|------------|
| **1 · Basic** | `Authorization: Basic base64(usuario:pass)` | base64 ≠ cifrado. Solo sobre HTTPS |
| **2 · Session** | cookie `session_id` httpOnly, estado en server | revocación inmediata · es la cookie de la facultad |
| **3 · Token opaco** | `Bearer <token aleatorio>` guardado en server | igual que session, sin cookie → para APIs |
| **4 · JWT header** | `Bearer <jwt firmado>` | **stateless**: no hay estado que revocar |
| **5 · JWT cookie** | el mismo JWT, pero en cookie httpOnly | tradeoff XSS vs CSRF según el vehículo |
| **6 · OAuth2** | `POST /token` (grant_type=password) | OAuth2 es el PROTOCOLO; JWT es el FORMATO |
| **7 · SSO** | el IdP emite id_token validado (iss/aud) | SSO es la experiencia; JIT provisioning |

Y la frutilla: **rate limit** — 6 intentos fallidos → `429 Retry-After`.

> Todos resuelven la MISMA pregunta: **"¿cómo demuestro quién soy?"**
> Ninguno responde **"¿qué puedo hacer?"**. Ese hueco se llama AUTORIZACIÓN.

---

<!-- note: |
  La conexión directa con el cierre del módulo 04: la tabla de "las 3
  preguntas". Este es el momento de activar la memoria: el 04 prometió este
  módulo. Ahora llega. La pregunta clave de la slide es la 2ª.
  Timing: apertura 6-8 min
-->

<!-- _class: smaller -->

## Las 3 preguntas (la promesa del Módulo 04)

En el 04 vimos esta tabla y quedó una promesa pendiente:

| Pregunta | Nombre | Estado |
|----------|--------|--------|
| 1 · ¿Quién sos? | **Autenticación** | ✅ Clases 04 y 05 |
| 2 · ¿Qué podés hacer? | **Autorización** | ⬅️ **HOY** (aula invertida) |
| 3 · ¿Cómo lo demuestro? | Sesión / Token | ✅ Clases 04 y 05 |

> *"La autorización es el próximo módulo"* — lo dijo la clase 04.
> **Hoy es ese próximo módulo.** Y termina la trilogía de la seguridad.

---

<!-- _class: brecha -->
<!-- note: |
  LA LECCIÓN CENTRAL DE TODO EL CURSO. OWASP A01 es la brecha #1 desde 2021.
  Mostrar el ejemplo concreto del IDOR: viewer@acme.com pidiendo GET /5
  (plan secreto de Globex). Si el server responde 200 → IDOR. Ese ejemplo
  lo van a ver en vivo en el frontend del módulo.
  No mostrar el 5 humillando al que no leyó; es la pregunta de la clase.
  Timing: apertura 8-9 min
-->

## La brecha #1 de la industria (OWASP A01)

Desde 2021, el **Top 10 de OWASP** pone en primer lugar:

> **Broken Access Control** — "la autorización rota" supera a la inyección.

La pesadilla en una línea:

```
Sos viewer de Acme. Pedís GET /api/documents/5 (plan secreto de Globex).
Tu rol no debería poder. Pero NADA en el server lo verifica.
Respuesta: 200 OK. 🕳️
```

Ese caso (conocido como **IDOR**) es EXACTAMENTE el que vas a arreglar hoy:
el endpoint existe, el documento existe, y el server **no pregunta quién pide**.

> La autenticación de las clases 04-05 ya te dijo *quién sos*.
> La autorización de hoy decide si ese *quién* tiene **permiso**. Son las
> dos caras de la puerta: sin la 2ª, la 1ª no alcanza.

---

<!-- note: |
  INTRO 06. Los 5 pilares del módulo (match con el README del módulo).
  No entrar en detalle de cada uno — la spec y el material previo lo cubren.
  Este es el MAPA conceptual para que la lectura tenga dónde colgarse.
  Timing: apertura 9-10 min
-->

<!-- _class: fase -->

## El módulo 06 — los 5 pilares

| Pilar | Qué resuelve | El caso que vas a probar |
|-------|--------------|--------------------------|
| **RBAC** | Roles `admin`·`editor`·`viewer` con permisos | viewer recibe 403 al borrar |
| **Object-level** | Un editor no ve el privado de otro | **IDOR mitigado** en `GET /documents/{id}` |
| **Scopes** | El TOKEN tiene límites propios | admin con scope `read` no crea documentos |
| **Multi-tenancy** | Cada empresa ve SOLO la suya | admin de Globex no ve usuarios de Acme |
| **Deny-by-default** | Endpoint sin autorización = bug | cualquier endpoint sin `Depends` es una puerta abierta |

> **La matriz de autorización**: cada celda define qué HTTP code devuelve
> cada rol. El script `verificar_authz.sh` (44 checks) la mide por vos.

---

<!-- note: |
  La matriz resumida. Es la "tabla de verdad" de todo el módulo — va a
  aparecer en la spec, en el frontend y en la defensa oral. No explicar cada
  celda acá: es el hook de la lectura.
  Timing: apertura 10-11 min
-->

<!-- _class: smaller -->

## La matriz (el corazón de la entrega)

| Operación | admin | editor | viewer |
|-----------|:-----:|:------:|:------:|
| Listar usuarios / cambiar roles | ✅ | 403 | 403 |
| Crear / editar / publicar documentos | ✅ | ✅ lo suyo | 403 (scope read) |
| **Ver doc privado de OTRO** | ✅ | **403** | **403** |
| Ver doc de otra empresa | 403 | 403 | 403 |
| Borrar documentos | ✅ | 403 | 403 |
| Escribir con token `read` | 403 | 403 | 403 |

> Las celdas en **rojo son las que el script verifica**: 44 casos de esta
> matriz, uno por uno. Tu trabajo es que el server las devuelva tal cual.

---

<!-- note: |
  El plan de la actividad: aula invertida + trabajo individual obligatorio.
  Es distinto al resto del curso (grupos): hoy es INDIVIDUAL y CON ENTREGA.
  Marcar el timing: 60 min + la fecha límite del 22/09.
  Timing: apertura 11-12 min → ¡a trabajar!
-->

<!-- _class: fase -->

## El plan — aula invertida + entrega individual

> La lectura ya la hiciste en casa. Hoy construís **SOLO**.

| Min | Qué hacés |
|-----|-----------|
| 0-5 | **Leé la SPEC** (`SPEC.md`) — la spec de la entrega manda |
| 5-30 | **Backend**: `dependencies.py` → `users_controller.py` → `documents_controller.py` |
| 30-40 | **Verificá**: `bash scripts/verificar_authz.sh` (mete 44/44 verdes) |
| 40-55 | **Frontend**: completá `authz.ts` y alineá la UI con el server |
| 55-60 | **Prepará la entrega**: fork + PR + copiá la salida del script |

```bash
cd 06-autorizacion-rbac/backend && uv sync && uv run -m app.main   # :8000
cd ../frontend && pnpm install && pnpm dev                          # :5173
```

> **Regla del taller**: el docente no da respuestas. Hace preguntas.
> *"¿Qué debería devolver el server si vos fueras viewer?"* destraba casi todo.

---

<!-- _class: entrega -->
<!-- note: |
  LA ENTREGA OBLIGATORIA. Leer los números en voz alta y lenta:
  FECHA 22/09 23:59 · 4 ARCHIVOS · SCRIPT 40% · DEFENSA ORAL 30%.
  Aclarar: la solución NO está en el repo y se libera DESPUÉS de la fecha
  (rama solucion), como en el módulo 04. Copiar = defensa imposible.
  Timing: 30 segundos (ya está en la spec)
-->

## 🚦 La entrega — obligatoria

- **Qué**: fork del repo de la cátedra + PR con los **4 archivos 🔓**
  (`dependencies.py`, `users_controller.py`, `documents_controller.py`, `authz.ts`)
- **Cuándo**: antes del **miércoles 22/09 23:59** — no se recibe por otro canal
- **Cómo se corrige**: script `verificar_authz.sh` (**44 checks**) + revisión
  de código + **defensa oral de 5 min** en la clase siguiente
- **Nota**: script 40% · código 30% · defensa oral 30%

> La solución se publica en la rama `solucion` del repo base **después** de la
> entrega. Copiarla sin entender solo te deja con un script que pasa y una
> defensa oral que no vas a poder sostener ni un minuto.

---

<!-- _class: biblio -->
<!-- note: |
  LECTURAS PARA PROFUNDIZAR — 3 niveles: lo oficial (OWASP), la teoría
  (NIST/RFC) y la práctica (artículos). No obligatorias para la entrega,
  pero son las que separan un 6 de un 10 en la defensa oral.
  Timing: si sobra tiempo de la apertura; si no, queda para casa.
-->

## Lecturas sugeridas para profundizar

**Oficial (leé al menos una)**

- OWASP Top 10 · A01 *Broken Access Control* — owasp.org/Top10/A01_2021-Broken_Access_Control/
- OWASP *Authorization Cheat Sheet* — cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
- OWASP API Security Top 10 2023 · BOLA (el IDOR en APIs) — owasp.org/API-Security/

**Teoría (para la defensa oral)**

- **RBAC**: NIST/INCITS 359-2012 — la definición formal de roles y permisos
- **Scopes**: RFC 6749 (OAuth 2.0), §3.3 *Access Token Scope* — de dónde sale el `scope` del token
- **Tenancy**: *multi-tenancy authorization patterns* — por qué el tenant es parte de la identidad

**Práctica (las que más se aprenden)**

- Write-ups de **IDOR** en bug bounty (HackerOne) — el tipo de bug que hoy aprendés a cerrar
- El `MATERIAL_PREVIO.md` del módulo — con su propia bibliografía comentada

> En la defensa oral, citar de dónde sale cada decisión (OWASP, NIST, RFC)
> es la diferencia entre "seguí la guía" y "entendí la materia".

---

<!-- _class: lead -->
<!-- note: |
  Cierre de la apertura. La frase final engancha con el front-end: la lección
  viva se ve en la consola (200 verde = puerta abierta, 403 rojo = cerrada).
  Dar el picado: "eso que está en rojo en la consola es el bug que te querés
  comer; que en verde solo aparezca lo que la matriz dice" .
  Timing: 30 segundos → start.
-->

## Hoy la API decide

### Quién sos ya lo sabe (04-05). **Qué podés hacer** lo construís vos.

> *"La Universidad te da el mapa. El recorrido lo hacés vos."*
> — y este recorrido tiene fecha: **22/09**.