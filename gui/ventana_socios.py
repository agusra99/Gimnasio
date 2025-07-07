
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QFrame, QHeaderView, QMessageBox
from PySide6.QtCore import Qt
from modelos.socio import Socio
from datetime import datetime

class VentanaSocios(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUI()
        self.cargar_socios()

    def setupUI(self):
        layout = QVBoxLayout(self)
        self.input_nombre = QLineEdit()
        self.input_apellido = QLineEdit()
        self.input_dni = QLineEdit()
        self.input_telefono = QLineEdit()
        btn_agregar = QPushButton("Agregar Socio")
        btn_agregar.clicked.connect(self.agregar_socio)

        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("Nombre:"))
        form_layout.addWidget(self.input_nombre)
        form_layout.addWidget(QLabel("Apellido:"))
        form_layout.addWidget(self.input_apellido)
        form_layout.addWidget(QLabel("DNI:"))
        form_layout.addWidget(self.input_dni)
        form_layout.addWidget(QLabel("Teléfono:"))
        form_layout.addWidget(self.input_telefono)
        form_layout.addWidget(btn_agregar)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Apellido", "DNI", "Teléfono", "Fecha Alta"])

        layout.addLayout(form_layout)
        layout.addWidget(self.tabla)

    def agregar_socio(self):
        nombre = self.input_nombre.text().strip()
        apellido = self.input_apellido.text().strip()
        dni = self.input_dni.text().strip()
        telefono = self.input_telefono.text().strip()
        if not nombre or not apellido or not dni:
            return
        fecha = datetime.today().strftime("%Y-%m-%d")
        Socio.agregar(nombre, apellido, dni, telefono, fecha)
        self.input_nombre.clear()
        self.input_apellido.clear()
        self.input_dni.clear()
        self.input_telefono.clear()
        self.cargar_socios()

        # 🔄 Notificar a la ventana principal que actualice la lista de socios en pagos
        if self.parent() and hasattr(self.parent(), "actualizar_socios_en_pagos"):
            self.parent().actualizar_socios_en_pagos()

    def cargar_socios(self):
        socios = Socio.obtener_todos()
        self.tabla.setRowCount(len(socios))
        for i, socio in enumerate(socios):
            for j, valor in enumerate(socio):
                item = QTableWidgetItem(str(valor))
                item.setTextAlignment(Qt.AlignCenter)
                self.tabla.setItem(i, j, item)
