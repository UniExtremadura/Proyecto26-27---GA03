"""US-17 · Integración de Outlook (Microsoft 365) en el campus."""
import os
import secrets
from urllib.parse import urlencode

from flask import Blueprint, current_app, redirect, render_template, session, url_for

from .. import registry
from ..auth import login_required

bp = Blueprint("outlook", __name__, url_prefix="/correo")
AUTORIZACION = "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize"
SCOPES = "openid profile offline_access Mail.Read"


def ajustes():
    """Lee la configuración de la app o, si falta, de variables de entorno."""
    cfg = current_app.config
    return {
        "tenant": cfg.get("M365_TENANT_ID") or os.environ.get("M365_TENANT_ID", ""),
        "client_id": cfg.get("M365_CLIENT_ID") or os.environ.get("M365_CLIENT_ID", ""),
        "outlook_url": cfg.get("OUTLOOK_URL", "https://outlook.office.com/mail/"),
    }


def esta_configurado(a):
    return bool(a["tenant"] and a["client_id"])


def construir_url_autorizacion(a, redirect_uri, estado):
    params = {"client_id": a["client_id"], "response_type": "code", "redirect_uri": redirect_uri,
              "response_mode": "query", "scope": SCOPES, "state": estado}
    return AUTORIZACION.format(tenant=a["tenant"]) + "?" + urlencode(params)


@bp.get("/conectar")
@login_required
def conectar():
    a = ajustes()
    if not esta_configurado(a):
        return render_template("error.html", codigo=503,
                               mensaje="La integración con Microsoft 365 todavía no está configurada."), 503
    session["m365_state"] = secrets.token_urlsafe(16)
    return redirect(construir_url_autorizacion(a, url_for("outlook.vista", _external=True), session["m365_state"]))
@bp.get("/")
@login_required
def vista():
    a = ajustes()
    return render_template("outlook/correo.html", configurado=esta_configurado(a), outlook_url=a["outlook_url"])


registry.register_nav("Correo", "outlook.vista", "Servicios", 30)
