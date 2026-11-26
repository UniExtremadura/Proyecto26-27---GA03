"""US-11 · Directorio de perfiles de alumnos y profesores."""
from flask import Blueprint, abort, render_template, request

from .. import registry
from ..auth import login_required
from ..db import get_db

bp = Blueprint("directorio", __name__, url_prefix="/directorio")
ROLES_VISIBLES = ("alumno", "profesor")


def listar_perfiles(db, q="", rol=""):
    """Filtra por nombre (contiene) y por rol; consulta parametrizada."""
    sql, params = "SELECT id, name, role FROM users WHERE role IN ('alumno', 'profesor')", []
    if q:
        sql += " AND name LIKE ?"
        params.append(f"%{q}%")
    if rol in ROLES_VISIBLES:
        sql += " AND role = ?"
        params.append(rol)
    return db.execute(sql + " ORDER BY name", params).fetchall()


@bp.get("/")
@login_required
def lista():
    q, rol = request.args.get("q", "").strip(), request.args.get("rol", "")
    return render_template("directorio/lista.html", perfiles=listar_perfiles(get_db(), q, rol), q=q, rol=rol)


registry.register_nav("Directorio", "directorio.lista", "Servicios", 20)
@bp.get("/<int:user_id>")
@login_required
def perfil(user_id):
    fila = get_db().execute("SELECT id, name, role, email FROM users WHERE id = ? AND role IN ('alumno', 'profesor')",
                            (user_id,)).fetchone()
    if fila is None:
        abort(404)
    return render_template("directorio/perfil.html", p=fila)
