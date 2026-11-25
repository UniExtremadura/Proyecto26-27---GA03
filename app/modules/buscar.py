"""US-05 · Buscador transversal: consulta los buscadores que registra cada módulo."""
from flask import Blueprint, render_template, request

from .. import registry

bp = Blueprint("buscar", __name__)
MIN_CARACTERES = 2


@bp.get("/buscar")
def resultados():
    q = request.args.get("q", "").strip()
    encontrados = []
    if len(q) >= MIN_CARACTERES:
        for proveedor in registry.search_providers():
            encontrados.extend(proveedor(q))
    return render_template("buscar/resultados.html", q=q, resultados=encontrados,
                           demasiado_corta=bool(q) and len(q) < MIN_CARACTERES)
