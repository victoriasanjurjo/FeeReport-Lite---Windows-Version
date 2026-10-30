"""
Punto de entrada principal para FeeReport Lite.
Inicializa el entorno de escritorio Qt con PySide6 y lanza la ventana principal.
"""
import sys
import os
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from src.ui.main_window import MainWindow
from src.ui.styles import APP_STYLESHEET
from src.utils.paths import get_app_icon_path


def main():
    """Inicializa y ejecuta la aplicación de escritorio FeeReport Lite."""
    # Configuración de renderizado de alta densidad (High DPI)
    if hasattr(Qt, "AA_EnableHighDpiScaling"):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, "AA_UseHighDpiPixmaps"):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("FeeReport Lite")
    app.setOrganizationName("FeeReport")

    # Ícono global de la aplicación
    icon_path = get_app_icon_path()
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    # Aplicar estilos modernos
    app.setStyleSheet(APP_STYLESHEET)

    # Crear y mostrar la ventana principal
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
