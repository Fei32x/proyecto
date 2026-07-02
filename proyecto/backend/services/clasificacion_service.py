import os
import sqlite3

DB = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "tienda.db"))


def obtener_estadisticas():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""

    SELECT
        p.id,
        p.nombre,
        IFNULL(SUM(d.cantidad),0),
        IFNULL(SUM(d.subtotal),0)

    FROM productos p

    LEFT JOIN detalles_venta d
    ON p.id=d.id_producto

    GROUP BY p.id

    """)

    productos = cursor.fetchall()

    total_ventas = sum(x[3] for x in productos)

    resultado = []

    for p in productos:

        porcentaje = 0

        if total_ventas > 0:
            porcentaje = (p[3] / total_ventas) * 100

        if porcentaje >= 80:
            clasificacion = "Estrella"
        elif porcentaje <= 20:
            clasificacion = "Hueso"
        else:
            clasificacion = "Normal"

        resultado.append({
            "id": p[0],
            "nombre": p[1],
            "cantidad": int(p[2]),
            "ventas": round(float(p[3]), 2),
            "participacion": round(float(porcentaje), 2),
            "clasificacion": clasificacion
        })

    conn.close()

    return resultado


def obtener_hueso():

    productos = obtener_estadisticas()

    hueso = [
        p for p in productos
        if p["clasificacion"] == "Hueso"
    ]

    hueso.sort(key=lambda x: x["cantidad"])

    return hueso


def obtener_estrella():

    productos = obtener_estadisticas()

    estrella = [
        p for p in productos
        if p["clasificacion"] == "Estrella"
    ]

    estrella.sort(key=lambda x: x["cantidad"], reverse=True)

    return estrella


def obtener_dashboard_data():

    clasificacion = obtener_estadisticas()
    productos_estrella = obtener_estrella()

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.nombre, IFNULL(SUM(d.cantidad), 0) AS cantidad, IFNULL(SUM(d.subtotal), 0) AS ventas
        FROM productos p
        LEFT JOIN detalles_venta d ON p.id = d.id_producto
        GROUP BY p.id
        ORDER BY cantidad DESC
    """)

    ventas_por_producto = [
        {
            "producto": row[0],
            "cantidad": int(row[1]),
            "ventas": round(float(row[2]), 2)
        }
        for row in cursor.fetchall()
    ]

    cursor.execute("SELECT IFNULL(SUM(total), 0) FROM ventas")
    total_ventas = round(float(cursor.fetchone()[0]), 2)

    conn.close()

    resumen = {
        "total_ventas": total_ventas,
        "productos_estrella": len(productos_estrella),
        "productos_hueso": sum(1 for p in clasificacion if p["clasificacion"] == "Hueso")
    }

    return {
        "resumen": resumen,
        "clasificacion": clasificacion,
        "productos_estrella": productos_estrella,
        "ventas_por_producto": ventas_por_producto
    }