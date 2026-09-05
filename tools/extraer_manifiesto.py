# -*- coding: utf-8 -*-
"""Lee los catálogos PDF publicados y reconstruye su contenido exacto:
por página, cada foto (emparejada con el archivo del sitio por huella
perceptual), su nombre y su subtítulo. Sirve para regenerar el catálogo
sin depender de memoria: tools/manifiesto-*.json"""
import fitz, os, json
from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)


def huella(im):
    g = im.convert('L').resize((16, 16), Image.LANCZOS)
    px = list(g.getdata()); m = sum(px) / len(px)
    return ''.join('1' if p > m else '0' for p in px)


def dist(a, b):
    return sum(x != y for x, y in zip(a, b))


assets = {}
for root, _, files in os.walk('assets/img'):
    for f in files:
        if f.lower().endswith(('.jpg', '.png')) and not f.startswith('t-'):
            p = os.path.join(root, f).replace(os.sep, '/')
            try:
                assets[p] = huella(Image.open(p))
            except Exception:
                pass
print('assets indexados:', len(assets))


def manifiesto(pdf):
    doc = fitz.open(pdf); out = []
    for pno, page in enumerate(doc, 1):
        imgs = []
        for info in page.get_image_info(xrefs=True):
            x = info['xref']
            if not x:
                continue
            r = fitz.Rect(info['bbox'])
            if r.width < 120 or r.height < 120:      # logos y decoración
                continue
            pix = fitz.Pixmap(doc, x)
            if pix.n - pix.alpha >= 4:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            modo = 'RGB' if pix.n - pix.alpha == 3 else 'L'
            im = Image.frombytes(modo, (pix.width, pix.height), pix.samples).convert('RGB')
            h = huella(im)
            mejor = min(assets.items(), key=lambda kv: dist(kv[1], h))
            imgs.append({'rect': [round(v) for v in r], 'asset': mejor[0], 'd': dist(mejor[1], h)})
        textos = []
        for b in page.get_text('dict')['blocks']:
            for l in b.get('lines', []):
                for sp in l['spans']:
                    t = sp['text'].strip()
                    if t:
                        textos.append({'t': t, 'x': round(sp['bbox'][0]), 'y': round(sp['bbox'][1]),
                                       'font': sp['font'], 'size': round(sp['size'], 1),
                                       'color': '#%06x' % sp['color']})
        out.append({'page': pno, 'imgs': sorted(imgs, key=lambda i: (i['rect'][1], i['rect'][0])), 'textos': textos})
    return out


for pdf, nom in [('CC-Entertainment-Catalogo-Tematicas.pdf', 'general'),
                 ('CC-Entertainment-Catalogo-Navidad.pdf', 'navidad')]:
    m = manifiesto(pdf)
    json.dump(m, open(f'tools/manifiesto-{nom}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    dudosos = [(p['page'], i['asset'], i['d']) for p in m for i in p['imgs'] if i['d'] > 40]
    print(f"\n=== {nom}: {len(m)} páginas, {sum(len(p['imgs']) for p in m)} fotos; dudosos(d>40): {dudosos}")
    for p in m:
        for i in p['imgs']:
            x0, y0, x1, y1 = i['rect']
            nombre = [t for t in p['textos'] if t['size'] >= 13 and y1 - 4 <= t['y'] <= y1 + 40 and x0 - 60 <= t['x'] <= x1]
            sub = [t for t in p['textos'] if 7 <= t['size'] <= 9 and y1 + 14 <= t['y'] <= y1 + 62 and x0 - 60 <= t['x'] <= x1]
            print(f"  p{p['page']:02d} {str(i['rect']):<22} {i['asset']:<46} d={i['d']:<3}| {nombre[0]['t'] if nombre else '?':<28}| {sub[0]['t'] if sub else ''}")
