/**
 * 🔓 COMPLETÁS VOS — la autorización en la INTERFAZ.
 */

import type { DocumentRead, Role } from "./types";

export function scopeAllowsWrite(scope: string | undefined): boolean {
  return scope?.split(" ").includes("write") ?? false;
}

export function canManageUsers(role: Role | undefined): boolean {
  return role === "admin";
}

export function canChangeRole(role: Role | undefined): boolean {
  return role === "admin";
}

export function canDelete(role: Role | undefined): boolean {
  return role === "admin";
}

export function canEdit(
  userId: number,
  doc: DocumentRead,
  role: Role | undefined
): boolean {
  return doc.owner_id === userId || role === "admin";
}

export function canPublish(
  userId: number,
  doc: DocumentRead,
  role: Role | undefined
): boolean {
  return doc.owner_id === userId || role === "admin";
}