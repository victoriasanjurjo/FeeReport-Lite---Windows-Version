"""
Modelos de datos para Ítems y Presupuesto global con cálculo financiero reactivo.
"""
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Optional
import uuid

from .cliente import Cliente
from .profesional import Profesional


@dataclass
class ItemPresupuesto:
    """Representa una línea o ítem presupuestado."""
    descripcion: str
    cantidad: float = 1.0
    precio_unitario: float = 0.0

    @property
    def subtotal(self) -> float:
        """Cálculo automático de la línea: cantidad * precio_unitario."""
        return max(0.0, float(self.cantidad) * float(self.precio_unitario))

    def es_valido(self) -> bool:
        """Verifica que el ítem tenga descripción y valores numéricos válidos."""
        return bool(self.descripcion.strip()) and self.cantidad > 0 and self.precio_unitario >= 0


@dataclass
class Presupuesto:
    """Modelo maestro que agrupa cliente, profesional, ítems y parámetros de facturación."""
    numero: str = field(default_factory=lambda: f"PRE-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:4].upper()}")
    fecha_emision: date = field(default_factory=date.today)
    validez_dias: int = 15
    cliente: Cliente = field(default_factory=Cliente)
    profesional: Profesional = field(default_factory=Profesional)
    items: List[ItemPresupuesto] = field(default_factory=list)
    moneda_simbolo: str = "$"
    moneda_codigo: str = "ARS"
    tasa_descuento: float = 0.0  # Porcentaje (0 a 100)
    tasa_impuesto: float = 21.0  # Porcentaje (ej. IVA 21%)
    aplicar_impuesto: bool = True
    notas: str = "Presupuesto válido por 15 días hábiles. Precios sujetos a modificación sin previo aviso."

    def calcular_subtotal_bruto(self) -> float:
        """Suma de los subtotales de todos los ítems."""
        return sum(item.subtotal for item in self.items)

    def calcular_monto_descuento(self) -> float:
        """Monto deducido en base a la tasa de descuento porcentual."""
        if self.tasa_descuento <= 0:
            return 0.0
        return self.calcular_subtotal_bruto() * (min(self.tasa_descuento, 100.0) / 100.0)

    def calcular_subtotal_neto(self) -> float:
        """Subtotal tras aplicar descuento."""
        return max(0.0, self.calcular_subtotal_bruto() - self.calcular_monto_descuento())

    def calcular_monto_impuesto(self) -> float:
        """Monto de impuesto/IVA calculado sobre el subtotal neto si está habilitado."""
        if not self.aplicar_impuesto or self.tasa_impuesto <= 0:
            return 0.0
        return self.calcular_subtotal_neto() * (self.tasa_impuesto / 100.0)

    def calcular_total(self) -> float:
        """Total definitivo a abonar por el cliente."""
        return self.calcular_subtotal_neto() + self.calcular_monto_impuesto()

    def total_items_count(self) -> int:
        """Cantidad de conceptos en el presupuesto."""
        return len(self.items)
