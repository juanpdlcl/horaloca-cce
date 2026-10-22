"""Dibuja un mosaico de copos de nieve que repite sin costura.

Un copo real tiene simetria de orden 6: se dibuja UNA rama y se repite
girada seis veces. Cada copo lleva ramitas laterales a distintas alturas,
que es lo que los hace parecer cristales y no estrellas.

Para que el mosaico empalme, cada copo se pinta NUEVE veces (el propio y
sus ocho desplazamientos de una baldosa). Lo que se sale por un lado entra
por el otro exactamente igual.
"""
from PIL import Image, ImageDraw, ImageFilter
import math, random, os, sys

OUT = os.path.normpath('C:/Users/EQUIPO/AppData/Local/Temp/claude/'
                       'C--Users-EQUIPO-Desktop-Proyectos-claude/'
                       '743bcc5d-28f7-4b2e-a146-7922b8ed0f28/scratchpad/nv')
DEST = 'assets/img/deco/nv-copos.webp'

LADO = 1000          # baldosa, se sirve reducida
SUP = 3              # se dibuja 3x y se reduce: bordes suaves sin dientes
random.seed(7)       # mismo resultado siempre


def rama(dr, cx, cy, r, ang, grosor, color):
    """Una rama del copo, con ramitas laterales y un remate."""
    x2 = cx + r * math.cos(ang)
    y2 = cy + r * math.sin(ang)
    dr.line([(cx, cy), (x2, y2)], fill=color, width=grosor)
    for frac, largo, abre in ((0.34, 0.30, 0.62), (0.58, 0.24, 0.58), (0.80, 0.16, 0.55)):
        bx = cx + r * frac * math.cos(ang)
        by = cy + r * frac * math.sin(ang)
        for lado in (-1, 1):
            a = ang + lado * abre
            dr.line([(bx, by),
                     (bx + r * largo * math.cos(a), by + r * largo * math.sin(a))],
                    fill=color, width=max(1, int(grosor * 0.72)))
    # remate en punta
    for lado in (-1, 1):
        a = ang + lado * 0.5
        dr.line([(x2, y2),
                 (x2 + r * 0.1 * math.cos(a), y2 + r * 0.1 * math.sin(a))],
                fill=color, width=max(1, int(grosor * 0.6)))


def copo(dr, cx, cy, r, grosor, color, giro):
    for k in range(6):
        rama(dr, cx, cy, r, giro + k * math.pi / 3, grosor, color)
    h = max(2, int(grosor * 1.5))
    dr.ellipse([cx - h, cy - h, cx + h, cy + h], fill=color)


L = LADO * SUP
img = Image.new('RGBA', (L, L), (0, 0, 0, 0))
dr = ImageDraw.Draw(img)

# tamanos y opacidades variados, como en la referencia
PIEZAS = [
    (0.115, 190), (0.082, 150), (0.098, 165), (0.062, 120),
    (0.105, 175), (0.072, 135), (0.055, 110), (0.088, 155),
    (0.045, 95),  (0.068, 125), (0.050, 100), (0.078, 140),
]
puestos = []
for rel, alfa in PIEZAS:
    r = L * rel
    for _ in range(260):                       # busca sitio sin solaparse
        cx, cy = random.random() * L, random.random() * L
        if all((cx - px) ** 2 + (cy - py) ** 2 > (r + pr) ** 2 * 0.85
               for px, py, pr in puestos):
            break
    puestos.append((cx, cy, r))
    col = (255, 255, 255, alfa)
    g = max(SUP, int(r * 0.045))
    giro = random.random() * math.pi / 3
    for dx in (-L, 0, L):                      # las nueve copias: asi empalma
        for dy in (-L, 0, L):
            copo(dr, cx + dx, cy + dy, r, g, col, giro)

img = img.filter(ImageFilter.GaussianBlur(SUP * 0.35))
img = img.resize((LADO, LADO), Image.LANCZOS)

if '--guardar' in sys.argv:
    img.save(DEST, 'WEBP', quality=82, method=6)
    print('guardado', DEST, os.path.getsize(DEST) // 1024, 'KB')

# vista previa: 2x2 baldosas sobre el fondo de la pagina, para ver la costura
V = 760
chico = img.resize((V // 2, V // 2), Image.LANCZOS)
vista = Image.new('RGBA', (V, V), (11, 23, 18, 255))
for i in range(2):
    for j in range(2):
        vista.alpha_composite(chico, (i * V // 2, j * V // 2))
vista.convert('RGB').save(OUT + '/copos-prueba.jpg', quality=92)
print('->', OUT + '/copos-prueba.jpg')
