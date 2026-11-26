def test_requiere_sesion_y_rol_alumno(client, login):
    assert client.get("/documentos/").status_code == 302
    login("profesor1")
    assert client.get("/documentos/").status_code == 403
    assert client.get("/documentos/matricula/descargar").status_code == 403


def test_descarga_documento_propio(client, login):
    login("alumno1")
    r = client.get("/documentos/matricula/descargar")
    assert r.status_code == 200
    assert r.mimetype == "text/plain"
    assert "attachment" in r.headers["Content-Disposition"]
    assert "Ana Alumna Demo" in r.get_data(as_text=True)


def test_documento_incluye_matriculas_activas(app, client, login):
    from app.db import get_db
    with app.app_context():
        db = get_db()
        db.execute("INSERT INTO matriculas (user_id, asignatura_id) SELECT 1, id FROM asignaturas WHERE codigo = 'ASG101'")
        db.commit()
    login("alumno1")
    assert "ASG101" in client.get("/documentos/expediente/descargar").get_data(as_text=True)


def test_tipo_desconocido_404(client, login):
    login("alumno1")
    assert client.get("/documentos/pasaporte/descargar").status_code == 404


def test_historial_registra_descargas(client, login):
    login("alumno1")
    assert "Todavía no has descargado" in client.get("/documentos/historial").get_data(as_text=True)
    client.get("/documentos/matricula/descargar")
    assert "Resguardo de matrícula" in client.get("/documentos/historial").get_data(as_text=True)
