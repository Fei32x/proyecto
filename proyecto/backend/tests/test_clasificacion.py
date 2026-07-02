from fastapi.testclient import TestClient

from backend.main import app
from backend.services.clasificacion_service import obtener_estadisticas


client = TestClient(app)


def test_porcentaje():

    datos = obtener_estadisticas()

    total = 0

    for p in datos:
        total += p["participacion"]

    assert round(total) == 100 or total == 0


def test_clasificacion():

    datos = obtener_estadisticas()

    for p in datos:

        assert p["clasificacion"] in [
            "Estrella",
            "Normal",
            "Hueso"
        ]


def test_dashboard_endpoint_consolidado():

    response = client.get("/api/dashboard")

    assert response.status_code == 200
    payload = response.json()

    assert "resumen" in payload
    assert "clasificacion" in payload
    assert "productos_estrella" in payload
    assert "ventas_por_producto" in payload


def test_registrar_producto():

    nombre = "Producto Test"
    response = client.post(
        "/api/productos",
        json={"nombre": nombre, "precio": 19.99}
    )

    assert response.status_code == 200
    assert response.json()["mensaje"] == "Producto agregado correctamente"

    productos = client.get("/api/productos")
    datos = productos.json()["data"]
    assert any(item["nombre"] == nombre for item in datos)