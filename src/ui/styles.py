"""
Estilos visuales modernos y profesionales para FeeReport Lite (PySide6 / QSS).
Paleta clara, neutra y balanceada con tipografía de alto contraste y buen espaciado.
"""

APP_STYLESHEET = """
/* ==========================================================================
   Configuración Global
   ========================================================================== */
QWidget {
    background-color: #F8FAFC;
    color: #1E293B;
    font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, "Roboto", sans-serif;
    font-size: 13px;
}

/* ==========================================================================
   Contenedores y Tarjetas (Cards)
   ========================================================================== */
QGroupBox {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    margin-top: 14px;
    padding-top: 18px;
    padding-bottom: 12px;
    padding-left: 12px;
    padding-right: 12px;
    font-weight: 600;
    color: #0F172A;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 14px;
    padding: 0 6px;
    background-color: #FFFFFF;
    color: #1E293B;
}

/* ==========================================================================
   Campos de Texto y Entradas
   ========================================================================== */
QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 7px 10px;
    color: #0F172A;
    selection-background-color: #2563EB;
    selection-color: #FFFFFF;
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
    border-radius: 6px;
    padding: 8px 14px;
    font-weight: 600;
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
    font-size: 14px;
    padding: 10px 20px;
}

QPushButton#btnPrimary:hover {
    background-color: #1E293B;
    border-color: #1E293B;
}

QPushButton#btnPrimary:pressed {
    background-color: #334155;
}

/* Botón de Éxito / Acción Destacada */
QPushButton#btnSuccess {
    background-color: #059669;
    color: #FFFFFF;
    border: 1px solid #047857;
    font-size: 13px;
    padding: 8px 14px;
}

QPushButton#btnSuccess:hover {
    background-color: #047857;
}

/* Botón de Peligro / Eliminar */
QPushButton#btnDanger {
    background-color: #FEE2E2;
    color: #DC2626;
    border: 1px solid #FECACA;
}

QPushButton#btnDanger:hover {
    background-color: #FCA5A5;
    color: #991B1B;
}

/* ==========================================================================
   Tabla de Ítems
   ========================================================================== */
QTableWidget {
    background-color: #FFFFFF;
    alternate-background-color: #F8FAFC;
    border: 1px solid #E2E8F0;
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
    padding: 8px 6px;
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
    text-transform: uppercase;
}

QLabel#lblTotalFinal {
    font-size: 22px;
    font-weight: 800;
    color: #0F172A;
}

QLabel#lblSubtotal {
    font-size: 14px;
    font-weight: 600;
    color: #334155;
}

/* ==========================================================================
   Barras de Scroll
   ========================================================================== */
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
