"""US-01 · Matrícula online guiada."""
from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from .. import registry
from ..auth import role_required
from ..db import get_db

bp = Blueprint("matricula", __name__, url_prefix="/matricula")
MAX_CREDITOS = 60


def matriculas_activas(db, user_id):
    return db.execute(
        "SELECT a.codigo, a.nombre, a.creditos FROM matriculas m JOIN asignaturas a ON a.id = m.asignatura_id "
        "WHERE m.user_id = ? AND m.estado = 'activa' ORDER BY a.codigo", (user_id,)).fetchall()


def plazas_libres(db, asignatura):
    ocupadas = db.execute("SELECT COUNT(*) FROM matriculas WHERE asignatura_id = ? AND estado = 'activa'",
                          (asignatura["id"],)).fetchone()[0]
    return asignatura["plazas"] - ocupadas


def validar_matricula(db, user_id, codigos):
    """Valida la selección. Devuelve (errores, asignaturas_nuevas)."""
    codigos = list(dict.fromkeys(c for c in codigos if c))        # sin vacíos ni duplicados
    if not codigos:
        return ["Selecciona al menos una asignatura."], []
    marcadores = ",".join("?" * len(codigos))
    encontradas = db.execute(f"SELECT * FROM asignaturas WHERE codigo IN ({marcadores}) ORDER BY codigo", codigos).fetchall()
    errores = [f"La asignatura {c} no existe." for c in codigos if c not in {a["codigo"] for a in encontradas}]
    actuales = matriculas_activas(db, user_id)
    ya = {m["codigo"] for m in actuales}
    nuevas = []
    for a in encontradas:
        if a["codigo"] in ya:
            errores.append(f"Ya estás matriculado en {a['codigo']}.")
        elif plazas_libres(db, a) <= 0:
            errores.append(f"La asignatura {a['codigo']} no tiene plazas libres.")
        else:
            nuevas.append(a)
    total = sum(m["creditos"] for m in actuales) + sum(a["creditos"] for a in nuevas)
    if total > MAX_CREDITOS:
        errores.append(f"Superas el máximo de {MAX_CREDITOS} ECTS ({total} ECTS).")
    return errores, nuevas
def _asignaturas_con_plazas(db):
    filas = db.execute("SELECT * FROM asignaturas ORDER BY curso, codigo").fetchall()
    return [{**dict(a), "libres": plazas_libres(db, a)} for a in filas]


def _render_formulario(db, errores=(), seleccion=(), estado=200):
    actuales = matriculas_activas(db, g.user["id"])
    return render_template("matricula/formulario.html", asignaturas=_asignaturas_con_plazas(db), errores=errores,
                           seleccion=set(seleccion), creditos=sum(m["creditos"] for m in actuales),
                           maximo=MAX_CREDITOS), estado


@bp.get("/")
@role_required("alumno")
def formulario():
    return _render_formulario(get_db())


@bp.post("/revisar")
@role_required("alumno")
def revisar():
    db = get_db()
    codigos = request.form.getlist("codigos")
    errores, nuevas = validar_matricula(db, g.user["id"], codigos)
    if errores:
        return _render_formulario(db, errores, codigos, 422)
    actuales = sum(m["creditos"] for m in matriculas_activas(db, g.user["id"]))
    nuevos = sum(a["creditos"] for a in nuevas)
    return render_template("matricula/confirmar.html", asignaturas=nuevas, nuevos=nuevos, total=actuales + nuevos)


registry.register_nav("Matrícula", "matricula.formulario", "Trámites", 10)
