"""Mosaico de campanas para el fondo de la pagina, que repite sin costura.

Cada campana va a un tamano, un giro y una opacidad distintos, para que al
repetir no se lea como papel pintado. Para que el mosaico empalme, cada
campana se pega NUEVE veces (la propia y sus ocho desplazamientos de una
baldosa): lo que se sale por un lado entra por el otro igual.
"""
from PIL import Image
import random, os, sys

SRC = r'C:/Users/EQUIPO/Downloads/NicePng_gold-christmas-bow-png_3206953.png'
OUT = os.path.normpath('C:/Users/EQUIPO/AppData/Local/Temp/claude/'
                       'C--Users-EQUIPO-Desktop-Proyectos-claude/'
                       '743bcc5d-28f7-4b2e-a146-7922b8ed0f28/scratchpad/nv')
DEST = 'assets/img/deco/nv-fondo-campanas.webp'

LADO = 1000
random.seed(11)

base = Image.open(SRC).convert('RGBA')
base = base.crop(base.getbbox())

# Pocas y bien separadas: tres por baldosa, y la baldosa se sirve grande.
# Con mas, el fondo se convierte en papel pintado y compite con el contenido.
PIEZAS = [
    (0.195, 0.30),   # una grande
    (0.125, 0.22),   # una mediana
    (0.085, 0.16),   # una chica, casi insinuada
]

tile = Image.new('RGBA', (LADO, LADO), (0, 0, 0, 0))
puestas = []
for rel, op in PIEZAS:
    w = int(LADO * rel)
    h = int(base.size[1] * w / base.size[0])
    r = max(w, h) / 2
    for _ in range(320):                       # busca sitio sin amontonarse
        cx, cy = random.random() * LADO, random.random() * LADO
        if all((cx - px) ** 2 + (cy - py) ** 2 > (r + pr) ** 2 * 2.20
               for px, py, pr in puestas):
            break
    puestas.append((cx, cy, r))

    pieza = base.resize((w, h), Image.LANCZOS)
    pieza = pieza.rotate(random.uniform(-16, 16), expand=True,
                         resample=Image.BICUBIC)
    a = pieza.getchannel('A').point(lambda v: int(v * op))
    pieza.putalpha(a)

    px0 = int(cx - pieza.size[0] / 2)
    py0 = int(cy - pieza.size[1] / 2)
    for dx in (-LADO, 0, LADO):                # las nueve copias: asi empalma
        for dy in (-LADO, 0, LADO):
            tile.alpha_composite(pieza, (px0 + dx, py0 + dy))

if '--guardar' in sys.argv:
    tile.save(DEST, 'WEBP', quality=80, method=6)
    print('guardado', DEST, os.path.getsize(DEST) // 1024, 'KB')

# vista previa: 2x2 baldosas sobre el fondo real de la pagina
V = 820
chico = tile.resize((V // 2, V // 2), Image.LANCZOS)
vista = Image.new('RGBA', (V, V), (7, 16, 12, 255))
for i in range(2):
    for j in range(2):
        vista.alpha_composite(chico, (i * V // 2, j * V // 2))
vista.convert('RGB').save(OUT + '/campanas-fondo.jpg', quality=92)
print('->', OUT + '/campanas-fondo.jpg')
