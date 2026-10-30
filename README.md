# FeeReport Lite • Generador de Presupuestos para Windows

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE.txt)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![GUI: PySide6](https://img.shields.io/badge/GUI-PySide6%20%28Qt%206%29-informational.svg)](https://wiki.qt.io/Qt_for_Python)
[![PDF: ReportLab](https://img.shields.io/badge/PDF-ReportLab%20Platypus-orange.svg)](https://www.reportlab.com/)

**FeeReport Lite** es una aplicación de escritorio moderna, ágil y profesional diseñada para profesionales independientes, freelancers, consultores y prestadores de servicios que necesitan confeccionar y emitir cotizaciones y presupuestos en PDF con una presentación minimalista, clara y formal en cuestión de segundos.

---

## 🌟 Características Principales

- **Formulario Simple y Directo**:
  - **Datos del Cliente**: Nombre, apellido, teléfono y correo electrónico.
  - **Datos del Profesional**: Nombre, apellido, teléfono y especialidad/título.
  - **Guardado Automático de Perfil**: Posibilidad de almacenar los datos del emisor como predeterminados para no reescribirlos en cada cotización.
- **Tabla Dinámica de Ítems**:
  - Adición, edición en línea y eliminación fluida de conceptos.
  - Control de cantidad y precio unitario con soporte de decimales.
  - Subtotal automático por ítem en tiempo real.
- **Motor Financiero Reactivo**:
  - Moneda configurable (`$`, `USD $`, `ARS $`, `EUR €`, `CLP $`, etc.).
  - Descuentos porcentuales con impacto inmediato en el subtotal neto.
  - Cálculo opcional de Impuestos / IVA con tasa configurable (ej. 21%, 10.5%).
  - Resumen visual destacado del Total Final.
- **Emisión de PDF Profesional y Minimalista**:
  - Maquetado tipográfico de alta precisión con ReportLab Platypus.
  - Diseño sobrio en tonos pizarra y azul corporativo sin saturaciones visuales.
  - Numeración correlativa o única por presupuesto y control de fecha y validez.
  - Bloque estructurado de emisor y receptor.
  - Tabla alineada numéricamente con filas legibles.
  - Pie de página automático con numeración (`Página X de Y`).
- **Listo para Windows**:
  - Soporte de alta densidad de píxeles (High DPI).
  - Ícono nativo (.ico) integrado.
  - Empaquetado a ejecutable standalone listo para usar sin requerir Python instalado.

---

## 🏛 Arquitectura y Componentes

El proyecto sigue una arquitectura desacoplada orientada al dominio:

```text
FeeReport Lite - Windows Version/
├── docs/                     # Documentación técnica, decisiones de diseño (ADR) y arquitectura
│   ├── architecture.md       # Diagrama de componentes y responsabilidades
│   └── decisions.md          # Registro de decisiones de diseño (ADR)
├── tests/                    # Pruebas unitarias e integración con pytest
│   ├── test_models.py        # Pruebas de modelos y cálculos financieros
│   ├── test_pdf_generator.py # Pruebas de renderizado y compilación de PDF
│   └── test_config_service.py# Pruebas de almacenamiento y lectura JSON
├── config/                   # Archivos de configuración y persistencia local
│   ├── default_settings.json # Configuración de respaldo por defecto
│   └── settings.json         # Preferencias y datos del profesional (creado automáticamente)
├── assets/                   # Recursos visuales e identidad del sistema
│   ├── app_icon.png          # Ícono en formato PNG
│   └── app_icon.ico          # Ícono multirresolución en formato ICO
├── outputs/                  # Salida de presupuestos PDF generados
├── src/                      # Código fuente principal
│   ├── models/               # Entidades de dominio (Cliente, Profesional, Item, Presupuesto)
│   ├── services/             # Motor de generación PDF y persistencia de configuración
│   ├── ui/                   # Interfaz gráfica PySide6, widgets y estilos modernos QSS
│   └── utils/                # Formateadores numéricos, rutas y utilidades de soporte
├── .gitignore                # Reglas de exclusión de git
├── requirements.txt          # Dependencias y versiones exactas instaladas
├── LICENSE.txt               # Licencia MIT de código abierto
├── README.md                 # Guía general del proyecto
└── main.py                   # Punto de entrada de la aplicación de escritorio
```

---

## 🚀 Requisitos e Instalación

### Requisitos Previos
- **Windows 10 / 11** (o compatible).
- **Python 3.10 o superior** instalado y disponible en el `PATH`.

### Paso 1: Clonar o descargar el repositorio
```bash
git clone https://github.com/tu-usuario/feereport-lite.git
cd "FeeReport Lite - Windows Version"
```

### Paso 2: Crear y activar el entorno virtual
En PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Paso 3: Instalar dependencias
```powershell
pip install -r requirements.txt
```

---

## 💻 Guía de Ejecución

### Modo Desarrollo (con Python)
Para iniciar la interfaz gráfica desde la terminal:
```powershell
python main.py
```

### Ejecutar las Pruebas Unitarias
El proyecto cuenta con una suite completa de pruebas para validar cálculos matemáticos y generación de PDFs:
```powershell
python -m pytest -v
```

---

## 📦 Ejecutable Standalone (PyInstaller)

La aplicación puede compilarse en un ejecutable `.exe` independiente para distribuirse a usuarios finales sin necesidad de instalar Python:

```powershell
pyinstaller --noconfirm --onedir --windowed --name "FeeReportLite" --icon "assets/app_icon.ico" --add-data "assets;assets" --add-data "config/default_settings.json;config" main.py
```

El ejecutable resultante se ubicará en `dist/FeeReportLite/FeeReportLite.exe`.

---

## 📄 Formato del PDF Emitido

Cada presupuesto generado en `outputs/` incluye:
1. **Cabecera Formal**: Identificador correlativo del presupuesto, fecha de emisión y plazo de validez.
2. **Bloque de Partes**:
   - **Emisor**: Nombre completo, teléfono, correo electrónico y especialidad.
   - **Receptor**: Nombre completo, teléfono y correo electrónico.
3. **Detalle de Ítems**: Número de orden, descripción detallada del servicio o producto, cantidad, precio unitario y subtotal.
4. **Desglose Contable**:
   - Subtotal bruto acumulado.
   - Descuento aplicado (porcentaje y valor monetario).
   - Subtotal neto.
   - Impuesto / IVA (si aplica).
   - **Total Definitivo** destacado en bloque de alto contraste.
5. **Notas Legales y Pie de Página**: Condiciones comerciales y numeración de páginas.

---

## 📜 Licencia

Distribuido bajo la Licencia **MIT**. Consulta el archivo [LICENSE.txt](LICENSE.txt) para obtener más información.
