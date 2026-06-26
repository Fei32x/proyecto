from fastapi import APIRouter

from backend.services.clasificacion_service import (
    obtener_estadisticas,
    obtener_hueso
)

router = APIRouter()

@router.get("/clasificacion")
def clasificacion():

    return {
        "data": obtener_estadisticas()
    }


@router.get("/productos-hueso")
def productos_hueso():

    return {
        "data": obtener_hueso()
    }