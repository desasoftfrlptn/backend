"""
Almacenamiento EN MEMORIA (para el ejemplo) — usuarios + documentos + tenancy.

En producción esto es PostgreSQL/otro. Acá usamos dicts para que el módulo sea
autocontenido: corre sin infra y el script de corrección se puede ejecutar en
cualquier máquina.

EL SEED es el DATASET FIJO de la entrega: dos empresas (tenants), cuatro
usuarios demo y cinco documentos. Todas las verificaciones automáticas se
basan en estos datos, así que NO los borres ni los renombres (podés agregar).

  Tenant 1 · Acme Corp              Tenant 2 · Globex Inc
    admin@acme.com   (admin)          admin@globex.com (admin)
    editor@acme.com  (editor)
    viewer@acme.com  (viewer)

  Documentos:
    #1 "Manual de bienvenida"  público, publicado   (owner: admin acme)
    #2 "Estrategia 2026"       privado, draft        (owner: admin acme)
    #3 "Notas de reunión"      privado, draft        (owner: editor acme)
    #4 "Informe público Q3"    público, publicado    (owner: editor acme)
    #5 "Plan secreto Globex"   privado, draft        (owner: admin globex)

  Password de TODOS los usuarios demo: demo12345

Este archivo NO se modifica en la entrega. La autorización se escribe en las
dependencias y los controllers, no acá (el storage solo guarda y busca).
"""

from datetime import datetime, timezone
from threading import RLock

from app import security
from app.config import DEFAULT_TENANT_ID, DEMO_PASSWORD
from app.models import Document, DocumentCreate, DocumentUpdate, Role, User, UserCreate

# RLock reentrante: seed() crea users y docs, y ambas funciones adquieren el
# mismo lock. Con Lock() normal eso es un DEADLOCK.
_lock = RLock()


def _now() -> datetime:
    return datetime.now(timezone.utc)


# ── Estado en memoria ──────────────────────────────────────────────────────

tenants: dict[int, str] = {
    1: "Acme Corp",
    2: "Globex Inc",
}

users: dict[int, User] = {}
documents: dict[int, Document] = {}

_next_user_id: int = 1
_next_doc_id: int = 1


# ── Seed ───────────────────────────────────────────────────────────────────


def seed() -> None:
    """Crea el dataset demo (si no existe). Se llama al arrancar el server."""
    with _lock:
        if users:
            return
        admin_acme = create_user(
            UserCreate(email="admin@acme.com", name="Admin Acme", password=DEMO_PASSWORD),
            role=Role.ADMIN,
            tenant_id=1,
        )
        editor_acme = create_user(
            UserCreate(email="editor@acme.com", name="Editor Acme", password=DEMO_PASSWORD),
            role=Role.EDITOR,
            tenant_id=1,
        )
        create_user(
            UserCreate(email="viewer@acme.com", name="Viewer Acme", password=DEMO_PASSWORD),
            role=Role.VIEWER,
            tenant_id=1,
        )
        admin_globex = create_user(
            UserCreate(email="admin@globex.com", name="Admin Globex", password=DEMO_PASSWORD),
            role=Role.ADMIN,
            tenant_id=2,
        )

        create_document(admin_acme, DocumentCreate(
            title="Manual de bienvenida",
            content="Cómo configurar tu cuenta y tus herramientas.",
        ), visibility="public", published=True)
        create_document(admin_acme, DocumentCreate(
            title="Estrategia 2026",
            content="Objetivos anuales y presupuesto. CONFIDENCIAL.",
        ), visibility="private", published=False)
        create_document(editor_acme, DocumentCreate(
            title="Notas de reunión",
            content="Acciones acordadas con el equipo de marketing.",
        ), visibility="private", published=False)
        create_document(editor_acme, DocumentCreate(
            title="Informe público Q3",
            content="Resultados del trimestre, versión para clientes.",
        ), visibility="public", published=True)
        create_document(admin_globex, DocumentCreate(
            title="Plan secreto Globex",
            content="Lanzamiento sorpresa. NO debe verlo Acme.",
        ), visibility="private", published=False)


# ── Usuarios ───────────────────────────────────────────────────────────────


def create_user(body: UserCreate, role: Role = Role.VIEWER, tenant_id: int | None = None) -> User | None:
    """Crea un usuario. Devuelve None si el email ya existe.

    Un usuario nuevo SIEMPRE nace como viewer (regla de negocio): el rol lo
    asigna un admin después con PATCH /api/users/{id}/role.
    """
    global _next_user_id
    email = body.email.lower().strip()
    with _lock:
        if get_user_by_email(email) is not None:
            return None
        user = User(
            id=_next_user_id,
            email=email,
            name=body.name,
            password_hash=security.hash_password(body.password),
            role=role,
            tenant_id=tenant_id or DEFAULT_TENANT_ID,
        )
        users[user.id] = user
        _next_user_id += 1
        return user


def get_user_by_email(email: str) -> User | None:
    with _lock:
        for u in users.values():
            if u.email == email.lower().strip():
                return u
    return None


def get_user_by_id(user_id: int) -> User | None:
    with _lock:
        return users.get(user_id)


def list_users(tenant_id: int) -> list[User]:
    """TODOS los usuarios de UNA empresa. La regla de tenancy se aplica ACÁ:
    nunca se devuelve un usuario de otra empresa. El que llama ya autorizó."""
    with _lock:
        return [u for u in users.values() if u.tenant_id == tenant_id]


def set_user_role(user_id: int, role: Role) -> User | None:
    """Cambia el rol de un usuario. Devuelve None si el usuario no existe."""
    with _lock:
        user = users.get(user_id)
        if user is None:
            return None
        user.role = role
        return user


def user_count() -> int:
    with _lock:
        return len(users)


# ── Documentos ─────────────────────────────────────────────────────────────


def create_document(
    owner: User,
    body: DocumentCreate,
    visibility: str = "private",
    published: bool = False,
) -> Document:
    """Crea un documento a nombre del owner, en el tenant del owner.

    El tenant_id NO viene del body: viene del usuario autenticado. Un usuario
    de Acme no puede crear documentos de Globex ni a palos (no hay forma de
    pedirlo).
    """
    global _next_doc_id
    with _lock:
        doc = Document(
            id=_next_doc_id,
            owner_id=owner.id,
            tenant_id=owner.tenant_id,
            title=body.title,
            content=body.content,
            visibility=visibility,
            published=published,
        )
        documents[doc.id] = doc
        _next_doc_id += 1
        return doc


def get_document(doc_id: int) -> Document | None:
    with _lock:
        return documents.get(doc_id)


def list_documents(tenant_id: int, user_id: int) -> list[Document]:
    """Lo que un usuario PUEDE ver dentro de su empresa:
    - documentos públicos del tenant, + 
    - los documentos propios (cualquier visibilidad/estado).
    Los documentos de OTRA empresa jamás aparecen acá (tenancy en el storage).
    """
    with _lock:
        return [
            d for d in documents.values()
            if d.tenant_id == tenant_id and (d.visibility == "public" or d.owner_id == user_id)
        ]


def update_document(doc_id: int, body: DocumentUpdate) -> Document | None:
    """Aplica los campos presentes del body. Devuelve None si no existe."""
    with _lock:
        doc = documents.get(doc_id)
        if doc is None:
            return None
        if body.title is not None:
            doc.title = body.title
        if body.content is not None:
            doc.content = body.content
        if body.visibility is not None:
            doc.visibility = body.visibility
        return doc


def set_document_published(doc_id: int, published: bool) -> Document | None:
    """Publica (o despublica) un documento. Devuelve None si no existe."""
    with _lock:
        doc = documents.get(doc_id)
        if doc is None:
            return None
        doc.published = published
        return doc


def delete_document(doc_id: int) -> Document | None:
    """Borra un documento. Devuelve None si no existe."""
    with _lock:
        return documents.pop(doc_id, None)


def document_count() -> int:
    with _lock:
        return len(documents)


def tenant_count() -> int:
    with _lock:
        return len(tenants)