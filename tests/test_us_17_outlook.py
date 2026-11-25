from urllib.parse import parse_qs, urlparse

from app.modules import outlook


def _configurar(app):
    app.config.update(M365_TENANT_ID="tenant-demo", M365_CLIENT_ID="cliente-demo")


def test_requiere_sesion(client):
    assert client.get("/correo/").status_code == 302
    assert client.get("/correo/conectar").status_code == 302


def test_sin_configurar_informa_y_ofrece_alternativa(client, login):
    login()
    html = client.get("/correo/").get_data(as_text=True)
    assert "todavía no está configurada" in html
    assert "pestaña nueva" in html and "<iframe" not in html


def test_conectar_sin_configurar_es_503(client, login):
    login()
    assert client.get("/correo/conectar").status_code == 503


def test_vista_incrustada_con_titulo_accesible(app, client, login):
    _configurar(app)
    login()
    html = client.get("/correo/").get_data(as_text=True)
    assert "<iframe" in html and 'title="Bandeja de entrada de Outlook"' in html


def test_url_de_autorizacion_correcta(app):
    _configurar(app)
    with app.test_request_context():
        url = outlook.construir_url_autorizacion(outlook.ajustes(), "http://localhost/correo/", "estado123")
    partes = urlparse(url)
    consulta = parse_qs(partes.query)
    assert partes.netloc == "login.microsoftonline.com" and "/tenant-demo/" in partes.path
    assert consulta["client_id"] == ["cliente-demo"] and consulta["response_type"] == ["code"]
    assert consulta["state"] == ["estado123"] and "Mail.Read" in consulta["scope"][0]


def test_conectar_redirige_a_microsoft_y_guarda_el_state(app, client, login):
    _configurar(app)
    login()
    r = client.get("/correo/conectar")
    assert r.status_code == 302 and r.headers["Location"].startswith("https://login.microsoftonline.com/")
    with client.session_transaction() as s:
        assert len(s["m365_state"]) >= 16


def test_no_hay_secretos_en_el_repositorio():
    import pathlib
    codigo = pathlib.Path(outlook.__file__).read_text(encoding="utf-8")
    assert "client_secret" not in codigo.lower()
