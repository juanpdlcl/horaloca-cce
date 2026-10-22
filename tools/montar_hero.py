"""Monta las portadas navidenas con los videos bajados de las historias
destacadas (720x1280 originales).

Se generan DOS versiones:

  vertical  720x1280  para telefonos: el clip ocupa todo el cuadro.
  apaisada 1280x720  para laptops: TRES clips verticales uno al lado del
            otro, cada uno a todo lo alto. Asi en pantalla ancha no hay que
            recortar la imagen y no se corta ninguna cabeza, que es lo que
            pasaba al estirar un video vertical para cubrir el ancho.

La ultima toma repite la primera para que el bucle no se note al reiniciar.
"""
import subprocess, os, sys

FF = r'C:/Program Files (x86)/HikCentral/VSM Servers/SYS/ffmpeg.exe'
ORI = '.nv-origen/'
DUR = 4.0          # lo que dura cada toma
FADE = 0.7         # fundido entre tomas

# (clip, segundo por el que empieza)
VERT = [('c01', 1.0), ('c09', 1.0), ('c17', 0.2), ('c33', 0.3),
        ('c65', 2.0), ('c05', 1.0), ('c01', 1.0)]

# para la apaisada, tres columnas; cada fila es una escena
TRIP = [
    [('c01', 1.0), ('c65', 2.0), ('c09', 1.0)],
    [('c33', 0.3), ('c17', 0.2), ('c05', 1.0)],
    [('c61', 1.0), ('c73', 1.0), ('c21', 1.0)],
    [('c01', 1.0), ('c65', 2.0), ('c09', 1.0)],   # repite la primera: bucle
]


def corre(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-2200:])
        sys.exit(1)


def vertical(salida):
    ent, filtros, n = [], [], len(VERT)
    for i, (c, ini) in enumerate(VERT):
        ent += ['-ss', str(ini), '-t', str(DUR), '-i', ORI + c + '.mp4']
        filtros.append(
            '[%d:v]scale=720:1280:force_original_aspect_ratio=increase,'
            'crop=720:1280,fps=30,setpts=PTS-STARTPTS[v%d]' % (i, i))
    paso = DUR - FADE
    ult = 'v0'
    for i in range(1, n):
        et = 'x%d' % i
        filtros.append('[%s][v%d]xfade=transition=fade:duration=%s:offset=%s[%s]'
                       % (ult, i, FADE, round(i * paso, 3), et))
        ult = et
    cmd = [FF, '-y'] + ent + ['-filter_complex', ';'.join(filtros),
           '-map', '[%s]' % ult, '-an', '-c:v', 'libx264', '-preset', 'slow',
           '-crf', '23', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', salida]
    corre(cmd)
    print('vertical:', salida, os.path.getsize(salida) // 1024, 'KB',
          round(n * DUR - (n - 1) * FADE, 1), 's')


def apaisada(salida):
    ent, filtros = [], []
    k = 0
    escenas = []
    for e, trio in enumerate(TRIP):
        cols = []
        for (c, ini) in trio:
            ent += ['-ss', str(ini), '-t', str(DUR), '-i', ORI + c + '.mp4']
            # cada columna a todo lo alto; se recorta solo un 5% y por abajo,
            # asi las caras (que van arriba) quedan intactas
            filtros.append(
                '[%d:v]scale=426:-2,crop=426:720:0:(ih-720)*0.25,fps=30,'
                'setpts=PTS-STARTPTS[k%d]' % (k, k))
            cols.append('[k%d]' % k)
            k += 1
        filtros.append('%shstack=inputs=3,pad=1280:720:(ow-iw)/2:0[e%d]'
                       % (''.join(cols), e))
        escenas.append('e%d' % e)
    paso = DUR - FADE
    ult = escenas[0]
    for i in range(1, len(escenas)):
        et = 'y%d' % i
        filtros.append('[%s][%s]xfade=transition=fade:duration=%s:offset=%s[%s]'
                       % (ult, escenas[i], FADE, round(i * paso, 3), et))
        ult = et
    cmd = [FF, '-y'] + ent + ['-filter_complex', ';'.join(filtros),
           '-map', '[%s]' % ult, '-an', '-c:v', 'libx264', '-preset', 'slow',
           '-crf', '23', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', salida]
    corre(cmd)
    print('apaisada:', salida, os.path.getsize(salida) // 1024, 'KB',
          round(len(escenas) * DUR - (len(escenas) - 1) * FADE, 1), 's')


if __name__ == '__main__':
    if 'v' in sys.argv[1:] or not sys.argv[1:]:
        vertical('assets/hero-navidad.mp4')
    if 'a' in sys.argv[1:] or not sys.argv[1:]:
        apaisada('assets/hero-navidad-ancho.mp4')
