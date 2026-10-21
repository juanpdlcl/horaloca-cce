/* ═══════════════════════════════════════════
   MODO NAVIDAD — CC Entertainment
   Se enciende de dos formas:
     · con ?navidad=1 en la dirección (para verlo sin publicarlo)
     · poniendo ENCENDIDO = true aquí abajo (queda fijo para todos)
   Apagarlo es volver a poner false: no toca nada más de la página.

   La decoración NO son dibujos: la guirnalda y el resplandor salen
   recortados de las fotos reales del show (assets/img/deco).
   ═══════════════════════════════════════════ */
(() => {
  const ENCENDIDO = false;            // ← ponlo en true cuando quieras dejarlo fijo

  const url = new URLSearchParams(location.search);
  const f = url.get('navidad');
  const activo = f === '1' || f === 'si' ? true : f === '0' || f === 'no' ? false : ENCENDIDO;
  if (!activo) return;

  const T = 'assets/img/tematicas';
  document.documentElement.classList.add('navidad');

  const quieto = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const movil = matchMedia('(max-width:720px)').matches;

  const A = 'assets/img/navidad-adornos';

  /* ── guirnalda colgando sobre la portada ──
     Adorno propio de CC (lazos magenta y plumas turquesa/morado/dorado, los
     colores del logo), recortado de "NAVIDAD CC.png". Va DENTRO de la portada
     y arranca bajo la barra: cuelga del menu sin pisar el logo y se queda
     arriba al bajar, en vez de seguir fija en pantalla. */
  const portada = document.querySelector('.hero');
  if (portada) {
    const g = document.createElement('div');
    g.className = 'nv-guirnalda';
    g.setAttribute('aria-hidden', 'true');
    portada.prepend(g);
  }

  /* ── nieve ──
     Tres capas de profundidad: los copos del fondo son pequeños, lentos y
     tenues; los del frente, grandes y suaves, como en una foto de verdad.
     Un solo lienzo, se detiene al cambiar de pestaña, y no existe si el
     equipo pide menos movimiento. */
  if (!quieto) {
    const lienzo = document.createElement('canvas');
    lienzo.className = 'nv-nieve';
    lienzo.setAttribute('aria-hidden', 'true');
    document.body.appendChild(lienzo);
    const ctx = lienzo.getContext('2d', { alpha: true });

    const DPR = Math.min(devicePixelRatio || 1, 2);
    const CAPAS = movil
      ? [{ n: 10, r: [0.8, 1.6], v: [0.18, 0.40], o: [0.25, 0.45] },
         { n: 6,  r: [2.0, 3.4], v: [0.42, 0.75], o: [0.40, 0.60] }]
      : [{ n: 26, r: [0.7, 1.5], v: [0.15, 0.35], o: [0.22, 0.42] },
         { n: 18, r: [1.7, 3.0], v: [0.38, 0.70], o: [0.35, 0.58] },
         { n: 7,  r: [4.5, 8.0], v: [0.75, 1.15], o: [0.14, 0.26] }];

    let an = 0, al = 0;
    const copos = [];
    const rnd = ([a, b]) => a + Math.random() * (b - a);
    const medir = () => {
      an = innerWidth; al = innerHeight;
      lienzo.width = Math.round(an * DPR); lienzo.height = Math.round(al * DPR);
      lienzo.style.width = an + 'px'; lienzo.style.height = al + 'px';
      ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    };
    const nace = (c, arriba) => ({
      capa: c,
      x: Math.random() * an,
      y: arriba ? -14 - Math.random() * 40 : Math.random() * al,
      r: rnd(c.r), vy: rnd(c.v), vx: -0.18 + Math.random() * 0.36,
      o: rnd(c.o), fase: Math.random() * 6.283, amp: 0.2 + Math.random() * 0.5,
    });
    medir();
    CAPAS.forEach((c) => { for (let i = 0; i < c.n; i++) copos.push(nace(c, false)); });
    addEventListener('resize', medir, { passive: true });

    /* copo suave: degradado radial, no un círculo duro */
    const pinta1 = (c) => {
      const grad = ctx.createRadialGradient(c.x, c.y, 0, c.x, c.y, c.r);
      grad.addColorStop(0, 'rgba(255,255,255,' + c.o + ')');
      grad.addColorStop(0.45, 'rgba(255,255,255,' + (c.o * 0.72) + ')');
      grad.addColorStop(1, 'rgba(255,255,255,0)');
      ctx.fillStyle = grad;
      ctx.beginPath(); ctx.arc(c.x, c.y, c.r, 0, 6.283); ctx.fill();
    };

    let vivo = true, lazo = 0, t = 0;
    const paso = () => {
      if (!vivo) return;
      ctx.clearRect(0, 0, an, al);
      t += 0.006;
      const viento = Math.sin(t) * 0.22;
      for (let i = 0; i < copos.length; i++) {
        const c = copos[i];
        c.y += c.vy;
        c.fase += 0.009;
        c.x += c.vx + viento + Math.sin(c.fase) * c.amp;
        if (c.y - c.r > al) Object.assign(c, nace(c.capa, true));
        if (c.x < -20) c.x = an + 16;
        else if (c.x > an + 20) c.x = -16;
        pinta1(c);
      }
      lazo = requestAnimationFrame(paso);
    };
    paso();
    document.addEventListener('visibilitychange', () => {
      vivo = !document.hidden;
      if (vivo) paso(); else cancelAnimationFrame(lazo);
    });
  }

  /* ── franja de Navidad en la portada ──
     Las fotos NO se recortan: cada una conserva su proporción real, así que
     no queda ninguna cara cortada. */
  const strip = document.querySelector('.strip');
  if (strip) {
    /* ancho y alto reales de cada foto: el navegador le reserva el sitio
       antes de bajarla, así que el mosaico no pega saltos al cargar. */
    const fotos = [
      ['navidad/12.jpg', 1200, 900, 'Santa, elfos y Sra. Claus', 'Show completo'],
      ['navidad/17.jpg', 800, 1200, 'Elfa de Navidad', 'Elfas'],
      ['navidad/13.jpg', 800, 1200, 'Santa y la Sra. Claus', 'Santa y Sra. Claus'],
      ['blanca-navidad/01.jpg', 750, 1000, 'Blanca Navidad bajo la nieve', 'Blanca Navidad'],
      ['navidad/10.jpg', 1200, 900, 'Santa, la galleta y los elfos', 'Santa y la galleta'],
      ['navidad/04.jpg', 912, 913, 'Soldados de juguete', 'Soldaditos'],
    ];
    const banda = document.createElement('section');
    banda.className = 'nv-banda';
    banda.innerHTML =
      '<span class="nv-corona" aria-hidden="true"></span>' +
      '<div class="container nv-dentro">' +
        '<div class="nv-cab">' +
          '<span class="nv-ramo" aria-hidden="true"></span>' +
          '<span class="nv-eti">Temporada navideña</span>' +
          '<h2>La Navidad de tu evento,<br><span class="thin">a lo grande</span></h2>' +
          '<p>Santa, el Grinch, la galleta, elfas, soldaditos y zancos. Montamos el ' +
          'show completo para tu cena de fin de año, tu fiesta de empresa o tu casa.</p>' +
          '<a href="cotiza/" class="btn btn-nv">Reservar mi fecha</a>' +
        '</div>' +
        '<div class="nv-mosaico">' +
          fotos.map(([src, w, h, alt, pie]) =>
            '<figure><img src="' + T + '/' + src + '" width="' + w + '" height="' + h + '" ' +
            'alt="' + alt + '" loading="lazy" decoding="async">' +
            '<figcaption>' + pie + '</figcaption></figure>').join('') +
        '</div>' +
      '</div>';
    /* ── el elenco: un retrato por personaje ──
       Recortados de la sesion de estudio, cada uno con su cara completa.
       Animacion por CSS (no .reveal) para que no exista forma de que se
       queden invisibles si algo falla. */
    const ELENCO = [
      ['santa', 'Santa Claus'], ['sra', 'Sra. Claus'], ['grinch', 'El Grinch'],
      ['galleta', 'La galleta'], ['elfa', 'Elfas'], ['baston', 'Bastón de caramelo'],
      ['soldados', 'Soldaditos'], ['zancos', 'Zancos'], ['blanca', 'Blanca Navidad'],
    ];
    const elenco = document.createElement('div');
    elenco.className = 'container nv-elenco';
    elenco.innerHTML =
      '<span class="nv-cinta" aria-hidden="true"></span>' +
      '<h3>Los personajes</h3>' +
      '<p class="nv-elenco-sub">Arma tu show con los que quieras.</p>' +
      '<ul>' + ELENCO.map(([slug, nom], i) =>
        '<li style="--i:' + i + '">' +
        '<img src="assets/img/navidad-personajes/' + slug + '.webp" width="420" height="420" ' +
        'alt="' + nom + '" loading="lazy" decoding="async">' +
        '<span>' + nom + '</span></li>').join('') + '</ul>';
    banda.appendChild(elenco);

    const cierre = document.createElement('span');
    cierre.className = 'nv-cierre';
    cierre.setAttribute('aria-hidden', 'true');
    banda.appendChild(cierre);

    strip.after(banda);
  }

  /* ── los destacados de la portada pasan a ser navideños ──
     OJO: aquí NO se puede clonar ni reemplazar la tarjeta. main.js observa
     los .reveal una sola vez al cargar; un nodo nuevo nunca sería observado
     y se quedaría en opacity:0 para siempre (era el hueco del medio).
     Como este archivo corre ANTES que main.js, basta con quitarle el id
     featAlt: main.js no lo encuentra y ni siquiera monta el carrusel. */
  const alt = document.getElementById('featAlt');
  if (alt) {
    alt.removeAttribute('id');
    const capas = alt.querySelectorAll('.fa-img');
    capas.forEach((x, i) => { if (i) x.remove(); else x.classList.remove('fa-img', 'on'); });
  }

  /* La tarjeta destacada es 16/10 y estas fotos son 4:3, así que al
     encajarlas sobra alto. El encuadre va casi pegado al borde de arriba
     para que el recorte se coma el piso y NUNCA una cara. */
  const NAV = [
    { pack: 'nv-completa', img: 'navidad/12.jpg', t: 'Navidad completa',
      s: 'Santa, elfos y la Sra. Claus', c: '#e03131',
      fotos: ['navidad/12.jpg', 'navidad/10.jpg', 'navidad/01.jpg', 'navidad/03.jpg', 'navidad/05.jpg'] },
    { pack: 'nv-grinch', img: 'navidad/11.jpg', t: 'El Grinch y la galleta',
      s: 'Los que se roban el show', c: '#1fa365',
      fotos: ['navidad/11.jpg', 'navidad/15.jpg', 'navidad/16.jpg', 'navidad/18.jpg'] },
    { pack: 'nv-santa', img: 'navidad/09.jpg', t: 'Santa y los elfos',
      s: 'El clásico que nunca falla', c: '#e9c478',
      fotos: ['navidad/09.jpg', 'navidad/13.jpg', 'navidad/17.jpg', 'navidad/19.jpg', 'navidad/20.jpg'] },
  ];

  /* sus propias fotos en el visor: main.js las recoge de window.PACKS_EXTRA */
  window.PACKS_EXTRA = Object.assign({}, window.PACKS_EXTRA);
  NAV.forEach((d) => {
    window.PACKS_EXTRA[d.pack] = { name: d.t, imgs: d.fotos.map((f) => T + '/' + f) };
  });

  document.querySelectorAll('.feat').forEach((el, i) => {
    const d = NAV[i];
    if (!d) return;
    const img = el.querySelector('.feat-cover img');
    if (img) { img.src = T + '/' + d.img; img.style.objectPosition = '50% 8%'; img.alt = d.t; }
    const cov = el.querySelector('.feat-cover');
    if (cov) { cov.dataset.pack = d.pack; cov.setAttribute('aria-label', 'Ver todas las fotos de ' + d.t); }
    const h3 = el.querySelector('h3'), p = el.querySelector('.feat-bar p'), bar = el.querySelector('.feat-bar');
    if (h3) h3.textContent = d.t;
    if (p) p.textContent = d.s;
    if (bar) bar.style.setProperty('--fc', d.c);
  });

  const et = document.querySelector('#destacados .sec-label');
  if (et) et.innerHTML = '<i class="nv-lazo" aria-hidden="true"></i>Navidad 2026';
  const h2 = document.querySelector('#destacados h2');
  if (h2) h2.textContent = 'Los shows de Navidad';
})();
