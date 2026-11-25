"""US-11 · Directorio de perfiles de alumnos y profesores."""
from flask import Blueprint, render_template

from .. import registry
from ..auth import login_required
from ..db import get_db

bp = Blueprint("directorio", __name__, url_prefix="/directorio")
ROLES_VISIBLES = ("alumno", "profesor")


def listar_perfiles(db):
    return db.execute("SELECT id, name, role FROM users WHERE role IN ('alumno', 'profesor') ORDER BY name").fetchall()


@bp.get("/")
@login_required
def lista():
    return render_template("directorio/lista.html", perfiles=listar_perfiles(get_db()))


registry.register_nav("Directorio", "directorio.lista", "Servicios", 20)
