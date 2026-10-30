"""
Módulo de gestión de rutas centralizadas para FeeReport Lite.
Garantiza compatibilidad tanto en modo desarrollo como empaquetado con PyInstaller.
"""
import sys
import os
from pathlib import Path


def get_base_dir() -> Path:
    """
    Retorna la ruta raíz de la aplicación.
    Si se ejecuta como binario congelado (PyInstaller), usa sys._MEIPASS
    o el directorio del ejecutable según corresponda.
    """
    if getattr(sys, "frozen", False):
        # Modo ejecutable empaquetado
        return Path(sys.executable).resolve().parent
    # Modo script desarrollo: raíz es dos niveles arriba de src/utils
    return Path(__file__).resolve().parent.parent.parent


def get_bundle_dir() -> Path:
    """
    Retorna la ruta interna de recursos de PyInstaller (sys._MEIPASS) o el base_dir.
    """
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return get_base_dir()


def get_assets_dir() -> Path:
    """Retorna la ruta absoluta al directorio de assets."""
    bundle_assets = get_bundle_dir() / "assets"
    if bundle_assets.exists():
        return bundle_assets
    return get_base_dir() / "assets"


def get_config_dir() -> Path:
    """Retorna la ruta absoluta al directorio de configuración."""
    config_dir = get_base_dir() / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_outputs_dir() -> Path:
    """Retorna la ruta absoluta al directorio de salidas (PDFs generados)."""
    outputs_dir = get_base_dir() / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    return outputs_dir


def get_app_icon_path() -> Path:
    """Retorna la ruta preferida del ícono de la aplicación (.ico en Windows, fallback a .png)."""
    assets = get_assets_dir()
    ico = assets / "app_icon.ico"
    if ico.exists():
        return ico
    return assets / "app_icon.png"
