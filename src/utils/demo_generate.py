"""
Script para generar un PDF de presupuesto de demostración en outputs/.
"""
from src.models.cliente import Cliente
from src.models.profesional import Profesional
from src.models.presupuesto import ItemPresupuesto, Presupuesto
from src.services.pdf_generator import PDFGeneratorService

def main():
    cliente = Cliente(
        nombre="Martín",
        apellido="González",
        telefono="+54 9 11 4433-2211",
        email="martin.gonzalez@empresa.com"
    )
    profesional = Profesional(
        nombre="Alejandro",
        apellido="Valenzuela",
        telefono="+54 9 11 9988-7766",
        email="alejandro@techsolutions.io",
        titulo_profesional="Consultor en Arquitectura de Software"
    )
    presupuesto = Presupuesto(
        numero="PRE-2026-0001",
        validez_dias=15,
        cliente=cliente,
        profesional=profesional,
        items=[
            ItemPresupuesto("Desarrollo de Módulo de Facturación y Presupuestos", 1.0, 350000.0),
            ItemPresupuesto("Integración de Motor de Reportes PDF Automatizados", 1.0, 180000.0),
            ItemPresupuesto("Horas de Capacitación y Puesta en Producción", 8.0, 15000.0),
            ItemPresupuesto("Soporte Técnico y Mantenimiento Evolutivo (1 Mes)", 1.0, 95000.0),
        ],
        moneda_simbolo="$",
        tasa_descuento=5.0,
        tasa_impuesto=21.0,
        aplicar_impuesto=True,
        notas="Presupuesto válido por 15 días corridos. Los pagos se efectuarán según hitos acordados. No incluye costos de infraestructura en la nube."
    )

    pdf_service = PDFGeneratorService()
    pdf_path = pdf_service.generate(presupuesto)
    print(f"Demostración generada exitosamente en:\n{pdf_path}")

if __name__ == "__main__":
    main()
