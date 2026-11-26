"""US-13 · Acceso móvil al campus (PWA mobile-first)."""
from flask import Blueprint, g, jsonify, render_template

from ..auth import token_required
from ..db import get_db

bp = Blueprint("movil", __name__)


@bp.get("/m/")
def inicio():
    return render_template("movil/inicio.html")
@bp.get("/api/m/resumen")
@token_required
def resumen():
    filas = get_db().execute(
        "SELECT a.creditos FROM matriculas m JOIN asignaturas a ON a.id = m.asignatura_id "
        "WHERE m.user_id = ? AND m.estado = 'activa'", (g.user["id"],)).fetchall()
    return jsonify(usuario=g.user["name"], rol=g.user["role"],
                   matriculas_activas=len(filas), creditos=sum(f["creditos"] for f in filas))
@bp.get("/m/login")
def login():
    return render_template("movil/login.html")
