"""
Servicio de generación de presupuestos en PDF de alta calidad con ReportLab.
Diseño minimalista, moderno, limpio y profesional.
"""
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
    HRFlowable,
)
from reportlab.pdfgen import canvas

from ..models.presupuesto import Presupuesto
from ..utils.paths import get_outputs_dir
from ..utils.formatters import format_currency, format_percent, format_date


class NumberedCanvas(canvas.Canvas):
    """Canvas de dos pasadas para calcular y dibujar el número total de páginas y pie de página."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count: int):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Línea de pie de página
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(40, 35, A4[0] - 40, 35)

        # Texto de pie de página
        footer_text = f"FeeReport Lite • Documento emitido electrónicamente • Página {self._pageNumber} de {page_count}"
        self.drawString(40, 23, footer_text)
        self.restoreState()


class PDFGeneratorService:
    """Motor de generación de presupuestos formales en PDF."""

    def __init__(self, outputs_dir: Optional[Path] = None):
        self.outputs_dir = outputs_dir or get_outputs_dir()
        self.outputs_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, presupuesto: Presupuesto) -> str:
        """
        Compila el presupuesto a PDF y retorna la ruta absoluta del archivo generado.
        """
        # Sanitizar nombre de archivo
        cliente_clean = re.sub(r"[^\w\s-]", "", presupuesto.cliente.nombre_completo).strip()
        cliente_clean = re.sub(r"[-\s]+", "_", cliente_clean) or "Cliente"
        num_clean = re.sub(r"[^\w-]", "", presupuesto.numero)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Presupuesto_{num_clean}_{cliente_clean}_{timestamp}.pdf"
        output_path = self.outputs_dir / filename

        # Configuración del documento A4 con márgenes de 40 pt (1.4 cm)
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=A4,
            leftMargin=40,
            rightMargin=40,
            topMargin=40,
            bottomMargin=48,
        )

        styles = getSampleStyleSheet()

        # Paleta de colores minimalista
        c_primary = colors.HexColor("#0F172A")       # Slate 900
        c_secondary = colors.HexColor("#1E293B")     # Slate 800
        c_accent = colors.HexColor("#0284C7")        # Blue 600
        c_text = colors.HexColor("#334155")          # Slate 700
        c_muted = colors.HexColor("#64748B")         # Slate 500
        c_border = colors.HexColor("#E2E8F0")        # Slate 200
        c_bg_subtle = colors.HexColor("#F8FAFC")     # Slate 50
        c_bg_header = colors.HexColor("#0F172A")     # Encabezado tabla

        # Estilos tipográficos
        style_title = ParagraphStyle(
            "DocTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            textColor=c_primary,
        )
        style_subtitle = ParagraphStyle(
            "DocSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=13,
            textColor=c_muted,
        )
        style_meta_label = ParagraphStyle(
            "MetaLabel",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=12,
            textColor=c_muted,
            alignment=2,  # Derecha
        )
        style_meta_val = ParagraphStyle(
            "MetaVal",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=c_primary,
            alignment=2,  # Derecha
        )

        style_card_title = ParagraphStyle(
            "CardTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=12,
            textColor=c_accent,
            spaceAfter=4,
        )
        style_card_name = ParagraphStyle(
            "CardName",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=c_primary,
        )
        style_card_text = ParagraphStyle(
            "CardText",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=c_text,
        )

        style_th = ParagraphStyle(
            "TableHead",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=12,
            textColor=colors.white,
        )
        style_td = ParagraphStyle(
            "TableCell",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=c_text,
        )
        style_td_num = ParagraphStyle(
            "TableCellNum",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=c_text,
            alignment=2,
        )
        style_td_bold_num = ParagraphStyle(
            "TableCellBoldNum",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=12,
            textColor=c_primary,
            alignment=2,
        )

        story = []

        # ==========================================
        # 1. ENCABEZADO SUPERIOR (Título y Metadatos)
        # ==========================================
        header_left = [
            Paragraph("PRESUPUESTO", style_title),
            Paragraph(presupuesto.profesional.titulo_profesional or "Cotización de Servicios", style_subtitle),
        ]

        header_right = [
            Paragraph(f"<b>N° Presupuesto:</b> {presupuesto.numero}", style_meta_val),
            Paragraph(f"<b>Fecha de Emisión:</b> {format_date(presupuesto.fecha_emision)}", style_meta_val),
            Paragraph(f"<b>Validez:</b> {presupuesto.validez_dias} días corridos", style_meta_val),
        ]

        header_table = Table(
            [[header_left, header_right]],
            colWidths=[315, 200],
        )
        header_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 14))

        # Línea divisoria moderna
        story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceAfter=14))

        # ==========================================
        # 2. BLOQUE DE PARTES (Profesional y Cliente)
        # ==========================================
        # Bloque Profesional
        prof_info = [
            Paragraph("EMITIDO POR (PROFESIONAL)", style_card_title),
            Paragraph(presupuesto.profesional.nombre_completo, style_card_name),
        ]
        if presupuesto.profesional.telefono:
            prof_info.append(Paragraph(f"<b>Teléfono:</b> {presupuesto.profesional.telefono}", style_card_text))
        if presupuesto.profesional.email:
            prof_info.append(Paragraph(f"<b>Email:</b> {presupuesto.profesional.email}", style_card_text))

        # Bloque Cliente
        client_info = [
            Paragraph("PRESUPUESTADO PARA (CLIENTE)", style_card_title),
            Paragraph(presupuesto.cliente.nombre_completo, style_card_name),
        ]
        if presupuesto.cliente.telefono:
            client_info.append(Paragraph(f"<b>Teléfono:</b> {presupuesto.cliente.telefono}", style_card_text))
        if presupuesto.cliente.email:
            client_info.append(Paragraph(f"<b>Email:</b> {presupuesto.cliente.email}", style_card_text))

        parties_table = Table(
            [[prof_info, client_info]],
            colWidths=[250, 250],
        )
        parties_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BACKGROUND", (0, 0), (0, 0), c_bg_subtle),
            ("BACKGROUND", (1, 0), (1, 0), c_bg_subtle),
            ("BOX", (0, 0), (0, 0), 0.75, c_border),
            ("BOX", (1, 0), (1, 0), 0.75, c_border),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ]))
        story.append(parties_table)
        story.append(Spacer(1, 18))

        # ==========================================
        # 3. TABLA DE CONCEPTOS / ÍTEMS
        # ==========================================
        table_headers = [
            Paragraph("#", ParagraphStyle("TH0", parent=style_th, alignment=1)),
            Paragraph("Descripción del Concepto / Servicio", style_th),
            Paragraph("Cant.", ParagraphStyle("TH2", parent=style_th, alignment=2)),
            Paragraph("Precio Unit.", ParagraphStyle("TH3", parent=style_th, alignment=2)),
            Paragraph("Subtotal", ParagraphStyle("TH4", parent=style_th, alignment=2)),
        ]

        items_data = [table_headers]
        sym = presupuesto.moneda_simbolo

        for idx, item in enumerate(presupuesto.items, start=1):
            cant_str = f"{item.cantidad:g}"
            unit_str = format_currency(item.precio_unitario, sym)
            sub_str = format_currency(item.subtotal, sym)

            row = [
                Paragraph(str(idx), ParagraphStyle("TDi", parent=style_td, alignment=1)),
                Paragraph(item.descripcion, style_td),
                Paragraph(cant_str, style_td_num),
                Paragraph(unit_str, style_td_num),
                Paragraph(sub_str, style_td_bold_num),
            ]
            items_data.append(row)

        # Anchos de columnas (total = 515 pt)
        col_widths = [28, 257, 50, 90, 90]
        items_table = Table(items_data, colWidths=col_widths, repeatRows=1)

        t_style = [
            ("BACKGROUND", (0, 0), (-1, 0), c_bg_header),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("GRID", (0, 0), (-1, -1), 0.5, c_border),
        ]

        # Alternar color de fondo para filas de datos
        for r_idx in range(1, len(items_data)):
            bg = colors.white if r_idx % 2 != 0 else c_bg_subtle
            t_style.append(("BACKGROUND", (0, r_idx), (-1, r_idx), bg))

        items_table.setStyle(TableStyle(t_style))
        story.append(items_table)
        story.append(Spacer(1, 14))

        # ==========================================
        # 4. RESUMEN DE TOTALES Y CONDICIONES
        # ==========================================
        subtotal_bruto = presupuesto.calcular_subtotal_bruto()
        descuento = presupuesto.calcular_monto_descuento()
        subtotal_neto = presupuesto.calcular_subtotal_neto()
        impuesto = presupuesto.calcular_monto_impuesto()
        total_final = presupuesto.calcular_total()

        # Filas del bloque resumen
        summary_rows = [
            [
                Paragraph("<b>Subtotal Ítems:</b>", style_meta_label),
                Paragraph(format_currency(subtotal_bruto, sym), style_td_bold_num),
            ]
        ]

        if presupuesto.tasa_descuento > 0:
            summary_rows.append([
                Paragraph(f"Descuento ({format_percent(presupuesto.tasa_descuento)}):", style_meta_label),
                Paragraph(f"- {format_currency(descuento, sym)}", style_td_num),
            ])
            summary_rows.append([
                Paragraph("Subtotal Neto:", style_meta_label),
                Paragraph(format_currency(subtotal_neto, sym), style_td_bold_num),
            ])

        if presupuesto.aplicar_impuesto and presupuesto.tasa_impuesto > 0:
            summary_rows.append([
                Paragraph(f"Impuestos / IVA ({format_percent(presupuesto.tasa_impuesto)}):", style_meta_label),
                Paragraph(format_currency(impuesto, sym), style_td_num),
            ])

        # Fila TOTAL FINAL destacada
        style_total_label = ParagraphStyle(
            "TotLabel",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=colors.white,
            alignment=2,
        )
        style_total_val = ParagraphStyle(
            "TotVal",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=colors.white,
            alignment=2,
        )

        summary_rows.append([
            Paragraph("TOTAL FINAL:", style_total_label),
            Paragraph(format_currency(total_final, sym), style_total_val),
        ])

        summary_table = Table(summary_rows, colWidths=[120, 110])
        summary_style = [
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("LINEBELOW", (0, 0), (-1, -2), 0.5, c_border),
            # Fondo especial para la última fila (TOTAL FINAL)
            ("BACKGROUND", (0, -1), (-1, -1), c_primary),
            ("TOPPADDING", (0, -1), (-1, -1), 6),
            ("BOTTOMPADDING", (0, -1), (-1, -1), 6),
        ]
        summary_table.setStyle(TableStyle(summary_style))

        # Bloque de notas / términos a la izquierda del resumen
        notes_content = [
            Paragraph("<b>Términos y Condiciones:</b>", style_card_title),
            Paragraph(presupuesto.notas or "Presupuesto válido por 15 días hábiles.", style_card_text),
        ]
        notes_table = Table([[notes_content]], colWidths=[265])
        notes_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), c_bg_subtle),
            ("BOX", (0, 0), (-1, -1), 0.75, c_border),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ]))

        bottom_composite = Table(
            [[notes_table, summary_table]],
            colWidths=[275, 240],
        )
        bottom_composite.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))

        story.append(KeepTogether(bottom_composite))

        # Construcción del PDF
        doc.build(story, canvasmaker=NumberedCanvas)
        return str(output_path)
