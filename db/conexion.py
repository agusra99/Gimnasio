import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "gimnasio.db"

def conectar():
    return sqlite3.connect(DB_PATH)

def crear_tablas():
    with conectar() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS socios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            dni TEXT UNIQUE NOT NULL,
            telefono TEXT,
            fecha_alta TEXT NOT NULL
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pagos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            socio_id INTEGER NOT NULL,
            fecha_pago TEXT NOT NULL,
            monto REAL NOT NULL,
            periodo TEXT NOT NULL,
            FOREIGN KEY (socio_id) REFERENCES socios(id)
        )
        """)
        
        conn.commit()