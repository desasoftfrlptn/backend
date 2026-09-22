/**
 * 🔓 COMPLETÁS VOS — la autorización en la INTERFAZ.
 *
 * El módulo te enseñó que la SEGURIDAD vive en el SERVER (dependencies.py
 * y los controllers): si el server está roto, ocultar botones no protege
 * nada. PERO una UI profesional también respeta la matriz — no es
 * seguridad, es UX honesta: no mostrás una acción que el server va a
 * rechazar con 403.
 *
 * ESTADO ACTUAL (como el backend): TODO devuelve `true` a propósito.
 * La UI "dice que sí" siempre: te muestra el botón BORRAR aunque seas
 * viewer, el panel de USUARIOS a cualquiera, y acciones de escritura
 * aunque tu token sea "read" solamente.
 *
 * 🔴 Probalo ANTES de completar: logueate como viewer, mirá cómo la UI
 * te ofrece BORRAR y ADMINISTRAR USUARIOS. Clickleá: el server (recién
 * cuando completes el backend) responde 403. La UI y el server deben
 * quedar ALINEADOS.
 *
 * ✅ TU TRABAJO: que cada helper devuelva lo que la MATRIZ (SPEC.md,
 * sección 3) espera. Son 6 funciones; el resto de la UI ya las usa.
 * Compará SIEMPRE con lo que responde el server en vivo.
 *
 * La matriz en una línea:
 *
 *   | helper              | admin | editor | viewer |
 *   |---------------------|:-----:|:------:|:------:|
 *   | scopeAllowsWrite    |  ✅   |   ✅   |   ❌   |  (depende del TOKEN, no del rol)
 *   | canManageUsers      |  ✅   |   ❌   |   ❌   |
 *   | canChangeRole       |  ✅   |   ❌   |   ❌   |
 *   | canDelete           |  ✅   |   ❌   |   ❌   |
 *   | canEdit (doc ajeno) |  ✅   |   ❌   |   ❌   |
 *   | canEdit (doc propio)|  ✅   |   ✅   |   ✅   |
 *   | canPublish          |  ✅   |  ✅ (lo suyo) | ❌ |
 */

import type { DocumentRead, Role } from "./types";

/**
 * ¿Este TOKEN puede escribir? El scope viaja en el JWT
 * ("read" | "read write") y lo limita el LOGIN, no el rol:
 * un admin puede loguearse con scope "read" y quedar SOLO LECTURA.
 */
export const scopeAllowsWrite = (scope: string | undefined): boolean => {
  // Verificamos si el scope existe y contiene "write"
  if (!scope) return false;
  return scope.split(" ").includes("write");
};

export const canManageUsers = (role: Role | undefined): boolean => {
  // Solo los administradores gestionan la lista de usuarios
  return role === "admin";
};

export const canChangeRole = (role: Role | undefined): boolean => {
  // La operación más sensible está restringida estrictamente a administradores
  return role === "admin";
};

export const canDelete = (role: Role | undefined): boolean => {
  // Según la matriz, ni el dueño ni el editor pueden borrar, solo admin
  return role === "admin";
};

export const canEdit = (userId: number, doc: any, role: Role | undefined): boolean => {
  // Object-level: podés editar si sos el dueño exacto del documento, o si sos admin
  return doc.owner_id === userId || role === "admin";
};

export const canPublish = (userId: number, doc: any, role: Role | undefined): boolean => {
  // Object-level: idéntica lógica que la edición
  return doc.owner_id === userId || role === "admin";
};