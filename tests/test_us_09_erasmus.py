from app.db import get_db
from app.modules import erasmus

MOTIVO = "Quiero mejorar mi nivel de idiomas y conocer otra forma de estudiar."


def test_requiere_rol_alumno(client, login):
    assert client.get("/erasmus/").status_code == 302
    login("profesor1")
    assert client.get("/erasmus/").status_code == 403


def test_formulario_accesible(client, login):
    login()
    html = client.get("/erasmus/").get_data(as_text=True)
    assert 'for="destino"' in html and 'for="motivo"' in html and "required" in html


def test_validacion(client, login):
    login()
    r = client.post("/erasmus/", data={"destino": "Inventada", "motivo": "corto"})
    html = r.get_data(as_text=True)
    assert r.status_code == 422 and 'role="alert"' in html
    assert "Elige un destino" in html and "entre 20 y 1000" in html


def test_envio_y_consulta_de_estado(client, login):
    login()
    r = client.post("/erasmus/", data={"destino": erasmus.DESTINOS[0], "motivo": MOTIVO}, follow_redirects=True)
    assert "enviada correctamente" in r.get_data(as_text=True)
    html = client.get("/erasmus/estado").get_data(as_text=True)
    assert "Universidad de Lisboa" in html and "Enviada" in html


def test_estado_vacio_y_privacidad(app, client, login):
    login("alumno2")
    assert "Todavía no has enviado" in client.get("/erasmus/estado").get_data(as_text=True)
    with app.app_context():
        erasmus.crear_solicitud(get_db(), 1, erasmus.DESTINOS[1], MOTIVO)   # solicitud de alumno1
    assert "Bolonia" not in client.get("/erasmus/estado").get_data(as_text=True)


def test_documentacion_indica_donde_y_como(client, login):
    login()
    html = client.get("/erasmus/documentacion").get_data(as_text=True)
    assert "Oficina de Relaciones Internacionales" in html and "registro electrónico" in html
