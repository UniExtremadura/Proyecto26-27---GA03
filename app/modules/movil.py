"""US-13 · Acceso móvil al campus (PWA mobile-first)."""
from flask import Blueprint, render_template

bp = Blueprint("movil", __name__)


@bp.get("/m/")
def inicio():
    return render_template("movil/inicio.html")
