import re

from app import registry


def _tokens(app):
    css = open(app.static_folder + "/css/theme.css", encoding="utf-8").read()
    return css, dict(re.findall(r"--([a-z-]+):\s*(#[0-9a-fA-F]{6})", css))


def _luminancia(hex_):
    canales = [int(hex_[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in canales]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contraste(a, b):
    la, lb = sorted((_luminancia(a), _luminancia(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def test_la_hoja_de_tema_se_carga_en_todas_las_paginas(client):
    for ruta in ("/", "/login"):
        assert "css/theme.css" in client.get(ruta).get_data(as_text=True)


def test_contraste_wcag_aa(app):
    _, t = _tokens(app)
    pares = [("color-texto", "color-fondo"), ("color-sobre-primario", "color-primario"),
             ("color-menu-titulo", "color-primario"), ("color-primario", "color-fondo"),
             ("color-texto", "color-superficie")]
    for a, b in pares:
        assert contraste(t[a], t[b]) >= 4.5, f"{a} sobre {b} no alcanza 4,5:1"


def test_diseno_adaptable(app, client):
    css, _ = _tokens(app)
    assert "@media (max-width: 40rem)" in css and "auto-fit" in css
    assert 'name="viewport"' in client.get("/").get_data(as_text=True)


def test_banner_decorativo_no_molesta_a_lectores_de_pantalla(client):
    html = client.get("/").get_data(as_text=True)
    assert 'class="banner"' in html and 'alt=""' in html


def test_tarjetas_de_inicio_salen_del_registro(client):
    registry.register_nav("Cosa de prueba", "index", "Servicios", 1)
    try:
        html = client.get("/").get_data(as_text=True)
        assert 'class="tarjeta"' in html and "Cosa de prueba" in html
    finally:
        registry._NAV[:] = [i for i in registry._NAV if i["label"] != "Cosa de prueba"]
