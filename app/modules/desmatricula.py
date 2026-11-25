"""US-02 · Desmatriculación online."""
from datetime import date

from flask import Blueprint, abort, current_app, flash, g, redirect, render_template, url_for

from .. import registry
from ..auth import role_required
from ..db import get_db

bp = Blueprint("desmatricula", __name__, url_prefix="/desmatricula")
PLAZO_POR_DEFECTO = "2099-12-31"


def puede_desmatricular(matricula, hoy, plazo):
    """Devuelve (permitido, motivo). Las fechas son cadenas ISO (AAAA-MM-DD)."""
    if matricula["estado"] != "activa":
        return False, "Esta matrícula ya está cancelada."
    if hoy > plazo:
        return False, f"El plazo de desmatriculación terminó el {plazo}."
    return True, ""


def matriculas_del_alumno(db, user_id):
    return db.execute(
        "SELECT m.id, m.estado, a.codigo, a.nombre, a.creditos FROM matriculas m "
        "JOIN asignaturas a ON a.id = m.asignatura_id WHERE m.user_id = ? AND m.estado = 'activa' ORDER BY a.codigo",
        (user_id,)).fetchall()


def obtener_matricula_propia(db, matricula_id, user_id):
    return db.execute(
        "SELECT m.id, m.estado, a.codigo, a.nombre, a.creditos FROM matriculas m "
        "JOIN asignaturas a ON a.id = m.asignatura_id WHERE m.id = ? AND m.user_id = ?",
        (matricula_id, user_id)).fetchone()


def cancelar(db, matricula_id):
    db.execute("UPDATE matriculas SET estado = 'cancelada', cancelada = CURRENT_TIMESTAMP WHERE id = ?", (matricula_id,))
    db.commit()
