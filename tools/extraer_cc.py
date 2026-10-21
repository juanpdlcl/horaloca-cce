"""Separa NAVIDAD CC.png en sus piezas sueltas.

Agrupa por alfa: se dilata un poco la mascara para que el follaje ralo de una
misma pieza quede unido, se etiquetan los grupos y se recorta cada uno con el
alfa ORIGINAL (la dilatacion solo sirve para agrupar, no se guarda).
Saca una hoja numerada para decidir que es cada cosa; con --guardar escribe
los .webp en la carpeta del proyecto.
"""
from PIL import Image, ImageDraw
import numpy as np
from scipy import ndimage
import os, sys

SRC = r'C:/Users/EQUIPO/Downloads/NAVIDAD CC.png'
OUT = os.path.normpath('C:/Users/EQUIPO/AppData/Local/Temp/claude/'
                       'C--Users-EQUIPO-Desktop-Proyectos-claude/'
                       '743bcc5d-28f7-4b2e-a146-7922b8ed0f28/scratchpad/nv')
DEST = 'assets/img/navidad-adornos'
UMBRAL = 40        # por debajo de esto, el alfa es halo flojo
UNIR = 9           # radio de dilatacion para unir follaje de una misma pieza
MIN_AREA = 2500    # grupos mas chicos que esto son motas

im = Image.open(SRC).convert('RGBA')
W, H = im.size
arr = np.array(im)
alfa = arr[:, :, 3].astype(np.int16)

# alfa limpio: el halo flojo a cero
alfa_limpio = np.where(alfa <= UMBRAL, 0, alfa).astype(np.uint8)

mask = alfa_limpio > 0
unida = ndimage.binary_dilation(mask, ndimage.generate_binary_structure(2, 2),
                                iterations=UNIR)
etiq, n = ndimage.label(unida)
print('grupos encontrados:', n)

piezas = []
for i in range(1, n + 1):
    ys, xs = np.where(etiq == i)
    area = int(mask[etiq == i].sum())        # area real, sin contar la dilatacion
    if area < MIN_AREA:
        continue
    y0, y1 = int(ys.min()), int(ys.max()) + 1
    x0, x1 = int(xs.min()), int(xs.max()) + 1
    # recortar al contenido real dentro de la caja
    sub = mask[y0:y1, x0:x1] & (etiq[y0:y1, x0:x1] == i)
    fy, fx = np.where(sub)
    y0b, y1b = y0 + int(fy.min()), y0 + int(fy.max()) + 1
    x0b, x1b = x0 + int(fx.min()), x0 + int(fx.max()) + 1
    piezas.append((x0b, y0b, x1b, y1b, area, i))

# ordenar como se leen: por filas de arriba a abajo, luego de izquierda a derecha
piezas.sort(key=lambda p: (round(p[1] / 90), p[0]))
print('piezas utiles:', len(piezas))

recortes = []
for idx, (x0, y0, x1, y1, area, lab) in enumerate(piezas, 1):
    rec = Image.fromarray(arr[y0:y1, x0:x1].copy(), 'RGBA')
    # dentro de la caja puede colarse un trozo de la pieza vecina: se borra
    propio = (etiq[y0:y1, x0:x1] == lab)
    a = np.array(rec.getchannel('A'))
    a = np.where(propio, np.where(a <= UMBRAL, 0, a), 0).astype(np.uint8)
    rec.putalpha(Image.fromarray(a, 'L'))
    recortes.append((idx, rec, x1 - x0, y1 - y0, area))
    print('  %2d  %4dx%-4d  area %6d' % (idx, x1 - x0, y1 - y0, area))

# hoja numerada sobre el fondo de la pagina
COL, CEL = 3, 470
filas = (len(recortes) + COL - 1) // COL
hoja = Image.new('RGB', (COL * CEL, filas * (CEL + 24)), (13, 13, 17))
dr = ImageDraw.Draw(hoja)
for i, (idx, rec, w, h, area) in enumerate(recortes):
    e = min((CEL - 20) / w, (CEL - 20) / h, 1.0)
    chico = rec.resize((max(1, int(w * e)), max(1, int(h * e))), Image.LANCZOS)
    cx = (i % COL) * CEL + (CEL - chico.size[0]) // 2
    cy = (i // COL) * (CEL + 24) + (CEL - chico.size[1]) // 2
    base = Image.new('RGBA', chico.size, (13, 13, 17, 255))
    base.alpha_composite(chico)
    hoja.paste(base.convert('RGB'), (cx, cy))
    dr.rectangle([(i % COL) * CEL + 2, (i // COL) * (CEL + 24) + 2,
                  (i % COL) * CEL + CEL - 2, (i // COL) * (CEL + 24) + CEL - 2],
                 outline=(60, 60, 70))
    dr.text(((i % COL) * CEL + 8, (i // COL) * (CEL + 24) + CEL + 5),
            '#%d  %dx%d' % (idx, w, h), fill=(255, 235, 120))
hoja.save(OUT + '/cc-piezas.jpg', quality=90)
print('->', OUT + '/cc-piezas.jpg')

if '--guardar' in sys.argv:
    os.makedirs(DEST, exist_ok=True)
    for idx, rec, w, h, area in recortes:
        rec.save('%s/p%02d.webp' % (DEST, idx), 'WEBP', quality=86, method=6)
    print('guardadas', len(recortes), 'piezas en', DEST)
