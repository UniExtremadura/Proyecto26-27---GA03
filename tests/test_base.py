def test_index(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"Plataforma digital de la UNEX" in r.data


def test_login_correcto_y_incorrecto(client, login):
    assert login("alumno1", "mala").status_code == 401
    assert login("alumno1", "demo1234").status_code == 302


def test_token_y_yo(client):
    r = client.post("/api/token", json={"username": "alumno1", "password": "demo1234"})
    assert r.status_code == 200
    token = r.get_json()["token"]
    r = client.get("/api/yo", headers={"Authorization": f"Bearer {token}"})
    assert r.get_json()["rol"] == "alumno"
    assert client.get("/api/yo").status_code == 401


def test_404_amigable(client):
    assert client.get("/no-existe").status_code == 404
