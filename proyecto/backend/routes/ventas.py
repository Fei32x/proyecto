from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import sqlite3
from datetime import datetime

router = APIRouter()

DB = "tienda.db"


class ProductoVenta(BaseModel):
    id_producto: int
    cantidad: int


class Venta(BaseModel):
    productos: List[ProductoVenta]


@router.post("/ventas")
def registrar_venta(venta: Venta):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    total = 0

    # Calcular total
    for item in venta.productos:

        cursor.execute(
            "SELECT precio FROM productos WHERE id=?",
            (item.id_producto,)
        )

        precio = cursor.fetchone()[0]

        total += precio * item.cantidad

    # Registrar venta
    cursor.execute(
        "INSERT INTO ventas(fecha,total) VALUES(?,?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), total)
    )

    id_venta = cursor.lastrowid

    # Registrar detalle
    for item in venta.productos:

        cursor.execute(
            "SELECT precio FROM productos WHERE id=?",
            (item.id_producto,)
        )

        precio = cursor.fetchone()[0]

        subtotal = precio * item.cantidad

        cursor.execute(
            """
            INSERT INTO detalles_venta
            (id_venta,id_producto,cantidad,subtotal)
            VALUES(?,?,?,?)
            """,
            (
                id_venta,
                item.id_producto,
                item.cantidad,
                subtotal
            )
        )

    conn.commit()
    conn.close()

    return {
        "mensaje": "Venta registrada correctamente",
        "total": total
    }