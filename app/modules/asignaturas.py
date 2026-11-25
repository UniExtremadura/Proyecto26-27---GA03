"""US-06 · Ficha de asignatura con sus docentes."""
from flask import Blueprint, abort, render_template

from .. import registry
from ..db import get_db

bp = Blueprint("asignaturas", __name__, url_prefix="/asignaturas")

SCHEMA = """
CREATE TABLE IF NOT EXISTS docentes (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS asignatura_docente (
    asignatura_id INTEGER NOT NULL REFERENCES asignaturas (id),
    docente_id INTEGER NOT NULL REFERENCES docentes (id),
    parte TEXT NOT NULL,
    PRIMARY KEY (asignatura_id, docente_id)
);
INSERT OR IGNORE INTO docentes (id, nombre) VALUES
    (1, 'Dra. Elena Docente Demo'), (2, 'Dr. Mario Docente Demo'), (3, 'Dra. Rosa Docente Demo');
INSERT OR IGNORE INTO asignatura_docente (asignatura_id, docente_id, parte)
    SELECT id, 1, 'Teoría' FROM asignaturas WHERE codigo IN ('ASG101', 'ASG102', 'ASG103', 'ASG104');
INSERT OR IGNORE INTO asignatura_docente (asignatura_id, docente_id, parte)
    SELECT id, 2, 'Prácticas de laboratorio' FROM asignaturas WHERE codigo IN ('ASG101', 'ASG104');
INSERT OR IGNORE INTO asignatura_docente (asignatura_id, docente_id, parte)
    SELECT id, 3, 'Seminarios' FROM asignaturas WHERE codigo = 'ASG103';
"""
def obtener_detalle(db, codigo):
    """Devuelve la asignatura con sus docentes y partes, o None si no existe."""
    asig = db.execute("SELECT * FROM asignaturas WHERE codigo = ?", (codigo,)).fetchone()
    if asig is None:
        return None
    docentes = db.execute(
        "SELECT d.nombre, ad.parte FROM asignatura_docente ad JOIN docentes d ON d.id = ad.docente_id "
        "WHERE ad.asignatura_id = ? ORDER BY d.nombre", (asig["id"],)).fetchall()
    return {**dict(asig), "docentes": [dict(d) for d in docentes]}


def listar_asignaturas(db):
    return db.execute("SELECT codigo, nombre, creditos, curso FROM asignaturas ORDER BY curso, codigo").fetchall()
