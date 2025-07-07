from db.conexion import conectar

class Pago:
    @staticmethod
    def registrar(socio_id, fecha_pago, monto, periodo):
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pagos (socio_id, fecha_pago, monto, periodo)
                VALUES (?, ?, ?, ?)
            """, (socio_id, fecha_pago, monto, periodo))
            conn.commit()

    @staticmethod
    def obtener_por_socio(socio_id):
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pagos WHERE socio_id = ?", (socio_id,))
            return cursor.fetchall()

    @staticmethod
    def obtener_ultimo_periodo_pagado(socio_id):
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT periodo FROM pagos 
                WHERE socio_id = ? 
                ORDER BY fecha_pago DESC 
                LIMIT 1
            """, (socio_id,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None