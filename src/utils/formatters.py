"""
Módulo de formateo de números, monedas y fechas para interfaz y reportes PDF.
"""
from datetime import datetime, date
from typing import Union


def format_currency(amount: float, symbol: str = "$") -> str:
    """
    Formatea un monto numérico con separador de miles y dos decimales.
    Ejemplo: 12500.50 -> "$ 12.500,50"
    """
    try:
        val = float(amount)
    except (ValueError, TypeError):
        val = 0.0

    # Formato con coma para decimales y punto para miles
    formatted_num = f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{symbol} {formatted_num}"


def format_percent(val: float) -> str:
    """Formatea un porcentaje numérico. Ejemplo: 21.0 -> '21%' o '21.5%'."""
    try:
        v = float(val)
        if v.is_integer():
            return f"{int(v)}%"
        return f"{v:.1f}%"
    except (ValueError, TypeError):
        return "0%"


def format_date(dt: Union[date, datetime, str, None] = None) -> str:
    """Retorna una fecha en formato legible DD/MM/AAAA."""
    if dt is None:
        return datetime.now().strftime("%d/%m/%Y")
    if isinstance(dt, (date, datetime)):
        return dt.strftime("%d/%m/%Y")
    return str(dt)
