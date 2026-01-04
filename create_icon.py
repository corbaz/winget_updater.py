"""
Crear un icono personalizado para Win-Upgrade
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Crear imagen de 256x256 con fondo azul de Windows
img = Image.new('RGBA', (256, 256), (0, 120, 215, 255))  # Azul de Windows
draw = ImageDraw.Draw(img)

# Dibujar un símbolo de actualización (flecha circular)
# Círculo exterior blanco
draw.ellipse([40, 40, 216, 216], outline='white', width=20)

# Flecha hacia arriba (parte de actualización)
arrow_points = [
    (128, 70),   # Punta
    (100, 110),  # Izquierda
    (118, 110),  # Centro izq
    (118, 180),  # Abajo izq
    (138, 180),  # Abajo der
    (138, 110),  # Centro der
    (156, 110),  # Derecha
]
draw.polygon(arrow_points, fill='white')

# Pequeña flecha circular en la esquina (símbolo de refresh)
draw.arc([160, 160, 210, 210], start=180, end=450, fill='#4CC2FF', width=12)
# Punta de la flecha
draw.polygon([(185, 155), (210, 160), (205, 180)], fill='#4CC2FF')

# Guardar en múltiples tamaños para el .ico
icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
images = []

for size in icon_sizes:
    resized = img.resize(size, Image.Resampling.LANCZOS)
    images.append(resized)

# Guardar como .ico con múltiples tamaños
output_path = os.path.join(os.path.dirname(__file__), 'win-upgrade.ico')
images[0].save(output_path, format='ICO', sizes=icon_sizes, append_images=images[1:])

print(f"✓ Icono creado: {output_path}")
print(f"  Tamaños incluidos: {icon_sizes}")

