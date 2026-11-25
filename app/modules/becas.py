"""US-03 · Solicitud de becas y seguimiento de su estado."""
from flask import Blueprint

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
