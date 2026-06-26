from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.dashboard import router as dashboard
from backend.routes.ventas import router as ventas

import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    dashboard,
    prefix="/api/dashboard"
)
app.include_router(
    ventas,
    prefix="/api"
)


@app.get("/api/productos")
def productos():

    conn = sqlite3.connect("tienda.db")

    cursor = conn.cursor()

    cursor.execute("""

    SELECT
    id,
    nombre,
    precio

    FROM productos

    """)

    datos = cursor.fetchall()

    conn.close()

    return {

        "data":[

            {
                "id":x[0],
                "nombre":x[1],
                "precio":x[2]
            }

            for x in datos

        ]

    }