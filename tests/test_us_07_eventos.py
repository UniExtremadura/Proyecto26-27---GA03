from app.db import get_db
from app.modules import eventos


def test_listado_ordenado_por_fecha(client):
    datos = client.get("/api/eventos").get_json()
    fechas = [e["fecha"] for e in datos]
    assert fechas == sorted(fechas) and len(datos) == 4


def test_detalle_y_no_encontrado(client):
    assert client.get("/api/eventos/1").get_json()["titulo"] == "Jornada de bienvenida"
    assert client.get("/api/eventos/999").status_code == 404
    assert client.get("/eventos/999").status_code == 404
    assert b"Aula Magna" in client.get("/eventos/1").data


def test_filtros_se_combinan(client):
    assert len(client.get("/api/eventos?tipo=taller").get_json()) == 1
    assert len(client.get("/api/eventos?q=becas").get_json()) == 1
    assert len(client.get("/api/eventos?desde=2026-12-01").get_json()) == 2
    assert len(client.get("/api/eventos?desde=2026-12-01&tipo=feria").get_json()) == 1
    assert client.get("/api/eventos?q=zzz").get_json() == []


def test_filtro_resistente_a_inyeccion_sql(client):
    assert client.get("/api/eventos?q=' OR 1=1 --").get_json() == []


def test_pagina_con_estado_vacio(client):
    assert "No hay eventos" in client.get("/eventos?q=zzz").get_data(as_text=True)


def test_validacion_del_modelo():
    assert eventos.validar_evento({"titulo": "Ok", "fecha": "2026-11-01"}) == []
    errores = eventos.validar_evento({"titulo": " ", "fecha": "01/11/2026", "aforo": -1, "tipo": "x",
                                      "enlace_inscripcion": "http://inseguro"})
    assert len(errores) == 5


def test_proveedor_del_buscador(app):
    with app.app_context():
        assert [r["title"] for r in eventos.buscar_en_eventos("feria")] == ["Feria de empleo"]
