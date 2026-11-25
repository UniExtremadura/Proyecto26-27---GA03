"""US-14 · Guardado automático de borradores de trámites."""
import json
import re
from datetime import datetime, timedelta, timezone

from flask import Blueprint, g, jsonify, request

from ..auth import login_required, role_required
from ..db import get_db

bp = Blueprint("borradores", __name__, url_prefix="/api/borradores")

SCHEMA = """
CREATE TABLE IF NOT EXISTS borradores (
    user_id INTEGER NOT NULL REFERENCES users (id),
    tramite TEXT NOT NULL,
    datos TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    actualizado TEXT NOT NULL,
    caduca TEXT NOT NULL,
    PRIMARY KEY (user_id, tramite)
);
"""
TRAMITE_RE = re.compile(r"^[a-z0-9_-]{1,40}$")
MAX_BYTES = 64 * 1024
TTL_DIAS = 7


def _iso(momento):
    return momento.astimezone(timezone.utc).isoformat(timespec="seconds")


def _ahora():
    return datetime.now(timezone.utc)


def guardar_borrador(db, user_id, tramite, datos, ahora=None):
    ahora = ahora or _ahora()
    texto = json.dumps(datos, ensure_ascii=False, sort_keys=True)
    actual = db.execute("SELECT version FROM borradores WHERE user_id = ? AND tramite = ?",
                        (user_id, tramite)).fetchone()
    version = (actual["version"] + 1) if actual else 1
    db.execute(
        "INSERT INTO borradores (user_id, tramite, datos, version, actualizado, caduca) VALUES (?, ?, ?, ?, ?, ?) "
        "ON CONFLICT (user_id, tramite) DO UPDATE SET datos = excluded.datos, version = excluded.version, "
        "actualizado = excluded.actualizado, caduca = excluded.caduca",
        (user_id, tramite, texto, version, _iso(ahora), _iso(ahora + timedelta(days=TTL_DIAS))))
    db.commit()
    return version


def obtener_borrador(db, user_id, tramite, ahora=None):
    fila = db.execute("SELECT datos, version, actualizado, caduca FROM borradores WHERE user_id = ? AND tramite = ?",
                      (user_id, tramite)).fetchone()
    if fila is None:
        return None
    return {"datos": json.loads(fila["datos"]), "version": fila["version"], "actualizado": fila["actualizado"]}


def _tramite_valido(tramite):
    return bool(TRAMITE_RE.match(tramite))


@bp.get("/<tramite>")
@login_required
def recuperar(tramite):
    if not _tramite_valido(tramite):
        return jsonify(error="Trámite no válido"), 400
    borrador = obtener_borrador(get_db(), g.user["id"], tramite)
    if borrador is None:
        return jsonify(error="No hay borrador"), 404
    return jsonify(borrador)


@bp.put("/<tramite>")
@login_required
def guardar(tramite):
    if not _tramite_valido(tramite):
        return jsonify(error="Trámite no válido"), 400
    if request.content_length and request.content_length > MAX_BYTES:
        return jsonify(error="El borrador es demasiado grande"), 413
    cuerpo = request.get_json(silent=True)
    if not isinstance(cuerpo, dict) or not isinstance(cuerpo.get("datos"), dict):
        return jsonify(error="Se esperaba un objeto «datos»"), 400
    db = get_db()
    return jsonify(version=guardar_borrador(db, g.user["id"], tramite, cuerpo["datos"]))


@bp.delete("/<tramite>")
@login_required
def eliminar(tramite):
    db = get_db()
    db.execute("DELETE FROM borradores WHERE user_id = ? AND tramite = ?", (g.user["id"], tramite))
    db.commit()
    return "", 204
