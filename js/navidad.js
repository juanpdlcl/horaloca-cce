/* ═══════════════════════════════════════════
   MODO NAVIDAD — CC Entertainment
   Se enciende de dos formas:
     · con ?navidad=1 en la dirección (para verlo sin publicarlo)
     · poniendo ENCENDIDO = true aquí abajo (queda fijo para todos)
   Apagarlo es volver a poner false: no toca nada más de la página.
   ═══════════════════════════════════════════ */
(() => {
  const ENCENDIDO = false;            // ← ponlo en true cuando quieras dejarlo fijo

  const url = new URLSearchParams(location.search);
  const forzado = url.get('navidad');
  const activo = forzado === '1' || forzado === 'si' ? true
    : forzado === '0' || forzado === 'no' ? false
    : ENCENDIDO;
  if (!activo) return;

  const T = 'assets/img/tematicas';
  const html = document.documentElement;
  html.classList.add('navidad');

  const quieto = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const movil = matchMedia('(max-width:720px)').matches;

  /* ── guirnalda de luces bajo la barra ── */
  const guirnalda = document.createElement('div');
  guirnalda.className = 'nv-luces';
  guirnalda.setAttribute('aria-hidden', 'true');
  guirnalda.innerHTML = Array.from({ length: 40 }, (_, i) =>
    `<i style="--d:${(i % 7) * 0.28}s"></i>`).join('');
  document.body.prepend(guirnalda);

  /* ── nieve ──
     Lienzo único y ligero: 40 copos en escritorio, 16 en teléfono. Se
     detiene solo al cambiar de pestaña y no existe si el equipo pide
     menos movimiento. */
  if (!quieto) {
    const lienzo = document.createElement('canvas');
    lienzo.className = 'nv-nieve';
    lienzo.setAttribute('aria-hidden', 'true');
    document.body.appendChild(lienzo);
    const ctx = lienzo.getContext('2d');
    let an = 0, al = 0, copos = [];
    const CUANTOS = movil ? 16 : 40;

    const medir = () => {
      an = lienzo.width = innerWidth;
      al = lienzo.height = innerHeight;
    };
    const nuevo = (arriba) => ({
      x: Math.random() * an,
      y: arriba ? -10 - Math.random() * al : Math.random() * al,
      r: 1 + Math.random() * 2.6,
      vy: 0.25 + Math.random() * 0.75,
      vx: -0.25 + Math.random() * 0.5,
      o: 0.35 + Math.random() * 0.5,
      f: Math.random() * Math.PI * 2,
    });
    medir();
    copos = Array.from({ length: CUANTOS }, () => nuevo(false));
    addEventListener('resize', medir, { passive: true });

    let corriendo = true, lazo = 0;
    const pinta = () => {
      if (!corriendo) return;
      ctx.clearRect(0, 0, an, al);
      ctx.fillStyle = '#fff';
      copos.forEach((c) => {
        c.y += c.vy;
        c.f += 0.012;
        c.x += c.vx + Math.sin(c.f) * 0.35;
        if (c.y > al + 12) Object.assign(c, nuevo(true));
        if (c.x < -12) c.x = an + 10;
        if (c.x > an + 12) c.x = -10;
        ctx.globalAlpha = c.o;
        ctx.beginPath();
        ctx.arc(c.x, c.y, c.r, 0, 6.283);
        ctx.fill();
      });
      ctx.globalAlpha = 1;
      lazo = requestAnimationFrame(pinta);
    };
    pinta();
    document.addEventListener('visibilitychange', () => {
      corriendo = !document.hidden;
      if (corriendo) pinta(); else cancelAnimationFrame(lazo);
    });
  }

  /* ── franja de Navidad en la portada, con las mejores fotos ── */
  const strip = document.querySelector('.strip');
  if (strip) {
    const banda = document.createElement('section');
    banda.className = 'nv-banda';
    banda.innerHTML = `
      <div class="container">
        <div class="nv-cab">
          <span class="nv-eti">★ Temporada navideña</span>
          <h2>La Navidad de tu empresa, <span class="thin">a lo grande</span></h2>
          <p>Santa, el Grinch, la galleta, elfas, soldaditos y zancos. Montamos el show
             completo para tu cena de fin de año, tu fiesta de empresa o tu casa.</p>
          <a href="cotiza/#navidad" class="btn btn-nv">Reservar mi fecha</a>
        </div>
        <div class="nv-fotos">
          <figure class="nv-f1"><img src="${T}/navidad/12.jpg" alt="Show de Navidad completo" loading="lazy"><figcaption>Show completo</figcaption></figure>
          <figure class="nv-f2"><img src="${T}/navidad/13.jpg" alt="Santa y sus ayudantes" loading="lazy"><figcaption>Santa y sus ayudantes</figcaption></figure>
          <figure class="nv-f3"><img src="${T}/blanca-navidad/01.jpg" alt="Blanca Navidad" loading="lazy"><figcaption>Blanca Navidad</figcaption></figure>
          <figure class="nv-f4"><img src="${T}/navidad/17.jpg" alt="Elfa" loading="lazy"><figcaption>Elfas</figcaption></figure>
          <figure class="nv-f5"><img src="${T}/navidad/04.jpg" alt="Soldados de juguete" loading="lazy"><figcaption>Soldados de juguete</figcaption></figure>
        </div>
      </div>`;
    strip.after(banda);
  }

  /* ── en la portada, los destacados pasan a ser navideños ── */
  /* La tarjeta del medio va rotando sola (el carrusel de la portada) y
     revertía lo que le pusiéramos. Se sustituye por un clon: el temporizador
     se queda hablando con el nodo viejo, que ya no está en la página. */
  const alt = document.getElementById('featAlt');
  if (alt) {
    const tarjeta = alt.closest('.feat');
    if (tarjeta) {
      const copia = tarjeta.cloneNode(true);
      /* sin los identificadores, el temporizador ya no la encuentra */
      ['featAlt', 'faTitle', 'faSub'].forEach((id) => {
        const e = copia.querySelector('#' + id);
        if (e) e.removeAttribute('id');
      });
      copia.querySelectorAll('.fa-img').forEach((x, i) => { if (i) x.remove(); else x.classList.remove('fa-img'); });
      tarjeta.replaceWith(copia);
    }
  }

  const feats = document.querySelectorAll('.feat');
  if (feats.length >= 3) {
    const nav = [
      { img: `${T}/navidad/12.jpg`, pos: '50% 38%', t: 'Navidad completa', s: 'Santa, el Grinch y la galleta', c: 'var(--red)' },
      { img: `${T}/navidad/09.jpg`, pos: '50% 34%', t: 'Santa y los elfos', s: 'El clásico que nunca falla', c: 'var(--green)' },
      { img: `${T}/blanca-navidad/01.jpg`, pos: '50% 30%', t: 'Blanca Navidad', s: 'Invierno en blanco y plata', c: '#d7dce8' },
    ];
    feats.forEach((f, i) => {
      const d = nav[i];
      if (!d) return;
      const img = f.querySelector('.feat-cover img');
      if (img) { img.src = d.img; img.style.objectPosition = d.pos; img.alt = d.t; }
      f.querySelectorAll('.feat-cover img').forEach((x, k) => { if (k) x.remove(); });
      const h3 = f.querySelector('h3'), p = f.querySelector('.feat-bar p'), bar = f.querySelector('.feat-bar');
      if (h3) h3.textContent = d.t;
      if (p) p.textContent = d.s;
      if (bar) bar.style.setProperty('--fc', d.c);
    });
    const et = document.querySelector('#destacados .sec-label');
    if (et) et.innerHTML = '<span style="color:var(--red)">★</span>Navidad 2026';
    const h2 = document.querySelector('#destacados h2');
    if (h2) h2.textContent = 'Los shows de Navidad';
  }
})();
