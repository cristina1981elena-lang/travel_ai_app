import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "travel_ai.db")


def crear_base_datos():
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()

    # TABLA USUARIOS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT,
        plan TEXT DEFAULT 'free'
    )
    """)

    # 👉 NUEVA TABLA USO (CLAVE)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS uso (
        email TEXT PRIMARY KEY,
        consultas INTEGER DEFAULT 0
    )
    """)

    conexion.commit()
    conexion.close()