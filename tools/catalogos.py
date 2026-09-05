# -*- coding: utf-8 -*-
"""Catálogos PDF de CC Entertainment — diseño OSCURO (como la página web), fotos SIN recorte.

    python tools/catalogos.py            -> PDFs en la raíz del repo
    python tools/catalogos.py --hoja DIR -> además, hojas de contacto para revisar

Cada foto se coloca completa: el marco se adapta a sus proporciones (nunca se corta).
Las filas fluyen: dos fotos por fila (o una a lo ancho si es horizontal y va destacada),
y la altura de cada fila la marca la foto más alta. Solo fotos y nombres.
Tipos de elemento:
  ('Nombre', 'ruta.jpg')                  -> una foto
  ('Nombre', ['a.jpg', 'b.jpg'])          -> dos fotos con un solo nombre centrado
  ANCHO('Nombre', 'ruta.jpg')             -> foto horizontal a todo lo ancho
  PAGINA('hero_port', [...])              -> hoja completa: 1 foto grande a la izquierda + 2 al lado (+ 2 abajo)
"""
import io, os, sys, math
import fitz
from PIL import Image, ImageOps

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)
FUENTES = os.path.join(RAIZ, 'tools', 'fonts')
T = 'assets/img/tematicas'


def hx(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


# ─── paleta de la página web ───
BG = hx('0b0b0e'); TXT = hx('f3f2f5'); MUTED = hx('9c99a8'); LINE = hx('2a2a33')
GOLD = hx('f5c542'); CYAN = hx('2fd0ff'); MAGENTA = hx('ff2fb0'); LIME = hx('cdea1f'); VIOLET = hx('a06bf5')
RED = hx('e63946'); GREEN = hx('1a9a50'); SILVER = hx('d4d9e6')
ARCOIRIS = [GOLD, CYAN, MAGENTA, LIME, VIOLET]

W, H = 595, 842
M = 42
ANCHO_UTIL = W - 2 * M          # 511
COL = (ANCHO_UTIL - 18) / 2     # 246.5 por columna
TEL = '(829) 343-5460'
IG = '@horaloca_cce'
WEB = 'horaloca-cce.vercel.app'


# ═══════════════════════════════════════════════════════════════
#  CONTENIDO
# ═══════════════════════════════════════════════════════════════
def t(d, n):
    return f'{T}/{d}/{n:02d}.jpg'


def ANCHO(nombre, img):
    return {'n': nombre, 'img': img, 'ancho': True}


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
    ANCHO('Dorado', 'assets/img/destacado/dorado-4.jpg'),
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
    ('Años 80', t('anos-80', 2)),
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
    ANCHO('Show LED', t('led-show', 3)),
    ('Zancos LED', t('led-show', 1)),
    ('Alas LED', t('alas-led', 3)),
    ('Alas LED', t('alas-led', 1)),
    ('Robot LED espejo', t('robot-espejo', 2)),
    ('Show LED — escena', t('led-show', 4)),
    ('Show LED — tambores', t('led-show', 2)),
]

DOMINICANO = [
    ANCHO('Carnaval Dominicano', 'assets/img/ig/carnaval.jpg'),
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

NAVIDAD = [   # las cuatro horizontales van a lo ancho, alternadas con las verticales
    ANCHO('Show Navidad completo', t('navidad', 12)),
    ('Cascanueces y elfa', t('navidad', 15)),
    ('Pareja Candy', t('navidad', 18)),
    ANCHO('Santa y los elfos', t('navidad', 9)),
    ('Elfa roja', t('navidad', 16)),
    ('Cocineros navideños', t('navidad', 19)),
    ANCHO('El Grinch y la galleta', t('navidad', 11)),
    ('Santa y sus ayudantes', t('navidad', 13)),
    ('Santa', t('navidad', 7)),
    ANCHO('Santa con elfos y galleta', t('navidad', 10)),
    ('Chicas de Santa', t('navidad', 2)),
    ('Soldados de juguete', t('navidad', 4)),
    ('Zancos navideños', t('navidad', 5)),
    ('Alas LED navideñas', t('navidad', 6)),
    ('Blanca Navidad', t('blanca-navidad', 1)),
    ('Cascanueces y Santa', t('navidad', 3)),
]

EXTRAS = [
    ANCHO('Zanqueros', 'assets/img/promo/zancos.jpg'),
    ('Percusión en vivo', 'assets/img/promo/musicos.jpg'),
    ('Coreografía personalizada', 'assets/img/destacado/plata-1.jpg'),
    ('Robot LED', 'assets/img/promo/robot-espejo.jpg'),
    ('Bailarines adicionales', 'assets/img/promo/bailarinas-led.jpg'),
]

SECCIONES = [
    dict(num='01', titulo='Disco Ball', etiqueta='DISCO BALL', color=SILVER, items=DISCO_BALL),
    dict(num='02', titulo='Temáticas', etiqueta='TEMÁTICAS', color=GOLD, items=TEMATICAS),
    dict(num='03', titulo='Show LED', etiqueta='SHOW LED', color=CYAN, items=SHOW_LED),
    dict(num='04', titulo='Ritmo Dominicano', etiqueta='RITMO DOMINICANO', color=RED, items=DOMINICANO),
    dict(num='05', titulo='Navidad', etiqueta='NAVIDAD', color=GREEN, items=NAVIDAD, navidad=True),
    dict(num='06', titulo='Extras para tu show', etiqueta='EXTRAS', color=VIOLET, items=EXTRAS),
]


# ═══════════════════════════════════════════════════════════════
#  TIPOGRAFÍA
# ═══════════════════════════════════════════════════════════════
ARCHIVO_FUENTE = {'B': 'Outfit-Bold.ttf', 'S': 'Outfit-SemiBold.ttf', 'M': 'Outfit-Medium.ttf', 'L': 'Outfit-Light.ttf'}
_FONT = {k: fitz.Font(fontfile=os.path.join(FUENTES, v)) for k, v in ARCHIVO_FUENTE.items()}


def ancho_txt(s, k, size):
    return _FONT[k].text_length(s, fontsize=size)


def texto(page, s, y, size, k='M', color=TXT, x=None, alinear='izq', opacidad=1.0):
    """y = borde superior del texto. x=None centra en la página."""
    w = ancho_txt(s, k, size)
    if x is None:
        px = (W - w) / 2
    elif alinear == 'der':
        px = x - w
    elif alinear == 'centro':
        px = x - w / 2
    else:
        px = x
    page.insert_text((px, y + size * 0.78), s, fontname='ou' + k, fontfile=os.path.join(FUENTES, ARCHIVO_FUENTE[k]),
                     fontsize=size, color=color, fill_opacity=opacidad)
    return w


def linea(page, x0, y, x1, color, grosor=2):
    page.draw_line((x0, y), (x1, y), color=color, width=grosor)


def arcoiris(page, x0, x1, y, grosor=2):
    seg = (x1 - x0) / len(ARCOIRIS)
    for i, c in enumerate(ARCOIRIS):
        linea(page, x0 + i * seg, y, x0 + (i + 1) * seg, c, grosor)


# ═══════════════════════════════════════════════════════════════
#  IMÁGENES (sin recorte)
# ═══════════════════════════════════════════════════════════════
_tam = {}
_cache = {}


def tam(path):
    if path not in _tam:
        _tam[path] = ImageOps.exif_transpose(Image.open(path)).size
    return _tam[path]


def ajustar(path, w_max, h_max):
    """Tamaño de la foto completa dentro de w_max × h_max, sin recortar."""
    w, h = tam(path)
    e = min(w_max / w, h_max / h)
    return w * e, h * e


def es_horizontal(path, umbral=1.25):
    w, h = tam(path)
    return w / h >= umbral


def jpeg(path, w_pt, h_pt, escala=2.0):
    key = (path, round(w_pt), round(h_pt))
    if key not in _cache:
        im = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
        im = im.resize((max(1, int(w_pt * escala)), max(1, int(h_pt * escala))), Image.LANCZOS)
        b = io.BytesIO(); im.save(b, 'JPEG', quality=84, optimize=True, progressive=True)
        _cache[key] = b.getvalue()
    return _cache[key]


def redondeado(page, rect, r, fill=None, color=None, width=0.6, opacidad=1.0):
    sh = page.new_shape()
    sh.draw_rect(rect, radius=r / min(rect.width, rect.height))
    sh.finish(color=color, fill=fill, width=width, fill_opacity=opacidad, stroke_opacity=opacidad)
    sh.commit()


def esquinas(page, rect, r, fondo=BG):
    x0, y0, x1, y1 = rect.x0, rect.y0, rect.x1, rect.y1
    for (cx, cy, ax, ay, bx, by) in [(x0, y0, x0 + r, y0, x0, y0 + r), (x1, y0, x1 - r, y0, x1, y0 + r),
                                     (x1, y1, x1 - r, y1, x1, y1 - r), (x0, y1, x0 + r, y1, x0, y1 - r)]:
        sh = page.new_shape()
        sh.draw_line((cx, cy), (ax, ay)); sh.draw_curve((ax, ay), (cx, cy), (bx, by)); sh.draw_line((bx, by), (cx, cy))
        sh.finish(color=fondo, fill=fondo, width=0.3, closePath=True); sh.commit()


def foto_en(page, path, rect, r=8):
    """Dibuja la foto completa ocupando exactamente rect (ya ajustado a su proporción)."""
    page.insert_image(rect, stream=jpeg(path, rect.width, rect.height))
    esquinas(page, rect, r)
    redondeado(page, rect, r, color=(1, 1, 1), width=0.6, opacidad=0.10)


def jpeg_recorte(path, rect, foco=0.18, escala=2.0):
    """Recorta la foto a la proporción de rect (centrado; en vertical sesgado arriba)."""
    key = ('rec', path, round(rect.width), round(rect.height), foco)
    if key not in _cache:
        im = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
        r_cel = rect.width / rect.height; r_im = im.width / im.height
        if r_im > r_cel:
            nw = int(im.height * r_cel); x0 = (im.width - nw) // 2
            im = im.crop((x0, 0, x0 + nw, im.height))
        else:
            nh = int(im.width / r_cel); y0 = int((im.height - nh) * foco)
            im = im.crop((0, y0, im.width, y0 + nh))
        im = im.resize((int(rect.width * escala), int(rect.height * escala)), Image.LANCZOS)
        b = io.BytesIO(); im.save(b, 'JPEG', quality=84, optimize=True, progressive=True)
        _cache[key] = b.getvalue()
    return _cache[key]


MAX_RECORTE = 0.25   # como mucho se sacrifica un cuarto de la foto; si hace falta más, va completa


def foto_auto(page, path, caja, foco=0.18, r=8, alinear='centro'):
    """Llena la caja recortando un poco la foto; si habría que cortar demasiado, la pone completa."""
    r_im = ratio(path); r_caja = caja.width / caja.height
    corte = 1 - min(r_im, r_caja) / max(r_im, r_caja)
    if corte <= MAX_RECORTE:
        page.insert_image(caja, stream=jpeg_recorte(path, caja, foco))
        esquinas(page, caja, r)
        redondeado(page, caja, r, color=(1, 1, 1), width=0.6, opacidad=0.10)
        return caja
    return foto_ajustada(page, path, caja, alinear, r)


def foto_ajustada(page, path, caja, alinear='abajo', r=8):
    """Encaja la foto completa dentro de la caja (centrada en horizontal). Devuelve el rect real."""
    w, h = ajustar(path, caja.width, caja.height)
    x0 = caja.x0 + (caja.width - w) / 2
    if alinear == 'abajo':
        y0 = caja.y1 - h
    elif alinear == 'centro':
        y0 = caja.y0 + (caja.height - h) / 2
    else:
        y0 = caja.y0
    rect = fitz.Rect(x0, y0, x0 + w, y0 + h)
    foto_en(page, path, rect, r)
    return rect


_xref = {}


def imagen_compartida(page, rect, key, bytes_fn):
    doc_key = (id(page.parent), key)
    if doc_key in _xref:
        page.insert_image(rect, xref=_xref[doc_key])
    else:
        _xref[doc_key] = page.insert_image(rect, stream=bytes_fn())


def png_plumas(alpha):
    im = Image.open('assets/img/logo-mark-glow.png').convert('RGBA')
    im.putalpha(im.getchannel('A').point(lambda v: int(v * alpha)))
    b = io.BytesIO(); im.save(b, 'PNG'); return b.getvalue()


def png_qr():
    import qrcode
    im = qrcode.make('https://' + WEB, box_size=10, border=1).convert('RGB')
    b = io.BytesIO(); im.save(b, 'PNG'); return b.getvalue()


# ═══════════════════════════════════════════════════════════════
#  ELEMENTOS DE PÁGINA (diseño original oscuro)
# ═══════════════════════════════════════════════════════════════
def fondo(page):
    page.draw_rect(page.rect, color=None, fill=BG)


def plumas(page, rect, alpha):
    imagen_compartida(page, rect, ('plumas', alpha), lambda: png_plumas(alpha))


def cabeza(page, sec, numero):
    fondo(page)
    plumas(page, fitz.Rect(110, 196, 485, 626), 0.10)
    texto(page, 'CC ENTERTAINMENT', 36, 10, 'B', TXT, x=M)
    texto(page, sec['etiqueta'], 52, 7.5, 'M', sec['color'], x=M)
    texto(page, f'{numero:02d}', 41, 11, 'B', GOLD, x=W - M, alinear='der')
    arcoiris(page, M, W - M, 69, 2)
    texto(page, f'{TEL} · {IG}', 804, 7.5, 'M', MUTED, x=M)
    if sec.get('navidad'):
        campana(page, 505, 46, 0.75); lucecitas(page, 48, 547, 72, 24)
        copo(page, 50, 790, 7); copo(page, 545, 785, 7)


def etiqueta(page, x, y, nombre, color, grande=False, centro=None):
    """Guion de color + nombre. y = borde superior del texto."""
    ts = 19 if grande else 14
    dx, gl = (48, 30) if grande else (34, 22)
    if centro is not None:
        w = ancho_txt(nombre, 'S', ts)
        x_txt = centro - (w + gl + 8) / 2 + gl + 8
        linea(page, x_txt - gl - 8, y + ts * 0.55, x_txt - 8, color, 2.5)
        texto(page, nombre, y, ts, 'S', TXT, x=x_txt)
        return
    linea(page, x, y + ts * 0.55, x + gl, color, 2.5)
    texto(page, nombre, y, ts, 'S', TXT, x=x + dx)


# ─── decoración navideña (como el original) ───
def campana(page, cx, cy, s=1.0, color=GOLD):
    sh = page.new_shape()
    sh.draw_line((cx, cy - 22 * s), (cx, cy - 17 * s)); sh.draw_circle((cx, cy - 22 * s), 2 * s)
    sh.draw_bezier((cx - 12 * s, cy + 6 * s), (cx - 12 * s, cy - 14 * s), (cx + 12 * s, cy - 14 * s), (cx + 12 * s, cy + 6 * s))
    sh.draw_line((cx - 15 * s, cy + 6 * s), (cx + 15 * s, cy + 6 * s))
    sh.finish(color=color, width=1.3 * s)
    sh.draw_circle((cx, cy + 9 * s), 2.2 * s); sh.finish(color=color, fill=color, width=0.5); sh.commit()


def copo(page, cx, cy, r=7, color=SILVER):
    sh = page.new_shape()
    for i in range(6):
        a = math.radians(i * 60); x1, y1 = cx + r * math.cos(a), cy + r * math.sin(a)
        sh.draw_line((cx, cy), (x1, y1))
        for lado in (-1, 1):
            b = a + lado * math.radians(35); xm, ym = cx + r * 0.6 * math.cos(a), cy + r * 0.6 * math.sin(a)
            sh.draw_line((xm, ym), (xm + r * 0.3 * math.cos(b), ym + r * 0.3 * math.sin(b)))
    sh.finish(color=color, width=0.7); sh.commit()


def lucecitas(page, x0, x1, y, n=24):
    colores = [RED, GREEN, GOLD, CYAN, MAGENTA]
    paso = (x1 - x0) / (n - 1); sh = page.new_shape()
    for i in range(n):
        sh.draw_circle((x0 + i * paso, y + (3 if i % 2 else 6)), 1.6); sh.finish(color=colores[i % 5], fill=colores[i % 5], width=0.3)
    sh.commit()


# ═══════════════════════════════════════════════════════════════
#  MAQUETACIÓN FLUIDA
# ═══════════════════════════════════════════════════════════════
Y_INI = 88          # primera fila bajo la cabecera
Y_FIN = 782         # límite inferior (encima del pie)
ALTO_MAX = 300      # alto máximo de una foto en fila de dos (2 filas por hoja)
ALTO_ANCHO = 280    # alto máximo de una foto a lo ancho (deja sitio a otra fila debajo)
GAP_FILA = 52       # nombre + aire entre filas
GAP_PAR = 18        # separación entre las dos fotos de una fila


def norm(it):
    if isinstance(it, dict):
        return it['n'], it['img'], it.get('ancho', False)
    return it[0], it[1], False


def es_par(it):
    return isinstance(it, tuple) and isinstance(it[1], list)


def es_pagina(it):
    return isinstance(it, dict) and 'pagina' in it


ALTO_MIN_PAR = 200   # si dos fotos juntas quedan más bajas que esto, van una por fila a lo ancho


def ratio(path):
    w, h = tam(path)
    return w / h


def ratio(path):
    w, h = tam(path)
    return w / h


def es_horizontal_item(it):
    n, img, ancho = norm(it)
    return ancho or ratio(img) >= 1.0


def filas_de(items):
    """Verticales de dos en dos (celdas iguales); horizontales solas a todo lo ancho."""
    pend = list(items); filas = []
    while pend:
        it = pend.pop(0)
        if es_par(it) or es_horizontal_item(it):
            filas.append([it]); continue
        fila = [it]
        for j, cand in enumerate(pend):
            if not es_par(cand) and not es_horizontal_item(cand):
                fila.append(pend.pop(j)); break
        filas.append(fila)
    return filas


def alto_fila(fila):
    if len(fila) == 1 and not es_par(fila[0]) and es_horizontal_item(fila[0]):
        n, img, ancho = norm(fila[0])
        return min(ALTO_ANCHO, ANCHO_UTIL / ratio(img))
    return ALTO_MAX


def pinta_fila(page, fila, y, alto, sec):
    """Celdas del mismo tamaño en la fila; el nombre debajo de cada foto."""
    if len(fila) == 1 and es_par(fila[0]):
        nombre, rutas = fila[0]
        for k, p in enumerate(rutas):
            caja = fitz.Rect(M + k * (COL + GAP_PAR), y, M + k * (COL + GAP_PAR) + COL, y + alto)
            foto_auto(page, p, caja, alinear='abajo')
        etiqueta(page, 0, y + alto + 10, nombre, sec['color'], centro=W / 2)
        return
    if len(fila) == 1 and es_horizontal_item(fila[0]):
        nombre, img, ancho = norm(fila[0])
        r = foto_auto(page, img, fitz.Rect(M, y, W - M, y + alto), alinear='abajo')
        etiqueta(page, r.x0, y + alto + 10, nombre, sec['color'], grande=True)
        return
    if len(fila) == 1:                                   # vertical suelta: centrada
        nombre, img, _ = norm(fila[0])
        x0 = M + (ANCHO_UTIL - COL) / 2
        r = foto_auto(page, img, fitz.Rect(x0, y, x0 + COL, y + alto), alinear='abajo')
        etiqueta(page, r.x0, y + alto + 10, nombre, sec['color'])
        return
    for k, it in enumerate(fila):
        nombre, img, _ = norm(it)
        caja = fitz.Rect(M + k * (COL + GAP_PAR), y, M + k * (COL + GAP_PAR) + COL, y + alto)
        r = foto_auto(page, img, caja, alinear='abajo')
        etiqueta(page, r.x0, y + alto + 10, nombre, sec['color'])


def pagina_hero_port(doc, items, sec, num):
    """Hoja completa: foto grande a la izquierda, dos apiladas a la derecha y (opcional) dos abajo."""
    page = doc.new_page(width=W, height=H); cabeza(page, sec, num)
    tres = len(items) <= 3
    hero = fitz.Rect(M, Y_INI, 322, 700 if tres else 500)
    lados = [fitz.Rect(334, Y_INI, W - M, 372 if tres else 268), fitz.Rect(334, 424 if tres else 320, W - M, 700 if tres else 500)]
    r = foto_auto(page, items[0][1], hero, alinear='centro')
    etiqueta(page, r.x0, r.y1 + 12, items[0][0], sec['color'], grande=True)
    for it, caja in zip(items[1:3], lados):
        r = foto_auto(page, it[1], caja, alinear='abajo')
        etiqueta(page, r.x0, caja.y1 + 8, it[0], sec['color'])
    if not tres and items[3:]:
        y0 = 560; alto = 200
        for k, it in enumerate(items[3:5]):
            caja = fitz.Rect(M + k * (COL + GAP_PAR), y0, M + k * (COL + GAP_PAR) + COL, y0 + alto)
            r = foto_auto(page, it[1], caja, alinear='abajo')
            etiqueta(page, r.x0, y0 + alto + 10, it[0], sec['color'])
    return num + 1


def seccion(doc, sec, num):
    """Maqueta la sección con filas fluidas; las PAGINA se insertan como hojas completas."""
    pendientes = []

    def vaciar(pendientes, num):
        filas = filas_de(pendientes)
        page = None; y = Y_INI
        for fila in filas:
            alto = alto_fila(fila)
            if page is None or y + alto + 28 > Y_FIN:
                page = doc.new_page(width=W, height=H); cabeza(page, sec, num); num += 1; y = Y_INI
            pinta_fila(page, fila, y, alto, sec)
            y += alto + GAP_FILA
        return num

    for it in sec['items']:
        if es_pagina(it):
            if pendientes:
                num = vaciar(pendientes, num); pendientes = []
            num = pagina_hero_port(doc, it['items'], sec, num)
        else:
            pendientes.append(it)
    if pendientes:
        num = vaciar(pendientes, num)
    return num


# ═══════════════════════════════════════════════════════════════
#  PORTADA, PORTADILLAS, CONTRAPORTADA (diseño original)
# ═══════════════════════════════════════════════════════════════
def portada(doc, titulo, lema, color_lema, navidad=False):
    page = doc.new_page(width=W, height=H); fondo(page)
    page.insert_image(fitz.Rect(178, 130, 417, 405), filename='assets/img/logo-mark-glow.png')
    texto(page, 'CC ENTERTAINMENT', 425, 34, 'B')
    texto(page, 'PRODUCCIÓN DE ESPECTÁCULOS TEMÁTICOS', 474, 9.5, 'M', MUTED)
    if navidad:
        for i, c in enumerate([GREEN, RED, GOLD]):
            linea(page, 187 + i * 74, 508, 187 + (i + 1) * 74 - 4, c, 2.5)
    else:
        arcoiris(page, 187, 408, 508, 2.5)
    texto(page, titulo, 543, 30, 'L')
    texto(page, lema, 590, 11, 'S', color_lema)
    texto(page, 'República Dominicana', 752, 10.5, 'M', MUTED)
    texto(page, f'{TEL}  ·  {IG}', 786, 10.5, 'S')
    if navidad:
        campana(page, 95, 118, 1.4); campana(page, 500, 118, 1.4)
        for (x, y, r) in [(60, 300, 9), (535, 318, 9), (78, 560, 7), (515, 585, 7), (150, 690, 6), (438, 695, 6)]:
            copo(page, x, y, r)
        lucecitas(page, 150, 445, 706, 14)
    return page


def nombres_de(sec):
    out = []
    for it in sec['items']:
        grupo = it['items'] if es_pagina(it) else [it]
        for x in grupo:
            n = norm(x)[0]
            if n not in out:
                out.append(n)
    return out


def portadilla(doc, sec):
    page = doc.new_page(width=W, height=H); fondo(page)
    plumas(page, fitz.Rect(80, 161, 515, 661), 0.13)
    texto(page, sec['num'], 240, 60, 'B', sec['color'])
    texto(page, sec['titulo'], 326, 34, 'L')
    linea(page, 208, 388, 388, SILVER, 1.5)
    nombres = nombres_de(sec)
    if len(nombres) <= 12:
        y = 424
        for n in nombres:
            texto(page, n, y, 11.5, 'M', MUTED); y += 20
    else:                                   # dos columnas
        por_col = math.ceil(min(len(nombres), 26) / 2)
        for i, n in enumerate(nombres[:26]):
            col, fila = divmod(i, por_col)
            texto(page, n, 424 + fila * 17, 9.5, 'M', MUTED, x=W / 2 - 200 + col * 220)
        if len(nombres) > 26:
            texto(page, '…', 424 + por_col * 17, 9.5, 'M', MUTED, x=W / 2 - 200 + 220)
    texto(page, 'CC ENTERTAINMENT · CATÁLOGO DE TEMÁTICAS', 804, 7.5, 'M', MUTED, x=M)
    if sec.get('navidad'):
        campana(page, 505, 60, 0.9); copo(page, 60, 700, 8); copo(page, 535, 690, 8)


def contraportada(doc, navidad=False):
    page = doc.new_page(width=W, height=H); fondo(page)
    plumas(page, fitz.Rect(71, 151, 524, 671), 0.13)
    texto(page, 'Convertimos tu evento', 304, 26, 'L')
    texto(page, 'en un espectáculo', 336, 26, 'L')
    arcoiris(page, 208, 388, 388, 2.5)
    texto(page, 'Cotiza tu show a la medida:', 425, 11, 'M', MUTED)
    texto(page, WEB, 443, 13, 'S', CYAN)
    texto(page, f'WhatsApp {TEL}', 478, 12, 'S')
    texto(page, f'Instagram {IG}', 498, 12, 'S')
    # QR a la web
    redondeado(page, fitz.Rect(W / 2 - 52, 540, W / 2 + 52, 644), 8, fill=(1, 1, 1))
    imagen_compartida(page, fitz.Rect(W / 2 - 46, 546, W / 2 + 46, 638), 'qr', png_qr)
    texto(page, 'Escanea y cotiza tu show', 654, 8.5, 'M', MUTED)
    texto(page, 'CC Entertainment · Producción de espectáculos temáticos · República Dominicana', 774, 8.5, 'M', MUTED)
    if navidad:
        lucecitas(page, 150, 445, 706, 14); copo(page, 60, 300, 9); copo(page, 535, 318, 9)


# ═══════════════════════════════════════════════════════════════
def catalogo_general():
    doc = fitz.open()
    portada(doc, 'Catálogo de Temáticas', 'HORAS LOCAS · SHOWS TEMÁTICOS', GOLD)
    num = 1
    for sec in SECCIONES:
        portadilla(doc, sec)
        num = seccion(doc, sec, num)
    contraportada(doc)
    return doc


def catalogo_navidad():
    doc = fitz.open()
    sec = dict(num='01', titulo='Navidad', etiqueta='EDICIÓN NAVIDAD', color=GREEN, items=NAVIDAD, navidad=True)
    portada(doc, 'Edición Navidad', 'SHOWS NAVIDEÑOS · HORAS LOCAS', GREEN, navidad=True)
    seccion(doc, sec, 1)
    contraportada(doc, navidad=True)
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
            grupo = it['items'] if es_pagina(it) else [it]
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
