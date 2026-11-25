"""US-03 · Solicitud de becas y seguimiento de su estado."""
from flask import Blueprint, abort, flash, g, jsonify, redirect, render_template, request, url_for

from .. import registry
from ..auth import role_required
from ..db import get_db

bp = Blueprint("becas", __name__, url_prefix="/becas")

SCHEMA = """
CREATE TABLE IF NOT EXISTS solicitudes_beca (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users (id),
    tipo TEXT NOT NULL,
    observaciones TEXT NOT NULL DEFAULT '',
    estado TEXT NOT NULL DEFAULT 'pendiente',
    creada TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizada TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS beca_pendientes (
    id INTEGER PRIMARY KEY,
    solicitud_id INTEGER NOT NULL REFERENCES solicitudes_beca (id),
    descripcion TEXT NOT NULL,
    resuelto INTEGER NOT NULL DEFAULT 0
);
"""

TIPOS = ("General", "Movilidad", "Colaboración")
ESTADOS = {
    "pendiente": "Pendiente de revisión",
    "en_revision": "En revisión",
    "falta_documentacion": "Falta documentación",
    "resuelta": "Resuelta: concedida",
    "denegada": "Denegada",
}
TRANSICIONES = {
    "pendiente": {"en_revision"},
    "en_revision": {"falta_documentacion", "resuelta", "denegada"},
    "falta_documentacion": {"en_revision"},
    "resuelta": set(),
    "denegada": set(),
}


def crear_solicitud(db, user_id, tipo, observaciones=""):
    if tipo not in TIPOS:
        raise ValueError("Tipo de beca no válido.")
    cursor = db.execute("INSERT INTO solicitudes_beca (user_id, tipo, observaciones) VALUES (?, ?, ?)",
                        (user_id, tipo, observaciones.strip()[:1000]))
    db.commit()
    return cursor.lastrowid


def cambiar_estado(db, solicitud_id, nuevo):
    actual = db.execute("SELECT estado FROM solicitudes_beca WHERE id = ?", (solicitud_id,)).fetchone()
    if actual is None:
        raise LookupError("La solicitud no existe.")
    if nuevo not in ESTADOS or nuevo not in TRANSICIONES[actual["estado"]]:
        raise ValueError(f"No se puede pasar de «{actual['estado']}» a «{nuevo}».")
    db.execute("UPDATE solicitudes_beca SET estado = ?, actualizada = CURRENT_TIMESTAMP WHERE id = ?", (nuevo, solicitud_id))
    db.commit()
def obtener_solicitud(db, solicitud_id):
    return db.execute("SELECT * FROM solicitudes_beca WHERE id = ?", (solicitud_id,)).fetchone()


def _solicitud_visible_o_404(solicitud_id):
    """Un alumno solo ve las suyas; el PAS ve todas. Si no es visible se responde 404."""
    s = obtener_solicitud(get_db(), solicitud_id)
    if s is None or (g.user["role"] != "pas" and s["user_id"] != g.user["id"]):
        abort(404)
    return s


@bp.get("/")
@role_required("alumno")
def lista():
    filas = get_db().execute("SELECT * FROM solicitudes_beca WHERE user_id = ? ORDER BY id DESC", (g.user["id"],)).fetchall()
    return render_template("becas/lista.html", solicitudes=filas, estados=ESTADOS)


@bp.route("/nueva", methods=["GET", "POST"])
@role_required("alumno")
def nueva():
    if request.method == "POST":
        try:
            sid = crear_solicitud(get_db(), g.user["id"], request.form.get("tipo", ""), request.form.get("observaciones", ""))
        except ValueError as error:
            return render_template("becas/nueva.html", tipos=TIPOS, error=str(error)), 422
        flash("Solicitud enviada. Podrás seguir su estado desde esta página.", "info")
        return redirect(url_for("becas.detalle", solicitud_id=sid))
    return render_template("becas/nueva.html", tipos=TIPOS)


@bp.get("/<int:solicitud_id>")
@role_required("alumno", "pas")
def detalle(solicitud_id):
    db = get_db()
    s = _solicitud_visible_o_404(solicitud_id)
    return render_template("becas/detalle.html", s=s, estados=ESTADOS, pendientes=pendientes_de(db, solicitud_id))


registry.register_nav("Becas", "becas.lista", "Trámites", 30)
def pendientes_de(db, solicitud_id):
    return db.execute("SELECT * FROM beca_pendientes WHERE solicitud_id = ? ORDER BY id", (solicitud_id,)).fetchall()


def anadir_pendiente(db, solicitud_id, descripcion):
    descripcion = descripcion.strip()
    if not descripcion:
        raise ValueError("Indica qué documentación falta.")
    db.execute("INSERT INTO beca_pendientes (solicitud_id, descripcion) VALUES (?, ?)", (solicitud_id, descripcion[:300]))
    db.commit()


@bp.post("/<int:solicitud_id>/pendientes")
@role_required("pas")
def registrar_pendiente(solicitud_id):
    _solicitud_visible_o_404(solicitud_id)
    try:
        anadir_pendiente(get_db(), solicitud_id, request.form.get("descripcion", ""))
    except ValueError as error:
        flash(str(error), "error")
    return redirect(url_for("becas.detalle", solicitud_id=solicitud_id))
