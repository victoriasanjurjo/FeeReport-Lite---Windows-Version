"""
Estilos visuales modernos, compactos y profesionales para FeeReport Lite (PySide6 / QSS).
Paleta clara, neutra y balanceada con tipografía de alto contraste y espaciado optimizado.
"""

APP_STYLESHEET = """
/* ==========================================================================
   Configuración Global
   ========================================================================== */
QWidget {
    background-color: #F8FAFC;
    color: #1E293B;
    font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, "Roboto", sans-serif;
    font-size: 12px;
}

/* ==========================================================================
   Contenedores y Tarjetas (Cards Compactas)
   ========================================================================== */
QGroupBox {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    margin-top: 10px;
    padding-top: 12px;
    padding-bottom: 6px;
    padding-left: 10px;
    padding-right: 10px;
    font-weight: 600;
    font-size: 12px;
    color: #0F172A;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    padding: 0 4px;
    background-color: #FFFFFF;
    color: #1E293B;
}

/* ==========================================================================
   Campos de Texto y Entradas Compactos
   ========================================================================== */
QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 4px;
    padding: 4px 8px;
    color: #0F172A;
    font-size: 12px;
    selection-background-color: #2563EB;
    selection-color: #FFFFFF;
    min-height: 22px;
}

QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
    border: 1.5px solid #2563EB;
    background-color: #FFFFFF;
}

QLineEdit:disabled, QSpinBox:disabled, QDoubleSpinBox:disabled, QComboBox:disabled {
    background-color: #F1F5F9;
    color: #94A3B8;
    border-color: #E2E8F0;
}

/* ==========================================================================
   Botones
   ========================================================================== */
QPushButton {
    background-color: #F1F5F9;
    color: #334155;
    border: 1px solid #CBD5E1;
    border-radius: 5px;
    padding: 5px 12px;
    font-weight: 600;
    font-size: 12px;
}

QPushButton:hover {
    background-color: #E2E8F0;
    color: #0F172A;
    border-color: #94A3B8;
}

QPushButton:pressed {
    background-color: #CBD5E1;
}

/* Botón de Acción Principal (Primario) */
QPushButton#btnPrimary {
    background-color: #0F172A;
    color: #FFFFFF;
    border: 1px solid #0F172A;
    font-size: 13px;
    font-weight: bold;
    padding: 8px 18px;
}

QPushButton#btnPrimary:hover {
    background-color: #1E293B;
    border-color: #1E293B;
}

QPushButton#btnPrimary:pressed {
    background-color: #334155;
}

/* Botón de Éxito / Agregar Ítem */
QPushButton#btnSuccess {
    background-color: #059669;
    color: #FFFFFF;
    border: 1px solid #047857;
    font-size: 12px;
    padding: 5px 12px;
}

QPushButton#btnSuccess:hover {
    background-color: #047857;
}

/* Botón de Peligro / Eliminar */
QPushButton#btnDanger {
    background-color: #FEE2E2;
    color: #DC2626;
    border: 1px solid #FECACA;
    padding: 5px 12px;
}

QPushButton#btnDanger:hover {
    background-color: #FCA5A5;
    color: #991B1B;
}

/* Botón discreto / secundario de tarjeta */
QPushButton#btnSubtle {
    background-color: transparent;
    color: #2563EB;
    border: 1px dashed #93C5FD;
    padding: 3px 8px;
    font-size: 11px;
}

QPushButton#btnSubtle:hover {
    background-color: #EFF6FF;
    border-color: #3B82F6;
}

/* ==========================================================================
   Tabla de Ítems (Visualmente Destacada y con Altura Amplia)
   ========================================================================== */
QTableWidget {
    background-color: #FFFFFF;
    alternate-background-color: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    gridline-color: #E2E8F0;
    selection-background-color: #EFF6FF;
    selection-color: #1E40AF;
}

QHeaderView::section {
    background-color: #0F172A;
    color: #FFFFFF;
    font-weight: 600;
    font-size: 12px;
    padding: 6px 8px;
    border: none;
    border-right: 1px solid #334155;
}

QHeaderView::section:last {
    border-right: none;
}

/* ==========================================================================
   Etiquetas y Resumen
   ========================================================================== */
QLabel {
    color: #475569;
}

QLabel#lblFieldTitle {
    font-size: 11px;
    font-weight: 600;
    color: #64748B;
}

QLabel#lblTotalFinal {
    font-size: 20px;
    font-weight: 800;
    color: #0F172A;
}

QLabel#lblSubtotal {
    font-size: 13px;
    font-weight: 600;
    color: #334155;
}

/* ==========================================================================
   Scroll Area y Barras de Scroll
   ========================================================================== */
QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollBar:vertical {
    border: none;
    background-color: #F1F5F9;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #CBD5E1;
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #94A3B8;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""
