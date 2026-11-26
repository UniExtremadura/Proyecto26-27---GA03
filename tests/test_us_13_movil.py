import json

from app.db import get_db


def _token(client, usuario="alumno1", clave="demo1234"):
    return client.post("/api/token", json={"username": usuario, "password": clave}).get_json()["token"]


def test_pantallas_son_mobile_first(client):
    for ruta in ("/m/", "/m/login"):
        html = client.get(ruta).get_data(as_text=True)
        assert 'name="viewport"' in html and 'lang="es"' in html
        assert "manifest.webmanifest" in html and "movil.css" in html


def test_manifiesto_es_json_valido_e_instalable(app):
    datos = json.load(open(app.static_folder + "/manifest.webmanifest", encoding="utf-8"))
    assert datos["display"] == "standalone" and datos["start_url"] == "/m/"


def test_login_movil_accesible(client):
    html = client.get("/m/login").get_data(as_text=True)
    assert 'for="usuario"' in html and 'for="clave"' in html and 'role="alert"' in html


def test_resumen_exige_token(client):
    assert client.get("/api/m/resumen").status_code == 401
    r = client.get("/api/m/resumen", headers={"Authorization": "Bearer inventado"})
    assert r.status_code == 401


def test_resumen_con_token(app, client):
    with app.app_context():
        db = get_db()
        db.execute("INSERT INTO matriculas (user_id, asignatura_id) SELECT 1, id FROM asignaturas WHERE codigo IN ('ASG101', 'ASG102')")
        db.commit()
    r = client.get("/api/m/resumen", headers={"Authorization": f"Bearer {_token(client)}"})
    assert r.status_code == 200
    assert r.get_json() == {"usuario": "Ana Alumna Demo", "rol": "alumno", "matriculas_activas": 2, "creditos": 12}


def test_credenciales_incorrectas_no_dan_token(client):
    assert client.post("/api/token", json={"username": "alumno1", "password": "mala"}).status_code == 401
