"""US-09 · Solicitud ERASMUS accesible."""
from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from .. import registry
from ..auth import role_required
from ..db import get_db

bp = Blueprint("erasmus", __name__, url_prefix="/erasmus")

SCHEMA = """
CREATE TABLE IF NOT EXISTS solicitudes_erasmus (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users (id),
    destino TEXT NOT NULL,
    motivo TEXT NOT NULL,
    estado TEXT NOT NULL DEFAULT 'enviada',
    creada TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""
DESTINOS = ("Universidad de Lisboa (PT)", "Universidad de Bolonia (IT)",
            "Universidad de Gante (BE)", "Universidad de Cracovia (PL)")


def validar_solicitud(destino, motivo):
    errores = []
    if destino not in DESTINOS:
        errores.append("Elige un destino de la lista.")
    if not 20 <= len(motivo.strip()) <= 1000:
        errores.append("La motivación debe tener entre 20 y 1000 caracteres.")
    return errores


def crear_solicitud(db, user_id, destino, motivo):
    cursor = db.execute("INSERT INTO solicitudes_erasmus (user_id, destino, motivo) VALUES (?, ?, ?)",
                        (user_id, destino, motivo.strip()))
    db.commit()
    return cursor.lastrowid


@bp.get("/")
@role_required("alumno")
def formulario():
    return render_template("erasmus/formulario.html", destinos=DESTINOS)


@bp.post("/")
@role_required("alumno")
def enviar():
    destino, motivo = request.form.get("destino", ""), request.form.get("motivo", "")
    errores = validar_solicitud(destino, motivo)
    if errores:
        return render_template("erasmus/formulario.html", destinos=DESTINOS, errores=errores,
                               destino=destino, motivo=motivo), 422
    crear_solicitud(get_db(), g.user["id"], destino, motivo)
    flash("Solicitud ERASMUS enviada correctamente.", "info")
    return redirect(url_for("erasmus.formulario"))


registry.register_nav("ERASMUS", "erasmus.formulario", "Trámites", 40)
ESTADOS = {"enviada": "Enviada", "en_revision": "En revisión", "admitida": "Admitida", "rechazada": "Rechazada"}


@bp.get("/estado")
@role_required("alumno")
def estado():
    filas = get_db().execute("SELECT * FROM solicitudes_erasmus WHERE user_id = ? ORDER BY id DESC", (g.user["id"],)).fetchall()
    return render_template("erasmus/estado.html", solicitudes=filas, estados=ESTADOS)
DOCUMENTACION = [
    {"documento": "Formulario de solicitud firmado", "donde": "Oficina de Relaciones Internacionales (Rectorado, planta 1)",
     "como": "En persona (lunes a viernes, 9:00–14:00) o por registro electrónico"},
    {"documento": "Certificado de idiomas", "donde": "Oficina de Relaciones Internacionales",
     "como": "Copia compulsada en papel o PDF por registro electrónico"},
    {"documento": "Expediente académico", "donde": "Se descarga desde el campus (Documentos oficiales)",
     "como": "Adjuntar el archivo descargado al registro electrónico"},
]


@bp.get("/documentacion")
@role_required("alumno")
def documentacion():
    return render_template("erasmus/documentacion.html", documentos=DOCUMENTACION)
