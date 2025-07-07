from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
from modelos.socio import Socio
from modelos.pago import Pago
from datetime import datetime

class VentanaPagos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Pagos")

        layout = QVBoxLayout()
        form_layout = QHBoxLayout()

        self.combo_socios = QComboBox()
        self.input_monto = QLineEdit()
        self.input_periodo = QLineEdit()
        self.input_periodo.setPlaceholderText("Ej: 2025-07")
        btn_registrar = QPushButton("Registrar Pago")

        form_layout.addWidget(QLabel("Socio:"))
        form_layout.addWidget(self.combo_socios)
        form_layout.addWidget(QLabel("Monto:"))
        form_layout.addWidget(self.input_monto)
        form_layout.addWidget(QLabel("Período:"))
        form_layout.addWidget(self.input_periodo)
        form_layout.addWidget(btn_registrar)

        layout.addLayout(form_layout)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["ID", "Fecha", "Monto", "Periodo"])
        layout.addWidget(self.tabla)

        self.setLayout(layout)

        self.cargar_socios()
        self.combo_socios.currentIndexChanged.connect(self.cargar_historial)
        btn_registrar.clicked.connect(self.registrar_pago)

    def cargar_socios(self):
        self.socios = Socio.obtener_todos()
        self.combo_socios.clear()
        for socio in self.socios:
            self.combo_socios.addItem(f"{socio[1]} {socio[2]} (DNI: {socio[3]})", socio[0])
        self.cargar_historial()

    def cargar_historial(self):
        socio_id = self.combo_socios.currentData()
        if socio_id is None:
            return
        pagos = Pago.obtener_por_socio(socio_id)
        self.tabla.setRowCount(len(pagos))
        for i, pago in enumerate(pagos):
            for j, valor in enumerate(pago[1:]):
                self.tabla.setItem(i, j, QTableWidgetItem(str(valor)))

    def registrar_pago(self):
        socio_id = self.combo_socios.currentData()
        monto = self.input_monto.text()
        periodo = self.input_periodo.text()
        fecha = datetime.today().strftime("%Y-%m-%d")

        if socio_id and monto and periodo:
            Pago.registrar(socio_id, fecha, float(monto), periodo)
            self.input_monto.clear()
            self.input_periodo.clear()
            self.cargar_historial()