"""US-04 · Descarga de documentos oficiales."""
from flask import Blueprint, Response, abort, g, render_template

from .. import registry
from ..auth import role_required
from ..db import get_db

bp = Blueprint("documentos", __name__, url_prefix="/documentos")

TIPOS = {
    "matricula": "Resguardo de matrícula",
    "expediente": "Expediente académico",
}


def generar_documento(db, user, tipo):
    """Genera el texto del documento SOLO con datos del usuario indicado."""
    filas = db.execute(
        "SELECT a.codigo, a.nombre, a.creditos FROM matriculas m JOIN asignaturas a ON a.id = m.asignatura_id "
        "WHERE m.user_id = ? AND m.estado = 'activa' ORDER BY a.codigo", (user["id"],)).fetchall()
    lineas = [TIPOS[tipo].upper(), f"Alumno: {user['name']}", "-" * 40]
    lineas += [f"{f['codigo']}  {f['nombre']}  ({f['creditos']} ECTS)" for f in filas] or ["Sin asignaturas matriculadas."]
    lineas.append(f"Total créditos: {sum(f['creditos'] for f in filas)}")
    if tipo == "expediente":
        lineas.append("Calificaciones: no disponibles en la demostración.")
    return "\n".join(lineas) + "\n"


@bp.get("/<tipo>/descargar")
@role_required("alumno")
def descargar(tipo):
    if tipo not in TIPOS:
        abort(404)
    texto = generar_documento(get_db(), g.user, tipo)
    return Response(texto, mimetype="text/plain; charset=utf-8",
                    headers={"Content-Disposition": f'attachment; filename="{tipo}.txt"'})
@bp.get("/")
@role_required("alumno")
def lista():
    return render_template("documentos/lista.html", tipos=TIPOS)


registry.register_nav("Documentos oficiales", "documentos.lista", "Trámites", 20)
