from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
from modelos.socio import Socio
from datetime import datetime

class VentanaSocios(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Socios")

        layout = QVBoxLayout()
        form_layout = QHBoxLayout()

        self.input_nombre = QLineEdit()
        self.input_apellido = QLineEdit()
        self.input_dni = QLineEdit()
        self.input_telefono = QLineEdit()
        btn_agregar = QPushButton("Agregar Socio")

        form_layout.addWidget(QLabel("Nombre:"))
        form_layout.addWidget(self.input_nombre)
        form_layout.addWidget(QLabel("Apellido:"))
        form_layout.addWidget(self.input_apellido)
        form_layout.addWidget(QLabel("DNI:"))
        form_layout.addWidget(self.input_dni)
        form_layout.addWidget(QLabel("Teléfono:"))
        form_layout.addWidget(self.input_telefono)
        form_layout.addWidget(btn_agregar)

        btn_agregar.clicked.connect(self.agregar_socio)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Apellido", "DNI", "Teléfono"])

        layout.addLayout(form_layout)
        layout.addWidget(self.tabla)
        self.setLayout(layout)

        self.cargar_socios()

    def agregar_socio(self):
        nombre = self.input_nombre.text()
        apellido = self.input_apellido.text()
        dni = self.input_dni.text()
        telefono = self.input_telefono.text()
        fecha = datetime.today().strftime("%Y-%m-%d")

        if nombre and apellido and dni:
            Socio.agregar(nombre, apellido, dni, telefono, fecha)
            self.input_nombre.clear()
            self.input_apellido.clear()
            self.input_dni.clear()
            self.input_telefono.clear()
            self.cargar_socios()

    def cargar_socios(self):
        socios = Socio.obtener_todos()
        self.tabla.setRowCount(len(socios))
        for i, socio in enumerate(socios):
            for j, valor in enumerate(socio[:5]):
                self.tabla.setItem(i, j, QTableWidgetItem(str(valor)))