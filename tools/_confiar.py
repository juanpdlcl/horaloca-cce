# Abre `claude` en una pseudo-terminal, acepta el diálogo de confianza de la carpeta y sale.
import os, re, sys, time
from winpty import PtyProcess

PROY = r'C:\Users\EQUIPO\Desktop\Proyectos claude\horaloca-cce'
CLI = r'C:\Users\EQUIPO\claude-cli\claude.cmd'
limpio = lambda s: re.sub(r'\x1b\[[0-9;?]*[A-Za-z]|\x1b\][^\x07]*\x07|\r', '', s)

env = dict(os.environ)
env['PATH'] = r'C:\Users\EQUIPO\claude-cli;C:\Program Files\nodejs;' + env.get('PATH', '')
p = PtyProcess.spawn(f'cmd /c "{CLI}"', cwd=PROY, env=env, dimensions=(40, 140))
buf = ''; fase = 'esperando_dialogo'; t0 = time.time(); ultimo = t0
while p.isalive() and time.time() - t0 < 150:
    try:
        chunk = p.read()
        if chunk:
            buf += chunk; ultimo = time.time()
    except Exception:
        time.sleep(0.2)
    texto = limpio(buf)
    if fase == 'esperando_dialogo' and re.search(r'trust|conf[ií]a', texto, re.I) and time.time() - ultimo > 1.5:
        p.write('\r'); fase = 'aceptado'; t_acepto = time.time()
    elif fase == 'aceptado' and time.time() - t_acepto > 6:
        p.write('/exit\r'); fase = 'saliendo'; t_salida = time.time()
    elif fase == 'saliendo' and time.time() - t_salida > 6:
        try:
            p.terminate(force=True)
        except Exception:
            pass
        break
    time.sleep(0.15)
texto = limpio(buf)
print('FASE FINAL:', fase)
print('--- ultimas lineas ---')
print('\n'.join([l for l in texto.splitlines() if l.strip()][-25:]))
