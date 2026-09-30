import type { DocumentRead, Role } from "./types";

/**
 * ¿Este TOKEN puede escribir? El scope viaja en el JWT
 * ("read" | "read write") y lo limita el LOGIN, no el rol:
 * un admin puede loguearse con scope "read" y quedar SOLO LECTURA.
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
 * ¿Puede EDITAR un documento? Regla de la matriz:
 *   - el DUEÑO siempre puede (object-level)
 *   - el ADMIN puede editar cualquiera de su empresa
 *   - un editor NO edita el privado de otro → false
 */
export function canEdit(userId: number, doc: DocumentRead, role: Role | undefined): boolean {
  return doc.owner_id === userId || role === "admin";
}

/**
 * ¿Puede PUBLICAR un documento? Misma regla que editar
 * (dueño o admin) — pero fijate que el viewer queda afuera
 * por su scope "read", que también bloquea la UI con scopeAllowsWrite.
 */
export function canPublish(userId: number, doc: DocumentRead, role: Role | undefined): boolean {
  return doc.owner_id === userId || role === "admin";
}