"""
Pruebas de integración para la generación de PDFs con ReportLab.
"""
from pathlib import Path
from src.models.cliente import Cliente
from src.models.profesional import Profesional
from src.models.presupuesto import ItemPresupuesto, Presupuesto
from src.services.pdf_generator import PDFGeneratorService


def test_generacion_pdf_presupuesto(tmp_path):
    cliente = Cliente(
        nombre="Laura",
        apellido="Martínez",
        telefono="+54 9 11 5555-4444",
        email="laura@empresa.com",
    )
    profesional = Profesional(
        nombre="Martín",
        apellido="Rossi",
        telefono="+54 9 11 2222-3333",
        email="martin@freelance.io",
        titulo_profesional="Arquitecto de Soluciones",
    )
    presupuesto = Presupuesto(
        numero="PRE-TEST-001",
        validez_dias=10,
        cliente=cliente,
        profesional=profesional,
        items=[
            ItemPresupuesto("Auditoría de Sistemas", 1.0, 150000.0),
            ItemPresupuesto("Optimización de Base de Datos", 2.0, 80000.0),
        ],
        moneda_simbolo="$",
        tasa_descuento=5.0,
        tasa_impuesto=21.0,
        aplicar_impuesto=True,
    )

    pdf_service = PDFGeneratorService(outputs_dir=tmp_path)
    output_file = pdf_service.generate(presupuesto)

    file_path = Path(output_file)
    assert file_path.exists()
    assert file_path.is_file()
    assert file_path.stat().st_size > 1000  # Archivo PDF válido con contenido

    # Verificar firma de cabecera PDF (%PDF-)
    with open(file_path, "rb") as f:
        header = f.read(5)
        assert header == b"%PDF-"
