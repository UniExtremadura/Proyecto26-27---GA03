"""Autenticación básica de demostración (sesión para la web, token para apps)."""
import functools

from flask import (Blueprint, abort, current_app, flash, g, jsonify, redirect,
                   render_template, request, session, url_for)
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from werkzeug.security import check_password_hash

from .db import get_db

bp = Blueprint("auth", __name__)
TOKEN_TTL_S = 3600


def _usuario_por_id(uid):
    return get_db().execute(
        "SELECT id, username, name, role, email FROM users WHERE id = ?", (uid,)
    ).fetchone()


@bp.before_app_request
def cargar_usuario():
    uid = session.get("user_id")
    g.user = _usuario_por_id(uid) if uid is not None else None


def login_required(vista):
    @functools.wraps(vista)
    def envuelta(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("auth.login", next=request.path))
        return vista(*args, **kwargs)
    return envuelta


def role_required(*roles):
    def decorador(vista):
        @functools.wraps(vista)
        @login_required
        def envuelta(*args, **kwargs):
            if g.user["role"] not in roles:
                abort(403)
            return vista(*args, **kwargs)
        return envuelta
    return decorador


def _serializador():
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt="api-token")


def token_required(vista):
    """Protege endpoints JSON para las apps de escritorio y móvil (Bearer token)."""
    @functools.wraps(vista)
    def envuelta(*args, **kwargs):
        cabecera = request.headers.get("Authorization", "")
        if not cabecera.startswith("Bearer "):
            return jsonify(error="Falta el token de acceso"), 401
        try:
            uid = _serializador().loads(cabecera[7:], max_age=TOKEN_TTL_S)
        except SignatureExpired:
            return jsonify(error="El token ha caducado"), 401
        except BadSignature:
            return jsonify(error="Token no válido"), 401
        g.user = _usuario_por_id(uid)
        if g.user is None:
            return jsonify(error="Usuario no encontrado"), 401
        return vista(*args, **kwargs)
    return envuelta


def _credenciales_validas(username, password):
    fila = get_db().execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if fila is not None and check_password_hash(fila["password_hash"], password):
        return fila
    return None


def _destino_seguro(destino):
    return destino if destino and destino.startswith("/") and not destino.startswith("//") else url_for("index")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = _credenciales_validas(request.form.get("username", "").strip(),
                                        request.form.get("password", ""))
        if usuario is None:
            flash("Usuario o contraseña incorrectos.", "error")
            return render_template("login.html"), 401
        session.clear()
        session["user_id"] = usuario["id"]
        return redirect(_destino_seguro(request.args.get("next")))
    return render_template("login.html")


@bp.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@bp.post("/api/token")
def emitir_token():
    datos = request.get_json(silent=True) or {}
    usuario = _credenciales_validas(str(datos.get("username", "")), str(datos.get("password", "")))
    if usuario is None:
        return jsonify(error="Credenciales incorrectas"), 401
    return jsonify(token=_serializador().dumps(usuario["id"]), expira_en=TOKEN_TTL_S)


@bp.get("/api/yo")
@token_required
def yo():
    return jsonify(id=g.user["id"], nombre=g.user["name"], rol=g.user["role"])
