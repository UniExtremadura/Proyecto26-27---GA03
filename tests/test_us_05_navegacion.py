from app import registry


def test_menu_global_en_todas_las_paginas(client):
    for ruta in ("/", "/login", "/no-existe"):
        html = client.get(ruta).get_data(as_text=True)
        assert 'aria-label="Navegación principal"' in html
        assert 'role="search"' in html


def test_pagina_actual_marcada(client):
    assert 'aria-current="page"' in client.get("/").get_data(as_text=True)


def test_buscador_estados(client):
    assert "Escribe qué quieres buscar" in client.get("/buscar").get_data(as_text=True)
    assert "al menos 2 caracteres" in client.get("/buscar?q=a").get_data(as_text=True)
    assert "No hay resultados" in client.get("/buscar?q=zzzzzz").get_data(as_text=True)


def test_buscador_usa_proveedores_registrados(client):
    def proveedor(q):
        return [{"title": f"Cosa {q}", "url": "/cosa", "section": "Prueba"}]

    registry.register_search(proveedor)
    try:
        assert "Cosa campus" in client.get("/buscar?q=campus").get_data(as_text=True)
    finally:
        registry._SEARCH.remove(proveedor)


def test_secciones_del_menu_aparecen(client):
    registry.register_nav("Cosa de prueba", "index", "Información", 1)
    try:
        html = client.get("/").get_data(as_text=True)
        assert "Cosa de prueba" in html and "Información" in html
    finally:
        registry._NAV[:] = [i for i in registry._NAV if i["label"] != "Cosa de prueba"]
