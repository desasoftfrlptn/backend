/**
 * Autorización en la interfaz.
 *
 * La seguridad real vive en el server; acá solo evitamos mostrar acciones que
 * el server va a rechazar con 403, siguiendo la matriz de la SPEC (sección 3).
 *
 *   | helper              | admin | editor | viewer |
 *   |---------------------|:-----:|:------:|:------:|
 *   | scopeAllowsWrite    |  ✅   |   ✅   |   ❌   |  (depende del token, no del rol)
 *   | canManageUsers      |  ✅   |   ❌   |   ❌   |
 *   | canChangeRole       |  ✅   |   ❌   |   ❌   |
 *   | canDelete           |  ✅   |   ❌   |   ❌   |
 *   | canEdit (doc ajeno) |  ✅   |   ❌   |   ❌   |
 *   | canEdit (doc propio)|  ✅   |   ✅   |   ✅   |
 *   | canPublish          |  ✅   | ✅ (lo suyo) | ❌ |
 */

import type { DocumentRead, Role } from "./types";

/** ¿El token puede escribir? El scope lo fija el login ("read" | "read write"). */
export function scopeAllowsWrite(scope: string | undefined): boolean {
  return scope?.split(" ").includes("write") ?? false;
}

/** ¿Puede ver el panel de usuarios? Solo admin. */
export function canManageUsers(role: Role | undefined): boolean {
  return role === "admin";
}

/** ¿Puede cambiar el rol de otro usuario? Solo admin. */
export function canChangeRole(role: Role | undefined): boolean {
  return role === "admin";
}

/** ¿Puede borrar documentos? Solo admin. */
export function canDelete(role: Role | undefined): boolean {
  return role === "admin";
}

/** ¿Puede editar el documento? El dueño o un admin. */
export function canEdit(userId: number, doc: DocumentRead, role: Role | undefined): boolean {
  return doc.owner_id === userId || role === "admin";
}

/** ¿Puede publicar el documento? Misma regla que editar (el viewer queda afuera por su scope). */
export function canPublish(userId: number, doc: DocumentRead, role: Role | undefined): boolean {
  return doc.owner_id === userId || role === "admin";
}