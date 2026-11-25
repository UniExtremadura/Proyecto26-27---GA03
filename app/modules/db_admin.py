"""US-15 · Gestión y optimización de la base de datos."""
from flask import Blueprint

from ..db import get_db  # noqa: F401  (se usa en las rutas del panel)

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
