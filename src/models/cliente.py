"""
Modelo de datos para el Cliente / Receptor del presupuesto.
"""
from dataclasses import dataclass


@dataclass
class Cliente:
    """Representa a la persona física o jurídica que recibe el presupuesto."""
    nombre: str = ""
    apellido: str = ""
    telefono: str = ""
    email: str = ""

    @property
    def nombre_completo(self) -> str:
        """Devuelve el nombre y apellido combinados de forma limpia."""
        partes = [p.strip() for p in (self.nombre, self.apellido) if p and p.strip()]
        return " ".join(partes) if partes else "Cliente no especificado"

    def es_valido(self) -> bool:
        """Verifica que al menos se haya especificado el nombre o apellido del cliente."""
        return bool(self.nombre.strip() or self.apellido.strip())
