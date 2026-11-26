from app.db import get_db
from app.modules import matricula


def _matricular(client, *codigos):
    revisar = client.post("/matricula/revisar", data={"codigos": list(codigos)})
    assert revisar.status_code == 200
    return client.post("/matricula/confirmar", data={"codigos": list(codigos)}, follow_redirects=True)


def test_requiere_rol_alumno(client, login):
    assert client.get("/matricula/").status_code == 302
    login("profesor1")
    assert client.get("/matricula/").status_code == 403


def test_flujo_completo(client, login):
    login()
    assert "Matrícula online" in client.get("/matricula/").get_data(as_text=True)
    html = _matricular(client, "ASG101", "ASG102").get_data(as_text=True)
    assert "Matrícula confirmada" in html and "ASG101" in html and "12 ECTS" in html


def test_sin_seleccion_da_error(client, login):
    login()
    r = client.post("/matricula/revisar", data={})
    assert r.status_code == 422 and "al menos una asignatura" in r.get_data(as_text=True)


def test_asignatura_inexistente_y_duplicada(client, login):
    login()
    assert "no existe" in client.post("/matricula/revisar", data={"codigos": ["XXX"]}).get_data(as_text=True)
    _matricular(client, "ASG101")
    assert "Ya estás matriculado" in client.post("/matricula/revisar", data={"codigos": ["ASG101"]}).get_data(as_text=True)


def test_sin_plazas(app, client, login):
    with app.app_context():
        db = get_db()
        db.execute("UPDATE asignaturas SET plazas = 0 WHERE codigo = 'ASG103'")
        db.commit()
    login()
    r = client.post("/matricula/revisar", data={"codigos": ["ASG103"]})
    assert r.status_code == 422 and "no tiene plazas libres" in r.get_data(as_text=True)


def test_maximo_de_creditos(app, client, login):
    with app.app_context():
        db = get_db()
        db.execute("UPDATE asignaturas SET creditos = 40 WHERE codigo IN ('ASG101', 'ASG102')")
        db.commit()
    login()
    r = client.post("/matricula/revisar", data={"codigos": ["ASG101", "ASG102"]})
    assert r.status_code == 422 and "Superas el máximo" in r.get_data(as_text=True)


def test_confirmar_revalida(app, client, login):
    """Si las plazas se agotan entre «revisar» y «confirmar», no se matricula."""
    login()
    with app.app_context():
        db = get_db()
        db.execute("UPDATE asignaturas SET plazas = 0 WHERE codigo = 'ASG104'")
        db.commit()
    r = client.post("/matricula/confirmar", data={"codigos": ["ASG104"]})
    assert r.status_code == 422
    assert "Todavía no estás matriculado" in client.get("/matricula/resumen").get_data(as_text=True)


def test_validar_sin_duplicados_en_la_peticion(app):
    with app.app_context():
        errores, nuevas = matricula.validar_matricula(get_db(), 1, ["ASG101", "ASG101"])
    assert errores == [] and len(nuevas) == 1
