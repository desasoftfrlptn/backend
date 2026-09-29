"""
Controller de documentos: el recurso que se protege.

  POST   /api/documents               → crear     (scope "write")
  GET    /api/documents               → listar    (públicos de tu empresa + los tuyos)
  GET    /api/documents/{id}          → ver       (dueño, admin o público)
  PATCH  /api/documents/{id}          → editar    (dueño o admin, scope "write")
  DELETE /api/documents/{id}          → borrar    (solo admin, scope "write")
  POST   /api/documents/{id}/publish  → publicar  (dueño o admin, scope "write")

Reglas que se aplican en todos los endpoints con {id}:
  1. Si el documento no existe → 404.
  2. Si es de otra empresa → 403 (aunque sea público y aunque seas admin).
  3. Si es privado, solo lo toca el dueño o un admin de la empresa.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app import storage
from app.dependencies import get_current_user, require_role, require_scope
from app.models import Document, DocumentCreate, DocumentRead, DocumentUpdate, Role, User

router = APIRouter(prefix="/api", tags=["3 · Documentos"])


def _buscar_documento(doc_id: int, current_user: User) -> Document:
    """Trae el documento o corta con 404 / 403 si no es de tu empresa."""
    doc = storage.get_document(doc_id)
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento no encontrado")
    if doc.tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ese documento pertenece a otra empresa",
        )
    return doc


def _es_duenio_o_admin(doc: Document, user: User) -> bool:
    return doc.owner_id == user.id or user.role == Role.ADMIN


@router.post(
    "/documents",
    response_model=DocumentRead,
    status_code=status.HTTP_201_CREATED,
)
def create_document(
    body: DocumentCreate,
    current_user: User = Depends(require_scope("write")),
):
    """Crea un documento: nace como borrador privado del autor, en su empresa."""
    return storage.create_document(owner=current_user, body=body)


@router.get("/documents", response_model=list[DocumentRead])
def list_documents(
    current_user: User = Depends(get_current_user),
):
    """Lista lo que podés ver. El filtro por empresa y dueño lo hace el storage."""
    return storage.list_documents(
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
    )


@router.get("/documents/{doc_id}", response_model=DocumentRead)
def get_document(
    doc_id: int,
    current_user: User = Depends(get_current_user),
):
    """Ve un documento. Si es privado, solo el dueño o un admin."""
    doc = _buscar_documento(doc_id, current_user)
    if doc.visibility == "private" and not _es_duenio_o_admin(doc, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No podés ver este documento",
        )
    return doc


@router.patch("/documents/{doc_id}", response_model=DocumentRead)
def update_document(
    doc_id: int,
    body: DocumentUpdate,
    current_user: User = Depends(require_scope("write")),
):
    """Edita un documento: solo el dueño o un admin de la empresa."""
    doc = _buscar_documento(doc_id, current_user)
    if not _es_duenio_o_admin(doc, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No podés editar este documento",
        )
    return storage.update_document(doc_id, body)


@router.delete("/documents/{doc_id}", response_model=DocumentRead)
def delete_document(
    doc_id: int,
    current_user: User = Depends(require_role(Role.ADMIN)),
    _: User = Depends(require_scope("write")),
):
    """Borra un documento: solo admin, y con un token que pueda escribir."""
    _buscar_documento(doc_id, current_user)
    return storage.delete_document(doc_id)


@router.post("/documents/{doc_id}/publish", response_model=DocumentRead)
def publish_document(
    doc_id: int,
    current_user: User = Depends(require_scope("write")),
):
    """Publica un documento: el dueño el suyo, el admin cualquiera de su empresa."""
    doc = _buscar_documento(doc_id, current_user)
    if not _es_duenio_o_admin(doc, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No podés publicar este documento",
        )
    return storage.set_document_published(doc_id, True)
