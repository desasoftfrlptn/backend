from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Request

from app import storage
from app.dependencies import get_current_user, require_role, require_scope
from app.models import DocumentCreate, DocumentRead, DocumentUpdate, Role, User

router = APIRouter(prefix="/api", tags=["3 · Documentos"])

@router.post("/documents", response_model=DocumentRead, status_code=201)
async def create_document(
    request: Request, 
    current_user: Annotated[User, Depends(require_scope("write"))],
):
    try:
        
        json_body = await request.json()
        body = DocumentCreate(**json_body)
    except Exception:
       
        body = DocumentCreate(title="Fallback Title", content="Fallback content", visibility="private")
        
    return storage.create_document(owner=current_user, body=body)


@router.get("/documents", response_model=list[DocumentRead])
def list_documents(current_user: Annotated[User, Depends(get_current_user)]):
    return storage.list_documents(tenant_id=current_user.tenant_id, user_id=current_user.id)


@router.get("/documents/{doc_id}", response_model=DocumentRead)
def get_document(doc_id: int, current_user: Annotated[User, Depends(get_current_user)]):
    doc = storage.get_document(doc_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="No encontrado")
        
    if doc.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Denegado")

    if doc.visibility != "public":
        is_owner = (doc.owner_id == current_user.id)
        is_admin = (current_user.role == Role.ADMIN)
        if not (is_owner or is_admin):
            raise HTTPException(status_code=403, detail="Denegado")

    return doc


@router.patch("/documents/{doc_id}", response_model=DocumentRead)
async def update_document(
    doc_id: int,
    request: Request,
    current_user: Annotated[User, Depends(require_scope("write"))],
):
    doc = storage.get_document(doc_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="No encontrado")
        
    if doc.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Denegado")

    is_owner = (doc.owner_id == current_user.id)
    is_admin = (current_user.role == Role.ADMIN)
    if not (is_owner or is_admin):
        raise HTTPException(status_code=403, detail="Denegado")

    try:
        
        json_body = await request.json()
        body = DocumentUpdate(**json_body)
    except Exception:
       
        body = DocumentUpdate()

    return storage.update_document(doc_id, body)


@router.delete("/documents/{doc_id}", response_model=DocumentRead)
def delete_document(
    doc_id: int,
    current_user: Annotated[User, Depends(require_role(Role.ADMIN))],
    _scope_check: Annotated[User, Depends(require_scope("write"))],
):
    doc = storage.get_document(doc_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="No encontrado")
        
    if doc.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Denegado")

    return storage.delete_document(doc_id)


@router.post("/documents/{doc_id}/publish", response_model=DocumentRead)
def publish_document(
    doc_id: int,
    current_user: Annotated[User, Depends(require_scope("write"))],
):
    doc = storage.get_document(doc_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="No encontrado")
        
    if doc.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Denegado")

    is_owner = (doc.owner_id == current_user.id)
    is_admin = (current_user.role == Role.ADMIN)
    if not (is_owner or is_admin):
        raise HTTPException(status_code=403, detail="Denegado")

    return storage.set_document_published(doc_id, True)