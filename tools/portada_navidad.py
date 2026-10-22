"""Monta el video de portada navideno a partir de las fotos de estudio.

Se generan los fotogramas uno a uno con PIL en vez de usar los filtros de
ffmpeg: asi se controla el encuadre exacto de cada foto y no hay sorpresas
con caras cortadas.

Cada foto lleva un movimiento lento de camara (acercarse, alejarse o
recorrer). Las verticales casi no se recortan; las horizontales se recorren
de lado a lado, que convierte el recorte en un efecto en vez de un problema.

El montaje es CICLICO: el final funde con el principio, asi que al repetirse
en bucle no se ve el corte.
"""
from PIL import Image
import os, subprocess, sys, shutil

W, H = 720, 1280          # mismo formato que la portada actual
FPS = 30
DUR = 4.2                 # segundos por foto, fundido incluido
FADE = 0.8                # fundido entre fotos

BASE = 'assets/img/tematicas/'
SALIDA_DIR = os.path.normpath('C:/Users/EQUIPO/AppData/Local/Temp/claude/'
                              'C--Users-EQUIPO-Desktop-Proyectos-claude/'
                              '743bcc5d-28f7-4b2e-a146-7922b8ed0f28/scratchpad/frames')
DEST = 'assets/hero-navidad.mp4'
FF = r'C:/Program Files (x86)/HikCentral/VSM Servers/SYS/ffmpeg.exe'

# (archivo, movimiento, parametros)
#   'zoom'   acercarse/alejarse:  (z0, z1, cx, cy)   z = cuanto se ve (1 = todo)
#   'pan'    recorrer de lado:    (x0, x1)           posicion horizontal 0..1
PLAN = [
    ('navidad/12.jpg', 'pan',  (0.12, 0.88)),   # el grupo entero, de lado a lado
    ('navidad/13.jpg', 'zoom', (1.00, 0.88, 0.5, 0.38)),
    ('navidad/17.jpg', 'zoom', (0.88, 1.00, 0.5, 0.34)),
    ('navidad/11.jpg', 'pan',  (0.86, 0.14)),   # Grinch y galleta, al reves
    ('blanca-navidad/01.jpg', 'zoom', (1.00, 0.90, 0.5, 0.40)),
    ('navidad/18.jpg', 'zoom', (0.90, 1.00, 0.5, 0.36)),
]

OBJ = W / H               # proporcion del lienzo (0.5625)


def ventana(im, mov, p, t):
    """Devuelve el recorte de la foto para el instante t (0..1)."""
    sw, sh = im.size
    if mov == 'pan':
        # se ve todo el alto; la ventana recorre a lo ancho
        vh = sh
        vw = vh * OBJ
        x0, x1 = p
        cx = x0 + (x1 - x0) * t
        izq = cx * (sw - vw)
        izq = max(0, min(izq, sw - vw))
        return (izq, 0, izq + vw, vh)
    # zoom: z es la fraccion del alto que se ve
    z0, z1, cx, cy = p
    z = z0 + (z1 - z0) * t
    vh = sh * z
    vw = vh * OBJ
    if vw > sw:                      # la foto no da de ancho: limitar
        vw = sw
        vh = vw / OBJ
    izq = cx * sw - vw / 2
    arr = cy * sh - vh / 2
    izq = max(0, min(izq, sw - vw))
    arr = max(0, min(arr, sh - vh))
    return (izq, arr, izq + vw, arr + vh)


def fotograma(im, mov, p, t):
    return im.resize((W, H), Image.LANCZOS, box=ventana(im, mov, p, t))


def main():
    if os.path.isdir(SALIDA_DIR):
        shutil.rmtree(SALIDA_DIR)
    os.makedirs(SALIDA_DIR)

    fotos = [Image.open(BASE + f).convert('RGB') for f, _, _ in PLAN]
    n = len(PLAN)
    paso = DUR - FADE                      # lo que avanza la linea de tiempo por foto
    total = int(round(paso * n * FPS))     # ciclico: el ultimo funde con el primero
    print('fotos:', n, ' duracion:', round(total / FPS, 2), 's ', total, 'fotogramas')

    marcoFade = FADE * FPS
    marcoPaso = paso * FPS
    marcoDur = DUR * FPS          # lo que dura una foto en pantalla, fundidos incluidos

    for k in range(total):
        capas = []
        for i in range(n):
            # d = cuanto llevamos dentro de esta foto, contando la vuelta al principio
            d = k - i * marcoPaso
            if d < -total / 2:
                d += total
            elif d > total / 2:
                d -= total
            if d < 0 or d > marcoDur:
                continue
            # entra durante el primer fundido, sale durante el ultimo; en medio,
            # opaca. Asi dos fotos consecutivas siempre suman 1 y no se fantasman.
            if d < marcoFade:
                a = d / marcoFade
            elif d > marcoPaso:
                a = 1 - (d - marcoPaso) / marcoFade
            else:
                a = 1.0
            if a <= 0.001:
                continue
            capas.append((fotograma(fotos[i], PLAN[i][1], PLAN[i][2], d / marcoDur), a))

        if not capas:
            continue
        base = capas[0][0]
        acc = capas[0][1]
        for img, a in capas[1:]:
            acc2 = acc + a
            base = Image.blend(base, img, a / acc2 if acc2 else 0)
            acc = acc2
        base.save('%s/f%05d.jpg' % (SALIDA_DIR, k), quality=95)
        if k % 90 == 0:
            print('  ', k, '/', total)

    print('codificando...')
    cmd = [FF, '-y', '-framerate', str(FPS), '-i', SALIDA_DIR + '/f%05d.jpg',
           '-c:v', 'libx264', '-preset', 'slow', '-crf', '23',
           '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
           '-an', DEST]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1500:])
        sys.exit(1)
    print('listo:', DEST, os.path.getsize(DEST) // 1024, 'KB')


if __name__ == '__main__':
    main()
