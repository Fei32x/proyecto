import sqlite3

conn = sqlite3.connect("tienda.db")
cursor = conn.cursor()

# ===============================
# TABLA PRODUCTOS
# ===============================

cursor.execute("""
CREATE TABLE IF NOT EXISTS productos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL
)
""")

# ===============================
# TABLA VENTAS
# ===============================

cursor.execute("""
CREATE TABLE IF NOT EXISTS ventas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    total REAL NOT NULL
)
""")

# ===============================
# DETALLE VENTAS
# ===============================

cursor.execute("""
CREATE TABLE IF NOT EXISTS detalles_venta(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_venta INTEGER,
    id_producto INTEGER,
    cantidad INTEGER,
    subtotal REAL,
    FOREIGN KEY(id_venta) REFERENCES ventas(id),
    FOREIGN KEY(id_producto) REFERENCES productos(id)
)
""")

# ===============================
# PRODUCTOS DE PRUEBA
# ===============================

productos = [
    ("Camiseta Deportiva",25.99),
    ("Zapatillas Runner",89.50),
    ("Gorra Nike",15),
    ("Short Deportivo",30),
    ("Sudadera",50)
]

cursor.executemany("""
INSERT INTO productos(nombre,precio)
SELECT ?,?
WHERE NOT EXISTS(
SELECT 1 FROM productos WHERE nombre=?
)
""",[(p[0],p[1],p[0]) for p in productos])

conn.commit()
conn.close()

print("Base de datos creada correctamente")