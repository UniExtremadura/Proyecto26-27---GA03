from app.db import get_db
from app.modules import asignaturas


def test_detalle_con_docentes_y_partes(app):
    with app.app_context():
        d = asignaturas.obtener_detalle(get_db(), "ASG101")
    assert d["nombre"] == "Fundamentos de Programación"
    assert {x["parte"] for x in d["docentes"]} == {"Teoría", "Prácticas de laboratorio"}


def test_detalle_inexistente(app):
    with app.app_context():
        assert asignaturas.obtener_detalle(get_db(), "NOPE") is None


def test_listado_y_ficha_son_publicos(client):
    assert b"Fundamentos de Programaci" in client.get("/asignaturas/").data
    r = client.get("/asignaturas/ASG101")
    assert r.status_code == 200 and b"Teor" in r.data


def test_estado_vacio_sin_docentes(client):
    r = client.get("/asignaturas/ASG108")
    assert r.status_code == 200
    assert "Todavía no hay docentes" in r.get_data(as_text=True)


def test_estado_error_codigo_desconocido(client):
    r = client.get("/asignaturas/NOPE")
    assert r.status_code == 404 and "no existe" in r.get_data(as_text=True)


def test_proveedor_para_el_buscador_transversal(app):
    with app.app_context():
        titulos = [r["title"] for r in asignaturas.buscar_en_asignaturas("Bases")]
    assert titulos == ["ASG104 · Bases de Datos"]
