# -*- coding: utf-8 -*-
"""Catálogos PDF de CC Entertainment — diseño editorial claro.

    python tools/catalogos.py            -> PDFs en la raíz del repo
    python tools/catalogos.py --hoja DIR -> además, hojas de contacto para revisar

Fondo marfil, tipografía Outfit (tools/fonts), fotos con esquinas redondeadas y
sombra suave, portada en mosaico, índice, portadillas con foto grande y QR a la web.
El contenido está en las listas de la sección CONTENIDO. Tipos de elemento:
  ('Nombre', 'ruta.jpg', 'subtítulo')                 -> una celda
  ('Nombre', ['a.jpg', 'b.jpg'], 'subtítulo')         -> dos celdas, título centrado
  F('Nombre', 'ruta.jpg', 'sub', foco=0.3)            -> igual, con encuadre vertical (0 arriba…1 abajo)
  TEXTO('Título', 'cuerpo')                           -> panel de texto que ocupa una fila
  PAGINA('hero_port'|'hero_land'|'grandes'|'grid', [...]) -> página completa con ese esquema
"""
import io, os, sys
import fitz
from PIL import Image, ImageOps

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)
FUENTES = os.path.join(RAIZ, 'tools', 'fonts')
T = 'assets/img/tematicas'


def hx(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


# ─── paleta editorial ───
BG = hx('FBFAF6'); PANEL = hx('F1EEE7'); RULE = hx('E3DFD6')
TXT = hx('15141A'); MUTED = hx('7C7987'); SOFT = hx('A9A6B2')
GOLD = hx('C39A1F'); CYAN = hx('1590AE'); MAGENTA = hx('D6287F'); LIME = hx('7DA218'); VIOLET = hx('7649CF')
RED = hx('D0303C'); GREEN = hx('1F8A4C'); SLATE = hx('5C6370'); NIEVE = hx('B9C3D3')
MARCA = [hx('F5C542'), hx('2FD0FF'), hx('FF2FB0'), hx('CDEA1F'), hx('A06BF5')]   # plumas del logo

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


def F(nombre, img, sub='', foco=0.18):
    return {'n': nombre, 'img': img, 'sub': sub, 'foco': foco}


def TEXTO(titulo, cuerpo):
    return {'texto': (titulo, cuerpo)}


def PAGINA(tipo, items):
    return {'pagina': tipo, 'items': items}


DISCO_BALL = [
    PAGINA('hero_port', [
        ('Bar Neón', t('bar-neon', 1), 'Hostess iluminada con bandeja de canapés'),
        ('Disco Ball', f'{T}/espejos/main.jpg', 'El paquete plateado completo'),
        ('Disco Ball — gorras', t('espejos', 9), 'Trajes de espejos con gorras de cristal'),
        ('Disco Ball — salida', t('espejos', 11), 'Cabezas de bola disco con capas LED'),
        ('Chicas de espejos', 'assets/img/destacado/plata-1.jpg', ''),
    ]),
    ('Hombre LED', 'assets/img/destacado/plata-2.jpg', ''),
    ('Hombre espejo', 'assets/img/destacado/plata-3.jpg', ''),
    ('Disco Ball — grupo', 'assets/img/destacado/plata-4.jpg', ''),
    ('Show en vivo', t('espejos', 1), 'Cabeza de bola disco en evento'),
    ('Show en vivo', t('espejos', 5), 'Disco Ball en evento'),
    ('Bar Neón — en evento', t('bar-neon', 2), 'Canapés con luces en la pista'),
    TEXTO('El show que abre la pista', 'Trajes de espejos, cabezas de bola disco y luces LED: la entrada que convierte cualquier salón en una discoteca. Ideal para bodas, XV años y fiestas corporativas.'),
]

TEMATICAS = [
    ('Dorado', 'assets/img/destacado/dorado-4.jpg', 'El clásico que nunca falla'),
    ('Shine Gold', t('shine-gold', 1), ''),
    ('Dorado — show girls', t('dorado', 6), 'Plumas y lentejuelas'),
    ('Brazil plateada', t('brasil-plata', 1), ''),
    ('Brazil', t('brazil', 1), ''),
    ('Viva las Vegas', t('vegas', 1), ''),
    ('Viva las Vegas — show girls', t('vegas', 3), 'Plumas blancas en escena'),
    ('Neón', t('neon', 5), ''),
    ('Neón — grupo', t('neon', 6), ''),
    ('Tropical', 'assets/img/ig/tropical-sunset.jpg', ''),
    ('Gatsby', t('gatsby', 1), ''),
    ('Gatsby — pareja', t('gatsby', 2), ''),
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
    ('Viva las Vegas — host', t('vegas', 5), 'Recibimiento de entrada'),
    ('Personaje de corazón', t('corazon', 1), ''),
    ('Personaje de playa', t('personaje-playa', 1), ''),
    ('Hadas', t('hadas', 1), ''),
    ('Astronauta y alien', t('astronauta', 1), ''),
    ('Cabezones', 'assets/img/promo/artistas.jpg', 'Bad Bunny, Karol G y Daddy Yankee'),
    PAGINA('hero_port', [
        ('Vogue', t('vogue', 1), 'Recibimiento en blanco y rojo'),
        ('Vogue — blanco', t('vogue', 2), 'Rosas blancas'),
        ('Vogue — rojo', t('vogue', 4), 'Rosas rojas'),
        ('Vogue — anfitriones', t('vogue', 7), 'Lentejuelas rojas para recibir a tus invitados'),
        ('Vogue — anfitriones', t('vogue', 8), 'Coreografía de bienvenida'),
    ]),
    ('Feria/Circo', [t('feria-circo', 1), t('feria-circo', 2)], 'Payasos y mimos'),
    ('Disco', t('disco', 1), ''),
    F('Años 80', t('anos-80', 2), 'Colores fluorescentes y boombox', foco=0.45),
    ('Años 90', t('anos-90', 1), ''),
    ('Brigeston', t('brigeston', 1), ''),
    ('Pilotos Formula 1', t('pilotos', 5), 'Equipo de carreras'),
    ('Pilotos Formula 1 — pit stop', t('pilotos', 3), ''),
    ('Marineros', t('marineros', 1), ''),
    ('Mimos', t('mimos', 1), ''),
    ('Catrinas', 'assets/img/catrinas.jpg', ''),
    ('Venezia', 'assets/img/ig/venetian.jpg', ''),
]

SHOW_LED = [
    ('Show LED', t('led-show', 3), 'Robots, tambores y zancos iluminados'),
    ('Zancos LED', t('led-show', 1), 'Zanquero iluminado en la pista'),
    ('Alas LED', t('alas-led', 3), 'Alas de luz desplegadas'),
    ('Alas LED', t('alas-led', 1), 'Show nocturno'),
    ('Robot LED espejo', t('robot-espejo', 2), 'Futurista y brillante'),
    TEXTO('Luz que se roba la pista', 'Los shows LED se lucen con las luces bajas: perfectos para la apertura de la pista, el corte del pastel o el punto alto de la noche.'),
]

DOMINICANO = [
    ('Carnaval Dominicano', 'assets/img/ig/carnaval.jpg', 'Diablos cojuelos y lechones'),
    ('Carnaval — comparsa', t('carnaval', 2), 'Tambora, color y confeti'),
    ('Diablo cojuelo', 'assets/img/ig/carnaval-2.jpg', 'Carnaval Dominicano'),
    ('Zancos dominicanos', t('zanqueros-rd', 1), 'Con la bandera en alto'),
    ('Dominicana', t('dominicana', 1), 'Vestido de bandera'),
    ('Pareja dominicana', t('dominicana', 2), ''),
    ('Dominicana en evento', t('dominicana', 5), ''),
    ('Marchantas', t('marchantas', 1), ''),
    ('Marchanta', t('marchantas', 3), ''),
    TEXTO('Sabor criollo', 'Bandera, tambora y güira: llevamos la fiesta dominicana a bodas, aniversarios y eventos corporativos con orgullo patrio.'),
    PAGINA('hero_port', [
        ('Pelota dominicana', t('pelota', 3), 'Con las mascotas de los equipos'),
        ('Pelota dominicana', t('pelota', 1), 'Equipos de beisbol'),
        ('Pelota dominicana', t('pelota', 2), 'Animación en el evento'),
        TEXTO('La pasión del béisbol', 'Peloteros, mascotas y animadoras de los equipos: una hora loca con el deporte que une a todos los dominicanos. Perfecta para fiestas infantiles, corporativas y celebraciones familiares.'),
    ]),
]

NAVIDAD = [   # familias de fotos alternadas para que no se repitan seguidas
    PAGINA('grandes', [('Show Navidad completo', t('navidad', 12), 'Grinch, Santa, galleta de jengibre y elfos'),
                       ('Santa y los elfos', t('navidad', 9), '')]),
    PAGINA('grid', [('Cascanueces y elfa', t('navidad', 15), 'Trío rojo y dorado'), ('Pareja Candy', t('navidad', 18), 'Bastones de caramelo'),
                    ('Elfa roja', t('navidad', 16), ''), ('Cocineros navideños', t('navidad', 19), 'Con cuchara y palomitas gigantes')]),
    PAGINA('grandes', [('El Grinch y la galleta', t('navidad', 11), ''),
                       ('Santa con elfos y galleta', t('navidad', 10), '')]),
    PAGINA('grid', [('Santa y sus ayudantes', t('navidad', 13), ''), ('Santa', t('navidad', 7), 'Con soldados de juguete y tambores'),
                    ('Chicas de Santa', t('navidad', 2), ''), ('Soldados de juguete', t('navidad', 4), '')]),
    PAGINA('grid', [('Zancos navideños', t('navidad', 5), ''), ('Alas LED navideñas', t('navidad', 6), ''),
                    ('Blanca Navidad', t('blanca-navidad', 1), ''),
                    TEXTO('Diciembre a otro nivel', 'Santa, el Grinch, elfos y cascanueces para fiestas familiares, empresas y encendidos de árbol.')]),
]

EXTRAS = [
    ('Zanqueros', 'assets/img/promo/zancos.jpg', 'Altura y espectáculo que llenan la pista'),
    ('Percusión en vivo', 'assets/img/promo/musicos.jpg', 'Tambores que encienden la pista'),
    ('Coreografía personalizada', 'assets/img/destacado/plata-1.jpg', 'Entradas, aperturas y sorpresas'),
    ('Robot LED', 'assets/img/promo/robot-espejo.jpg', ''),
    ('Bailarines adicionales', 'assets/img/promo/bailarinas-led.jpg', ''),
    TEXTO('¿Tienes otra idea?', 'Producimos cualquier temática a la medida de tu evento. Cuéntanos qué imaginas y la hacemos realidad.'),
]

SECCIONES = [
    dict(num='01', titulo='Disco Ball', etiqueta='DISCO BALL', color=SLATE, defecto='HORA LOCA', items=DISCO_BALL,
         imagen=f'{T}/espejos/main.jpg', desc='Espejos, luces y brillo plateado: el show que abre la pista.'),
    dict(num='02', titulo='Temáticas', etiqueta='TEMÁTICAS', color=GOLD, defecto='HORA LOCA', items=TEMATICAS,
         imagen='assets/img/destacado/dorado-4.jpg', desc='Del dorado clásico a los personajes de recibimiento: una hora loca para cada estilo.'),
    dict(num='03', titulo='Show LED', etiqueta='SHOW LED', color=CYAN, defecto='SHOW LED', items=SHOW_LED,
         imagen=t('led-show', 3), desc='Robots, alas y zancos iluminados para el punto alto de la noche.'),
    dict(num='04', titulo='Ritmo Dominicano', etiqueta='RITMO DOMINICANO', color=RED, defecto='HORA LOCA', items=DOMINICANO,
         imagen='assets/img/ig/carnaval.jpg', desc='Carnaval, bandera y pelota: la fiesta con sabor criollo.'),
    dict(num='05', titulo='Navidad', etiqueta='NAVIDAD', color=GREEN, defecto='SHOW NAVIDEÑO', items=NAVIDAD,
         imagen=t('navidad', 12), desc='Santa, el Grinch, elfos y cascanueces para las fiestas de diciembre.'),
    dict(num='06', titulo='Extras para tu show', etiqueta='EXTRAS', color=VIOLET, defecto='EXTRA', items=EXTRAS,
         imagen='assets/img/promo/zancos.jpg', desc='Complementos que elevan cualquier hora loca.'),
]

MOSAICO_PORTADA = [f'{T}/espejos/main.jpg', t('vogue', 1), t('vegas', 5), t('bar-neon', 1), t('dorado', 6), t('navidad', 12)]
MOSAICO_NAVIDAD = [t('navidad', 12), t('navidad', 15), t('navidad', 18), t('navidad', 19), t('navidad', 13), t('navidad', 7)]


# ═══════════════════════════════════════════════════════════════
#  TIPOGRAFÍA
# ═══════════════════════════════════════════════════════════════
ARCHIVO_FUENTE = {'B': 'Outfit-Bold.ttf', 'S': 'Outfit-SemiBold.ttf', 'M': 'Outfit-Medium.ttf', 'L': 'Outfit-Light.ttf'}
_FONT = {k: fitz.Font(fontfile=os.path.join(FUENTES, v)) for k, v in ARCHIVO_FUENTE.items()}


def ancho(s, k, size, tracking=0.0):
    return _FONT[k].text_length(s, fontsize=size) + tracking * size * max(len(s) - 1, 0)


def texto(page, s, y, size, k='M', color=TXT, x=None, alinear='izq', tracking=0.0):
    """y = borde superior del texto. x=None centra en la página. tracking en em."""
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
            page.insert_text((cx, base), ch, fontname='ou' + k, fontfile=ff, fontsize=size, color=color)
            cx += _FONT[k].text_length(ch, fontsize=size) + tracking * size
    else:
        page.insert_text((px, base), s, fontname='ou' + k, fontfile=ff, fontsize=size, color=color)
    return w


def parrafo(page, s, x, y, w, size, k='M', color=MUTED, lh=1.45, max_lineas=6):
    palabras = s.split(); lineas = []; actual = ''
    for p in palabras:
        prueba = (actual + ' ' + p).strip()
        if ancho(prueba, k, size) <= w:
            actual = prueba
        else:
            lineas.append(actual); actual = p
    if actual:
        lineas.append(actual)
    for i, l in enumerate(lineas[:max_lineas]):
        texto(page, l, y + i * size * lh, size, k, color, x=x)
    return y + len(lineas[:max_lineas]) * size * lh


def linea(page, x0, y, x1, color=RULE, grosor=0.6):
    page.draw_line((x0, y), (x1, y), color=color, width=grosor)


def barra_marca(page, x, y, w=44, grosor=2.2):
    seg = w / len(MARCA)
    for i, c in enumerate(MARCA):
        page.draw_line((x + i * seg, y), (x + (i + 1) * seg - 1.2, y), color=c, width=grosor)


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


def sombra(page, rect, r):
    for dy, op in ((8, 0.035), (5, 0.045), (2, 0.06)):
        redondeado(page, rect + (0, dy, 0, dy), r, fill=(0, 0, 0), opacidad=op)


def esquinas(page, rect, r, fondo=BG):
    x0, y0, x1, y1 = rect.x0, rect.y0, rect.x1, rect.y1
    for (cx, cy, ax, ay, bx, by) in [(x0, y0, x0 + r, y0, x0, y0 + r), (x1, y0, x1 - r, y0, x1, y0 + r),
                                     (x1, y1, x1 - r, y1, x1, y1 - r), (x0, y1, x0 + r, y1, x0, y1 - r)]:
        sh = page.new_shape()
        sh.draw_line((cx, cy), (ax, ay)); sh.draw_curve((ax, ay), (cx, cy), (bx, by)); sh.draw_line((bx, by), (cx, cy))
        sh.finish(color=fondo, fill=fondo, width=0.3, closePath=True); sh.commit()


def celda(page, path, rect, r=10, foco=0.18, con_sombra=True):
    if con_sombra:
        sombra(page, rect, r)
    page.insert_image(rect, stream=foto(path, rect, foco))
    esquinas(page, rect, r)
    redondeado(page, rect, r, color=RULE, width=0.6)


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
def fondo(page):
    page.draw_rect(page.rect, color=None, fill=BG)


def cabeza(page, etiqueta_sec, color_sec, numero, navidad=False):
    fondo(page)
    texto(page, 'CC ENTERTAINMENT', 34, 7.5, 'B', TXT, x=M, tracking=0.18)
    texto(page, etiqueta_sec, 34.5, 7, 'M', color_sec, x=W - M - 30, alinear='der', tracking=0.18)
    texto(page, f'{numero:02d}', 32, 9.5, 'B', TXT, x=W - M, alinear='der')
    linea(page, M, 56, W - M)
    pie(page)
    if navidad:
        campana(page, W - M - 44, 42, 0.62)
        lucecitas(page, M + 4, W - M - 4, 59)
        copo(page, M + 6, 787, 6); copo(page, W - M - 6, 783, 6)


def pie(page):
    barra_marca(page, M, 806)
    texto(page, f'{WEB}   ·   {TEL}   ·   {IG}', 800, 7, 'M', MUTED, x=W - M, alinear='der')


def etiqueta(page, rect, nombre, sub, color, defecto, grande=False, centrada=False):
    ts, ss = (16, 9) if grande else (12.5, 8)
    y_n = rect.y1 + 10
    if centrada:
        cx = (rect.x0 + rect.x1) / 2
        w = ancho(nombre, 'S', ts)
        redondeado(page, fitz.Rect(cx - w / 2 - 14, y_n + ts * 0.32, cx - w / 2 - 8, y_n + ts * 0.32 + 6), 1.2, fill=color)
        texto(page, nombre, y_n, ts, 'S', TXT, x=cx + 3, alinear='centro')
        if sub:
            texto(page, sub, y_n + ts + 5, ss, 'M', color, x=cx, alinear='centro')
        else:
            texto(page, defecto, y_n + ts + 6, 6.5, 'M', SOFT, x=cx, alinear='centro', tracking=0.16)
        return
    redondeado(page, fitz.Rect(rect.x0, y_n + ts * 0.32, rect.x0 + 6, y_n + ts * 0.32 + 6), 1.2, fill=color)
    texto(page, nombre, y_n, ts, 'S', TXT, x=rect.x0 + 14)
    if sub:
        texto(page, sub, y_n + ts + 5, ss, 'M', color, x=rect.x0 + 14)
    else:
        texto(page, defecto, y_n + ts + 6, 6.5, 'M', SOFT, x=rect.x0 + 14, tracking=0.16)


def lineas_de(s, w, size, k):
    palabras = s.split(); lineas = []; actual = ''
    for p in palabras:
        prueba = (actual + ' ' + p).strip()
        if ancho(prueba, k, size) <= w:
            actual = prueba
        else:
            lineas.append(actual); actual = p
    if actual:
        lineas.append(actual)
    return lineas


def panel_texto(page, rect, titulo, cuerpo, color):
    """Panel compacto: el alto se ajusta al texto (no llena la fila entera)."""
    ts = 22 if rect.width > 300 else 19
    w = rect.width - 44
    h_tit = len(lineas_de(titulo, w, ts, 'L')) * ts * 1.15
    h_cue = len(lineas_de(cuerpo, w, 9.5, 'M')) * 9.5 * 1.5
    alto = 42 + h_tit + 10 + h_cue + 28
    caja = fitz.Rect(rect.x0, rect.y0, rect.x1, rect.y0 + max(alto, 112))
    redondeado(page, caja, 10, fill=PANEL)
    redondeado(page, fitz.Rect(caja.x0 + 22, caja.y0 + 26, caja.x0 + 50, caja.y0 + 28.5), 1, fill=color)
    y = parrafo(page, titulo, caja.x0 + 22, caja.y0 + 42, w, ts, 'L', TXT, lh=1.15, max_lineas=3)
    parrafo(page, cuerpo, caja.x0 + 22, y + 10, w, 9.5, 'M', MUTED, lh=1.5, max_lineas=8)


# ─── decoración navideña ───
def campana(page, cx, cy, s=1.0, color=GOLD):
    sh = page.new_shape()
    sh.draw_line((cx, cy - 22 * s), (cx, cy - 17 * s)); sh.draw_circle((cx, cy - 22 * s), 2 * s)
    sh.draw_bezier((cx - 12 * s, cy + 6 * s), (cx - 12 * s, cy - 14 * s), (cx + 12 * s, cy - 14 * s), (cx + 12 * s, cy + 6 * s))
    sh.draw_line((cx - 15 * s, cy + 6 * s), (cx + 15 * s, cy + 6 * s))
    sh.finish(color=color, width=1.2 * s)
    sh.draw_circle((cx, cy + 9 * s), 2.2 * s); sh.finish(color=color, fill=color, width=0.5); sh.commit()


def copo(page, cx, cy, r=7, color=NIEVE):
    import math
    sh = page.new_shape()
    for i in range(6):
        a = math.radians(i * 60); x1, y1 = cx + r * math.cos(a), cy + r * math.sin(a)
        sh.draw_line((cx, cy), (x1, y1))
        for lado in (-1, 1):
            b = a + lado * math.radians(35); xm, ym = cx + r * 0.6 * math.cos(a), cy + r * 0.6 * math.sin(a)
            sh.draw_line((xm, ym), (xm + r * 0.3 * math.cos(b), ym + r * 0.3 * math.sin(b)))
    sh.finish(color=color, width=0.7); sh.commit()


def lucecitas(page, x0, x1, y, n=26):
    colores = [RED, GREEN, GOLD, CYAN, MAGENTA]
    paso = (x1 - x0) / (n - 1); sh = page.new_shape()
    for i in range(n):
        sh.draw_circle((x0 + i * paso, y + (2 if i % 2 else 5)), 1.5); sh.finish(color=colores[i % 5], fill=colores[i % 5], width=0.3)
    sh.commit()


# ═══════════════════════════════════════════════════════════════
#  PLANTILLAS
# ═══════════════════════════════════════════════════════════════
CEL = {
    'hero_land': dict(hero=fitz.Rect(M, 78, W - M, 400), abajo=[fitz.Rect(M, 452, 294, 712), fitz.Rect(301, 452, W - M, 712)]),
    'hero_port': dict(hero=fitz.Rect(M, 78, 322, 500), lado=[fitz.Rect(334, 78, W - M, 272), fitz.Rect(334, 318, W - M, 500)],
                      abajo=[fitz.Rect(M, 556, 294, 760), fitz.Rect(301, 556, W - M, 760)]),
    'grid': [[fitz.Rect(M, 78, 294, 378), fitz.Rect(301, 78, W - M, 378)], [fitz.Rect(M, 436, 294, 736), fitz.Rect(301, 436, W - M, 736)]],
    'grandes': [fitz.Rect(M, 78, W - M, 376), fitz.Rect(M, 432, W - M, 730)],
}


def norm(it):
    """-> (nombre, img|[img,img]|None, sub, foco, texto|None)"""
    if isinstance(it, dict):
        if 'texto' in it:
            return (None, None, None, 0.18, it['texto'])
        return (it['n'], it['img'], it['sub'], it.get('foco', 0.18), None)
    return (it[0], it[1], it[2], 0.18, None)


def es_par(it):
    return isinstance(it, tuple) and isinstance(it[1], list)


def es_fila_entera(it):
    return es_par(it) or (isinstance(it, dict) and 'texto' in it)


def pinta_celda(page, it, rect, sec, grande=False):
    n, img, sub, foco, txt = norm(it)
    celda(page, img, rect, foco=foco)
    etiqueta(page, rect, n, sub, sec['color'], sec['defecto'], grande=grande)


def pinta_fila(page, fila, celdas, sec):
    if len(fila) == 1 and es_fila_entera(fila[0]):
        it = fila[0]
        union = fitz.Rect(celdas[0].x0, celdas[0].y0, celdas[1].x1, celdas[1].y1)
        if es_par(it):
            n, rutas, sub = it
            celda(page, rutas[0], celdas[0]); celda(page, rutas[1], celdas[1])
            etiqueta(page, union, n, sub, sec['color'], sec['defecto'], centrada=True)
        else:
            titulo, cuerpo = it['texto']
            panel_texto(page, union, titulo, cuerpo, sec['color'])
        return
    for it, r in zip(fila, celdas):
        pinta_celda(page, it, r, sec)


def filas_de(items):
    pend = list(items); filas = []
    while pend:
        it = pend.pop(0)
        if es_fila_entera(it):
            filas.append([it]); continue
        fila = [it]
        for j, cand in enumerate(pend):
            if not es_fila_entera(cand):
                fila.append(pend.pop(j)); break
        filas.append(fila)
    return filas


def pagina_especial(doc, spec, sec, num, navidad):
    tipo, items = spec['pagina'], spec['items']
    page = doc.new_page(width=W, height=H); cabeza(page, sec['etiqueta'], sec['color'], num, navidad)
    if tipo == 'hero_port':
        c = CEL['hero_port']
        pinta_celda(page, items[0], c['hero'], sec, grande=True)
        for it, r in zip(items[1:3], c['lado']):
            pinta_celda(page, it, r, sec)
        resto = items[3:]
        if resto:
            fila = resto[:2]
            if len(fila) == 1 and not es_fila_entera(fila[0]):
                pinta_celda(page, fila[0], c['abajo'][0], sec)
            else:
                pinta_fila(page, fila, c['abajo'], sec)
    elif tipo == 'hero_land':
        c = CEL['hero_land']
        pinta_celda(page, items[0], c['hero'], sec, grande=True)
        pinta_fila(page, items[1:3], c['abajo'], sec)
    elif tipo == 'grandes':
        for it, r in zip(items[:2], CEL['grandes']):
            pinta_celda(page, it, r, sec, grande=True)
    elif tipo == 'grid':
        filas = filas_de(items)
        for k in range(2):
            if filas:
                pinta_fila(page, filas.pop(0), CEL['grid'][k], sec)
    return num + 1


def seccion(doc, sec, num, navidad=False):
    """Pagina los elementos de una sección. Devuelve el siguiente número de página."""
    items = list(sec['items'])
    sec['pagina'] = num
    if items and not isinstance(items[0], dict):
        hero = items.pop(0)
        page = doc.new_page(width=W, height=H); cabeza(page, sec['etiqueta'], sec['color'], num, navidad); num += 1
        c = CEL['hero_land']
        pinta_celda(page, hero, c['hero'], sec, grande=True)
        primeros = []
        while items and len(primeros) < 2 and not (isinstance(items[0], dict) and 'pagina' in items[0]):
            if es_fila_entera(items[0]):
                if not primeros:
                    primeros = [items.pop(0)]
                break
            primeros.append(items.pop(0))
        if primeros:
            pinta_fila(page, primeros, c['abajo'], sec)

    def vaciar(pendientes, num):
        filas = filas_de(pendientes)
        while filas:
            page = doc.new_page(width=W, height=H); cabeza(page, sec['etiqueta'], sec['color'], num, navidad); num += 1
            for k in range(2):
                if filas:
                    pinta_fila(page, filas.pop(0), CEL['grid'][k], sec)
        return num

    pendientes = []
    for it in items:
        if isinstance(it, dict) and 'pagina' in it:
            num = vaciar(pendientes, num); pendientes = []
            num = pagina_especial(doc, it, sec, num, navidad)
        else:
            pendientes.append(it)
    num = vaciar(pendientes, num)
    return num


# ═══════════════════════════════════════════════════════════════
#  PORTADA, ÍNDICE, PORTADILLAS, CONTRAPORTADA
# ═══════════════════════════════════════════════════════════════
def mosaico(page, rutas, y0, y1, gutter=8):
    cw = (W - 2 * M - 2 * gutter) / 3; ch = (y1 - y0 - gutter) / 2
    for i, p in enumerate(rutas[:6]):
        x = M + (i % 3) * (cw + gutter); y = y0 + (i // 3) * (ch + gutter)
        celda(page, p, fitz.Rect(x, y, x + cw, y + ch), r=10, foco=0.15, con_sombra=False)


def portada(doc, titulo, lema, color, stats, rutas, navidad=False):
    page = doc.new_page(width=W, height=H); fondo(page)
    mosaico(page, rutas, 42, 448)
    imagen_compartida(page, fitz.Rect(M, 482, M + 54, 536), 'logo', png_logo)
    texto(page, 'CC ENTERTAINMENT', 492, 15, 'B', TXT, x=M + 66, tracking=0.14)
    texto(page, 'PRODUCCIÓN DE ESPECTÁCULOS TEMÁTICOS', 516, 7.5, 'M', MUTED, x=M + 66, tracking=0.18)
    texto(page, titulo, 566, 42, 'L', TXT, x=M)
    texto(page, lema, 626, 9.5, 'S', color, x=M, tracking=0.16)
    y = 672
    x = M
    for numero, label in stats:
        texto(page, numero, y, 20, 'B', TXT, x=x)
        texto(page, label, y + 27, 7, 'M', MUTED, x=x, tracking=0.16)
        x += max(ancho(numero, 'B', 20), ancho(label, 'M', 7, 0.16)) + 40
    linea(page, M, 760, W - M)
    barra_marca(page, M, 790, w=120, grosor=3)
    texto(page, f'{TEL}  ·  {IG}  ·  {WEB}', 782, 8.5, 'M', MUTED, x=W - M, alinear='der')
    if navidad:
        campana(page, W - M - 20, 500, 1.1); copo(page, W - M - 70, 494, 7); copo(page, W - M - 44, 530, 5)
        lucecitas(page, M, W - M, 764, 30)
    return page


def indice(doc, pno, secciones, total_tem, total_ext):
    page = doc.new_page(pno=pno, width=W, height=H); fondo(page)
    texto(page, 'CONTENIDO', 40, 7.5, 'M', MUTED, x=M, tracking=0.22)
    texto(page, 'Un show para cada evento', 58, 34, 'L', TXT, x=M)
    parrafo(page, 'Somos CC Entertainment: producimos horas locas, coreografías y shows temáticos con vestuario y utilería propios. '
                  'Cada propuesta de este catálogo se adapta a bodas, cumpleaños, fiestas corporativas y celebraciones familiares en toda República Dominicana.',
            M, 112, W - 2 * M - 40, 10, 'M', MUTED, lh=1.5)
    y = 190
    for s in secciones:
        celda(page, s['imagen'], fitz.Rect(M, y, M + 78, y + 58), r=8, foco=0.2, con_sombra=False)
        texto(page, s['num'], y + 4, 10, 'B', s['color'], x=M + 96, tracking=0.1)
        texto(page, s['titulo'], y + 19, 15, 'S', TXT, x=M + 96)
        texto(page, s['desc'], y + 41, 8, 'M', MUTED, x=M + 96)
        texto(page, f"{s['pagina']:02d}", y + 16, 15, 'L', TXT, x=W - M, alinear='der')
        linea(page, M, y + 72, W - M)
        y += 86
    y += 14
    texto(page, f'{total_tem}', y, 22, 'B', TXT, x=M); texto(page, 'TEMÁTICAS', y + 28, 7, 'M', MUTED, x=M, tracking=0.16)
    texto(page, f'{total_ext}', y, 22, 'B', TXT, x=M + 130); texto(page, 'EXTRAS', y + 28, 7, 'M', MUTED, x=M + 130, tracking=0.16)
    texto(page, '2026', y, 22, 'B', TXT, x=M + 240); texto(page, 'EDICIÓN', y + 28, 7, 'M', MUTED, x=M + 240, tracking=0.16)
    pie(page)


def portadilla(doc, sec, navidad=False):
    page = doc.new_page(width=W, height=H); fondo(page)
    celda(page, sec['imagen'], fitz.Rect(M, 42, W - M, 440), r=14, foco=0.2)
    texto(page, sec['num'], 458, 96, 'L', sec['color'], x=M - 4)
    texto(page, sec['titulo'], 566, 36, 'L', TXT, x=M)
    parrafo(page, sec['desc'], M, 618, W - 2 * M - 60, 10.5, 'M', MUTED, lh=1.45, max_lineas=2)
    nombres = []
    for it in sec['items']:
        if isinstance(it, dict) and 'pagina' in it:
            nombres += [norm(x)[0] for x in it['items'] if norm(x)[0]]
        else:
            n = norm(it)[0]
            if n:
                nombres.append(n)
    unicos = []
    for n in nombres:
        if n not in unicos:
            unicos.append(n)
    y0 = 662; col = 0; y = y0
    for i, n in enumerate(unicos[:20]):
        texto(page, n, y, 8, 'M', MUTED, x=M + col * 250)
        y += 12.5
        if i == 9:
            col = 1; y = y0
    if len(unicos) > 20:
        texto(page, f'y {len(unicos) - 20} propuestas más', y, 8, 'M', SOFT, x=M + 250)
    pie(page)
    if navidad:
        campana(page, W - M - 20, 480, 1.0); copo(page, W - M - 60, 472, 7)


def contraportada(doc, ruta_foto):
    page = doc.new_page(width=W, height=H); fondo(page)
    celda(page, ruta_foto, fitz.Rect(M, 42, W - M, 400), r=14, foco=0.25)
    texto(page, 'Convertimos tu evento', 436, 32, 'L', TXT, x=M)
    texto(page, 'en un espectáculo', 474, 32, 'L', TXT, x=M)
    parrafo(page, 'Cotiza tu show a la medida en nuestra página: eliges la temática, agregas los extras y recibes la propuesta por WhatsApp.',
            M, 530, 300, 10, 'M', MUTED, lh=1.5)
    redondeado(page, fitz.Rect(M, 590, M + 118, 708), 8, fill=(1, 1, 1), color=RULE)
    imagen_compartida(page, fitz.Rect(M + 8, 598, M + 110, 700), 'qr', png_qr)
    texto(page, 'ESCANEA Y COTIZA', 592, 7, 'M', MUTED, x=M + 136, tracking=0.18)
    texto(page, WEB, 606, 15, 'S', CYAN, x=M + 136)
    texto(page, f'WhatsApp  {TEL}', 640, 12, 'S', TXT, x=M + 136)
    texto(page, f'Instagram  {IG}', 662, 12, 'S', TXT, x=M + 136)
    texto(page, 'Santo Domingo · República Dominicana', 690, 8.5, 'M', MUTED, x=M + 136)
    linea(page, M, 760, W - M)
    barra_marca(page, M, 790, w=120, grosor=3)
    texto(page, 'CC Entertainment · Producción de espectáculos temáticos', 782, 8, 'M', MUTED, x=W - M, alinear='der')


# ═══════════════════════════════════════════════════════════════
def contar(items):
    nombres = set()
    for it in items:
        grupo = it['items'] if isinstance(it, dict) and 'pagina' in it else [it]
        for x in grupo:
            n = norm(x)[0]
            if n:
                nombres.add(n.split(' — ')[0].strip())
    return len(nombres)


def temas_web():
    """Cantidad de temáticas publicadas en la página (THEMES de js/main.js), para que el catálogo diga lo mismo."""
    import re
    try:
        js = open('js/main.js', encoding='utf-8').read()
        ini = js.index('const THEMES = [')
        fin = js.index(chr(10) + '];', ini)
        bloque = js[ini:fin]
        ids = re.findall(r"\{ id: '([^']+)'", bloque)
        return len([i for i in ids if i != 'otra'])
    except Exception:
        return 0


def catalogo_general():
    doc = fitz.open()
    total_tem = temas_web() or sum(contar(s['items']) for s in SECCIONES[:-1]); total_ext = contar(EXTRAS)
    portada(doc, 'Catálogo de Temáticas', 'HORAS LOCAS  ·  SHOWS TEMÁTICOS  ·  EDICIÓN 2026', GOLD,
            [(str(total_tem), 'TEMÁTICAS'), (str(total_ext), 'EXTRAS'), ('RD', 'REPÚBLICA DOMINICANA')], MOSAICO_PORTADA)
    num = 1
    for sec in SECCIONES:
        portadilla(doc, sec)
        num = seccion(doc, sec, num)
    contraportada(doc, t('vegas', 6))
    indice(doc, 1, SECCIONES, total_tem, total_ext)
    return doc


def catalogo_navidad():
    doc = fitz.open()
    sec = dict(num='01', titulo='Navidad', etiqueta='EDICIÓN NAVIDAD', color=GREEN, defecto='SHOW NAVIDEÑO', items=NAVIDAD,
               imagen=t('navidad', 12), desc='Santa, el Grinch, elfos y cascanueces para las fiestas de diciembre.')
    n = contar(NAVIDAD)
    portada(doc, 'Edición Navidad', 'SHOWS NAVIDEÑOS  ·  HORAS LOCAS  ·  2026', GREEN,
            [(str(n), 'PROPUESTAS'), ('RD', 'REPÚBLICA DOMINICANA')], MOSAICO_NAVIDAD, navidad=True)
    seccion(doc, sec, 1, navidad=True)
    contraportada(doc, t('navidad', 10))
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
                if img:
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
