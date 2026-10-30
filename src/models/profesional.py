"""
Modelo de datos para el Profesional / Emisor del presupuesto.
"""
from dataclasses import dataclass


@dataclass
class Profesional:
    """Representa al profesional o prestador de servicios que emite el presupuesto."""
    nombre: str = ""
    apellido: str = ""
    telefono: str = ""
    email: str = ""
    titulo_profesional: str = "Servicios Profesionales"

    @property
    def nombre_completo(self) -> str:
        """Devuelve el nombre y apellido combinados de forma limpia."""
        partes = [p.strip() for p in (self.nombre, self.apellido) if p and p.strip()]
        return " ".join(partes) if partes else "Profesional no especificado"

    def to_dict(self) -> dict:
        """Serializa a diccionario para almacenamiento de configuración."""
        return {
            "nombre": self.nombre,
            "apellido": self.apellido,
            "telefono": self.telefono,
            "email": self.email,
            "titulo_profesional": self.titulo_profesional,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Profesional":
        """Instancia un Profesional a partir de un diccionario."""
        return cls(
            nombre=data.get("nombre", ""),
            apellido=data.get("apellido", ""),
            telefono=data.get("telefono", ""),
            email=data.get("email", ""),
            titulo_profesional=data.get("titulo_profesional", "Servicios Profesionales"),
        )
