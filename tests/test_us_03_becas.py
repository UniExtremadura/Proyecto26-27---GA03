import pytest

from app.db import get_db
from app.modules import becas


def test_alumno_crea_y_consulta_su_solicitud(client, login):
    login("alumno1")
    r = client.post("/becas/nueva", data={"tipo": "General", "observaciones": "Primera solicitud"}, follow_redirects=True)
    html = r.get_data(as_text=True)
    assert "Solicitud enviada" in html and "Pendiente de revisión" in html
    assert "Solicitud 1" in client.get("/becas/").get_data(as_text=True)


def test_tipo_invalido(client, login):
    login("alumno1")
    r = client.post("/becas/nueva", data={"tipo": "Inventada"})
    assert r.status_code == 422


def test_estado_vacio(client, login):
    login("alumno1")
    assert "Todavía no has solicitado" in client.get("/becas/").get_data(as_text=True)


def test_un_alumno_no_ve_solicitudes_ajenas(app, client, login):
    with app.app_context():
        sid = becas.crear_solicitud(get_db(), 2, "General")      # solicitud de alumno2
    login("alumno1")
    assert client.get(f"/becas/{sid}").status_code == 404
    assert client.get(f"/becas/{sid}/estado.json").status_code == 404


def test_transiciones_validas_e_invalidas(app):
    with app.app_context():
        db = get_db()
        sid = becas.crear_solicitud(db, 1, "Movilidad")
        with pytest.raises(ValueError):
            becas.cambiar_estado(db, sid, "resuelta")            # no se puede saltar la revisión
        becas.cambiar_estado(db, sid, "en_revision")
        becas.cambiar_estado(db, sid, "falta_documentacion")
        becas.cambiar_estado(db, sid, "en_revision")
        becas.cambiar_estado(db, sid, "resuelta")
        with pytest.raises(ValueError):
            becas.cambiar_estado(db, sid, "en_revision")         # estado final


def test_pas_registra_documentacion_pendiente_y_alumno_la_ve(app, client, login):
    with app.app_context():
        sid = becas.crear_solicitud(get_db(), 1, "General")
    login("pas1")
    client.post(f"/becas/{sid}/pendientes", data={"descripcion": "Certificado de ingresos"})
    login("alumno1")
    assert "Certificado de ingresos" in client.get(f"/becas/{sid}").get_data(as_text=True)


def test_alumno_no_puede_registrar_pendientes_ni_cambiar_estado(app, client, login):
    with app.app_context():
        sid = becas.crear_solicitud(get_db(), 1, "General")
    login("alumno1")
    assert client.post(f"/becas/{sid}/pendientes", data={"descripcion": "x"}).status_code == 403
    assert client.post(f"/becas/{sid}/estado", data={"estado": "resuelta"}).status_code == 403


def test_estado_en_tiempo_real_refleja_los_cambios(app, client, login):
    with app.app_context():
        sid = becas.crear_solicitud(get_db(), 1, "General")
    login("alumno1")
    assert client.get(f"/becas/{sid}/estado.json").get_json()["estado"] == "pendiente"
    login("pas1")
    client.post(f"/becas/{sid}/estado", data={"estado": "en_revision"})
    login("alumno1")
    datos = client.get(f"/becas/{sid}/estado.json").get_json()
    assert datos["estado"] == "en_revision" and datos["estado_texto"] == "En revisión"


def test_pas_no_puede_hacer_transiciones_invalidas(app, client, login):
    with app.app_context():
        sid = becas.crear_solicitud(get_db(), 1, "General")
    login("pas1")
    assert client.post(f"/becas/{sid}/estado", data={"estado": "resuelta"}).status_code == 422
