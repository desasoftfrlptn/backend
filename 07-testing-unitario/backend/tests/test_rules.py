"""Tests de autorización — EJERCICIO.

Los dos primeros son la REFERENCIA (ya completos, pasan). Los cuatro de abajo
tienen `assert False, "TODO..."` y FALLAN a propósito: son tu trabajo en la
Fase 1 de la guía.

Reglas:
  - Un test = un comportamiento. No pruebes todo junto.
  - Pensá el caso de borde (¿rol vacío? ¿scope vacío?).
  - Corré `uv run pytest` después de cada uno hasta verlo verde.
"""

from app.rules import (
    can_change_role,
    can_delete,
    can_edit,
    can_manage_users,
    scope_allows_write,
)


# ── Referencia (no tocar) ──────────────────────────────────────────────────

def test_scope_allows_write_con_write():
    # Arrange
    scope = "read write"
    # Act
    resultado = scope_allows_write(scope)
    # Assert
    assert resultado is True


def test_scope_allows_write_solo_read():
    assert scope_allows_write("read") is False


# ── Fase 1 · Completá los TODO ─────────────────────────────────────────────

def test_can_manage_users_solo_admin():
   assert can_manage_users("admin") is True
   assert can_manage_users("viewer") is False
   def can_manage_users(role):
    return role == "admin"
   

def test_can_delete_solo_admin():
    assert can_delete("admin") is True
    assert can_delete("editor") is False
def can_delete(role):
    return role == "admin"


def test_can_edit_dueño_puede():
    assert can_edit(owner_id=1, user_id=1) is True

def can_edit(owner_id, user_id):
    return owner_id == user_id

def test_can_edit_editor_no_puede_sobre_ajeno():
    # TODO: un editor NO puede editar el documento de otro (owner_id != user_id)
    assert False, "TODO: completá este test"
