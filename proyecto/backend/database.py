import sqlite3

conn = sqlite3.connect('tienda.db')
cursor = conn.cursor()

# Crear tablas
cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    total REAL NOT NULL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS detalles_venta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_venta INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    subtotal REAL NOT NULL,
    FOREIGN KEY (id_venta) REFERENCES ventas(id),
    FOREIGN KEY (id_producto) REFERENCES productos(id)
)''')

# Insertar datos de prueba (Smoke Data)
cursor.execute("INSERT OR IGNORE INTO productos (id, nombre, precio) VALUES (1, 'Camiseta Deportiva', 25.99)")
cursor.execute("INSERT OR IGNORE INTO productos (id, nombre, precio) VALUES (2, 'Zapatillas Runner', 89.50)")
conn.commit()
conn.close()
print("Base de datos y tablas creadas con éxito!")