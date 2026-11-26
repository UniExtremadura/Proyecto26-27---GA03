"""US-15 · Gestión y optimización de la base de datos."""
from flask import Blueprint, current_app, jsonify, render_template

from ..auth import role_required
from ..db import get_db

bp = Blueprint("db_admin", __name__, url_prefix="/admin/db")

# Índices para las consultas más frecuentes (idempotente).
SCHEMA = """
CREATE INDEX IF NOT EXISTS idx_users_role ON users (role);
CREATE INDEX IF NOT EXISTS idx_matriculas_user ON matriculas (user_id, estado);
CREATE INDEX IF NOT EXISTS idx_matriculas_asignatura ON matriculas (asignatura_id);
"""


def estadisticas_tablas(db):
    """Devuelve filas e índices de cada tabla de la base de datos."""
    tablas = [f["name"] for f in db.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
    resultado = []
    for nombre in tablas:
        filas = db.execute(f'SELECT COUNT(*) FROM "{nombre}"').fetchone()[0]
        indices = [i["name"] for i in db.execute(f'PRAGMA index_list("{nombre}")')]
        resultado.append({"tabla": nombre, "filas": filas, "indices": indices})
    return resultado
def integridad(db):
    return db.execute("PRAGMA integrity_check").fetchone()[0]


def alertas(db, umbral_filas=50000):
    """Alertas de monitorización: integridad, claves foráneas y tablas grandes sin índice."""
    resultado = []
    if integridad(db) != "ok":
        resultado.append({"tipo": "integridad", "mensaje": "La comprobación de integridad ha fallado."})
    if db.execute("PRAGMA foreign_keys").fetchone()[0] != 1:
        resultado.append({"tipo": "claves_foraneas", "mensaje": "Las claves foráneas están desactivadas."})
    for t in estadisticas_tablas(db):
        # Los índices automáticos de la clave primaria no cuentan como optimización.
        propios = [i for i in t["indices"] if not i.startswith("sqlite_autoindex")]
        if t["filas"] > umbral_filas and not propios:
            resultado.append({"tipo": "tabla_grande_sin_indice",
                              "mensaje": f"La tabla {t['tabla']} tiene {t['filas']} filas y ningún índice."})
    return resultado


@bp.get("/")
@role_required("pas")
def panel():
    db = get_db()
    return render_template("db_admin/panel.html", tablas=estadisticas_tablas(db),
                           alertas=alertas(db, current_app.config.get("DB_ALERTA_FILAS", 50000)))


@bp.get("/estado.json")
@role_required("pas")
def estado():
    db = get_db()
    return jsonify(integridad=integridad(db), tablas=estadisticas_tablas(db),
                   alertas=alertas(db, current_app.config.get("DB_ALERTA_FILAS", 50000)))
