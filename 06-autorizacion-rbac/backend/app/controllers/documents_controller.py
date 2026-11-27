"""
Controller de DOCUMENTOS — el recurso protegido (object-level + scopes + tenancy).
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app import storage
from app.dependencies import get_current_user, require_role, require_scope
from app.models import DocumentCreate, DocumentRead, DocumentUpdate, Role, User

router = APIRouter(prefix="/api", tags=["3 · Documentos"])


@router.post(
    "/documents",
    response_model=DocumentRead,
    status_code=status.HTTP_201_CREATED,
)
def create_document(
    body: DocumentCreate,
    current_user: User = Depends(require_scope("write")),
):
    """Crea un documento: draft privado a nombre tuyo, en TU empresa."""
    return storage.create_document(owner=current_user, body=body)


@router.get("/documents", response_model=list[DocumentRead])
def list_documents(
    current_user: User = Depends(get_current_user),
):
    """Lista lo que PODÉS ver: públicos de tu empresa + tus documentos."""
    return storage.list_documents(
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
    )


@router.get("/documents/{doc_id}", response_model=DocumentRead)
def get_document(
    doc_id: int,
    current_user: User = Depends(get_current_user),
):
    """Ve un documento por id con control de tenancy y object-level (mitiga IDOR)."""
    doc = storage.get_document(doc_id)
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento no encontrado")

    # 1. Tenancy: ningún usuario (ni siquiera admin) ve documentos de otra empresa.
    if doc.tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No podés ver documentos de otra empresa",
        )

    # 2. Si es público dentro del mismo tenant, todos los roles pueden verlo.
    if doc.visibility == "public":
        return doc

    # 3. Object-level: si es privado, solo el dueño o un admin de la empresa acceden.
    if doc.owner_id != current_user.id and current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tenés permiso para ver este documento privado",
        )

    return doc


@router.patch("/documents/{doc_id}", response_model=DocumentRead)
def update_document(
    doc_id: int,
    body: DocumentUpdate,
    current_user: User = Depends(require_scope("write")),
):
    """Edita un documento: exige scope write + mismo tenant + dueño o admin."""
    doc = storage.get_document(doc_id)
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento no encontrado")

    # Tenancy: bloquea edición cross-tenant.
    if doc.tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No podés editar documentos de otra empresa",
        )

    # Object-level: solo el dueño del documento o un admin del tenant pueden editar.
    if doc.owner_id != current_user.id and current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No podés editar este documento",
        )

    return storage.update_document(doc_id, body)


@router.delete("/documents/{doc_id}", response_model=DocumentRead)
def delete_document(
    doc_id: int,
    current_user: User = Depends(require_role(Role.ADMIN)),
    _write_check: User = Depends(require_scope("write")),
):
    """Borra un documento: SOLO admin con scope write y dentro de su empresa."""
    doc = storage.get_document(doc_id)
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento no encontrado")

    # Tenancy: un admin de Acme no puede borrar documentos de Globex.
    if doc.tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No podés borrar documentos de otra empresa",
        )

    deleted = storage.delete_document(doc_id)
    return deleted


@router.post("/documents/{doc_id}/publish", response_model=DocumentRead)
def publish_document(
    doc_id: int,
    current_user: User = Depends(require_scope("write")),
):
    """Publica un documento: exige scope write + mismo tenant + dueño o admin."""
    doc = storage.get_document(doc_id)
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento no encontrado")

    # Tenancy: bloquea publicación cross-tenant.
    if doc.tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No podés publicar documentos de otra empresa",
        )

    # Object-level: solo el dueño o un admin del tenant pueden publicar.
    if doc.owner_id != current_user.id and current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No podés publicar este documento",
        )

    return storage.set_document_published(doc_id, True)