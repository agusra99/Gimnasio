from db.conexion import conectar

class Socio:
    @staticmethod
    def agregar(nombre, apellido, dni, telefono, fecha_alta):
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO socios (nombre, apellido, dni, telefono, fecha_alta)
                VALUES (?, ?, ?, ?, ?)
            """, (nombre, apellido, dni, telefono, fecha_alta))
            conn.commit()

    @staticmethod
    def obtener_todos():
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM socios")
            return cursor.fetchall()

    @staticmethod
    def eliminar(id_socio):
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM socios WHERE id = ?", (id_socio,))
            conn.commit()