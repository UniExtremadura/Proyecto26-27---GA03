from app.db import get_db


def _matricular(app, user_id, codigo):
    with app.app_context():
        db = get_db()
        cur = db.execute("INSERT INTO matriculas (user_id, asignatura_id) SELECT ?, id FROM asignaturas WHERE codigo = ?",
                         (user_id, codigo))
        db.commit()
        return cur.lastrowid


def test_requiere_rol_alumno(client, login):
    assert client.get("/desmatricula/").status_code == 302
    login("profesor1")
    assert client.get("/desmatricula/").status_code == 403


def test_estado_vacio(client, login):
    login()
    assert "No tienes matrículas activas" in client.get("/desmatricula/").get_data(as_text=True)


def test_flujo_completo_libera_la_plaza(app, client, login):
    mid = _matricular(app, 1, "ASG101")
    login("alumno1")
    assert "ASG101" in client.get("/desmatricula/").get_data(as_text=True)
    assert "no se puede deshacer" in client.get(f"/desmatricula/{mid}/confirmar").get_data(as_text=True)
    r = client.post(f"/desmatricula/{mid}", follow_redirects=True)
    assert "Te has dado de baja de ASG101" in r.get_data(as_text=True)
    with app.app_context():
        estado = get_db().execute("SELECT estado, cancelada FROM matriculas WHERE id = ?", (mid,)).fetchone()
    assert estado["estado"] == "cancelada" and estado["cancelada"] is not None


def test_no_se_puede_cancelar_dos_veces(app, client, login):
    mid = _matricular(app, 1, "ASG101")
    login("alumno1")
    client.post(f"/desmatricula/{mid}")
    assert client.post(f"/desmatricula/{mid}").status_code == 409


def test_fuera_de_plazo_se_bloquea(app, client, login):
    app.config["DESMATRICULA_HASTA"] = "2000-01-01"
    mid = _matricular(app, 1, "ASG101")
    login("alumno1")
    r = client.post(f"/desmatricula/{mid}")
    assert r.status_code == 409 and "plazo" in r.get_data(as_text=True)
    with app.app_context():
        assert get_db().execute("SELECT estado FROM matriculas WHERE id = ?", (mid,)).fetchone()[0] == "activa"


def test_no_se_pueden_cancelar_matriculas_ajenas(app, client, login):
    mid = _matricular(app, 2, "ASG101")      # matrícula de alumno2
    login("alumno1")
    assert client.get(f"/desmatricula/{mid}/confirmar").status_code == 404
    assert client.post(f"/desmatricula/{mid}").status_code == 404
