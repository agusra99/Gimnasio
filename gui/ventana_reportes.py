from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QFrame, QHeaderView
from PySide6.QtCore import Qt
from modelos.pago import Pago
from modelos.socio import Socio

class VentanaReportes(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #ecf0f1;")
        self.setupUI()
        self.cargar_datos()

    def setupUI(self):
        layout = QVBoxLayout(self)
        
        titulo = QLabel("📊 Reporte de Pagos por Socio")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(titulo)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["Socio", "DNI", "Total Pagado"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tabla)

    def cargar_datos(self):
        socios = Socio.obtener_todos()
        self.tabla.setRowCount(0)
        for socio in socios:
            pagos = Pago.obtener_por_socio(socio[0])
            total = sum([p[3] for p in pagos])  # monto en la columna 4 (índice 3)
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            self.tabla.setItem(row, 0, QTableWidgetItem(f"{socio[1]} {socio[2]}"))
            self.tabla.setItem(row, 1, QTableWidgetItem(str(socio[3])))
            self.tabla.setItem(row, 2, QTableWidgetItem(f"${total:,.2f}"))

    def actualizar_reporte(self):
        self.cargar_datos()
