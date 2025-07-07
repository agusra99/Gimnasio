from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QStackedWidget, QMessageBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from gui.ventana_socios import VentanaSocios
from gui.ventana_pagos import VentanaPagos
from utils.notificador import obtener_socios_deudores

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Gimnasio")
        self.setGeometry(100, 100, 1000, 600)

        contenedor_principal = QHBoxLayout()
        menu_lateral = QVBoxLayout()
        self.stack = QStackedWidget()

        # Logo (omitido)
        logo = QLabel("LOGO AQUÍ")
        logo.setAlignment(Qt.AlignCenter)
        menu_lateral.addWidget(logo)

        # Botones menú
        btn_socios = QPushButton("Socios")
        btn_socios.clicked.connect(lambda: self.stack.setCurrentWidget(self.pagina_socios))
        menu_lateral.addWidget(btn_socios)

        btn_pagos = QPushButton("Pagos")
        btn_pagos.clicked.connect(lambda: self.stack.setCurrentWidget(self.pagina_pagos))
        menu_lateral.addWidget(btn_pagos)

        btn_salir = QPushButton("Salir")
        btn_salir.clicked.connect(self.close)
        menu_lateral.addWidget(btn_salir)

        menu_lateral.addStretch()

        # Secciones
        self.pagina_socios = VentanaSocios()
        self.pagina_pagos = VentanaPagos()
        self.stack.addWidget(self.pagina_socios)
        self.stack.addWidget(self.pagina_pagos)

        contenedor = QWidget()
        contenedor_principal.addLayout(menu_lateral, 1)
        contenedor_principal.addWidget(self.stack, 4)
        contenedor.setLayout(contenedor_principal)
        self.setCentralWidget(contenedor)

        # Notificaciones de deuda
        deudores = obtener_socios_deudores()
        if deudores:
            mensaje = "Socios con deuda:"
            for d in deudores:
                mensaje += f"- {d['nombre']} | Tel: {d['telefono']} | Periodo adeudado: {d['deuda']}\n"
            QMessageBox.warning(self, "Aviso de Deuda", mensaje)