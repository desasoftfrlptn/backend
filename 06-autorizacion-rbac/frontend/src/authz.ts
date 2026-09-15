/**
 * SOLUCIÓN — la autorización en la INTERFAZ.
 *
 * Cada helper replica la MATRIZ que el server implementa en
 * dependencies.py + controllers (SPEC.md sección 3). La UI los usa
 * para no mostrar acciones que el server va a rechazar con 403 —
 * eso es UX honesta, NO seguridad: la decisión real vive en el server.
 *
 * Regla de oro (la misma que en el backend):
 *   - El ROL decide qué acciones existen (RBAC + object-level).
 *   - El SCOPE (del token) limita qué puede hacer ESTE token, aunque el
 *     rol lo permita. scopeAllowsWrite es el único que mira el token.
 */

import type { DocumentRead, Role } from "./types";

/**
 * ¿Este TOKEN puede escribir? El scope viaja en el JWT
 * ("read" | "read write") y lo limita el LOGIN, no el rol:
 * un admin puede loguearse con scope "read" y quedar SOLO LECTURA.
 */
export function scopeAllowsWrite(scope: string | undefined): boolean {
  return (scope ?? "").split(" ").includes("write");
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
 *   - el ADMIN edita cualquiera de su empresa
 *   - un editor NO edita el privado de otro → false
 */
export function canEdit(userId: number, doc: DocumentRead, role: Role | undefined): boolean {
  return doc.owner_id === userId || role === "admin";
}

/**
 * ¿Puede PUBLICAR un documento? Misma regla que editar (dueño o admin).
 * El viewer queda afuera además por su scope "read", que también bloquea
 * la UI con scopeAllowsWrite — doble candado, como en el server.
 */
export function canPublish(userId: number, doc: DocumentRead, role: Role | undefined): boolean {
  return doc.owner_id === userId || role === "admin";
}