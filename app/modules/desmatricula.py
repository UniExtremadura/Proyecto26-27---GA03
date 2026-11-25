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
def _contexto(matricula_id):
    m = obtener_matricula_propia(get_db(), matricula_id, g.user["id"])
    if m is None:
        abort(404)
    plazo = current_app.config.get("DESMATRICULA_HASTA", PLAZO_POR_DEFECTO)
    permitido, motivo = puede_desmatricular(m, date.today().isoformat(), plazo)
    return m, permitido, motivo


@bp.get("/")
@role_required("alumno")
def lista():
    return render_template("desmatricula/lista.html", matriculas=matriculas_del_alumno(get_db(), g.user["id"]))


@bp.get("/<int:matricula_id>/confirmar")
@role_required("alumno")
def confirmacion(matricula_id):
    m, permitido, motivo = _contexto(matricula_id)
    return render_template("desmatricula/confirmar.html", m=m, permitido=permitido, motivo=motivo)


@bp.post("/<int:matricula_id>")
@role_required("alumno")
def baja(matricula_id):
    m, permitido, motivo = _contexto(matricula_id)
    if not permitido:
        return render_template("desmatricula/confirmar.html", m=m, permitido=False, motivo=motivo), 409
    cancelar(get_db(), m["id"])
    flash(f"Te has dado de baja de {m['codigo']}.", "info")
    return redirect(url_for("desmatricula.lista"))


registry.register_nav("Desmatriculación", "desmatricula.lista", "Trámites", 11)
