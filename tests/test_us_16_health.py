from concurrent.futures import ThreadPoolExecutor


def test_health_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["base_de_datos"] == "ok"


def test_cabecera_de_tiempo(client):
    assert "X-Response-Time-ms" in client.get("/").headers


def test_peticiones_lentas_se_cuentan(app):
    app.config["SLOW_REQUEST_MS"] = -1  # cualquier petición cuenta como lenta
    c = app.test_client()
    c.get("/")
    assert c.get("/health/metricas").get_json()["lentas"] >= 1


def test_carga_concurrente(app):
    """40 peticiones simultáneas deben responder bien sin bloquear la base de datos."""
    def pedir(_):
        return app.test_client().get("/health").status_code

    with ThreadPoolExecutor(max_workers=8) as pool:
        codigos = list(pool.map(pedir, range(40)))
    assert codigos == [200] * 40
    assert app.test_client().get("/health/metricas").get_json()["peticiones"] >= 40


def test_error_500_amigable(app):
    app.config["PROPAGATE_EXCEPTIONS"] = False

    @app.get("/boom")
    def boom():
        raise RuntimeError("fallo simulado")

    r = app.test_client().get("/boom")
    assert r.status_code == 500 and b"Ha ocurrido un error" in r.data
