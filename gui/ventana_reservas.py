from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt, QDate
from datetime import datetime

class VentanaReservas(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #ecf0f1;")
        self.reservas = []  # Lista en memoria por ahora
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout(self)
        
        titulo = QLabel("📅 Reservas de Mesas")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(titulo)

        form_layout = QHBoxLayout()
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre del cliente")
        self.input_fecha = QLineEdit()
        self.input_fecha.setPlaceholderText("Fecha (YYYY-MM-DD)")
        self.input_mesa = QLineEdit()
        self.input_mesa.setPlaceholderText("Número de mesa")

        btn_reservar = QPushButton("Reservar")
        btn_reservar.clicked.connect(self.reservar_mesa)

        form_layout.addWidget(self.input_nombre)
        form_layout.addWidget(self.input_fecha)
        form_layout.addWidget(self.input_mesa)
        form_layout.addWidget(btn_reservar)
        layout.addLayout(form_layout)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["Cliente", "Fecha", "Mesa"])
        layout.addWidget(self.tabla)

    def reservar_mesa(self):
        nombre = self.input_nombre.text().strip()
        fecha = self.input_fecha.text().strip()
        mesa = self.input_mesa.text().strip()

        if not nombre or not fecha or not mesa:
            QMessageBox.warning(self, "Campos incompletos", "Todos los campos son obligatorios.")
            return

        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            QMessageBox.warning(self, "Fecha inválida", "Formato de fecha incorrecto. Use YYYY-MM-DD.")
            return

        self.reservas.append((nombre, fecha, mesa))
        self.actualizar_tabla()
        self.input_nombre.clear()
        self.input_fecha.clear()
        self.input_mesa.clear()

    def actualizar_tabla(self):
        self.tabla.setRowCount(len(self.reservas))
        for i, (nombre, fecha, mesa) in enumerate(self.reservas):
            self.tabla.setItem(i, 0, QTableWidgetItem(nombre))
            self.tabla.setItem(i, 1, QTableWidgetItem(fecha))
            self.tabla.setItem(i, 2, QTableWidgetItem(mesa))
