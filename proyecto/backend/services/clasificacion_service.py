import sqlite3

DB = "tienda.db"


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
            "cantidad": p[2],
            "ventas": round(p[3],2),
            "participacion": round(porcentaje,2),
            "clasificacion": clasificacion

        })

    conn.close()

    return resultado


def obtener_hueso():

    productos = obtener_estadisticas()

    hueso = [
        p for p in productos
        if p["clasificacion"]=="Hueso"
    ]

    hueso.sort(key=lambda x:x["cantidad"])

    return hueso