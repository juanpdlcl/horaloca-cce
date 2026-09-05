# -*- coding: utf-8 -*-
"""Catálogos PDF de CC Entertainment — diseño FESTIVO.

    python tools/catalogos.py            -> PDFs en la raíz del repo
    python tools/catalogos.py --hoja DIR -> además, hojas de contacto para revisar

Fondos de color en degradado por sección, confeti, fotos con marco blanco y sombra,
nombre de la temática en grande. Solo fotos y nombres: sin índice, cifras ni textos.
Tipos de elemento en las listas de CONTENIDO:
  ('Nombre', 'ruta.jpg')                       -> una celda
  ('Nombre', ['a.jpg', 'b.jpg'])               -> dos celdas con un solo nombre centrado
  F('Nombre', 'ruta.jpg', foco=0.3)            -> igual, con encuadre vertical (0 arriba … 1 abajo)
  PAGINA('hero_port'|'hero_land'|'grandes'|'grid', [...]) -> hoja completa con ese esquema
"""
import io, os, sys, random, math
import fitz
from PIL import Image, ImageOps

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)
FUENTES = os.path.join(RAIZ, 'tools', 'fonts')
T = 'assets/img/tematicas'


def hx(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


WHITE = (1, 1, 1); BLACK = (0, 0, 0)
YELLOW = hx('FFD54F'); PINK = hx('FF4FA3'); CYANC = hx('4DD0E1'); LIMEC = hx('C6FF00'); ORANGE = hx('FF9F43'); LILA = hx('B388FF')
RED = hx('E53935'); GREEN = hx('43A047'); GOLD = hx('F5C542')
MARCA = [hx('F5C542'), hx('2FD0FF'), hx('FF2FB0'), hx('CDEA1F'), hx('A06BF5')]   # plumas del logo
CONFETI = [YELLOW, PINK, CYANC, LIMEC, ORANGE, WHITE, LILA]

W, H = 595, 842
M = 42
TEL = '(829) 343-5460'
IG = '@horaloca_cce'
WEB = 'horaloca-cce.vercel.app'


# ═══════════════════════════════════════════════════════════════
#  CONTENIDO
# ═══════════════════════════════════════════════════════════════
def t(d, n):
    return f'{T}/{d}/{n:02d}.jpg'


def F(nombre, img, foco=0.18):
    return {'n': nombre, 'img': img, 'foco': foco}


def PAGINA(tipo, items):
    return {'pagina': tipo, 'items': items}


DISCO_BALL = [
    PAGINA('hero_port', [
        ('Bar Neón', t('bar-neon', 1)),
        ('Disco Ball', f'{T}/espejos/main.jpg'),
        ('Disco Ball — gorras', t('espejos', 9)),
        ('Disco Ball — salida', t('espejos', 11)),
        ('Chicas de espejos', 'assets/img/destacado/plata-1.jpg'),
    ]),
    ('Hombre LED', 'assets/img/destacado/plata-2.jpg'),
    ('Hombre espejo', 'assets/img/destacado/plata-3.jpg'),
    ('Disco Ball — grupo', 'assets/img/destacado/plata-4.jpg'),
    ('Disco Ball — trío', t('espejos', 10)),
    ('Show en vivo', t('espejos', 1)),
    ('Show en vivo', t('espejos', 5)),
]

TEMATICAS = [
    ('Dorado', 'assets/img/destacado/dorado-4.jpg'),
    ('Shine Gold', t('shine-gold', 1)),
    ('Dorado — show girls', t('dorado', 6)),
    ('Brazil plateada', t('brasil-plata', 1)),
    ('Brazil', t('brazil', 1)),
    ('Brazil — carnaval', t('brazil', 2)),
    ('Viva las Vegas', t('vegas', 1)),
    ('Viva las Vegas — show girls', t('vegas', 3)),
    ('Neón', t('neon', 5)),
    ('Neón — grupo', t('neon', 6)),
    ('Tropical', 'assets/img/ig/tropical-sunset.jpg'),
    ('Gatsby', t('gatsby', 1)),
    ('Gatsby — pareja', t('gatsby', 2)),
    ('Neon 2000', t('neon-2000', 1)),
    ('Samba', t('samba', 1)),
    ('África', t('africa', 2)),
    ('Safari', t('safari', 3)),
    ('Tropical Cuba', t('tropical-cuba', 1)),
    ('Playa', t('playa', 1)),
    ('Hawaii', t('hawaii', 1)),
    ('Vaqueros', t('vaqueros', 1)),
    ('Porristas', t('porristas', 1)),
    ('Ingenieros', t('ingenieros', 1)),
    ('Cocineros', t('cocineros-show', 1)),
    ('Personajes para bienvenida', t('bienvenida', 1)),
    ('Viva las Vegas — host', t('vegas', 5)),
    ('Personaje de corazón', t('corazon', 1)),
    ('Personaje de playa', t('personaje-playa', 1)),
    ('Hadas', t('hadas', 1)),
    ('Astronauta y alien', t('astronauta', 1)),
    ('Cabezones', 'assets/img/promo/artistas.jpg'),
    PAGINA('hero_port', [
        ('Vogue', t('vogue', 1)),
        ('Vogue — blanco', t('vogue', 2)),
        ('Vogue — rojo', t('vogue', 4)),
        ('Vogue — anfitriones', t('vogue', 7)),
        ('Vogue — anfitriones', t('vogue', 8)),
    ]),
    ('Feria/Circo', [t('feria-circo', 1), t('feria-circo', 2)]),
    ('Disco', t('disco', 1)),
    F('Años 80', t('anos-80', 2), foco=0.45),
    ('Años 90', t('anos-90', 1)),
    ('Brigeston', t('brigeston', 1)),
    ('Pilotos Formula 1', t('pilotos', 5)),
    ('Pilotos Formula 1 — pit stop', t('pilotos', 3)),
    ('Marineros', t('marineros', 1)),
    ('Mimos', t('mimos', 1)),
    ('Catrinas', 'assets/img/catrinas.jpg'),
    ('Venezia', 'assets/img/ig/venetian.jpg'),
]

SHOW_LED = [
    ('Show LED', t('led-show', 3)),
    ('Zancos LED', t('led-show', 1)),
    ('Alas LED', t('alas-led', 3)),
    ('Alas LED', t('alas-led', 1)),
    ('Robot LED espejo', t('robot-espejo', 2)),
    ('Show LED — escena', t('led-show', 4)),
    ('Show LED — tambores', t('led-show', 2)),
]

DOMINICANO = [
    ('Carnaval Dominicano', 'assets/img/ig/carnaval.jpg'),
    ('Carnaval — comparsa', t('carnaval', 2)),
    ('Diablo cojuelo', 'assets/img/ig/carnaval-2.jpg'),
    ('Zancos dominicanos', t('zanqueros-rd', 1)),
    ('Dominicana', t('dominicana', 1)),
    ('Pareja dominicana', t('dominicana', 2)),
    ('Dominicana en evento', t('dominicana', 5)),
    ('Marchantas', t('marchantas', 1)),
    ('Marchanta', t('marchantas', 3)),
    PAGINA('hero_port', [
        ('Pelota dominicana', t('pelota', 3)),
        ('Pelota dominicana', t('pelota', 1)),
        ('Pelota dominicana', t('pelota', 2)),
    ]),
]

NAVIDAD = [   # familias de fotos alternadas para que no se repitan seguidas
    PAGINA('grandes', [('Show Navidad completo', t('navidad', 12)), ('Santa y los elfos', t('navidad', 9))]),
    PAGINA('grid', [('Cascanueces y elfa', t('navidad', 15)), ('Pareja Candy', t('navidad', 18)),
                    ('Elfa roja', t('navidad', 16)), ('Cocineros navideños', t('navidad', 19))]),
    PAGINA('grandes', [('El Grinch y la galleta', t('navidad', 11)), ('Santa con elfos y galleta', t('navidad', 10))]),
    PAGINA('grid', [('Santa y sus ayudantes', t('navidad', 13)), ('Santa', t('navidad', 7)),
                    ('Chicas de Santa', t('navidad', 2)), ('Soldados de juguete', t('navidad', 4))]),
    PAGINA('grid', [('Zancos navideños', t('navidad', 5)), ('Alas LED navideñas', t('navidad', 6)),
                    ('Blanca Navidad', t('blanca-navidad', 1)), ('Cascanueces y Santa', t('navidad', 3))]),
]

EXTRAS = [
    ('Zanqueros', 'assets/img/promo/zancos.jpg'),
    ('Percusión en vivo', 'assets/img/promo/musicos.jpg'),
    ('Coreografía personalizada', 'assets/img/destacado/plata-1.jpg'),
    ('Robot LED', 'assets/img/promo/robot-espejo.jpg'),
    ('Bailarines adicionales', 'assets/img/promo/bailarinas-led.jpg'),
]

# degradado (arriba -> abajo), color del acento de los nombres, imagen de portadilla
SECCIONES = [
    dict(num='01', titulo='Disco Ball', etiqueta='DISCO BALL', grad=('1E1B4B', '6D28D9'), acento=YELLOW, items=DISCO_BALL, imagen=f'{T}/espejos/main.jpg'),
    dict(num='02', titulo='Temáticas', etiqueta='TEMÁTICAS', grad=('BE185D', 'F97316'), acento=YELLOW, items=TEMATICAS, imagen='assets/img/destacado/dorado-4.jpg'),
    dict(num='03', titulo='Show LED', etiqueta='SHOW LED', grad=('0B3B8C', '06B6D4'), acento=LIMEC, items=SHOW_LED, imagen=t('led-show', 3)),
    dict(num='04', titulo='Ritmo Dominicano', etiqueta='RITMO DOMINICANO', grad=('B91C1C', 'F59E0B'), acento=CYANC, items=DOMINICANO, imagen='assets/img/ig/carnaval.jpg'),
    dict(num='05', titulo='Navidad', etiqueta='NAVIDAD', grad=('0F5132', '2E9E5B'), acento=YELLOW, items=NAVIDAD, imagen=t('navidad', 12), navidad=True),
    dict(num='06', titulo='Extras para tu show', etiqueta='EXTRAS', grad=('4C1D95', 'C026D3'), acento=YELLOW, items=EXTRAS, imagen='assets/img/promo/zancos.jpg'),
]
GRAD_PORTADA = ('6D28D9', 'DB2777')
GRAD_NAVIDAD = ('0F5132', 'B91C1C')
MOSAICO_PORTADA = [f'{T}/espejos/main.jpg', t('vogue', 1), t('vegas', 5), t('bar-neon', 1), t('dorado', 6), t('navidad', 12)]
MOSAICO_NAVIDAD = [t('navidad', 12), t('navidad', 15), t('navidad', 18), t('navidad', 19), t('navidad', 13), t('navidad', 7)]


# ═══════════════════════════════════════════════════════════════
#  TIPOGRAFÍA
# ═══════════════════════════════════════════════════════════════
ARCHIVO_FUENTE = {'B': 'Outfit-Bold.ttf', 'S': 'Outfit-SemiBold.ttf', 'M': 'Outfit-Medium.ttf', 'L': 'Outfit-Light.ttf'}
_FONT = {k: fitz.Font(fontfile=os.path.join(FUENTES, v)) for k, v in ARCHIVO_FUENTE.items()}


def ancho(s, k, size, tracking=0.0):
    return _FONT[k].text_length(s, fontsize=size) + tracking * size * max(len(s) - 1, 0)


def texto(page, s, y, size, k='B', color=WHITE, x=None, alinear='izq', tracking=0.0, opacidad=1.0):
    w = ancho(s, k, size, tracking)
    if x is None:
        px = (W - w) / 2
    elif alinear == 'der':
        px = x - w
    elif alinear == 'centro':
        px = x - w / 2
    else:
        px = x
    base = y + size * 0.78
    ff = os.path.join(FUENTES, ARCHIVO_FUENTE[k])
    if tracking:
        cx = px
        for ch in s:
            page.insert_text((cx, base), ch, fontname='ou' + k, fontfile=ff, fontsize=size, color=color, fill_opacity=opacidad)
            cx += _FONT[k].text_length(ch, fontsize=size) + tracking * size
    else:
        page.insert_text((px, base), s, fontname='ou' + k, fontfile=ff, fontsize=size, color=color, fill_opacity=opacidad)
    return w


def linea(page, x0, y, x1, color=WHITE, grosor=0.6, opacidad=1.0):
    sh = page.new_shape(); sh.draw_line((x0, y), (x1, y)); sh.finish(color=color, width=grosor, stroke_opacity=opacidad); sh.commit()


def barra_marca(page, x, y, w=44, grosor=2.4):
    seg = w / len(MARCA)
    for i, c in enumerate(MARCA):
        page.draw_line((x + i * seg, y), (x + (i + 1) * seg - 1.2, y), color=c, width=grosor)


# ═══════════════════════════════════════════════════════════════
#  FONDO FESTIVO
# ═══════════════════════════════════════════════════════════════
def degradado(page, c1, c2, bandas=72):
    a, b = hx(c1), hx(c2)
    alto = H / bandas
    for i in range(bandas):
        f = i / (bandas - 1)
        col = tuple(a[j] + (b[j] - a[j]) * f for j in range(3))
        page.draw_rect(fitz.Rect(0, i * alto - 0.5, W, (i + 1) * alto + 0.5), color=None, fill=col)


def confeti(page, semilla, cantidad=60, evitar=()):
    rnd = random.Random(semilla)
    sh = page.new_shape()
    for _ in range(cantidad):
        x, y = rnd.uniform(6, W - 6), rnd.uniform(6, H - 6)
        if any(r.contains(fitz.Point(x, y)) for r in evitar):
            continue
        col = rnd.choice(CONFETI); op = rnd.uniform(0.35, 0.9); tipo = rnd.random()
        if tipo < 0.45:
            sh.draw_circle((x, y), rnd.uniform(1.8, 5))
        elif tipo < 0.75:
            s = rnd.uniform(4, 9); a = rnd.uniform(0, math.pi)
            pts = [(x + s * math.cos(a + k * math.pi / 2), y + s * math.sin(a + k * math.pi / 2)) for k in range(4)]
            sh.draw_polyline(pts + [pts[0]])
        else:
            l, g = rnd.uniform(8, 16), rnd.uniform(2, 3.2); a = rnd.uniform(0, math.pi)
            dx, dy = math.cos(a), math.sin(a); nx, ny = -dy * g / 2, dx * g / 2
            pts = [(x - dx * l / 2 + nx, y - dy * l / 2 + ny), (x + dx * l / 2 + nx, y + dy * l / 2 + ny),
                   (x + dx * l / 2 - nx, y + dy * l / 2 - ny), (x - dx * l / 2 - nx, y - dy * l / 2 - ny)]
            sh.draw_polyline(pts + [pts[0]])
        sh.finish(color=None, fill=col, fill_opacity=op, closePath=True)
    sh.commit()


# ═══════════════════════════════════════════════════════════════
#  IMÁGENES
# ═══════════════════════════════════════════════════════════════
_cache = {}


def foto(path, rect, foco=0.18, escala=2.0):
    key = (path, round(rect.width), round(rect.height), foco)
    if key in _cache:
        return _cache[key]
    im = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    cw, ch = rect.width * escala, rect.height * escala
    r_cel = cw / ch; r_im = im.width / im.height
    if r_im > r_cel:
        nw = int(im.height * r_cel); x0 = (im.width - nw) // 2
        im = im.crop((x0, 0, x0 + nw, im.height))
    else:
        nh = int(im.width / r_cel); sobra = im.height - nh; y0 = int(sobra * foco)
        im = im.crop((0, y0, im.width, y0 + nh))
    im = im.resize((int(cw), int(ch)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=84, optimize=True, progressive=True)
    _cache[key] = b.getvalue()
    return _cache[key]


def redondeado(page, rect, r, fill=None, color=None, width=0.6, opacidad=1.0):
    sh = page.new_shape()
    sh.draw_rect(rect, radius=r / min(rect.width, rect.height))
    sh.finish(color=color, fill=fill, width=width, fill_opacity=opacidad, stroke_opacity=opacidad)
    sh.commit()


def esquinas(page, rect, r, fondo):
    x0, y0, x1, y1 = rect.x0, rect.y0, rect.x1, rect.y1
    for (cx, cy, ax, ay, bx, by) in [(x0, y0, x0 + r, y0, x0, y0 + r), (x1, y0, x1 - r, y0, x1, y0 + r),
                                     (x1, y1, x1 - r, y1, x1, y1 - r), (x0, y1, x0 + r, y1, x0, y1 - r)]:
        sh = page.new_shape()
        sh.draw_line((cx, cy), (ax, ay)); sh.draw_curve((ax, ay), (cx, cy), (bx, by)); sh.draw_line((bx, by), (cx, cy))
        sh.finish(color=fondo, fill=fondo, width=0.3, closePath=True); sh.commit()


def celda(page, path, rect, foco=0.18, marco=6, r=10):
    """Foto con marco blanco redondeado y sombra: tarjeta de fiesta."""
    fr = rect + (-marco, -marco, marco, marco)
    for dy, op in ((10, 0.10), (6, 0.12), (3, 0.14)):
        redondeado(page, fr + (0, dy, 0, dy), r + marco, fill=BLACK, opacidad=op)
    redondeado(page, fr, r + marco, fill=WHITE)
    page.insert_image(rect, stream=foto(path, rect, foco))
    esquinas(page, rect, r, WHITE)


_xref = {}


def imagen_compartida(page, rect, key, bytes_fn):
    doc_key = (id(page.parent), key)
    if doc_key in _xref:
        page.insert_image(rect, xref=_xref[doc_key])
    else:
        _xref[doc_key] = page.insert_image(rect, stream=bytes_fn())


def png_qr():
    import qrcode
    im = qrcode.make('https://' + WEB, box_size=10, border=1).convert('RGB')
    b = io.BytesIO(); im.save(b, 'PNG'); return b.getvalue()


def png_logo():
    return open('assets/img/logo-mark-glow.png', 'rb').read()


# ═══════════════════════════════════════════════════════════════
#  ELEMENTOS DE PÁGINA
# ═══════════════════════════════════════════════════════════════
def cabeza(page, sec, numero, semilla, evitar=()):
    degradado(page, *sec['grad'])
    confeti(page, semilla, 56, evitar)
    texto(page, 'CC ENTERTAINMENT', 30, 8, 'B', WHITE, x=M, tracking=0.18)
    texto(page, sec['etiqueta'], 30.5, 7.5, 'B', sec['acento'], x=W - M - 34, alinear='der', tracking=0.18)
    texto(page, f'{numero:02d}', 28, 10, 'B', WHITE, x=W - M, alinear='der')
    linea(page, M, 52, W - M, WHITE, 0.6, 0.4)
    pie(page)
    if sec.get('navidad'):
        campana(page, W - M - 50, 40, 0.6, GOLD)
        lucecitas(page, M + 4, W - M - 4, 55)
        copo(page, M + 8, 786, 6); copo(page, W - M - 8, 782, 6)


def pie(page):
    barra_marca(page, M, 806)
    texto(page, f'{WEB}   ·   {TEL}   ·   {IG}', 800, 7, 'M', WHITE, x=W - M, alinear='der', opacidad=0.85)


def etiqueta(page, rect, nombre, acento, grande=False, centrada=False):
    ts = 17 if grande else 12.5
    y_n = rect.y1 + 16
    if centrada:
        cx = (rect.x0 + rect.x1) / 2
        texto(page, nombre, y_n, ts, 'B', WHITE, x=cx, alinear='centro')
        redondeado(page, fitz.Rect(cx - 14, y_n + ts + 8, cx + 14, y_n + ts + 11.5), 1.5, fill=acento)
        return
    texto(page, nombre, y_n, ts, 'B', WHITE, x=rect.x0 + 2)
    redondeado(page, fitz.Rect(rect.x0 + 2, y_n + ts + 8, rect.x0 + 30, y_n + ts + 11.5), 1.5, fill=acento)


# ─── decoración navideña ───
def campana(page, cx, cy, s=1.0, color=GOLD):
    sh = page.new_shape()
    sh.draw_line((cx, cy - 22 * s), (cx, cy - 17 * s)); sh.draw_circle((cx, cy - 22 * s), 2 * s)
    sh.draw_bezier((cx - 12 * s, cy + 6 * s), (cx - 12 * s, cy - 14 * s), (cx + 12 * s, cy - 14 * s), (cx + 12 * s, cy + 6 * s))
    sh.draw_line((cx - 15 * s, cy + 6 * s), (cx + 15 * s, cy + 6 * s))
    sh.finish(color=color, width=1.2 * s)
    sh.draw_circle((cx, cy + 9 * s), 2.2 * s); sh.finish(color=color, fill=color, width=0.5); sh.commit()


def copo(page, cx, cy, r=7, color=WHITE):
    sh = page.new_shape()
    for i in range(6):
        a = math.radians(i * 60); x1, y1 = cx + r * math.cos(a), cy + r * math.sin(a)
        sh.draw_line((cx, cy), (x1, y1))
        for lado in (-1, 1):
            b = a + lado * math.radians(35); xm, ym = cx + r * 0.6 * math.cos(a), cy + r * 0.6 * math.sin(a)
            sh.draw_line((xm, ym), (xm + r * 0.3 * math.cos(b), ym + r * 0.3 * math.sin(b)))
    sh.finish(color=color, width=0.8, stroke_opacity=0.9); sh.commit()


def lucecitas(page, x0, x1, y, n=26):
    colores = [RED, YELLOW, CYANC, PINK, LIMEC]
    paso = (x1 - x0) / (n - 1); sh = page.new_shape()
    for i in range(n):
        sh.draw_circle((x0 + i * paso, y + (2 if i % 2 else 5)), 1.6); sh.finish(color=None, fill=colores[i % 5])
    sh.commit()


# ═══════════════════════════════════════════════════════════════
#  PLANTILLAS
# ═══════════════════════════════════════════════════════════════
CEL = {
    'hero_land': dict(hero=fitz.Rect(M, 74, W - M, 396), abajo=[fitz.Rect(M, 456, 294, 716), fitz.Rect(301, 456, W - M, 716)]),
    'hero_port': dict(hero=fitz.Rect(M, 74, 322, 496), lado=[fitz.Rect(334, 74, W - M, 266), fitz.Rect(334, 316, W - M, 496)],
                      abajo=[fitz.Rect(M, 560, 294, 758), fitz.Rect(301, 560, W - M, 758)]),
    'hero_port3': dict(hero=fitz.Rect(M, 74, 322, 700), lado=[fitz.Rect(334, 74, W - M, 366), fitz.Rect(334, 420, W - M, 700)]),
    'grid': [[fitz.Rect(M, 74, 294, 372), fitz.Rect(301, 74, W - M, 372)], [fitz.Rect(M, 436, 294, 734), fitz.Rect(301, 436, W - M, 734)]],
    'duo': [fitz.Rect(M, 150, 294, 620), fitz.Rect(301, 150, W - M, 620)],
    'grandes': [fitz.Rect(M, 74, W - M, 370), fitz.Rect(M, 434, W - M, 730)],
}


def norm(it):
    """-> (nombre, img|[img,img], foco)"""
    if isinstance(it, dict):
        return (it['n'], it['img'], it.get('foco', 0.18))
    return (it[0], it[1], 0.18)


def es_par(it):
    return isinstance(it, tuple) and isinstance(it[1], list)


def rects_de(fila, celdas):
    if len(fila) == 1 and es_par(fila[0]):
        return list(celdas)
    return list(celdas[:len(fila)])


def pinta_celda(page, it, rect, sec, grande=False):
    n, img, foco = norm(it)
    celda(page, img, rect, foco=foco)
    etiqueta(page, rect, n, sec['acento'], grande=grande)


def pinta_fila(page, fila, celdas, sec):
    if len(fila) == 1 and es_par(fila[0]):
        n, rutas = fila[0]
        celda(page, rutas[0], celdas[0]); celda(page, rutas[1], celdas[1])
        union = fitz.Rect(celdas[0].x0, celdas[0].y0, celdas[1].x1, celdas[1].y1)
        etiqueta(page, union, n, sec['acento'], centrada=True)
        return
    for it, r in zip(fila, celdas):
        pinta_celda(page, it, r, sec)


def filas_de(items):
    pend = list(items); filas = []
    while pend:
        it = pend.pop(0)
        if es_par(it):
            filas.append([it]); continue
        fila = [it]
        for j, cand in enumerate(pend):
            if not es_par(cand):
                fila.append(pend.pop(j)); break
        filas.append(fila)
    return filas


def nueva(doc, sec, num, evitar):
    page = doc.new_page(width=W, height=H)
    cabeza(page, sec, num, semilla=num * 7 + len(sec['titulo']), evitar=evitar)
    return page


def pagina_especial(doc, spec, sec, num):
    tipo, items = spec['pagina'], spec['items']
    if tipo == 'hero_port' and len(items) <= 3:
        tipo = 'hero_port3'
    if tipo in ('hero_port', 'hero_port3'):
        c = CEL[tipo]
        evitar = [c['hero']] + c['lado'] + (c.get('abajo') or [])
        page = nueva(doc, sec, num, evitar)
        pinta_celda(page, items[0], c['hero'], sec, grande=True)
        for it, r in zip(items[1:3], c['lado']):
            pinta_celda(page, it, r, sec)
        if tipo == 'hero_port' and items[3:]:
            pinta_fila(page, items[3:5], c['abajo'], sec)
    elif tipo == 'hero_land':
        c = CEL['hero_land']
        page = nueva(doc, sec, num, [c['hero']] + c['abajo'])
        pinta_celda(page, items[0], c['hero'], sec, grande=True)
        pinta_fila(page, items[1:3], c['abajo'], sec)
    elif tipo == 'grandes':
        page = nueva(doc, sec, num, CEL['grandes'])
        for it, r in zip(items[:2], CEL['grandes']):
            pinta_celda(page, it, r, sec, grande=True)
    elif tipo == 'grid':
        filas = filas_de(items)
        pagina_filas(doc, sec, num, filas[:2])
    return num + 1


def pagina_filas(doc, sec, num, filas):
    """Una hoja con 1 o 2 filas. Con una sola fila, las fotos van más altas (dúo)."""
    if len(filas) == 1:
        page = nueva(doc, sec, num, CEL['duo'])
        pinta_fila(page, filas[0], CEL['duo'], sec)
    else:
        page = nueva(doc, sec, num, CEL['grid'][0] + CEL['grid'][1])
        for k, fila in enumerate(filas[:2]):
            pinta_fila(page, fila, CEL['grid'][k], sec)
    return page


def seccion(doc, sec, num):
    items = list(sec['items'])
    if items and not isinstance(items[0], dict):
        hero = items.pop(0)
        c = CEL['hero_land']
        page = nueva(doc, sec, num, [c['hero']] + c['abajo']); num += 1
        pinta_celda(page, hero, c['hero'], sec, grande=True)
        primeros = []
        while items and len(primeros) < 2 and not (isinstance(items[0], dict) and 'pagina' in items[0]):
            if es_par(items[0]):
                if not primeros:
                    primeros = [items.pop(0)]
                break
            primeros.append(items.pop(0))
        if primeros:
            pinta_fila(page, primeros, c['abajo'], sec)

    def vaciar(pendientes, num):
        filas = filas_de(pendientes)
        while filas:
            pagina_filas(doc, sec, num, filas[:2]); filas = filas[2:]; num += 1
        return num

    pendientes = []
    for it in items:
        if isinstance(it, dict) and 'pagina' in it:
            num = vaciar(pendientes, num); pendientes = []
            num = pagina_especial(doc, it, sec, num)
        else:
            pendientes.append(it)
    return vaciar(pendientes, num)


# ═══════════════════════════════════════════════════════════════
#  PORTADA, PORTADILLAS, CONTRAPORTADA
# ═══════════════════════════════════════════════════════════════
def mosaico(page, rutas, y0, y1, gutter=12):
    cw = (W - 2 * M - 2 * gutter) / 3; ch = (y1 - y0 - gutter) / 2
    for i, p in enumerate(rutas[:6]):
        x = M + (i % 3) * (cw + gutter); y = y0 + (i // 3) * (ch + gutter)
        celda(page, p, fitz.Rect(x, y, x + cw, y + ch), foco=0.15, marco=5, r=8)


def portada(doc, grad, titulo1, titulo2, lema, rutas, navidad=False):
    page = doc.new_page(width=W, height=H)
    degradado(page, *grad); confeti(page, 2026, 110)
    mosaico(page, rutas, 46, 452)
    imagen_compartida(page, fitz.Rect(M, 486, M + 74, 560), 'logo', png_logo)
    texto(page, 'CC ENTERTAINMENT', 500, 22, 'B', WHITE, x=M + 88, tracking=0.14)
    texto(page, 'PRODUCCIÓN DE ESPECTÁCULOS TEMÁTICOS', 534, 8, 'B', YELLOW, x=M + 88, tracking=0.2)
    texto(page, titulo1, 596, 50, 'B', WHITE, x=M)
    texto(page, titulo2, 652, 50, 'B', YELLOW, x=M)
    texto(page, lema, 724, 10, 'B', WHITE, x=M, tracking=0.2)
    barra_marca(page, M, 790, w=130, grosor=3.2)
    texto(page, f'{TEL}  ·  {IG}  ·  {WEB}', 782, 8.5, 'M', WHITE, x=W - M, alinear='der', opacidad=0.9)
    if navidad:
        campana(page, W - M - 24, 512, 1.2, GOLD); copo(page, W - M - 80, 500, 8); copo(page, W - M - 50, 548, 6)
        lucecitas(page, M, W - M, 760, 30)
    return page


def portadilla(doc, sec):
    page = doc.new_page(width=W, height=H)
    degradado(page, *sec['grad']); confeti(page, 500 + int(sec['num']), 80, [fitz.Rect(M, 60, W - M, 470)])
    celda(page, sec['imagen'], fitz.Rect(M, 70, W - M, 470), foco=0.2, marco=7, r=14)
    texto(page, sec['num'], 486, 92, 'B', WHITE, x=M - 3, opacidad=0.3)
    texto(page, sec['titulo'], 590, 42, 'B', WHITE, x=M)
    redondeado(page, fitz.Rect(M, 650, M + 60, 654.5), 2, fill=sec['acento'])
    pie(page)
    if sec.get('navidad'):
        campana(page, W - M - 24, 500, 1.1, GOLD); copo(page, W - M - 70, 492, 8)


def contraportada(doc, grad, ruta_foto, navidad=False):
    page = doc.new_page(width=W, height=H)
    degradado(page, *grad); confeti(page, 9090, 90, [fitz.Rect(M, 30, W - M, 410)])
    celda(page, ruta_foto, fitz.Rect(M, 46, W - M, 400), foco=0.25, marco=7, r=14)
    texto(page, 'Convertimos tu evento', 440, 32, 'B', WHITE, x=M)
    texto(page, 'en un espectáculo', 478, 32, 'B', YELLOW, x=M)
    redondeado(page, fitz.Rect(M, 546, M + 126, 672), 10, fill=WHITE)
    imagen_compartida(page, fitz.Rect(M + 9, 555, M + 117, 663), 'qr', png_qr)
    texto(page, 'ESCANEA Y COTIZA TU SHOW', 552, 7.5, 'B', YELLOW, x=M + 146, tracking=0.2)
    texto(page, WEB, 568, 17, 'B', WHITE, x=M + 146)
    texto(page, f'WhatsApp  {TEL}', 608, 12.5, 'B', WHITE, x=M + 146)
    texto(page, f'Instagram  {IG}', 632, 12.5, 'B', WHITE, x=M + 146)
    texto(page, 'Santo Domingo · República Dominicana', 660, 9, 'M', WHITE, x=M + 146, opacidad=0.85)
    barra_marca(page, M, 790, w=130, grosor=3.2)
    texto(page, 'CC Entertainment · Producción de espectáculos temáticos', 782, 8, 'M', WHITE, x=W - M, alinear='der', opacidad=0.9)
    if navidad:
        lucecitas(page, M, W - M, 760, 30); copo(page, W - M - 30, 450, 8)


# ═══════════════════════════════════════════════════════════════
def catalogo_general():
    doc = fitz.open()
    portada(doc, GRAD_PORTADA, 'Catálogo de', 'Temáticas', 'HORAS LOCAS  ·  SHOWS TEMÁTICOS  ·  2026', MOSAICO_PORTADA)
    num = 1
    for sec in SECCIONES:
        portadilla(doc, sec)
        num = seccion(doc, sec, num)
    contraportada(doc, GRAD_PORTADA, t('vegas', 6))
    return doc


def catalogo_navidad():
    doc = fitz.open()
    sec = dict(num='01', titulo='Navidad', etiqueta='EDICIÓN NAVIDAD', grad=('0F5132', '2E9E5B'), acento=YELLOW, items=NAVIDAD,
               imagen=t('navidad', 12), navidad=True)
    portada(doc, GRAD_NAVIDAD, 'Edición', 'Navidad', 'SHOWS NAVIDEÑOS  ·  HORAS LOCAS  ·  2026', MOSAICO_NAVIDAD, navidad=True)
    seccion(doc, sec, 1)
    contraportada(doc, GRAD_NAVIDAD, t('navidad', 10), navidad=True)
    return doc


def hoja(pdf, destino):
    doc = fitz.open(pdf); Wt = 190; Ht = int(Wt * H / W); cols = 7
    filas = (doc.page_count + cols - 1) // cols
    sheet = Image.new('RGB', (cols * (Wt + 8) + 8, filas * (Ht + 8) + 8), (60, 60, 60))
    for i, p in enumerate(doc):
        pix = p.get_pixmap(matrix=fitz.Matrix(Wt / W, Wt / W))
        sheet.paste(Image.frombytes('RGB', (pix.width, pix.height), pix.samples), (8 + (i % cols) * (Wt + 8), 8 + (i // cols) * (Ht + 8)))
    sheet.save(destino, quality=82)


if __name__ == '__main__':
    rutas = []
    for s in SECCIONES:
        for it in s['items']:
            grupo = it['items'] if isinstance(it, dict) and 'pagina' in it else [it]
            for x in grupo:
                img = norm(x)[1]
                rutas += img if isinstance(img, list) else [img]
    faltan = [r for r in rutas if not os.path.exists(r)]
    if faltan:
        sys.exit('FALTAN FOTOS: ' + ', '.join(faltan))
    g = catalogo_general(); g.save('CC-Entertainment-Catalogo-Tematicas.pdf', garbage=4, deflate=True)
    n = catalogo_navidad(); n.save('CC-Entertainment-Catalogo-Navidad.pdf', garbage=4, deflate=True)
    print(f'General: {g.page_count} páginas, {os.path.getsize("CC-Entertainment-Catalogo-Tematicas.pdf")/1e6:.1f} MB')
    print(f'Navidad: {n.page_count} páginas, {os.path.getsize("CC-Entertainment-Catalogo-Navidad.pdf")/1e6:.1f} MB')
    if '--hoja' in sys.argv:
        d = sys.argv[sys.argv.index('--hoja') + 1]; os.makedirs(d, exist_ok=True)
        hoja('CC-Entertainment-Catalogo-Tematicas.pdf', os.path.join(d, 'general-HOJA.jpg'))
        hoja('CC-Entertainment-Catalogo-Navidad.pdf', os.path.join(d, 'navidad-HOJA.jpg'))
        print('hojas en', d)
