"""Convierte la foto de guirnalda sobre negro en una banda con transparencia,
repetible en horizontal, para colgarla bajo la barra de la pagina.

El fondo negro pasa a alfa por luminancia, asi que las agujas conservan el
borde suave y no queda recortada a tijera. Luego se espeja: la baldosa
[A | A invertida] empalma consigo misma sin costura, porque la columna del
extremo izquierdo y la del derecho son la misma.
"""
from PIL import Image, ImageFilter
import os, sys

BASE = os.path.normpath('C:/Users/EQUIPO/AppData/Local/Temp/claude/'
                        'C--Users-EQUIPO-Desktop-Proyectos-claude/'
                        '743bcc5d-28f7-4b2e-a146-7922b8ed0f28/scratchpad')
SRC = os.path.join(BASE, 'guirnaldas', 'pexels_unsplash-1', 'orig.jpg')
PREV = os.path.join(BASE, 'nv')
DEST = 'assets/img/deco/nv-guirnalda.webp'

ALTO = 260          # alto de la baldosa (el doble del que se ve, por pantallas 2x)
NEGRO, PLENO = 16, 62   # luminancia: <=NEGRO transparente del todo, >=PLENO opaco

im = Image.open(SRC).convert('RGB')
W, H = im.size

# 1. recorte: quedarse solo con la franja donde esta la guirnalda
gris = im.convert('L')
px = gris.load()
filas = []
for y in range(H):
    m = 0
    for x in range(0, W, 7):          # muestreo, basta para encontrar el borde
        v = px[x, y]
        if v > m:
            m = v
    filas.append(m)
ys = [y for y, v in enumerate(filas) if v > 72]
y0, y1 = min(ys), max(ys)
# la parte de abajo es sombra suelta; nos quedamos con el cuerpo denso
y1 = min(y1, y0 + int((y1 - y0) * 0.62))
print('franja util: y', y0, '..', y1, ' (de', H, ')')
# las pinas estan hacia x~900 y x~2750. Si el espejo cae sobre una pina
# salen dos gemelas pegadas y se nota el truco: cortamos en medio de las dos,
# donde solo hay follaje, y ahi el empalme no se ve.
X1 = 2450
rec = im.crop((0, y0, X1, y1))
print('corte horizontal: 0 ..', X1, 'de', W)

# 2. el negro pasa a alfa, por luminancia y con el borde suavizado
g = rec.convert('L')
alfa = g.point(lambda v: 0 if v <= NEGRO else (255 if v >= PLENO else
                int(255 * (v - NEGRO) / (PLENO - NEGRO))))
alfa = alfa.filter(ImageFilter.GaussianBlur(0.6))
rgba = rec.convert('RGBA')
rgba.putalpha(alfa)

# 3. escalar a la altura de la baldosa
w2 = max(1, int(rec.size[0] * ALTO / rec.size[1]))
rgba = rgba.resize((w2, ALTO), Image.LANCZOS)
print('media baldosa:', rgba.size)

# 4. espejar para que repita sin costura
baldosa = Image.new('RGBA', (w2 * 2, ALTO), (0, 0, 0, 0))
baldosa.paste(rgba, (0, 0))
baldosa.paste(rgba.transpose(Image.FLIP_LEFT_RIGHT), (w2, 0))

if '--guardar' in sys.argv:
    baldosa.save(DEST, 'WEBP', quality=72, method=6)
    print('guardado', DEST, os.path.getsize(DEST) // 1024, 'KB', baldosa.size)

# 5. vista previa: tres repeticiones sobre el fondo real de la pagina
ANCHO = 1400
rep = Image.new('RGBA', (ANCHO, ALTO), (0, 0, 0, 0))
x = 0
while x < ANCHO:
    rep.alpha_composite(baldosa, (x, 0))
    x += baldosa.size[0]
vista = Image.new('RGB', (ANCHO, ALTO + 150), (13, 13, 17))
vista.paste(Image.new('RGB', (ANCHO, 70), (24, 20, 34)), (0, 0))   # simula la barra
tmp = Image.new('RGBA', (ANCHO, ALTO), (13, 13, 17, 255))
tmp.alpha_composite(rep)
vista.paste(tmp.convert('RGB'), (0, 70))
vista.save(PREV + '/guirnalda-repetida.jpg', quality=92)
print('->', PREV + '/guirnalda-repetida.jpg')
