# -*- coding: utf-8 -*-
"""Genera los dos catálogos PDF de CC Entertainment a partir de las fotos
del sitio (assets/img). Correr desde cualquier carpeta:

    python tools/catalogos.py            -> PDFs en la raíz del repo
    python tools/catalogos.py --hoja DIR -> además, hojas de contacto para revisar

Diseño: A4 oscuro, tipografía Outfit (tools/fonts), fotos con esquinas
redondeadas, portadillas por sección con las plumas del logo como marca de agua.
Contenido: listas SECCIONES / NAVIDAD_GRANDES / NAVIDAD_GRID de abajo.
"""
import io, os, sys
import fitz
from PIL import Image, ImageDraw, ImageOps

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)
FUENTES = os.path.join(RAIZ, 'tools', 'fonts')
T = 'assets/img/tematicas'

# ─── paleta (la misma del sitio) ───
BG = (11/255, 11/255, 14/255)
TXT = (0xf3/255, 0xf2/255, 0xf5/255)
MUTED = (0x9c/255, 0x99/255, 0xa8/255)
SILVER = (0xd4/255, 0xd9/255, 0xe6/255)
GOLD = (0xf5/255, 0xc5/255, 0x42/255)
CYAN = (0x2f/255, 0xd0/255, 0xff/255)
MAGENTA = (0xff/255, 0x2f/255, 0xb0/255)
LIME = (0xcd/255, 0xea/255, 0x1f/255)
VIOLET = (0xa0/255, 0x6b/255, 0xf5/255)
RED = (0xe6/255, 0x39/255, 0x46/255)
GREEN = (0x1a/255, 0x9a/255, 0x50/255)
ARCOIRIS = [GOLD, CYAN, MAGENTA, LIME, VIOLET]

W, H = 595, 842
TEL = '(829) 343-5460'
IG = '@horaloca_cce'
WEB = 'horaloca-cce.vercel.app'

# ═══════════════════════════════════════════════════════════════
#  CONTENIDO — ('Nombre', 'ruta', 'subtítulo')  |  sub '' = etiqueta por defecto
#  Un par con título centrado: ('Nombre', ['ruta1', 'ruta2'], 'subtítulo')
# ═══════════════════════════════════════════════════════════════
def t(d, n):
    return f'{T}/{d}/{n:02d}.jpg'


DISCO_BALL = [
    ('Disco Ball', f'{T}/espejos/main.jpg', 'El paquete plateado completo'),
    ('Disco Ball — gorras', t('espejos', 9), 'Trajes de espejos con gorras de cristal'),
    ('Disco Ball — salida', t('espejos', 11), 'Cabezas de bola disco con capas LED'),
    ('Chicas de espejos', 'assets/img/destacado/plata-1.jpg', ''),
    ('Hombre LED', 'assets/img/destacado/plata-2.jpg', ''),
    ('Hombre espejo', 'assets/img/destacado/plata-3.jpg', ''),
    ('Disco Ball — grupo', 'assets/img/destacado/plata-4.jpg', ''),
    ('Show en vivo', t('espejos', 1), 'Cabeza de bola disco en evento'),
    ('Show en vivo', t('espejos', 5), 'Disco Ball en evento'),
]

TEMATICAS = [
    ('Dorado', 'assets/img/destacado/dorado-4.jpg', ''),
    ('Shine Gold', t('shine-gold', 1), ''),
    ('Dorado — show girls', t('dorado', 6), 'Plumas y lentejuelas'),
    ('Brazil plateada', t('brasil-plata', 1), ''),
    ('Brazil', t('brazil', 1), ''),
    ('Viva las Vegas', t('vegas', 1), ''),
    ('Neón', t('neon', 5), ''),
    ('Neón — grupo', t('neon', 6), ''),
    ('Tropical', 'assets/img/ig/tropical-sunset.jpg', ''),
    ('Gatsby', t('gatsby', 1), ''),
    ('Neon 2000', t('neon-2000', 1), ''),
    ('Samba', t('samba', 1), ''),
    ('África', t('africa', 2), ''),
    ('Safari', [t('safari', 3), t('safari', 1)], 'Exploradores'),
    ('Tropical Cuba', t('tropical-cuba', 1), ''),
    ('Playa', t('playa', 1), ''),
    ('Hawaii', t('hawaii', 1), ''),
    ('Vaqueros', t('vaqueros', 1), ''),
    ('Porristas', t('porristas', 1), ''),
    ('Ingenieros', t('ingenieros', 1), ''),
    ('Cocineros', t('cocineros-show', 1), ''),
    ('Personajes para bienvenida', t('bienvenida', 1), ''),
    # recibimiento / host de entrada
    ('Viva las Vegas — host', t('vegas', 5), 'Recibimiento de entrada'),
    ('Bienvenida Blanca', t('bienvenida-blanca', 1), 'Recibimiento con rosas blancas'),
    ('Bienvenida Roja', t('bienvenida-roja', 1), 'Recibimiento con rosas rojas'),
    ('Bar Neón', t('bar-neon', 1), 'Hostess iluminada con bandeja de canapés'),
    ('Personaje de corazón', t('corazon', 1), ''),
    ('Personaje de playa', t('personaje-playa', 1), ''),
    ('Hadas', t('hadas', 1), ''),
    ('Astronauta y alien', t('astronauta', 1), ''),
    ('Cabezones', 'assets/img/promo/artistas.jpg', 'Bad Bunny, Karol G y Daddy Yankee'),
    ('Feria/Circo', [t('feria-circo', 1), t('feria-circo', 2)], 'Payasos y mimos'),
    ('Disco', t('disco', 1), ''),
    ('Años 80', t('anos-80', 1), ''),
    ('Años 90', t('anos-90', 1), ''),
    ('Brigeston', t('brigeston', 1), ''),
    ('Pilotos Formula 1', t('pilotos', 1), ''),
    ('Pilotos Formula 1 — pit stop', t('pilotos', 3), ''),
    ('Marineros', t('marineros', 1), ''),
    ('Mimos', t('mimos', 1), ''),
    ('Rouge Royal', t('rouge', 1), 'Lentejuelas rojas'),
    ('Rouge Royal — baile', t('rouge', 2), ''),
    ('Rouge Royal — pareja', t('rouge', 3), 'Show girl de cartas'),
    ('Catrinas', 'assets/img/catrinas.jpg', ''),
    ('Venezia', 'assets/img/ig/venetian.jpg', ''),
]

SHOW_LED = [
    ('Show LED', t('led-show', 3), 'Robots, tambores y zancos iluminados'),
    ('Zancos LED', t('led-show', 1), 'Zanquero iluminado en la pista'),
    ('Alas LED', t('alas-led', 3), 'Alas de luz desplegadas'),
    ('Alas LED', t('alas-led', 1), 'Show nocturno'),
    ('Bar Neón — en evento', t('bar-neon', 2), 'Canapés con luces en la pista'),
]

DOMINICANO = [
    ('Carnaval Dominicano', t('carnaval', 2), 'Con diablos cojuelos y lechones'),
    ('Diablos cojuelos', 'assets/img/ig/carnaval.jpg', 'Carnaval Dominicano'),
    ('Diablo cojuelo', 'assets/img/ig/carnaval-2.jpg', 'Carnaval Dominicano'),
]
# los zanqueros patrios entran solos cuando llegue la foto profesional
if os.path.exists(t('zanqueros-rd', 1)):
    DOMINICANO.append(('Zancos dominicanos', t('zanqueros-rd', 1), 'Con la bandera en alto'))
DOMINICANO += [
    ('Dominicana', t('dominicana', 1), 'Vestido de bandera'),
    ('Pareja dominicana', t('dominicana', 2), ''),
    ('Dominicana en evento', t('dominicana', 5), ''),
    ('Marchantas', t('marchantas', 1), ''),
    ('Marchanta', t('marchantas', 3), ''),
    ('Pelota dominicana', t('pelota', 3), 'Con las mascotas de los equipos'),
    ('Pelota dominicana', t('pelota', 1), 'Equipos de beisbol'),
    ('Pelota dominicana', t('pelota', 2), ''),
]

NAVIDAD_GRANDES = [   # horizontales, dos por página a todo lo ancho
    ('Show Navidad completo', t('navidad', 12), 'Grinch, Santa, galleta de jengibre y elfos'),
    ('Santa con elfos y galleta', t('navidad', 10), ''),
    ('El Grinch y la galleta', t('navidad', 11), ''),
    ('Santa y los elfos', t('navidad', 9), ''),
]
NAVIDAD_GRID = [
    ('Santa y sus ayudantes', t('navidad', 13), ''),
    ('Cascanueces y elfa', t('navidad', 15), 'Trío rojo y dorado'),
    ('Elfa roja', t('navidad', 16), ''),
    ('Pareja Candy', t('navidad', 18), 'Bastones de caramelo'),
    ('Cocineros navideños', t('navidad', 19), 'Con cuchara y palomitas gigantes'),
    ('Santa', t('navidad', 7), 'Con soldados de juguete y tambores'),
    ('Chicas de Santa', t('navidad', 2), ''),
    ('Soldados de juguete', t('navidad', 4), ''),
    ('Zancos navideños', t('navidad', 5), ''),
    ('Alas LED navideñas', t('navidad', 6), ''),
    ('Blanca Navidad', t('blanca-navidad', 1), ''),
]

EXTRAS = [
    ('Zanqueros', 'assets/img/promo/zancos.jpg', ''),
    ('Percusión en vivo', 'assets/img/promo/musicos.jpg', 'Tambores que encienden la pista'),
    ('Coreografía personalizada', 'assets/img/destacado/plata-1.jpg', 'Entradas, aperturas y sorpresas'),
    ('Robot LED', 'assets/img/promo/robot-espejo.jpg', ''),
    ('Bailarines adicionales', 'assets/img/promo/bailarinas-led.jpg', ''),
]

SECCIONES = [
    dict(num='01', titulo='Disco Ball', etiqueta='DISCO BALL', color=SILVER, defecto='HORA LOCA', items=DISCO_BALL),
    dict(num='02', titulo='Temáticas', etiqueta='TEMÁTICAS', color=GOLD, defecto='HORA LOCA', items=TEMATICAS,
         resumen='{n} temáticas para tu show'),
    dict(num='03', titulo='Show LED', etiqueta='SHOW LED', color=CYAN, defecto='SHOW LED', items=SHOW_LED),
    dict(num='04', titulo='Ritmo Dominicano', etiqueta='RITMO DOMINICANO', color=RED, defecto='HORA LOCA', items=DOMINICANO),
    dict(num='05', titulo='Navidad', etiqueta='NAVIDAD', color=GREEN, defecto='SHOW NAVIDEÑO', grandes=NAVIDAD_GRANDES,
         items=NAVIDAD_GRID, resumen='{n} temáticas para tu show'),
    dict(num='06', titulo='Extras para tu show', etiqueta='EXTRAS', color=VIOLET, defecto='EXTRA', items=EXTRAS),
]


# ═══════════════════════════════════════════════════════════════
#  TIPOGRAFÍA E IMÁGENES
# ═══════════════════════════════════════════════════════════════
ARCHIVO_FUENTE = {'B': 'Outfit-Bold.ttf', 'S': 'Outfit-SemiBold.ttf', 'M': 'Outfit-Medium.ttf', 'L': 'Outfit-Light.ttf'}
_FONT = {k: fitz.Font(fontfile=os.path.join(FUENTES, v)) for k, v in ARCHIVO_FUENTE.items()}
_con_fuentes = set()


def fuentes(page):
    if id(page) in _con_fuentes:
        return
    for k, v in ARCHIVO_FUENTE.items():
        page.insert_font(fontname='ou' + k, fontfile=os.path.join(FUENTES, v))
    _con_fuentes.add(id(page))


def ancho(s, k, size):
    return _FONT[k].text_length(s, fontsize=size)


def texto(page, s, y, size, k='M', color=TXT, x=None, alinear='centro'):
    """y = borde superior del texto (como en el PDF original). x=None centra en la página."""
    fuentes(page)
    w = ancho(s, k, size)
    if x is None:
        px = (W - w) / 2
    elif alinear == 'derecha':
        px = x - w
    else:
        px = x
    page.insert_text((px, y + size * 0.78), s, fontname='ou' + k,
                     fontfile=os.path.join(FUENTES, ARCHIVO_FUENTE[k]), fontsize=size, color=color)
    return w


def linea(page, x0, y, x1, color, grosor=2):
    page.draw_line((x0, y), (x1, y), color=color, width=grosor)


def arcoiris(page, x0, x1, y, grosor=2):
    seg = (x1 - x0) / len(ARCOIRIS)
    for i, c in enumerate(ARCOIRIS):
        linea(page, x0 + i * seg, y, x0 + (i + 1) * seg, c, grosor)


_cache = {}


def png_plumas(alpha):
    key = ('plumas', alpha)
    if key not in _cache:
        im = Image.open('assets/img/logo-mark-glow.png').convert('RGBA')
        a = im.getchannel('A').point(lambda v: int(v * alpha))
        im.putalpha(a)
        b = io.BytesIO(); im.save(b, 'PNG'); _cache[key] = b.getvalue()
    return _cache[key]


def foto(path, rect, escala=2.0):
    """Recorta la foto al alto/ancho de la celda (cover) y la encuadra un poco
    hacia arriba (caras). Devuelve JPEG en bytes (liviano)."""
    key = (path, round(rect.width), round(rect.height))
    if key in _cache:
        return _cache[key]
    im = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    cw, ch = rect.width * escala, rect.height * escala
    r_cel = cw / ch; r_im = im.width / im.height
    if r_im > r_cel:                      # sobra ancho: recorte centrado
        nw = int(im.height * r_cel); x0 = (im.width - nw) // 2
        im = im.crop((x0, 0, x0 + nw, im.height))
    else:                                 # sobra alto: recorte sesgado arriba (caras)
        nh = int(im.width / r_cel); sobra = im.height - nh; y0 = int(sobra * 0.18)
        im = im.crop((0, y0, im.width, y0 + nh))
    im = im.resize((int(cw), int(ch)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=84, optimize=True, progressive=True)
    _cache[key] = b.getvalue()
    return _cache[key]


def esquinas(page, rect, r=8):
    """Redondea las esquinas tapándolas con el color de fondo (la foto va en JPEG)."""
    x0, y0, x1, y1 = rect.x0, rect.y0, rect.x1, rect.y1
    for (cx, cy, ax, ay, bx, by) in [
        (x0, y0, x0 + r, y0, x0, y0 + r),   # arriba-izq
        (x1, y0, x1 - r, y0, x1, y0 + r),   # arriba-der
        (x1, y1, x1 - r, y1, x1, y1 - r),   # abajo-der
        (x0, y1, x0 + r, y1, x0, y1 - r),   # abajo-izq
    ]:
        sh = page.new_shape()
        sh.draw_line((cx, cy), (ax, ay))
        sh.draw_curve((ax, ay), (cx, cy), (bx, by))   # cuarto de arco (control en la esquina)
        sh.draw_line((bx, by), (cx, cy))
        sh.finish(color=BG, fill=BG, width=0.3, closePath=True)
        sh.commit()


def celda(page, path, rect, radio=8):
    page.insert_image(rect, stream=foto(path, rect))
    esquinas(page, rect, radio)


_xref_plumas = {}


def plumas(page, rect, alpha):
    """Marca de agua de plumas; la imagen se incrusta una sola vez por documento."""
    doc = page.parent
    key = (id(doc), alpha)
    if key in _xref_plumas:
        page.insert_image(rect, xref=_xref_plumas[key])
    else:
        _xref_plumas[key] = page.insert_image(rect, stream=png_plumas(alpha))


def etiqueta(page, rect, nombre, sub, color, defecto, grande=False, centrada=False):
    """Guion de color + nombre + subtítulo bajo una celda."""
    if grande:
        ts, ss, dx, gl = 19, 9, 48, 30
    else:
        ts, ss, dx, gl = 14, 8, 34, 22
    y_n = rect.y1 + 2 if grande else rect.y1 + 3
    if centrada:
        w = ancho(nombre, 'S', ts)
        x_txt = (rect.x0 + rect.x1) / 2 - (w + gl + 8) / 2 + gl + 8
        linea(page, x_txt - gl - 8, y_n + ts * 0.55, x_txt - 8, color, 2.5)
        texto(page, nombre, y_n, ts, 'S', TXT, x=x_txt)
        if sub:
            texto(page, sub, y_n + ts + 6, ss, 'M', color, x=(rect.x0 + rect.x1) / 2 - ancho(sub, 'M', ss) / 2)
        else:
            texto(page, defecto, y_n + ts + 7, 7, 'M', MUTED, x=(rect.x0 + rect.x1) / 2 - ancho(defecto, 'M', 7) / 2)
        return
    linea(page, rect.x0, y_n + ts * 0.55, rect.x0 + gl, color, 2.5)
    texto(page, nombre, y_n, ts, 'S', TXT, x=rect.x0 + dx)
    if sub:
        texto(page, sub, y_n + ts + 6, ss, 'M', color, x=rect.x0 + dx)
    else:
        texto(page, defecto, y_n + ts + 7, 7, 'M', MUTED, x=rect.x0 + dx)


# ═══════════════════════════════════════════════════════════════
#  DECORACIÓN NAVIDAD
# ═══════════════════════════════════════════════════════════════
def campana(page, cx, cy, s=1.0, color=GOLD):
    sh = page.new_shape()
    sh.draw_line((cx, cy - 22 * s), (cx, cy - 17 * s))
    sh.draw_circle((cx, cy - 22 * s), 2 * s)
    # cuerpo: arco superior + laterales + borde
    sh.draw_bezier((cx - 12 * s, cy + 6 * s), (cx - 12 * s, cy - 14 * s), (cx + 12 * s, cy - 14 * s), (cx + 12 * s, cy + 6 * s))
    sh.draw_line((cx - 15 * s, cy + 6 * s), (cx + 15 * s, cy + 6 * s))
    sh.draw_line((cx - 12 * s, cy + 6 * s), (cx - 15 * s, cy + 6 * s))
    sh.draw_line((cx + 12 * s, cy + 6 * s), (cx + 15 * s, cy + 6 * s))
    sh.finish(color=color, width=1.3 * s)
    sh.draw_circle((cx, cy + 9 * s), 2.2 * s)
    sh.finish(color=color, fill=color, width=0.5)
    sh.commit()


def copo(page, cx, cy, r=7, color=SILVER):
    import math
    sh = page.new_shape()
    for i in range(6):
        a = math.radians(i * 60)
        x1, y1 = cx + r * math.cos(a), cy + r * math.sin(a)
        sh.draw_line((cx, cy), (x1, y1))
        for lado in (-1, 1):
            b = a + lado * math.radians(35)
            xm, ym = cx + r * 0.6 * math.cos(a), cy + r * 0.6 * math.sin(a)
            sh.draw_line((xm, ym), (xm + r * 0.3 * math.cos(b), ym + r * 0.3 * math.sin(b)))
    sh.finish(color=color, width=0.7)
    sh.commit()


def lucecitas(page, x0, x1, y, n=24):
    colores = [RED, GREEN, GOLD, CYAN, MAGENTA]
    paso = (x1 - x0) / (n - 1)
    sh = page.new_shape()
    for i in range(n):
        x = x0 + i * paso
        sh.draw_circle((x, y + (3 if i % 2 else 6)), 1.6)
        sh.finish(color=colores[i % 5], fill=colores[i % 5], width=0.3)
    sh.commit()


# ═══════════════════════════════════════════════════════════════
#  PÁGINAS
# ═══════════════════════════════════════════════════════════════
def fondo(page):
    page.draw_rect(page.rect, color=None, fill=BG)


def portada(doc, titulo, lema, color_lema, resumen, navidad=False):
    page = doc.new_page(width=W, height=H); fondo(page)
    page.insert_image(fitz.Rect(178, 130, 417, 405), filename='assets/img/logo-mark-glow.png')
    texto(page, 'CC ENTERTAINMENT', 425, 34, 'B')
    texto(page, 'PRODUCCIÓN DE ESPECTÁCULOS TEMÁTICOS', 474, 9.5, 'M', MUTED)
    if navidad:
        seg = [GREEN, RED, GOLD]
        for i, c in enumerate(seg):
            linea(page, 187 + i * 74, 508, 187 + (i + 1) * 74 - 4, c, 2.5)
    else:
        arcoiris(page, 187, 408, 508, 2.5)
    texto(page, titulo, 543, 30, 'L')
    texto(page, lema, 590, 11, 'S', color_lema)
    texto(page, resumen, 740, 10.5, 'M', MUTED)
    texto(page, 'República Dominicana · 2026', 758, 10.5, 'M', MUTED)
    texto(page, f'{TEL}  ·  {IG}', 786, 10.5, 'S')
    if navidad:
        campana(page, 95, 118, 1.4); campana(page, 500, 118, 1.4)
        for (x, y, r) in [(60, 300, 9), (535, 318, 9), (78, 560, 7), (515, 585, 7), (150, 690, 6), (438, 695, 6)]:
            copo(page, x, y, r)
        lucecitas(page, 150, 445, 706, 14)
    return page


def portadilla(doc, sec, es_navidad_ed=False):
    page = doc.new_page(width=W, height=H); fondo(page)
    plumas(page, fitz.Rect(80, 161, 515, 661), 0.13)
    texto(page, sec['num'], 240, 60, 'B', sec['color'])
    texto(page, sec['titulo'], 326, 34, 'L')
    linea(page, 208, 388, 388, SILVER, 1.5)
    if sec.get('resumen'):
        n = len(sec['items']) + len(sec.get('grandes', []))
        texto(page, sec['resumen'].format(n=n), 428, 12, 'M', MUTED)
    else:
        y = 424
        for it in sec['items']:
            texto(page, it[0], y, 11.5, 'M', MUTED); y += 20
    texto(page, 'CC ENTERTAINMENT · CATÁLOGO DE TEMÁTICAS', 804, 7.5, 'M', MUTED, x=42)
    return page


def cabeza(page, etiqueta_sec, color_sec, numero, navidad=False):
    fondo(page)
    plumas(page, fitz.Rect(110, 196, 485, 626), 0.10)
    texto(page, 'CC ENTERTAINMENT', 36, 10, 'B', TXT, x=42)
    texto(page, etiqueta_sec, 52, 7.5, 'M', color_sec, x=42)
    texto(page, f'{numero:02d}', 41, 11, 'B', GOLD, x=553, alinear='derecha')
    arcoiris(page, 42, 553, 69, 2)
    texto(page, f'{TEL} · {IG}', 804, 7.5, 'M', MUTED, x=42)
    if navidad:
        campana(page, 505, 46, 0.75)
        lucecitas(page, 48, 547, 72, 24)
        copo(page, 50, 790, 7); copo(page, 545, 785, 7)


CEL_HERO = fitz.Rect(42, 86, 553, 414)
CEL_HERO_ABAJO = [fitz.Rect(42, 470, 288, 722), fitz.Rect(306, 470, 553, 722)]
CEL_GRID = [[fitz.Rect(42, 86, 288, 386), fitz.Rect(307, 86, 553, 386)],
            [fitz.Rect(42, 456, 288, 756), fitz.Rect(307, 456, 553, 756)]]
CEL_GRANDE = [fitz.Rect(42, 86, 553, 382), fitz.Rect(42, 438, 553, 734)]


def es_par(it):
    return isinstance(it[1], list)


def filas_de(items):
    """Agrupa en filas de 2 celdas. Un par (dos fotos, título centrado) ocupa
    una fila entera; si la fila va por la mitad se adelanta el siguiente
    sencillo para no dejar huecos."""
    pend = list(items); filas = []
    while pend:
        it = pend.pop(0)
        if es_par(it):
            filas.append([it]); continue
        fila = [it]
        # buscar compañero sencillo
        for j, cand in enumerate(pend):
            if not es_par(cand):
                fila.append(pend.pop(j)); break
        filas.append(fila)
    return filas


def pinta_fila(page, fila, celdas, sec, grande=False):
    if len(fila) == 1 and es_par(fila[0]):
        nombre, rutas, sub = fila[0]
        celda(page, rutas[0], celdas[0]); celda(page, rutas[1], celdas[1])
        union = fitz.Rect(celdas[0].x0, celdas[0].y0, celdas[1].x1, celdas[1].y1)
        etiqueta(page, union, nombre, sub, sec['color'], sec['defecto'], centrada=True)
        return
    for it, r in zip(fila, celdas):
        celda(page, it[1], r)
        etiqueta(page, r, it[0], it[2], sec['color'], sec['defecto'], grande=grande)


def seccion(doc, sec, num_pag, navidad=False, con_hero=True):
    """Devuelve el siguiente número de página de contenido."""
    items = list(sec['items'])
    # páginas grandes (Navidad): dos horizontales por página
    for g in sec.get('grandes', []) and [sec['grandes'][i:i + 2] for i in range(0, len(sec['grandes']), 2)] or []:
        page = doc.new_page(width=W, height=H); cabeza(page, sec['etiqueta'], sec['color'], num_pag, navidad); num_pag += 1
        for it, r in zip(g, CEL_GRANDE):
            celda(page, it[1], r); etiqueta(page, r, it[0], it[2], sec['color'], sec['defecto'], grande=True)
    if con_hero and items and not sec.get('grandes'):
        hero = items.pop(0)
        page = doc.new_page(width=W, height=H); cabeza(page, sec['etiqueta'], sec['color'], num_pag, navidad); num_pag += 1
        celda(page, hero[1], CEL_HERO); etiqueta(page, CEL_HERO, hero[0], hero[2], sec['color'], sec['defecto'], grande=True)
        filas = filas_de(items)
        if filas:
            pinta_fila(page, filas.pop(0), CEL_HERO_ABAJO, sec)
    else:
        filas = filas_de(items)
    while filas:
        page = doc.new_page(width=W, height=H); cabeza(page, sec['etiqueta'], sec['color'], num_pag, navidad); num_pag += 1
        for k in range(2):
            if filas:
                pinta_fila(page, filas.pop(0), CEL_GRID[k], sec)
    return num_pag


def contraportada(doc):
    page = doc.new_page(width=W, height=H); fondo(page)
    plumas(page, fitz.Rect(71, 151, 524, 671), 0.13)
    texto(page, 'Convertimos tu evento', 304, 26, 'L')
    texto(page, 'en un espectáculo', 336, 26, 'L')
    arcoiris(page, 208, 388, 388, 2.5)
    texto(page, 'Cotiza tu show a la medida:', 425, 11, 'M', MUTED)
    texto(page, WEB, 443, 13, 'S', CYAN)
    texto(page, f'WhatsApp {TEL}', 478, 12, 'S')
    texto(page, f'Instagram {IG}', 498, 12, 'S')
    texto(page, 'CC Entertainment · Producción de espectáculos temáticos · República Dominicana', 774, 8.5, 'M', MUTED)


# ═══════════════════════════════════════════════════════════════
def catalogo_general():
    doc = fitz.open()
    n_tem = sum(len(s['items']) + len(s.get('grandes', [])) for s in SECCIONES[:-1])
    n_ext = len(EXTRAS)
    portada(doc, 'Catálogo de Temáticas', 'HORAS LOCAS · SHOWS TEMÁTICOS', GOLD,
            f'{n_tem} temáticas y {n_ext} extras de producción propia')
    num = 1
    for sec in SECCIONES:
        portadilla(doc, sec)
        num = seccion(doc, sec, num)
    contraportada(doc)
    return doc


def catalogo_navidad():
    doc = fitz.open()
    sec = dict(num='01', titulo='Navidad', etiqueta='EDICIÓN NAVIDAD', color=GREEN, defecto='SHOW NAVIDEÑO',
               grandes=NAVIDAD_GRANDES, items=NAVIDAD_GRID)
    n = len(NAVIDAD_GRANDES) + len(NAVIDAD_GRID)
    portada(doc, 'Edición Navidad', 'SHOWS NAVIDEÑOS · HORAS LOCAS', GREEN, f'{n} propuestas para tu fiesta navideña', navidad=True)
    seccion(doc, sec, 1, navidad=True, con_hero=False)
    contraportada(doc)
    return doc


def hoja(pdf, destino):
    doc = fitz.open(pdf); Wt = 190; Ht = int(Wt * H / W); cols = 7
    filas = (doc.page_count + cols - 1) // cols
    sheet = Image.new('RGB', (cols * (Wt + 8) + 8, filas * (Ht + 8) + 8), (40, 40, 40))
    for i, p in enumerate(doc):
        pix = p.get_pixmap(matrix=fitz.Matrix(Wt / W, Wt / W))
        sheet.paste(Image.frombytes('RGB', (pix.width, pix.height), pix.samples), (8 + (i % cols) * (Wt + 8), 8 + (i // cols) * (Ht + 8)))
    sheet.save(destino, quality=82)


if __name__ == '__main__':
    faltan = [r for s in SECCIONES for it in s['items'] + s.get('grandes', [])
              for r in (it[1] if isinstance(it[1], list) else [it[1]]) if not os.path.exists(r)]
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
