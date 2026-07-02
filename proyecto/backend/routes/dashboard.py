from fastapi import APIRouter

from backend.services.clasificacion_service import (
    obtener_dashboard_data,
    obtener_estadisticas,
    obtener_hueso,
    obtener_estrella
)

router = APIRouter()


@router.get("/")
def dashboard():
    return obtener_dashboard_data()


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


@router.get("/productos-estrella")
def productos_estrella():

    return {
        "data": obtener_estrella()
    }