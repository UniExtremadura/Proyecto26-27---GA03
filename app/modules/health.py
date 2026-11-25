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
