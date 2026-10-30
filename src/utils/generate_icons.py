"""
Script utilitario para generar el ícono oficial de FeeReport Lite.
Genera versiones .png y .ico con múltiples resoluciones (16x16 hasta 256x256).
"""
import os
from PIL import Image, ImageDraw

def create_app_icon(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    size = (512, 512)
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Fondo circular suave con esquinas redondeadas (Squircle)
    margin = 24
    rect_box = [margin, margin, size[0] - margin, size[1] - margin]
    # Gradiente o color principal azul pizarra elegante (Dark Slate Blue)
    draw.rounded_rectangle(rect_box, radius=90, fill="#1E293B", outline="#334155", width=6)

    # Representación de hoja de documento / presupuesto en perspectiva frontal
    doc_left, doc_top = 110, 85
    doc_right, doc_bottom = 402, 427
    draw.rounded_rectangle([doc_left, doc_top, doc_right, doc_bottom], radius=24, fill="#F8FAFC")

    # Cabecera de documento (color azul marino formal)
    draw.rounded_rectangle([doc_left, doc_top, doc_right, doc_top + 75], radius=24, fill="#0F172A")
    # Tapa el redondeo inferior de la cabecera
    draw.rectangle([doc_left, doc_top + 45, doc_right, doc_top + 75], fill="#0F172A")

    # Líneas de texto/datos simulados
    line_color = "#CBD5E1"
    draw.rounded_rectangle([140, 190, 370, 202], radius=6, fill="#64748B")
    draw.rounded_rectangle([140, 225, 330, 235], radius=5, fill=line_color)
    draw.rounded_rectangle([140, 255, 350, 265], radius=5, fill=line_color)
    draw.rounded_rectangle([140, 285, 290, 295], radius=5, fill=line_color)

    # Divisor
    draw.line([(140, 320), (370, 320)], fill="#E2E8F0", width=3)

    # Ícono circular de verificación / éxito monetario (Badge verde esmeralda)
    badge_center = (345, 365)
    badge_radius = 50
    draw.ellipse(
        [badge_center[0] - badge_radius, badge_center[1] - badge_radius,
         badge_center[0] + badge_radius, badge_center[1] + badge_radius],
        fill="#059669", outline="#FFFFFF", width=6
    )

    # Símbolo '$' limpio dentro del badge
    # Dibujamos trazos estilizados para el signo de pesos
    # Círculo o barra central y curvatura
    draw.line([(345, 335), (345, 395)], fill="#FFFFFF", width=6)
    # Trazos horizontales estables
    draw.arc([330, 340, 360, 365], start=90, end=270, fill="#FFFFFF", width=5)
    draw.arc([330, 365, 360, 390], start=270, end=90, fill="#FFFFFF", width=5)
    draw.line([(345, 365), (345, 365)], fill="#FFFFFF", width=5)

    # Guardar PNG en alta resolución (256x256 y 512x512)
    png_path = os.path.join(output_dir, "app_icon.png")
    image_256 = image.resize((256, 256), Image.Resampling.LANCZOS)
    image_256.save(png_path, "PNG")

    # Guardar ICO con múltiples tamaños
    ico_path = os.path.join(output_dir, "app_icon.ico")
    image.save(ico_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print(f"Iconos generados exitosamente en:\n - {png_path}\n - {ico_path}")

if __name__ == "__main__":
    import sys
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_dir = os.path.join(base_dir, "assets")
    create_app_icon(assets_dir)
