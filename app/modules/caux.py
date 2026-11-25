"""US-08 · Resolución de dudas con CAUX desde el campus."""
from flask import Blueprint, render_template

from .. import registry

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
