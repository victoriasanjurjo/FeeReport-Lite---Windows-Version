"""
Servicio de persistencia de configuración del usuario y perfil del profesional.
"""
import json
import logging
from pathlib import Path
from typing import Dict, Any

from ..utils.paths import get_config_dir
from ..models.profesional import Profesional

logger = logging.getLogger(__name__)


class ConfigService:
    """Gestiona la carga y persistencia de configuraciones en JSON."""

    def __init__(self):
        self.config_dir = get_config_dir()
        self.settings_file = self.config_dir / "settings.json"
        self.default_file = self.config_dir / "default_settings.json"
        self._data: Dict[str, Any] = self._load()

    def _load(self) -> Dict[str, Any]:
        """Carga la configuración desde settings.json con fallback a default_settings.json."""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error al leer {self.settings_file}: {e}")

        if self.default_file.exists():
            try:
                with open(self.default_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error al leer default_settings.json: {e}")

        # Configuración de respaldo mínima en memoria
        return {
            "professional": {
                "nombre": "",
                "apellido": "",
                "telefono": "",
                "email": "",
                "titulo_profesional": "Servicios Profesionales",
            },
            "preferences": {
                "currency_symbol": "$",
                "currency_code": "ARS",
                "default_tax_rate": 21.0,
                "default_discount_rate": 0.0,
                "include_tax_by_default": True,
                "pdf_footer_note": "Presupuesto válido por 15 días hábiles a partir de la fecha de emisión.",
            },
        }

    def save(self) -> bool:
        """Guarda la configuración actual en settings.json."""
        try:
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Error al guardar {self.settings_file}: {e}")
            return False

    def get_profesional(self) -> Profesional:
        """Recupera los datos predeterminados del profesional."""
        prof_data = self._data.get("professional", {})
        return Profesional.from_dict(prof_data)

    def save_profesional(self, profesional: Profesional) -> bool:
        """Actualiza y persiste los datos predeterminados del profesional."""
        self._data["professional"] = profesional.to_dict()
        return self.save()

    def get_preference(self, key: str, default: Any = None) -> Any:
        """Obtiene una preferencia específica."""
        return self._data.get("preferences", {}).get(key, default)

    def set_preference(self, key: str, value: Any) -> bool:
        """Establece y persiste una preferencia específica."""
        if "preferences" not in self._data:
            self._data["preferences"] = {}
        self._data["preferences"][key] = value
        return self.save()
