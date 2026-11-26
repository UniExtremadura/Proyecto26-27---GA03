"""US-16 · Estabilidad y salud del servicio."""
import logging
import threading
import time

from flask import Blueprint, current_app, g, jsonify, render_template, request

from ..db import get_db

bp = Blueprint("health", __name__)
log = logging.getLogger("campus.health")
ARRANQUE = time.time()


@bp.before_app_request
def configurar_acceso_bd():
    """Evita «database is locked»: la conexión espera hasta 5 s en lugar de fallar."""
    if request.endpoint == "static":
        return
    get_db().execute("PRAGMA busy_timeout = 5000")
_candado = threading.Lock()


def _metricas():
    return current_app.extensions.setdefault("metricas", {"peticiones": 0, "lentas": 0})


@bp.before_app_request
def iniciar_cronometro():
    g._inicio = time.perf_counter()


@bp.after_app_request
def medir_peticion(respuesta):
    inicio = g.pop("_inicio", None)
    if inicio is not None and request.endpoint != "static":
        ms = (time.perf_counter() - inicio) * 1000
        respuesta.headers["X-Response-Time-ms"] = f"{ms:.1f}"
        with _candado:
            m = _metricas()
            m["peticiones"] += 1
            if ms > current_app.config.get("SLOW_REQUEST_MS", 500):
                m["lentas"] += 1
                log.warning("Petición lenta: %s %s (%.0f ms)", request.method, request.path, ms)
    return respuesta


@bp.get("/health")
def salud():
    try:
        get_db().execute("SELECT 1").fetchone()
        bd = "ok"
    except Exception:  # noqa: BLE001 - cualquier fallo de BD implica servicio degradado
        bd = "error"
    estado = "ok" if bd == "ok" else "degradado"
    return jsonify(estado=estado, base_de_datos=bd, uptime_s=round(time.time() - ARRANQUE)), (200 if bd == "ok" else 503)


@bp.get("/health/metricas")
def metricas():
    return jsonify(_metricas())


@bp.app_errorhandler(500)
def error_interno(_e):
    log.exception("Error interno")
    return render_template("error.html", codigo=500,
                           mensaje="Ha ocurrido un error. Inténtalo de nuevo en unos minutos."), 500
