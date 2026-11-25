"""US-07 · Información de eventos académicos."""
import re

from flask import Blueprint, abort, jsonify, render_template, request

from .. import registry
from ..db import get_db

bp = Blueprint("eventos", __name__)

SCHEMA = """
CREATE TABLE IF NOT EXISTS eventos (
    id INTEGER PRIMARY KEY,
    titulo TEXT NOT NULL,
    descripcion TEXT NOT NULL DEFAULT '',
    fecha TEXT NOT NULL,
    hora TEXT NOT NULL DEFAULT '10:00',
    ubicacion TEXT NOT NULL DEFAULT '',
    organizador TEXT NOT NULL DEFAULT '',
    aforo INTEGER NOT NULL DEFAULT 0 CHECK (aforo >= 0),
    enlace_inscripcion TEXT NOT NULL DEFAULT '',
    tipo TEXT NOT NULL DEFAULT 'general',
    estado TEXT NOT NULL DEFAULT 'abierto'
);
INSERT OR IGNORE INTO eventos (id, titulo, descripcion, fecha, hora, ubicacion, organizador, aforo, enlace_inscripcion, tipo) VALUES
 (1, 'Jornada de bienvenida', 'Presentación del curso y servicios.', '2026-11-20', '10:00', 'Aula Magna', 'Vicerrectorado', 200, 'https://example.org/bienvenida', 'general'),
 (2, 'Taller de accesibilidad web', 'Buenas prácticas de diseño accesible.', '2026-11-25', '12:00', 'Laboratorio 3', 'Escuela Politécnica', 30, 'https://example.org/taller-accesibilidad', 'taller'),
 (3, 'Charla sobre becas Erasmus', 'Cómo solicitar una beca de movilidad.', '2026-12-02', '17:00', 'Sala de Grados', 'Oficina de Relaciones Internacionales', 80, 'https://example.org/charla-erasmus', 'charla'),
 (4, 'Feria de empleo', 'Empresas del sector tecnológico.', '2026-12-10', '09:30', 'Pabellón Deportivo', 'Servicio de Orientación', 500, 'https://example.org/feria', 'feria');
"""
TIPOS = ("general", "taller", "charla", "feria")
FECHA_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validar_evento(datos):
    """Devuelve la lista de errores de un evento (vacía si es válido)."""
    errores = []
    if not str(datos.get("titulo", "")).strip():
        errores.append("El título es obligatorio.")
    if not FECHA_RE.match(str(datos.get("fecha", ""))):
        errores.append("La fecha debe tener el formato AAAA-MM-DD.")
    if datos.get("tipo", "general") not in TIPOS:
        errores.append("El tipo de evento no es válido.")
    try:
        if int(datos.get("aforo", 0)) < 0:
            errores.append("El aforo no puede ser negativo.")
    except (TypeError, ValueError):
        errores.append("El aforo debe ser un número.")
    enlace = str(datos.get("enlace_inscripcion", ""))
    if enlace and not enlace.startswith("https://"):
        errores.append("El enlace de inscripción debe empezar por https://")
    return errores
