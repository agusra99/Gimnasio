from PySide6.QtWidgets import QApplication
from gui.ventana_principal import VentanaPrincipal
import sys
from db.conexion import crear_tablas

# Punto de entrada principal
if __name__ == "__main__":
    crear_tablas()  # Asegura que las tablas existan al iniciar
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())