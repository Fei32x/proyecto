import os
import sqlite3
from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

DB = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "tienda.db"))


class ProductoVenta(BaseModel):
    id_producto: int
    cantidad: int


class Venta(BaseModel):
    productos: List[ProductoVenta]


class ProductoNuevo(BaseModel):
    nombre: str
    precio: float


@router.post("/ventas")
def registrar_venta(venta: Venta):

    if not venta.productos:
        raise HTTPException(status_code=400, detail="Debes enviar al menos un producto")

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    total = 0

    for item in venta.productos:

        cursor.execute(
            "SELECT precio FROM productos WHERE id=?",
            (item.id_producto,)
        )
        producto = cursor.fetchone()

        if producto is None:
            conn.close()
            raise HTTPException(status_code=404, detail=f"Producto no encontrado: {item.id_producto}")

        precio = producto[0]
        total += precio * item.cantidad

    cursor.execute(
        "INSERT INTO ventas(fecha,total) VALUES(?,?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), total)
    )

    id_venta = cursor.lastrowid

    for item in venta.productos:

        cursor.execute(
            "SELECT precio FROM productos WHERE id=?",
            (item.id_producto,)
        )
        producto = cursor.fetchone()
        precio = producto[0]
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


@router.post("/productos")
def agregar_producto(producto: ProductoNuevo):
    if not producto.nombre.strip():
        raise HTTPException(status_code=400, detail="El nombre del producto es obligatorio")

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO productos(nombre, precio) VALUES(?, ?)",
        (producto.nombre.strip(), producto.precio)
    )
    conn.commit()
    conn.close()

    return {
        "mensaje": "Producto agregado correctamente",
        "producto": {
            "nombre": producto.nombre.strip(),
            "precio": producto.precio
        }
    }