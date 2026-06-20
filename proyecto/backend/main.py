from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

# Permitir que el Frontend (Streamlit) hable con este Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/productos")
def obtener_productos():
    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, precio FROM productos")
    productos = [{"id": row[0], "nombre": row[1], "precio": row[2]} for row in cursor.fetchall()]
    conn.close()
    return {"data": productos}