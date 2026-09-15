# Desarrollo de Software 2026 — Backend

> **Materia**: Desarrollo de Software
> **Carrera**: Ingeniería de Software — 4to año
> **Universidad**: UTN Facultad Regional La Plata

---

## Aviso Importante

**Este repositorio es de carácter exclusivamente académico y complementario.**

El material práctico de los módulos 00 a 05 **NO es obligatorio** para la
aprobación de la materia. No hay entregas que evaluar, ni puntos que sumar,
ni notas que dependan de estos módulos. Son formación de competencias
profesionales para quienes quieran ir más allá del contenido mínimo.

> **Única excepción**: el [**Módulo 06 — Autorización RBAC**](./06-autorizacion-rbac/)
> es una **entrega obligatoria** de la cursada (trabajo práctico individual,
> fecha límite y defensa oral definidos en su README). Es el cierre del ciclo
> autenticación → autorización que la materia evalúa.

El **único objetivo** es **formar competencias profesionales** en desarrollo backend. Está pensado para aquellos estudiantes que:

- Quieran ir más allá del contenido mínimo de la cursada
- Busquen desarrollar habilidades que las empresas demandan hoy
- Entiendan que la Universidad marca el camino, pero el **profesional se construye a sí mismo**

> *"La Universidad te da el mapa. El recorrido lo hacés vos."*

---

## Módulos

| # | Módulo | Estado | Contenido |
|---|--------|--------|-----------|
| 00 | [Introducción](./00-introduccion/) | ✅ | FastAPI y Fastify — Hola Mundo, Swagger, conceptos fundamentales |
| 01 | [Mi Primera APP](./01-mi-primera-app/) | ✅ | Taller guiado: API de Tareas + Frontend React en 90 minutos |
| 02 | [Persistencia con PostgreSQL](./02-persistencia-postgresql/) | ✅ | Datos que sobreviven: psycopg + pool, SQL básico, Docker demo + Supabase. Frontend del 01 reutilizado sin cambios |
| 03 | [Arquitectura en Capas + ORM](./03-arquitectura-en-capas/) | ✅ | Controller → Service → Repository, SQLModel (ORM), CRUD completo, frontend TypeScript. Taller por grupos en aula invertida |
| 04 | [Autenticación y Seguridad](./04-autenticacion-seguridad/) | ✅ | Usuarios, register + login, hash Argon2, JWT, sesiones (server-side vs token), SSO vs JWT, seguridad OWASP. Taller por grupos en aula invertida |
| 05 | [Métodos de Autenticación](./05-metodos-autenticacion/) | ✅ | Los 7 métodos lado a lado (Basic, Session, Token, JWT, Cookie, OAuth2, SSO), rate limiting, security headers, laboratorio frontend. Clase asincrónica |
| 06 | [**Autorización RBAC**](./06-autorizacion-rbac/) | ✅ | **Entrega OBLIGATORIA**: roles admin/editor/viewer, object-level access control (IDOR), scopes en JWT, multi-tenancy, deny-by-default. 44 checks de verificación + defensa oral |

---

## Roadmap

- [x] ~~Laboratorios de HTTP raw con `curl`~~ (incluido en módulo 01)
- [x] ~~Persistencia con PostgreSQL~~ (módulo 02: conexión, pool, SQL CRUD, schema)
- [ ] Servidor HTTP desde cero (sin frameworks)
- [x] ~~Arquitectura en capas completa~~ (módulo 03: Controller → Service → Repository + SQLModel)
- [x] ~~Autenticación JWT~~ (módulo 04: register + login, hash Argon2, JWT, sesiones, SSO vs JWT, OWASP)
- [x] ~~Autorización RBAC (roles y permisos)~~ (módulo 06: roles admin/editor/viewer, IDOR, scopes, tenancy, deny-by-default — entrega obligatoria)
- [ ] Migraciones formales con Alembic
- [ ] Testing automatizado (unitario + integración)
- [ ] Dockerización y CI/CD (módulo 02 solo usa Docker para el postgres de la demo)
- [x] ~~Frontend con TypeScript~~ (módulo 03: React-TS con tipos que reflejan el contrato de la API)
- [ ] Proyecto integrador: API de Gestión de Proyectos y Tareas

---

## Para el Estudiante

Cada módulo es **autocontenido** — tiene sus propias dependencias, configuración y notas. Cada uno incluye un archivo `NOTAS_ACADEMICAS.md` con explicación conceptual, análisis línea por línea y ejercicios progresivos.

La propuesta es simple:

1. Leé las notas académicas antes de ejecutar código
2. Ejecutá los ejemplos y experimentá modificándolos
3. Hacé los ejercicios — en especial los nivel 🟡 y 🔴
4. Investigá — usá las referencias para ir más profundo
5. Preguntá — en clase, en el foro, con tus compañeros

No importa si avanzás lento. Importa que **cada concepto lo entiendas de verdad**.

---

> *Este repositorio no te va a dar una nota. Te va a dar herramientas. Lo que hagas con ellas depende de vos.*
> **Ponete las pilas. El mercado no espera.**
