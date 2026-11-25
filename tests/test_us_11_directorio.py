def test_requiere_sesion(client):
    assert client.get("/directorio/").status_code == 302
    assert client.get("/directorio/1").status_code == 302


def test_lista_alumnos_y_profesores_sin_pas(client, login):
    login()
    html = client.get("/directorio/").get_data(as_text=True)
    assert ">Ana Alumna Demo</a>" in html and ">Elena Docente Demo</a>" in html
    assert "Paula Secretaría Demo" not in html


def test_filtro_por_rol_y_nombre(client, login):
    login()
    html = client.get("/directorio/?rol=profesor").get_data(as_text=True)
    assert ">Elena Docente Demo</a>" in html and ">Ana Alumna Demo</a>" not in html
    html = client.get("/directorio/?q=Marta").get_data(as_text=True)
    assert ">Marta Alumna Demo</a>" in html and "Luis" not in html


def test_estado_vacio(client, login):
    login()
    assert "No se han encontrado perfiles" in client.get("/directorio/?q=zzzz").get_data(as_text=True)


def test_ficha_de_perfil_y_pas_oculto(client, login):
    login()
    assert "ana.demo@example.org" in client.get("/directorio/1").get_data(as_text=True)
    assert client.get("/directorio/6").status_code == 404   # pas1 no es visible
    assert client.get("/directorio/999").status_code == 404
