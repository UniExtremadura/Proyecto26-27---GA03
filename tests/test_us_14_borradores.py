from datetime import datetime, timedelta, timezone

from app.db import get_db
from app.modules import borradores


def test_requiere_sesion(client):
    assert client.get("/api/borradores/matricula").status_code == 302


def test_guardar_y_recuperar(client, login):
    login()
    r = client.put("/api/borradores/matricula", json={"datos": {"codigos": ["ASG101"]}})
    assert r.status_code == 200 and r.get_json()["version"] == 1
    r = client.get("/api/borradores/matricula")
    assert r.get_json()["datos"] == {"codigos": ["ASG101"]}


def test_sin_borrador_devuelve_404(client, login):
    login()
    assert client.get("/api/borradores/nada").status_code == 404


def test_tramite_invalido_y_datos_invalidos(client, login):
    login()
    assert client.get("/api/borradores/Mal Nombre").status_code in (400, 404)
    assert client.put("/api/borradores/ok", json={"datos": "texto"}).status_code == 400


def test_reintento_identico_es_idempotente(client, login):
    login()
    datos = {"datos": {"a": "1"}}
    v1 = client.put("/api/borradores/t", json=datos).get_json()["version"]
    # el cliente no recibió la respuesta y reintenta con la versión anterior
    r = client.put("/api/borradores/t", json={**datos, "base_version": v1 - 1 or 0})
    assert r.status_code == 200 and r.get_json()["version"] == v1


def test_conflicto_si_otra_pestana_cambio_el_borrador(client, login):
    login()
    client.put("/api/borradores/t", json={"datos": {"a": "1"}})
    client.put("/api/borradores/t", json={"datos": {"a": "2"}, "base_version": 1})
    r = client.put("/api/borradores/t", json={"datos": {"a": "3"}, "base_version": 1})
    assert r.status_code == 409


def test_borrador_caducado_se_ignora_y_se_purga(app):
    with app.app_context():
        db = get_db()
        pasado = datetime.now(timezone.utc) - timedelta(days=borradores.TTL_DIAS + 1)
        borradores.guardar_borrador(db, 1, "t", {"a": "1"}, ahora=pasado)
        assert borradores.obtener_borrador(db, 1, "t") is None
        assert borradores.purgar_caducados(db) == 1


def test_borradores_son_privados_por_usuario(client, login):
    login("alumno1")
    client.put("/api/borradores/t", json={"datos": {"a": "1"}})
    login("alumno2")
    assert client.get("/api/borradores/t").status_code == 404


def test_javascript_contempla_reintentos_y_offline(app):
    js = open(app.static_folder + "/js/autosave.js", encoding="utf-8").read()
    for esperado in ("offline", "online", "Math.pow(2", "sincronizarPendiente"):
        assert esperado in js
