"""Plataforma digital UNEX (GA03): esqueleto base.

Cada historia de usuario vive en su propio módulo dentro de ``app/modules``.
Los módulos se descubren automáticamente: basta con que definan ``bp``
(Blueprint) y, opcionalmente, ``SCHEMA`` (SQL idempotente).
"""
import importlib
import os
import pkgutil

from flask import Flask, render_template

from . import auth, db, modules, registry


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-solo-desarrollo"),
        DATABASE=os.path.join(app.instance_path, "campus.db"),
        SCHEMAS=[],
    )
    if test_config:
        app.config.update(test_config)
    os.makedirs(app.instance_path, exist_ok=True)

    app.config["SCHEMAS"] = list(app.config["SCHEMAS"])
    for info in sorted(pkgutil.iter_modules(modules.__path__), key=lambda i: i.name):
        mod = importlib.import_module(f"{modules.__name__}.{info.name}")
        if hasattr(mod, "SCHEMA"):
            app.config["SCHEMAS"].append(mod.SCHEMA)
        if hasattr(mod, "bp"):
            app.register_blueprint(mod.bp)

    app.register_blueprint(auth.bp)
    db.init_app(app)

    @app.context_processor
    def inyectar_navegacion():
        return {"nav_items": registry.nav_items()}

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.errorhandler(403)
    def prohibido(_e):
        return render_template("error.html", codigo=403,
                               mensaje="No tienes permisos para ver esta página."), 403

    @app.errorhandler(404)
    def no_encontrado(_e):
        return render_template("error.html", codigo=404,
                               mensaje="No hemos encontrado lo que buscas."), 404

    return app
