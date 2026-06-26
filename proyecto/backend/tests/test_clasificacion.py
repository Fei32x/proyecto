from backend.services.clasificacion_service import obtener_estadisticas


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