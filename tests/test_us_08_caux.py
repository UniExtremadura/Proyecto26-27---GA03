from app.db import get_db
from app.modules import caux


def test_faq_publica_y_un_clic_desde_el_menu(client):
    r = client.get("/caux/")
    assert r.status_code == 200 and "¿Cómo me matriculo?" in r.get_data(as_text=True)


def test_formulario_accesible(client, login):
    login()
    html = client.get("/caux/").get_data(as_text=True)
    assert '<html lang="es"' in html
    assert 'for="asunto"' in html and 'for="mensaje"' in html
    assert "required" in html


def test_sin_sesion_se_invita_a_iniciar_sesion(client):
    assert "Inicia sesión" in client.get("/caux/").get_data(as_text=True)
    assert client.post("/caux/", data={"asunto": "Hola", "mensaje": "Mensaje largo aquí"}).status_code == 302


def test_errores_se_anuncian_a_lectores_de_pantalla(client, login):
    login()
    r = client.post("/caux/", data={"asunto": "a", "mensaje": "corto"})
    html = r.get_data(as_text=True)
    assert r.status_code == 422 and 'role="alert"' in html


def test_duda_con_faq_se_resuelve_al_instante(client, login):
    login()
    client.post("/caux/", data={"asunto": "Beca", "mensaje": "Quiero saber cómo pedir una beca"})
    assert "Resuelta" in client.get("/caux/mis-consultas").get_data(as_text=True)


def test_duda_sin_faq_queda_pendiente(app):
    with app.app_context():
        _, estado = caux.crear_duda(get_db(), 1, "Aparcamiento", "¿Dónde puedo aparcar mi bicicleta?")
    assert estado == "pendiente"


def test_estado_vacio_de_mis_consultas(client, login):
    login()
    assert "Todavía no has enviado" in client.get("/caux/mis-consultas").get_data(as_text=True)
