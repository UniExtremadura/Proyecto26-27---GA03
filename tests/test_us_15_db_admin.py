from app.db import get_db
from app.modules import db_admin


def test_indices_creados(app):
    with app.app_context():
        tablas = {t["tabla"]: t for t in db_admin.estadisticas_tablas(get_db())}
    assert "idx_users_role" in tablas["users"]["indices"]
    assert "idx_matriculas_user" in tablas["matriculas"]["indices"]


def test_sin_alertas_en_base_sana(app):
    with app.app_context():
        assert db_admin.alertas(get_db(), umbral_filas=1000) == []


def test_alerta_tabla_grande_sin_indice(app):
    with app.app_context():
        db = get_db()
        db.execute("CREATE TABLE registros (id INTEGER PRIMARY KEY, dato TEXT)")
        db.executemany("INSERT INTO registros (dato) VALUES (?)", [("x",)] * 30)
        tipos = [a["tipo"] for a in db_admin.alertas(db, umbral_filas=10)]
    assert "tabla_grande_sin_indice" in tipos


def test_panel_solo_para_pas(client, login):
    assert client.get("/admin/db/").status_code == 302
    login("alumno1")
    assert client.get("/admin/db/").status_code == 403
    login("pas1")
    r = client.get("/admin/db/")
    assert r.status_code == 200 and b"Estado de la base de datos" in r.data


def test_estado_json(client, login):
    login("pas1")
    datos = client.get("/admin/db/estado.json").get_json()
    assert datos["integridad"] == "ok" and datos["alertas"] == []
