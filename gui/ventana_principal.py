from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QMessageBox, QFrame, QScrollArea
)
from PySide6.QtCore import Qt
from gui.ventana_socios import VentanaSocios
from gui.ventana_pagos import VentanaPagos
from gui.ventana_reportes import VentanaReportes
from gui.ventana_reservas import VentanaReservas
from utils.notificador import obtener_socios_deudores

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión de Gimnasio")
        self.setGeometry(100, 100, 1200, 800)

        self.setupUI()
        self.mostrar_notificaciones()

    def setupUI(self):
        contenedor_principal = QWidget()
        self.setCentralWidget(contenedor_principal)
        layout_principal = QHBoxLayout(contenedor_principal)

        self.crear_panel_lateral(layout_principal)
        self.crear_area_contenido(layout_principal)

    def crear_panel_lateral(self, layout_principal):
        panel_lateral = QFrame()
        panel_lateral.setFixedWidth(250)
        layout_lateral = QVBoxLayout(panel_lateral)

        titulo = QLabel("💪 GYM MANAGER")
        titulo.setAlignment(Qt.AlignCenter)
        subtitulo = QLabel("Sistema de Gestión")
        subtitulo.setAlignment(Qt.AlignCenter)
        layout_lateral.addWidget(titulo)
        layout_lateral.addWidget(subtitulo)

        # Botones del menú
        self.btn_socios = QPushButton("👥 Gestión de Socios")
        self.btn_pagos = QPushButton("💳 Gestión de Pagos")
        self.btn_reportes = QPushButton("📊 Reportes")
        self.btn_reservas = QPushButton("📅 Reservas")
        btn_salir = QPushButton("🚪 Salir")

        # Conexiones
        self.btn_socios.clicked.connect(lambda: self.cambiar_pagina(0))
        self.btn_pagos.clicked.connect(lambda: self.cambiar_pagina(1))
        self.btn_reportes.clicked.connect(lambda: self.cambiar_pagina(2))
        self.btn_reservas.clicked.connect(lambda: self.cambiar_pagina(3))
        btn_salir.clicked.connect(self.close)

        # Estilo simple
        for btn in [self.btn_socios, self.btn_pagos, self.btn_reportes, self.btn_reservas, btn_salir]:
            btn.setFixedHeight(45)
            layout_lateral.addWidget(btn)

        layout_lateral.addStretch()
        layout_principal.addWidget(panel_lateral)

    def crear_area_contenido(self, layout_principal):
        area_contenido = QFrame()
        layout_contenido = QVBoxLayout(area_contenido)

        self.stack = QStackedWidget()

        self.pagina_socios = VentanaSocios(self)
        self.pagina_pagos = VentanaPagos()
        self.pagina_reportes = VentanaReportes()
        self.pagina_reservas = VentanaReservas()

        self.stack.addWidget(self.pagina_socios)
        self.stack.addWidget(self.pagina_pagos)
        self.stack.addWidget(self.pagina_reportes)
        self.stack.addWidget(self.pagina_reservas)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.stack)

        layout_contenido.addWidget(scroll_area)
        layout_principal.addWidget(area_contenido)

    def cambiar_pagina(self, indice):
        self.stack.setCurrentIndex(indice)

    def mostrar_notificaciones(self):
        deudores = obtener_socios_deudores()
        if deudores:
            mensaje = f"Se encontraron {len(deudores)} socio(s) con deudas pendientes:\n\n"
            for d in deudores:
                mensaje += f"• {d['nombre']} | 📱 {d['telefono']} | 📅 {d['deuda']}\n"
            QMessageBox.warning(self, "⚠️ Deudas Pendientes", mensaje)

    def actualizar_socios_en_pagos(self):
        self.pagina_pagos.cargar_socios()
''
