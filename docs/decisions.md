# Registro de Decisiones de Arquitectura y Diseño (ADR)

## ADR 001: Selección de Framework Gráfico (PySide6 / Qt para Python)
- **Contexto**: El usuario solicitó un generador de presupuestos en Python para entorno de escritorio Windows.
- **Decisión**: Se implementa la interfaz con **PySide6** (Qt 6).
- **Justificación**:
  - Proporciona widgets nativos, reactividad eficiente y aceleración de renderizado en Windows.
  - Soporta hojas de estilos CSS (QSS) para lograr una estética moderna, limpia y profesional sin estilos genéricos.
  - Soporte de modelos/vistas para tablas interactivas con cálculo en tiempo real.
  - Compatibilidad total con empaquetado a binario `.exe` standalone mediante `PyInstaller`.

## ADR 002: Generación de Documentos PDF con ReportLab
- **Contexto**: Se requiere emitir presupuestos en formato PDF con diseño limpio, minimalista, profesional y formal.
- **Decisión**: Utilizar **ReportLab** con `Platypus` (Page Layout and Typography Using Scripts).
- **Justificación**:
  - Es el estándar de la industria en Python para generación programática precisa de PDFs de alta calidad tipográfica.
  - Permite maquetar tablas con alineación numérica, anchos proporcionales, paletas de colores sobrias y encabezados consistentes.
  - No depende de navegadores headless ni herramientas externas pesadas (como wkhtmltopdf o WeasyPrint con dependencias C complejas en Windows).

## ADR 003: Persistencia de Configuración y Perfil del Profesional
- **Contexto**: El usuario indicó guardar los datos del profesional para evitar su reingreso manual en cada presupuesto.
- **Decisión**: Almacenamiento local mediante JSON estructurado en `config/settings.json`, con fallback automático a `config/default_settings.json`.
- **Justificación**:
  - Ligero, editable por el usuario y sin sobrecarga de un motor de base de datos relacional para una herramienta "Lite".
  - Permite guardar moneda preferida, porcentaje de impuestos y notas al pie por defecto.

## ADR 004: Modelo Reactivo de Cálculos Financieros
- **Contexto**: Cálculo automático e inmediato de subtotales por ítem, subtotal global, impuestos y total general.
- **Decisión**: Los cambios en cualquier celda de la tabla (cantidad, descripción, precio) o en los controles de impuestos/descuentos disparan señales Qt (`itemChanged`, `valueChanged`) que recalculan los totales inmediatamente.
- **Justificación**:
  - Experiencia de usuario fluida sin necesidad de pulsar botones de "recalcular".
  - Garantiza consistencia entre la vista en pantalla y el PDF emitido.
