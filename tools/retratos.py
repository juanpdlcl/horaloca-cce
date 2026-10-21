"""Retratos cuadrados de cada personaje navideno, recortados de la sesion de
estudio. (cx, ytop, lado) en fraccion del ANCHO de la foto original.
Primero saca una hoja para revisar a ojo; con --guardar escribe los .webp."""
from PIL import Image, ImageDraw
import os, sys

S = os.path.normpath('C:/Users/EQUIPO/AppData/Local/Temp/claude/'
                     'C--Users-EQUIPO-Desktop-Proyectos-claude/'
                     '743bcc5d-28f7-4b2e-a146-7922b8ed0f28/scratchpad/nv')
B = 'assets/img/tematicas/'
DEST = 'assets/img/navidad-personajes'

# nombre, archivo, slug, cx, ytop, lado   (cx/lado en fraccion del ancho; ytop del alto)
P = [
    ('Santa Claus',        'navidad/12.jpg',        'santa',    0.450, 0.090, 0.225),
    ('El Grinch',          'navidad/11.jpg',        'grinch',   0.440, 0.065, 0.215),
    ('La galleta',         'navidad/11.jpg',        'galleta',  0.605, 0.040, 0.215),
    ('Elfas',              'navidad/17.jpg',        'elfa',     0.500, 0.020, 0.880),
    ('Sra. Claus',         'navidad/18.jpg',        'sra',      0.660, 0.130, 0.400),
    ('Baston de caramelo', 'navidad/18.jpg',        'baston',   0.390, 0.130, 0.400),
    ('Soldaditos',         'navidad/04.jpg',        'soldados', 0.500, 0.060, 0.820),
    ('Zancos',             'navidad/05.jpg',        'zancos',   0.500, 0.030, 0.950),
    ('Blanca Navidad',     'blanca-navidad/01.jpg', 'blanca',   0.500, 0.040, 0.950),
]

LADO = 300
guardar = '--guardar' in sys.argv
if guardar:
    os.makedirs(DEST, exist_ok=True)

cols = 4
filas = (len(P) + cols - 1) // cols
hoja = Image.new('RGB', (cols * LADO, filas * (LADO + 22)), (16, 16, 20))
dr = ImageDraw.Draw(hoja)

for i, (nom, arch, slug, cx, ytop, ladof) in enumerate(P):
    im = Image.open(B + arch).convert('RGB')
    w, h = im.size
    lado = int(w * ladof)
    lado = min(lado, w, h)
    izq = max(0, min(int(w * cx - lado / 2), w - lado))
    top = max(0, min(int(h * ytop), h - lado))
    rec = im.crop((izq, top, izq + lado, top + lado))
    vista = rec.resize((LADO, LADO), Image.LANCZOS)
    x, y = (i % cols) * LADO, (i // cols) * (LADO + 22)
    hoja.paste(vista, (x, y))
    dr.text((x + 6, y + LADO + 5), nom + '  (' + str(lado) + 'px)', fill=(255, 235, 120))
    if guardar:
        rec.resize((420, 420), Image.LANCZOS).save(
            DEST + '/' + slug + '.webp', 'WEBP', quality=86, method=6)

hoja.save(S + '/retratos.jpg', quality=92)
print(S + '/retratos.jpg')
if guardar:
    print('guardados', len(P), 'retratos en', DEST)
