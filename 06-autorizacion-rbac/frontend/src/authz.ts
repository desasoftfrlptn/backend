import type { DocumentRead, Role } from "./types";

/**
 * ¿Este TOKEN puede escribir? El scope viaja en el JWT
 * ("read" | "read write") y lo limita el LOGIN, no el rol.
 */
export function scopeAllowsWrite(scope: string | undefined): boolean {
  return scope?.split(" ").includes("write") ?? false;
}

/** ¿Puede ver el panel de usuarios (GET /api/users)? Solo admin. */
export function canManageUsers(role: Role | undefined): boolean {
  return role === "admin";
}

/** ¿Puede cambiar el rol de otro usuario (PATCH /users/{id}/role)? Solo admin. */
export function canChangeRole(role: Role | undefined): boolean {
  return role === "admin";
}

/** ¿Puede BORRAR documentos (DELETE /api/documents/{id})? Solo admin. */
export function canDelete(role: Role | undefined): boolean {
  return role === "admin";
}

/**
 * ¿Puede EDITAR un documento? Dueño del documento o admin de la empresa.
 */
export function canEdit(userId: number, doc: DocumentRead, role: Role | undefined): boolean {
  return doc.owner_id === userId || role === "admin";
}

/**
 * ¿Puede PUBLICAR un documento? Dueño del documento o admin de la empresa.
 */
export function canPublish(userId: number, doc: DocumentRead, role: Role | undefined): boolean {
  return doc.owner_id === userId || role === "admin";
}