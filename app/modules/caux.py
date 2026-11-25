"""US-08 · Resolución de dudas con CAUX desde el campus."""
from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from .. import registry
from ..auth import login_required
from ..db import get_db

bp = Blueprint("caux", __name__, url_prefix="/caux")

FAQ = [
    {"claves": ("matricula", "matricularme", "matrícula"), "pregunta": "¿Cómo me matriculo?",
     "respuesta": "Entra en Trámites > Matrícula, elige tus asignaturas y confirma. Recibirás validación instantánea."},
    {"claves": ("beca", "becas"), "pregunta": "¿Cómo solicito una beca?",
     "respuesta": "En Trámites > Becas puedes crear la solicitud y consultar su estado en cualquier momento."},
    {"claves": ("documento", "certificado", "expediente"), "pregunta": "¿Dónde descargo mis documentos?",
     "respuesta": "En Trámites > Documentos oficiales puedes descargar tu resguardo de matrícula y tu expediente."},
]


@bp.get("/")
def pagina():
    return render_template("caux/pagina.html", faq=FAQ)


registry.register_nav("CAUX", "caux.pagina", "Servicios", 10)
SCHEMA = """
CREATE TABLE IF NOT EXISTS dudas_caux (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users (id),
    asunto TEXT NOT NULL,
    mensaje TEXT NOT NULL,
    estado TEXT NOT NULL DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'resuelta')),
    respuesta TEXT NOT NULL DEFAULT '',
    creada TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def buscar_faq(texto):
    """Devuelve la pregunta frecuente que mejor encaja con el texto, o None."""
    texto = texto.lower()
    for f in FAQ:
        if any(clave in texto for clave in f["claves"]):
            return f
    return None


def validar_duda(asunto, mensaje):
    errores = []
    if not 3 <= len(asunto.strip()) <= 120:
        errores.append("El asunto debe tener entre 3 y 120 caracteres.")
    if not 10 <= len(mensaje.strip()) <= 2000:
        errores.append("El mensaje debe tener entre 10 y 2000 caracteres.")
    return errores


def crear_duda(db, user_id, asunto, mensaje):
    """Crea la duda; si coincide con una FAQ queda resuelta al instante."""
    faq = buscar_faq(f"{asunto} {mensaje}")
    estado, respuesta = ("resuelta", faq["respuesta"]) if faq else ("pendiente", "")
    cursor = db.execute("INSERT INTO dudas_caux (user_id, asunto, mensaje, estado, respuesta) VALUES (?, ?, ?, ?, ?)",
                        (user_id, asunto.strip(), mensaje.strip(), estado, respuesta))
    db.commit()
    return cursor.lastrowid, estado


@bp.post("/")
@login_required
def enviar():
    asunto, mensaje = request.form.get("asunto", ""), request.form.get("mensaje", "")
    errores = validar_duda(asunto, mensaje)
    if errores:
        return render_template("caux/pagina.html", faq=FAQ, errores=errores, asunto=asunto, mensaje=mensaje), 422
    _, estado = crear_duda(get_db(), g.user["id"], asunto, mensaje)
    flash("Hemos respondido tu duda al instante." if estado == "resuelta"
          else "Tu duda ha sido enviada. Te responderemos lo antes posible.", "info")
    return redirect(url_for("caux.mis_consultas"))


@bp.get("/mis-consultas")
@login_required
def mis_consultas():
    filas = get_db().execute("SELECT * FROM dudas_caux WHERE user_id = ? ORDER BY id DESC", (g.user["id"],)).fetchall()
    return render_template("caux/mis_consultas.html", consultas=filas)


def buscar_en_faq(q):
    q = q.lower()
    return [{"title": f["pregunta"], "url": "/caux/", "section": "CAUX"}
            for f in FAQ if q in f["pregunta"].lower() or q in f["respuesta"].lower()]


registry.register_search(buscar_en_faq)
