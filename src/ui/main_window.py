"""
Ventana Principal de FeeReport Lite.
Diseño moderno, limpio y ultra compacto con foco en la tabla de ítems presupuestados.
"""
import os
import sys
import subprocess
from datetime import date
from pathlib import Path
from typing import List

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QDoubleSpinBox,
    QSpinBox,
    QComboBox,
    QCheckBox,
    QMessageBox,
    QScrollArea,
    QAbstractItemView,
)

from ..models.cliente import Cliente
from ..models.profesional import Profesional
from ..models.presupuesto import ItemPresupuesto, Presupuesto
from ..services.config_service import ConfigService
from ..services.pdf_generator import PDFGeneratorService
from ..utils.paths import get_app_icon_path, get_outputs_dir
from ..utils.formatters import format_currency


class MainWindow(QMainWindow):
    """Ventana principal para carga y confección de presupuestos con cálculo en tiempo real."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("FeeReport Lite • Generador de Presupuestos")
        self.resize(1020, 720)
        self.setMinimumSize(820, 500)

        # Servicios
        self.config_service = ConfigService()
        self.pdf_service = PDFGeneratorService()

        # Establecer icono de ventana
        icon_path = get_app_icon_path()
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        self._init_ui()
        self._load_saved_professional_data()
        self._add_initial_item()
        self._recalculate_all()

    def _init_ui(self):
        """Construye la jerarquía visual de la aplicación optimizada para pantallas de cualquier resolución."""
        # Scroll area contenedor principal para garantizar accesibilidad en pantallas de menor altura
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.setCentralWidget(scroll)

        content_widget = QWidget()
        scroll.setWidget(content_widget)

        main_layout = QVBoxLayout(content_widget)
        main_layout.setContentsMargins(14, 10, 14, 10)
        main_layout.setSpacing(8)

        # 1. Panel de Formularios Compactos (Profesional y Cliente en paralelo)
        forms_layout = QHBoxLayout()
        forms_layout.setSpacing(10)
        forms_layout.addWidget(self._create_professional_group(), stretch=1)
        forms_layout.addWidget(self._create_client_group(), stretch=1)
        main_layout.addLayout(forms_layout, stretch=0)

        # 2. Panel de Ítems Presupuestados (Prioridad de espacio y altura garantizada)
        main_layout.addWidget(self._create_items_group(), stretch=1)

        # 3. Panel Inferior Compacto: Opciones Financieras y Resumen de Totales
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(10)
        bottom_layout.addWidget(self._create_options_group(), stretch=1)
        bottom_layout.addWidget(self._create_summary_group(), stretch=1)
        main_layout.addLayout(bottom_layout, stretch=0)

        # 4. Barra de Acciones Globales
        main_layout.addLayout(self._create_actions_bar(), stretch=0)

    def _create_professional_group(self) -> QGroupBox:
        """Crea la tarjeta compacta de datos del emisor (Profesional) en 2 columnas."""
        box = QGroupBox("Datos del Profesional (Emisor)")
        layout = QGridLayout(box)
        layout.setVerticalSpacing(4)
        layout.setHorizontalSpacing(8)
        layout.setContentsMargins(8, 8, 8, 6)

        # Fila 0: Nombre y Apellido
        lbl_nombre = QLabel("Nombre:")
        self.txt_prof_nombre = QLineEdit()
        self.txt_prof_nombre.setPlaceholderText("Nombre...")

        lbl_apellido = QLabel("Apellido:")
        self.txt_prof_apellido = QLineEdit()
        self.txt_prof_apellido.setPlaceholderText("Apellido...")

        layout.addWidget(lbl_nombre, 0, 0)
        layout.addWidget(self.txt_prof_nombre, 0, 1)
        layout.addWidget(lbl_apellido, 0, 2)
        layout.addWidget(self.txt_prof_apellido, 0, 3)

        # Fila 1: Teléfono y Título/Especialidad
        lbl_tel = QLabel("Teléfono:")
        self.txt_prof_tel = QLineEdit()
        self.txt_prof_tel.setPlaceholderText("Teléfono...")

        lbl_esp = QLabel("Título/Especialidad:")
        self.txt_prof_titulo = QLineEdit()
        self.txt_prof_titulo.setPlaceholderText("Ej. Servicios Profesionales")

        layout.addWidget(lbl_tel, 1, 0)
        layout.addWidget(self.txt_prof_tel, 1, 1)
        layout.addWidget(lbl_esp, 1, 2)
        layout.addWidget(self.txt_prof_titulo, 1, 3)

        # Fila 2: Botón de guardado rápido alineado
        btn_save_prof = QPushButton("💾 Guardar mis datos por defecto")
        btn_save_prof.setObjectName("btnSubtle")
        btn_save_prof.setToolTip("Guarda estos datos para no reingresarlos en futuras sesiones")
        btn_save_prof.clicked.connect(self._save_professional_data)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(btn_save_prof)
        layout.addLayout(btn_row, 2, 0, 1, 4)

        return box

    def _create_client_group(self) -> QGroupBox:
        """Crea la tarjeta compacta de datos del receptor (Cliente) en 2 columnas."""
        box = QGroupBox("Datos del Cliente (Receptor)")
        layout = QGridLayout(box)
        layout.setVerticalSpacing(4)
        layout.setHorizontalSpacing(8)
        layout.setContentsMargins(8, 8, 8, 6)

        # Fila 0: Nombre y Apellido
        lbl_nombre = QLabel("Nombre:")
        self.txt_cli_nombre = QLineEdit()
        self.txt_cli_nombre.setPlaceholderText("Nombre del cliente...")

        lbl_apellido = QLabel("Apellido:")
        self.txt_cli_apellido = QLineEdit()
        self.txt_cli_apellido.setPlaceholderText("Apellido del cliente...")

        layout.addWidget(lbl_nombre, 0, 0)
        layout.addWidget(self.txt_cli_nombre, 0, 1)
        layout.addWidget(lbl_apellido, 0, 2)
        layout.addWidget(self.txt_cli_apellido, 0, 3)

        # Fila 1: Teléfono y Email
        lbl_tel = QLabel("Teléfono:")
        self.txt_cli_tel = QLineEdit()
        self.txt_cli_tel.setPlaceholderText("Teléfono...")

        lbl_email = QLabel("Email:")
        self.txt_cli_email = QLineEdit()
        self.txt_cli_email.setPlaceholderText("Email...")

        layout.addWidget(lbl_tel, 1, 0)
        layout.addWidget(self.txt_cli_tel, 1, 1)
        layout.addWidget(lbl_email, 1, 2)
        layout.addWidget(self.txt_cli_email, 1, 3)

        # Fila 2: Botón para limpiar cliente
        btn_clear_client = QPushButton("🧹 Limpiar datos del cliente")
        btn_clear_client.setObjectName("btnSubtle")
        btn_clear_client.clicked.connect(self._clear_client_fields)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(btn_clear_client)
        layout.addLayout(btn_row, 2, 0, 1, 4)

        return box

    def _create_items_group(self) -> QGroupBox:
        """Crea la sección de tabla de ítems con altura amplia garantizada y botones de acción."""
        box = QGroupBox("Conceptos / Ítems del Presupuesto")
        layout = QVBoxLayout(box)
        layout.setSpacing(6)
        layout.setContentsMargins(10, 10, 10, 8)

        # Tabla con altura mínima visible
        self.table_items = QTableWidget(0, 4)
        self.table_items.setMinimumHeight(240)
        self.table_items.setHorizontalHeaderLabels([
            "Descripción del Servicio / Producto",
            "Cantidad",
            "Precio Unitario",
            "Subtotal",
        ])
        header = self.table_items.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        self.table_items.setAlternatingRowColors(True)
        self.table_items.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_items.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_items.verticalHeader().setVisible(False)
        layout.addWidget(self.table_items, stretch=1)

        # Botonera de ítems (claramente visible)
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        btn_add = QPushButton("＋ Agregar nuevo ítem")
        btn_add.setObjectName("btnSuccess")
        btn_add.setCursor(Qt.PointingHandCursor)
        btn_add.clicked.connect(self._add_item_row)

        btn_del = QPushButton("✕ Eliminar ítem seleccionado")
        btn_del.setObjectName("btnDanger")
        btn_del.clicked.connect(self._delete_selected_item)

        btn_clear = QPushButton("Vaciar todos los ítems")
        btn_clear.clicked.connect(self._clear_all_items)

        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_del)
        btn_layout.addWidget(btn_clear)
        btn_layout.addStretch()

        layout.addLayout(btn_layout, stretch=0)
        return box

    def _create_options_group(self) -> QGroupBox:
        """Crea la tarjeta compacta de configuración financiera en 2 filas."""
        box = QGroupBox("Parámetros Financieros")
        layout = QGridLayout(box)
        layout.setVerticalSpacing(4)
        layout.setHorizontalSpacing(8)
        layout.setContentsMargins(8, 8, 8, 6)

        # Fila 0: Moneda y Validez
        lbl_cur = QLabel("Moneda:")
        self.cmb_currency = QComboBox()
        self.cmb_currency.addItems(["$", "USD $", "ARS $", "EUR €", "CLP $", "MXN $", "COP $", "S/."])
        saved_curr = self.config_service.get_preference("currency_symbol", "$")
        idx = self.cmb_currency.findText(saved_curr)
        if idx >= 0:
            self.cmb_currency.setCurrentIndex(idx)
        self.cmb_currency.currentTextChanged.connect(self._on_currency_changed)

        lbl_val = QLabel("Validez:")
        self.spn_validez = QSpinBox()
        self.spn_validez.setRange(1, 365)
        self.spn_validez.setValue(15)
        self.spn_validez.setSuffix(" días")

        layout.addWidget(lbl_cur, 0, 0)
        layout.addWidget(self.cmb_currency, 0, 1)
        layout.addWidget(lbl_val, 0, 2)
        layout.addWidget(self.spn_validez, 0, 3)

        # Fila 1: Descuento % e IVA / Impuesto
        lbl_disc = QLabel("Descuento (%):")
        self.spn_discount = QDoubleSpinBox()
        self.spn_discount.setRange(0.0, 100.0)
        self.spn_discount.setSingleStep(1.0)
        self.spn_discount.setSuffix(" %")
        saved_disc = self.config_service.get_preference("default_discount_rate", 0.0)
        self.spn_discount.setValue(saved_disc)
        self.spn_discount.valueChanged.connect(self._recalculate_all)

        self.chk_tax = QCheckBox("IVA / Impuesto:")
        saved_include_tax = self.config_service.get_preference("include_tax_by_default", True)
        self.chk_tax.setChecked(saved_include_tax)
        self.chk_tax.toggled.connect(self._on_tax_toggled)

        self.spn_tax = QDoubleSpinBox()
        self.spn_tax.setRange(0.0, 100.0)
        self.spn_tax.setSingleStep(0.5)
        self.spn_tax.setSuffix(" %")
        saved_tax = self.config_service.get_preference("default_tax_rate", 21.0)
        self.spn_tax.setValue(saved_tax)
        self.spn_tax.valueChanged.connect(self._recalculate_all)
        self.spn_tax.setEnabled(saved_include_tax)

        layout.addWidget(lbl_disc, 1, 0)
        layout.addWidget(self.spn_discount, 1, 1)
        layout.addWidget(self.chk_tax, 1, 2)
        layout.addWidget(self.spn_tax, 1, 3)

        return box

    def _create_summary_group(self) -> QGroupBox:
        """Crea la tarjeta compacta de totales calculados en 2 filas."""
        box = QGroupBox("Resumen de Totales")
        layout = QGridLayout(box)
        layout.setVerticalSpacing(4)
        layout.setHorizontalSpacing(10)
        layout.setContentsMargins(8, 8, 8, 6)

        # Fila 0: Subtotal y Descuento
        lbl_s_title = QLabel("Subtotal Ítems:")
        lbl_s_title.setObjectName("lblSubtotal")
        self.lbl_subtotal_val = QLabel("$ 0,00")
        self.lbl_subtotal_val.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.lbl_subtotal_val.setObjectName("lblSubtotal")

        lbl_d_title = QLabel("Descuento:")
        self.lbl_discount_val = QLabel("- $ 0,00")
        self.lbl_discount_val.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout.addWidget(lbl_s_title, 0, 0)
        layout.addWidget(self.lbl_subtotal_val, 0, 1)
        layout.addWidget(lbl_d_title, 0, 2)
        layout.addWidget(self.lbl_discount_val, 0, 3)

        # Fila 1: Impuesto y Total Final Destacado
        lbl_t_title = QLabel("IVA / Imp.:")
        self.lbl_tax_val = QLabel("+ $ 0,00")
        self.lbl_tax_val.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        lbl_tot_title = QLabel("TOTAL:")
        lbl_tot_title.setObjectName("lblTotalFinal")
        self.lbl_total_final = QLabel("$ 0,00")
        self.lbl_total_final.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.lbl_total_final.setObjectName("lblTotalFinal")

        layout.addWidget(lbl_t_title, 1, 0)
        layout.addWidget(self.lbl_tax_val, 1, 1)
        layout.addWidget(lbl_tot_title, 1, 2)
        layout.addWidget(self.lbl_total_final, 1, 3)

        return box

    def _create_actions_bar(self) -> QHBoxLayout:
        """Crea los botones de acción principal."""
        layout = QHBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(0, 4, 0, 4)

        btn_folder = QPushButton("📁 Carpeta de Salidas")
        btn_folder.setToolTip("Abre la carpeta donde se guardan los PDFs")
        btn_folder.clicked.connect(self._open_outputs_directory)

        btn_new = QPushButton("🔄 Nuevo Presupuesto")
        btn_new.setToolTip("Limpia los campos del cliente e ítems para iniciar otra cotización")
        btn_new.clicked.connect(self._reset_budget_form)

        btn_generate = QPushButton("📄 GENERAR PRESUPUESTO EN PDF")
        btn_generate.setObjectName("btnPrimary")
        btn_generate.setCursor(Qt.PointingHandCursor)
        btn_generate.clicked.connect(self._generate_pdf_budget)

        layout.addWidget(btn_folder)
        layout.addWidget(btn_new)
        layout.addStretch()
        layout.addWidget(btn_generate)

        return layout

    # =========================================================================
    # Lógica de Datos y Configuración
    # =========================================================================
    def _load_saved_professional_data(self):
        """Carga los datos guardados del profesional en los campos de entrada."""
        prof = self.config_service.get_profesional()
        self.txt_prof_nombre.setText(prof.nombre)
        self.txt_prof_apellido.setText(prof.apellido)
        self.txt_prof_tel.setText(prof.telefono)
        self.txt_prof_titulo.setText(prof.titulo_profesional)

    def _save_professional_data(self):
        """Persiste los datos actuales del profesional como predeterminados."""
        prof = Profesional(
            nombre=self.txt_prof_nombre.text().strip(),
            apellido=self.txt_prof_apellido.text().strip(),
            telefono=self.txt_prof_tel.text().strip(),
            titulo_profesional=self.txt_prof_titulo.text().strip() or "Servicios Profesionales",
        )
        if self.config_service.save_profesional(prof):
            self.config_service.set_preference("currency_symbol", self.cmb_currency.currentText())
            self.config_service.set_preference("default_tax_rate", self.spn_tax.value())
            self.config_service.set_preference("default_discount_rate", self.spn_discount.value())
            self.config_service.set_preference("include_tax_by_default", self.chk_tax.isChecked())

            QMessageBox.information(
                self,
                "Configuración Guardada",
                "Los datos del profesional y las preferencias fueron guardados correctamente y se usarán por defecto.",
            )
        else:
            QMessageBox.warning(self, "Error", "No se pudo guardar la configuración.")

    def _clear_client_fields(self):
        """Limpia los campos del formulario del cliente."""
        self.txt_cli_nombre.clear()
        self.txt_cli_apellido.clear()
        self.txt_cli_tel.clear()
        self.txt_cli_email.clear()
        self.txt_cli_nombre.setFocus()

    # =========================================================================
    # Lógica de la Tabla Dinámica de Ítems
    # =========================================================================
    def _add_initial_item(self):
        """Agrega una primera fila vacía para comodidad del usuario."""
        self._add_item_row(descripcion="Honorarios de desarrollo y consultoría", cantidad=1.0, precio=0.0)

    def _add_item_row(self, descripcion: str = "", cantidad: float = 1.0, precio: float = 0.0):
        """Inserta una fila interactiva en la tabla de ítems con widgets vinculados."""
        row_idx = self.table_items.rowCount()
        self.table_items.insertRow(row_idx)

        # 1. Descripción
        txt_desc = QLineEdit(descripcion)
        txt_desc.setPlaceholderText("Descripción del servicio o producto...")
        txt_desc.textChanged.connect(self._recalculate_all)
        self.table_items.setCellWidget(row_idx, 0, txt_desc)

        # 2. Cantidad (DoubleSpinBox)
        spn_qty = QDoubleSpinBox()
        spn_qty.setRange(0.01, 999999.0)
        spn_qty.setDecimals(2)
        spn_qty.setValue(cantidad)
        spn_qty.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        spn_qty.valueChanged.connect(self._recalculate_all)
        self.table_items.setCellWidget(row_idx, 1, spn_qty)

        # 3. Precio Unitario (DoubleSpinBox)
        spn_price = QDoubleSpinBox()
        spn_price.setRange(0.0, 999999999.0)
        spn_price.setDecimals(2)
        spn_price.setValue(precio)
        spn_price.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        spn_price.valueChanged.connect(self._recalculate_all)
        self.table_items.setCellWidget(row_idx, 2, spn_price)

        # 4. Subtotal (Item de celda de solo lectura, auto-calculado)
        item_sub = QTableWidgetItem("$ 0,00")
        item_sub.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        item_sub.setFlags(item_sub.flags() & ~Qt.ItemIsEditable)
        self.table_items.setItem(row_idx, 3, item_sub)

        self.table_items.selectRow(row_idx)
        self._recalculate_all()

    def _delete_selected_item(self):
        """Elimina la fila seleccionada de la tabla."""
        selected_rows = set(index.row() for index in self.table_items.selectedIndexes())
        if not selected_rows:
            current_row = self.table_items.currentRow()
            if current_row >= 0:
                selected_rows = {current_row}

        if not selected_rows:
            QMessageBox.information(self, "Atención", "Por favor, selecciona una fila para eliminar.")
            return

        for row in sorted(selected_rows, reverse=True):
            self.table_items.removeRow(row)

        self._recalculate_all()

    def _clear_all_items(self):
        """Elimina todas las filas de la tabla de ítems."""
        if self.table_items.rowCount() == 0:
            return
        reply = QMessageBox.question(
            self,
            "Confirmar",
            "¿Deseas vaciar todos los ítems presupuestados?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.table_items.setRowCount(0)
            self._recalculate_all()

    # =========================================================================
    # Cálculos Financieros Reactivos
    # =========================================================================
    def _on_tax_toggled(self, checked: bool):
        """Habilita o deshabilita el spinbox de porcentaje de impuesto."""
        self.spn_tax.setEnabled(checked)
        self._recalculate_all()

    def _on_currency_changed(self, _):
        """Actualiza los símbolos de moneda en pantalla cuando cambia el combo."""
        self._recalculate_all()

    def _get_items_from_table(self) -> List[ItemPresupuesto]:
        """Extrae la lista de ItemPresupuesto a partir de las filas de la tabla."""
        items = []
        sym = self.cmb_currency.currentText()

        for row in range(self.table_items.rowCount()):
            desc_widget = self.table_items.cellWidget(row, 0)
            qty_widget = self.table_items.cellWidget(row, 1)
            price_widget = self.table_items.cellWidget(row, 2)

            desc = desc_widget.text().strip() if isinstance(desc_widget, QLineEdit) else ""
            qty = qty_widget.value() if isinstance(qty_widget, QDoubleSpinBox) else 1.0
            price = price_widget.value() if isinstance(price_widget, QDoubleSpinBox) else 0.0

            item = ItemPresupuesto(descripcion=desc, cantidad=qty, precio_unitario=price)
            items.append(item)

            # Actualizar celda de subtotal de la fila
            sub_item = self.table_items.item(row, 3)
            if sub_item:
                sub_item.setText(format_currency(item.subtotal, sym))

        return items

    def _recalculate_all(self):
        """Recalcula todos los subtotales, descuentos, impuestos y el total definitivo."""
        items = self._get_items_from_table()
        sym = self.cmb_currency.currentText()

        subtotal_bruto = sum(item.subtotal for item in items)
        disc_rate = self.spn_discount.value()
        monto_descuento = subtotal_bruto * (min(disc_rate, 100.0) / 100.0)
        subtotal_neto = max(0.0, subtotal_bruto - monto_descuento)

        include_tax = self.chk_tax.isChecked()
        tax_rate = self.spn_tax.value() if include_tax else 0.0
        monto_impuesto = subtotal_neto * (tax_rate / 100.0)

        total_final = subtotal_neto + monto_impuesto

        # Actualizar etiquetas en pantalla
        self.lbl_subtotal_val.setText(format_currency(subtotal_bruto, sym))
        self.lbl_discount_val.setText(f"- {format_currency(monto_descuento, sym)}")
        self.lbl_tax_val.setText(f"+ {format_currency(monto_impuesto, sym)}")
        self.lbl_total_final.setText(format_currency(total_final, sym))

    # =========================================================================
    # Emisión de Presupuesto y Generación de PDF
    # =========================================================================
    def _build_presupuesto_model(self) -> Presupuesto:
        """Construye la entidad Presupuesto con los datos actuales de la interfaz."""
        cliente = Cliente(
            nombre=self.txt_cli_nombre.text().strip(),
            apellido=self.txt_cli_apellido.text().strip(),
            telefono=self.txt_cli_tel.text().strip(),
            email=self.txt_cli_email.text().strip(),
        )

        profesional = Profesional(
            nombre=self.txt_prof_nombre.text().strip(),
            apellido=self.txt_prof_apellido.text().strip(),
            telefono=self.txt_prof_tel.text().strip(),
            titulo_profesional=self.txt_prof_titulo.text().strip() or "Servicios Profesionales",
        )

        items = self._get_items_from_table()
        sym = self.cmb_currency.currentText()
        dias_validez = self.spn_validez.value()

        return Presupuesto(
            fecha_emision=date.today(),
            validez_dias=dias_validez,
            cliente=cliente,
            profesional=profesional,
            items=items,
            moneda_simbolo=sym,
            tasa_descuento=self.spn_discount.value(),
            tasa_impuesto=self.spn_tax.value(),
            aplicar_impuesto=self.chk_tax.isChecked(),
            notas=f"Presupuesto válido por {dias_validez} días a partir de su emisión.",
        )

    def _generate_pdf_budget(self):
        """Valida las entradas, emite el PDF y ofrece abrir el archivo o la carpeta."""
        cliente_nombre = self.txt_cli_nombre.text().strip()
        cliente_apellido = self.txt_cli_apellido.text().strip()
        if not cliente_nombre and not cliente_apellido:
            QMessageBox.warning(
                self,
                "Dato Requerido",
                "Por favor, ingresa al menos el Nombre o Apellido del Cliente antes de generar el presupuesto.",
            )
            self.txt_cli_nombre.setFocus()
            return

        items = self._get_items_from_table()
        if not items or len(items) == 0:
            QMessageBox.warning(
                self,
                "Sin Ítems",
                "Debes agregar al menos un ítem al presupuesto.",
            )
            return

        items_sin_desc = [idx + 1 for idx, it in enumerate(items) if not it.descripcion.strip()]
        if items_sin_desc:
            QMessageBox.warning(
                self,
                "Descripción Incompleta",
                f"El/los ítem(s) en la fila {items_sin_desc} no tienen descripción. Por favor completa el detalle.",
            )
            return

        try:
            presupuesto = self._build_presupuesto_model()
            pdf_path = self.pdf_service.generate(presupuesto)

            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("¡Presupuesto Generado con Éxito!")
            msg_box.setText(f"El presupuesto en PDF se ha generado correctamente:\n\n{Path(pdf_path).name}")
            msg_box.setIcon(QMessageBox.Information)

            btn_open_pdf = msg_box.addButton("Abrir PDF", QMessageBox.ActionRole)
            btn_open_folder = msg_box.addButton("Abrir Carpeta", QMessageBox.ActionRole)
            btn_ok = msg_box.addButton("Aceptar", QMessageBox.AcceptRole)

            msg_box.exec()

            if msg_box.clickedButton() == btn_open_pdf:
                self._open_file(pdf_path)
            elif msg_box.clickedButton() == btn_open_folder:
                self._open_outputs_directory()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error de Generación",
                f"Ocurrió un inconveniente al generar el archivo PDF:\n{str(e)}",
            )

    def _open_file(self, file_path: str):
        """Abre un archivo con la aplicación predeterminada del sistema operativo."""
        try:
            if sys.platform == "win32":
                os.startfile(file_path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", file_path])
            else:
                subprocess.Popen(["xdg-open", file_path])
        except Exception as e:
            QMessageBox.warning(self, "Aviso", f"No se pudo abrir el archivo automáticamente: {e}")

    def _open_outputs_directory(self):
        """Abre la carpeta de outputs en el explorador de archivos."""
        out_dir = get_outputs_dir()
        try:
            if sys.platform == "win32":
                os.startfile(str(out_dir))
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(out_dir)])
            else:
                subprocess.Popen(["xdg-open", str(out_dir)])
        except Exception as e:
            QMessageBox.warning(self, "Aviso", f"No se pudo abrir la carpeta: {e}")

    def _reset_budget_form(self):
        """Limpia el presupuesto actual para iniciar uno nuevo manteniendo al profesional."""
        reply = QMessageBox.question(
            self,
            "Nuevo Presupuesto",
            "¿Deseas iniciar un nuevo presupuesto? Se limpiarán los datos del cliente y los ítems cargados.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self._clear_client_fields()
            self.table_items.setRowCount(0)
            self._add_initial_item()
            self._recalculate_all()
