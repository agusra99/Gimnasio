from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QFrame, QHeaderView, QMessageBox, QDateEdit)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QDoubleValidator
from modelos.socio import Socio
from modelos.pago import Pago
from datetime import datetime

class VentanaPagos(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: #ecf0f1;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        self.setupUI()
        self.cargar_socios()
        
    def setupUI(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(30, 30, 30, 30)
        layout_principal.setSpacing(20)
        
        # Sección de formulario
        self.crear_seccion_formulario(layout_principal)
        
        # Sección de tabla
        self.crear_seccion_tabla(layout_principal)
        
    def crear_seccion_formulario(self, layout_principal):
        # Frame del formulario
        frame_formulario = QFrame()
        frame_formulario.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #bdc3c7;
                padding: 20px;
            }
        """)
        
        layout_formulario = QVBoxLayout(frame_formulario)
        layout_formulario.setContentsMargins(25, 25, 25, 25)
        layout_formulario.setSpacing(20)
        
        # Título de la sección
        titulo_form = QLabel("💳 Registrar Nuevo Pago")
        titulo_form.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 18px;
                font-weight: bold;
                background: transparent;
                padding-bottom: 10px;
            }
        """)
        layout_formulario.addWidget(titulo_form)
        
        # Campos del formulario en dos filas
        # Primera fila
        fila1 = QHBoxLayout()
        fila1.setSpacing(15)
        
        # Socio
        grupo_socio = QVBoxLayout()
        label_socio = QLabel("Socio *")
        label_socio.setStyleSheet(self.estilo_label())
        self.combo_socios = QComboBox()
        self.combo_socios.setStyleSheet(self.estilo_combo())
        grupo_socio.addWidget(label_socio)
        grupo_socio.addWidget(self.combo_socios)
        
        # Monto
        grupo_monto = QVBoxLayout()
        label_monto = QLabel("Monto *")
        label_monto.setStyleSheet(self.estilo_label())
        self.input_monto = QLineEdit()
        self.input_monto.setStyleSheet(self.estilo_input())
        self.input_monto.setPlaceholderText("Ej: 15000.00")
        # Validador para números decimales
        validator = QDoubleValidator(0.0, 999999.99, 2)
        self.input_monto.setValidator(validator)
        grupo_monto.addWidget(label_monto)
        grupo_monto.addWidget(self.input_monto)
        
        fila1.addLayout(grupo_socio)
        fila1.addLayout(grupo_monto)
        
        # Segunda fila
        fila2 = QHBoxLayout()
        fila2.setSpacing(15)
        
        # Período
        grupo_periodo = QVBoxLayout()
        label_periodo = QLabel("Período *")
        label_periodo.setStyleSheet(self.estilo_label())
        self.input_periodo = QLineEdit()
        self.input_periodo.setStyleSheet(self.estilo_input())
        self.input_periodo.setPlaceholderText("Ej: 2025-07")
        # Valor por defecto del período actual
        periodo_actual = datetime.now().strftime("%Y-%m")
        self.input_periodo.setText(periodo_actual)
        grupo_periodo.addWidget(label_periodo)
        grupo_periodo.addWidget(self.input_periodo)
        
        # Fecha
        grupo_fecha = QVBoxLayout()
        label_fecha = QLabel("Fecha de Pago")
        label_fecha.setStyleSheet(self.estilo_label())
        self.date_pago = QDateEdit()
        self.date_pago.setDate(QDate.currentDate())
        self.date_pago.setStyleSheet(self.estilo_date())
        self.date_pago.setCalendarPopup(True)
        grupo_fecha.addWidget(label_fecha)
        grupo_fecha.addWidget(self.date_pago)
        
        fila2.addLayout(grupo_periodo)
        fila2.addLayout(grupo_fecha)
        
        # Botón de registrar
        btn_registrar = QPushButton("✅ Registrar Pago")
        btn_registrar.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #219a52;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        btn_registrar.clicked.connect(self.registrar_pago)
        
        # Layout del botón
        layout_boton = QHBoxLayout()
        layout_boton.addStretch()
        layout_boton.addWidget(btn_registrar)
        
        layout_formulario.addLayout(fila1)
        layout_formulario.addLayout(fila2)
        layout_formulario.addLayout(layout_boton)
        
        layout_principal.addWidget(frame_formulario)
        
    def crear_seccion_tabla(self, layout_principal):
        # Frame de la tabla
        frame_tabla = QFrame()
        frame_tabla.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #bdc3c7;
                padding: 20px;
            }
        """)
        
        layout_tabla = QVBoxLayout(frame_tabla)
        layout_tabla.setContentsMargins(25, 25, 25, 25)
        layout_tabla.setSpacing(15)
        
        # Título de la sección con info del socio seleccionado
        layout_titulo = QHBoxLayout()
        
        self.titulo_tabla = QLabel("💰 Historial de Pagos")
        self.titulo_tabla.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 18px;
                font-weight: bold;
                background: transparent;
                padding-bottom: 10px;
            }
        """)
        
        self.info_socio = QLabel("")
        self.info_socio.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 14px;
                font-style: italic;
                background: transparent;
                padding-bottom: 10px;
            }
        """)
        
        layout_titulo.addWidget(self.titulo_tabla)
        layout_titulo.addStretch()
        layout_titulo.addWidget(self.info_socio)
        
        layout_tabla.addLayout(layout_titulo)
        
        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["ID", "Fecha Pago", "Monto", "Período", "Estado"])
        
        # Estilo de la tabla
        self.tabla.setStyleSheet("""
            QTableWidget {
                background-color: #fafafa;
                alternate-background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 8px;
                selection-background-color: #3498db;
                selection-color: white;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 12px 8px;
                border: none;
                border-bottom: 1px solid #eee;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                font-weight: bold;
                padding: 12px 8px;
                border: none;
                border-right: 1px solid #2c3e50;
            }
            QHeaderView::section:first {
                border-top-left-radius: 8px;
            }
            QHeaderView::section:last {
                border-top-right-radius: 8px;
                border-right: none;
            }
        """)
        
        # Configurar el comportamiento de la tabla
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla.setSortingEnabled(True)
        
        # Ajustar el tamaño de las columnas
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Fecha
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Monto
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Período
        header.setSectionResizeMode(4, QHeaderView.Stretch)  # Estado
        
        self.tabla.setColumnWidth(0, 60)  # ID más pequeño
        
        layout_tabla.addWidget(self.tabla)
        layout_principal.addWidget(frame_tabla)
        
    def estilo_label(self):
        return """
            QLabel {
                color: #2c3e50;
                font-size: 13px;
                font-weight: bold;
                background: transparent;
                margin-bottom: 5px;
            }
        """
        
    def estilo_input(self):
        return """
            QLineEdit {
                background-color: #ffffff;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 13px;
                color: #2c3e50;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #fbfcfd;
            }
            QLineEdit::placeholder {
                color: #95a5a6;
            }
        """
        
    def estilo_combo(self):
        return """
            QComboBox {
                background-color: #ffffff;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 13px;
                color: #2c3e50;
                min-width: 200px;
            }
            QComboBox:focus {
                border-color: #3498db;
                background-color: #fbfcfd;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border: 5px solid transparent;
                border-top: 5px solid #7f8c8d;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 8px;
                selection-background-color: #3498db;
                selection-color: white;
            }
        """
        
    def estilo_date(self):
        return """
            QDateEdit {
                background-color: #ffffff;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 13px;
                color: #2c3e50;
            }
            QDateEdit:focus {
                border-color: #3498db;
                background-color: #fbfcfd;
            }
            QDateEdit::drop-down {
                border: none;
                width: 20px;
            }
            QDateEdit::down-arrow {
                image: none;
                border: 5px solid transparent;
                border-top: 5px solid #7f8c8d;
                margin-right: 5px;
            }
        """
        
    def cargar_socios(self):
        try:
            self.socios = Socio.obtener_todos()
            self.combo_socios.clear()
            
            for socio in self.socios:
                texto = f"{socio[1]} {socio[2]} - DNI: {socio[3]}"
                self.combo_socios.addItem(texto, socio[0])
                
            # Conectar evento de cambio
            self.combo_socios.currentIndexChanged.connect(self.cargar_historial)
            
            # Cargar historial del primer socio
            self.cargar_historial()
            
        except Exception as e:
            self.mostrar_mensaje("Error", f"Error al cargar los socios: {str(e)}", QMessageBox.Critical)
            
    def cargar_historial(self):
        try:
            socio_id = self.combo_socios.currentData()
            if socio_id is None:
                self.tabla.setRowCount(0)
                self.info_socio.setText("")
                return
                
            # Actualizar información del socio
            texto_socio = self.combo_socios.currentText()
            self.info_socio.setText(f"Mostrando pagos de: {texto_socio}")
            
            # Cargar pagos
            pagos = Pago.obtener_por_socio(socio_id)
            self.tabla.setRowCount(len(pagos))
            
            for i, pago in enumerate(pagos):
                # ID
                item_id = QTableWidgetItem(str(pago[0]))
                item_id.setTextAlignment(Qt.AlignCenter)
                self.tabla.setItem(i, 0, item_id)
                
                # Fecha
                item_fecha = QTableWidgetItem(str(pago[2]))
                item_fecha.setTextAlignment(Qt.AlignCenter)
                self.tabla.setItem(i, 1, item_fecha)
                
                # Monto
                item_monto = QTableWidgetItem(f"${pago[3]:,.2f}")
                item_monto.setTextAlignment(Qt.AlignRight)
                self.tabla.setItem(i, 2, item_monto)
                
                # Período
                item_periodo = QTableWidgetItem(str(pago[4]))
                item_periodo.setTextAlignment(Qt.AlignCenter)
                self.tabla.setItem(i, 3, item_periodo)
                
                # Estado (calculado según el período)
                periodo_actual = datetime.now().strftime("%Y-%m")
                if pago[4] == periodo_actual:
                    estado = "✅ Al día"
                    color = "#27ae60"
                elif pago[4] > periodo_actual:
                    estado = "⏰ Adelantado"
                    color = "#3498db"
                else:
                    estado = "⚠️ Atrasado"
                    color = "#e74c3c"
                    
                item_estado = QTableWidgetItem(estado)
                item_estado.setTextAlignment(Qt.AlignCenter)
                self.tabla.setItem(i, 4, item_estado)
                
        except Exception as e:
            self.mostrar_mensaje("Error", f"Error al cargar el historial: {str(e)}", QMessageBox.Critical)
            
    def registrar_pago(self):
        socio_id = self.combo_socios.currentData()
        monto_text = self.input_monto.text().strip()
        periodo = self.input_periodo.text().strip()
        fecha = self.date_pago.date().toString("yyyy-MM-dd")
        
        # Validaciones
        if socio_id is None:
            self.mostrar_mensaje("Error", "Debe seleccionar un socio", QMessageBox.Warning)
            return
            
        if not monto_text:
            self.mostrar_mensaje("Error", "El monto es obligatorio", QMessageBox.Warning)
            self.input_monto.setFocus()
            return
            
        try:
            monto = float(monto_text)
            if monto <= 0:
                self.mostrar_mensaje("Error", "El monto debe ser mayor a cero", QMessageBox.Warning)
                self.input_monto.setFocus()
                return
        except ValueError:
            self.mostrar_mensaje("Error", "El monto debe ser un número válido", QMessageBox.Warning)
            self.input_monto.setFocus()
            return
            
        if not periodo:
            self.mostrar_mensaje("Error", "El período es obligatorio", QMessageBox.Warning)
            self.input_periodo.setFocus()
            return
            
        # Validar formato del período
        if not self.validar_formato_periodo(periodo):
            self.mostrar_mensaje("Error", "El período debe tener el formato YYYY-MM (ej: 2025-07)", QMessageBox.Warning)
            self.input_periodo.setFocus()
            return
        
        try:
            # Registrar el pago
            Pago.registrar(socio_id, fecha, monto, periodo)
            
            # Limpiar campos
            self.input_monto.clear()
            self.input_periodo.setText(datetime.now().strftime("%Y-%m"))
            self.date_pago.setDate(QDate.currentDate())
            
            # Recargar historial
            self.cargar_historial()
            
            # Mensaje de éxito
            socio_nombre = self.combo_socios.currentText()
            self.mostrar_mensaje("Éxito", f"Pago registrado correctamente para {socio_nombre}", QMessageBox.Information)
            
        except Exception as e:
            self.mostrar_mensaje("Error", f"Error al registrar el pago: {str(e)}", QMessageBox.Critical)
            
    def validar_formato_periodo(self, periodo):
        try:
            partes = periodo.split("-")
            if len(partes) != 2:
                return False
            
            año = int(partes[0])
            mes = int(partes[1])
            
            return (1900 <= año <= 2100) and (1 <= mes <= 12)
        except (ValueError, IndexError):
            return False
            
    def mostrar_mensaje(self, titulo, mensaje, tipo):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(titulo)
        msg_box.setText(mensaje)
        msg_box.setIcon(tipo)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: white;
                color: #2c3e50;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QMessageBox QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        msg_box.exec()
