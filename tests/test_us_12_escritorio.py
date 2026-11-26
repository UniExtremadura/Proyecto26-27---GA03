import io
import json
import threading
import urllib.error

import pytest
from werkzeug.serving import make_server

from desktop import ui
from desktop.client import ApiError, CampusClient


class Respuesta:
    def __init__(self, datos):
        self._bytes = json.dumps(datos).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def read(self):
        return self._bytes


def test_ui_se_importa_sin_entorno_grafico():
    assert ui.TITULO == "Campus UNEX"


def test_login_guarda_token_y_lo_envia(monkeypatch):
    peticiones = []

    def abrir(peticion, timeout):
        peticiones.append(peticion)
        return Respuesta({"token": "abc"} if peticion.full_url.endswith("/api/token")
                         else {"nombre": "Ana", "rol": "alumno"})

    cliente = CampusClient("http://servidor/", abrir=abrir)
    assert cliente.login("alumno1", "demo1234") == "abc"
    assert cliente.perfil()["nombre"] == "Ana"
    assert peticiones[1].get_header("Authorization") == "Bearer abc"


def test_credenciales_vacias_no_llaman_al_servidor():
    llamado = []
    cliente = CampusClient(abrir=lambda *a, **k: llamado.append(1))
    with pytest.raises(ApiError):
        cliente.login("", "x")
    assert llamado == []


def test_perfil_exige_login():
    with pytest.raises(ApiError):
        CampusClient().perfil()


def test_error_http_usa_el_mensaje_del_servidor():
    def abrir(peticion, timeout):
        raise urllib.error.HTTPError(peticion.full_url, 401, "No autorizado", {}, io.BytesIO(b'{"error": "Credenciales incorrectas"}'))

    with pytest.raises(ApiError) as e:
        CampusClient(abrir=abrir).login("a", "b")
    assert str(e.value) == "Credenciales incorrectas" and e.value.estado == 401


def test_sin_conexion_da_mensaje_claro():
    def abrir(peticion, timeout):
        raise urllib.error.URLError("sin red")

    with pytest.raises(ApiError, match="No se puede conectar"):
        CampusClient(abrir=abrir).login("a", "b")


def test_extremo_a_extremo_contra_el_servidor_real(app):
    servidor = make_server("127.0.0.1", 0, app, threaded=True)
    hilo = threading.Thread(target=servidor.serve_forever, daemon=True)
    hilo.start()
    try:
        cliente = CampusClient(f"http://127.0.0.1:{servidor.server_port}")
        cliente.login("alumno1", "demo1234")
        assert cliente.perfil()["rol"] == "alumno"
        with pytest.raises(ApiError):
            CampusClient(f"http://127.0.0.1:{servidor.server_port}").login("alumno1", "mala")
    finally:
        servidor.shutdown()
