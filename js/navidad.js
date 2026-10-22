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
  /* En la rama navidad-local va ENCENDIDO: esta rama ES la vista previa de
     Navidad, asi que la pagina abre navidena sin tener que anadir nada a la
     direccion. Para verla sin Navidad, ?navidad=0.
     En main no existe este archivo, asi que lo publicado no se entera. */
  const ENCENDIDO = true;

  const url = new URLSearchParams(location.search);
  const f = url.get('navidad');
  const activo = f === '1' || f === 'si' ? true : f === '0' || f === 'no' ? false : ENCENDIDO;
  if (!activo) return;

  const T = 'assets/img/tematicas';
  document.documentElement.classList.add('navidad');

  /* ── iconos navideños ──
     Dibujados en la misma retícula 24×24 y el mismo trazo de 1.5 que los
     iconos que la página ya usa (i-spark, i-music, i-drum). Así se leen como
     parte de la interfaz y no como una pegatina encima.
     Se inyectan desde aquí: con Navidad apagado, la página no los carga. */
  const sprite = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  sprite.setAttribute('width', '0');
  sprite.setAttribute('height', '0');
  sprite.setAttribute('aria-hidden', 'true');
  sprite.style.position = 'absolute';
  sprite.innerHTML =
    '<defs>' +
    '<symbol id="i-campana" viewBox="0 0 24 24">' +
      '<path d="M12 5.1a5.1 5.1 0 0 0-5.1 5.1c0 2.9-.6 4.5-1.5 5.5-.4.4-.1 1.1.5 1.1h12.2c.6 0 .9-.7.5-1.1-.9-1-1.5-2.6-1.5-5.5A5.1 5.1 0 0 0 12 5.1z"/>' +
      '<path d="M12 5.1V3.2"/><path d="M10.1 19.1a2 2 0 0 0 3.8 0"/>' +
    '</symbol>' +
    '<symbol id="i-estrella" viewBox="0 0 24 24">' +
      '<path d="m12 3.4 2.5 5.3 5.8.8-4.2 4 1 5.8-5.1-2.7-5.1 2.7 1-5.8-4.2-4 5.8-.8z"/>' +
    '</symbol>' +
    '<symbol id="i-copo" viewBox="0 0 24 24">' +
      '<path d="M12 2.8v18.4M4 7.4l16 9.2M20 7.4 4 16.6"/>' +
      '<path d="M12 6.6 9.8 4.9M12 6.6l2.2-1.7M12 17.4l-2.2 1.7M12 17.4l2.2 1.7"/>' +
      '<path d="M7.6 9.3 7.4 6.6M7.6 9.3 5.1 10M16.4 14.7l.2 2.7M16.4 14.7l2.5-.7"/>' +
      '<path d="M16.4 9.3 16.6 6.6M16.4 9.3l2.5.7M7.6 14.7l-.2 2.7M7.6 14.7l-2.5.7"/>' +
    '</symbol>' +
    '</defs>';
  document.body.appendChild(sprite);

  const icono = (id, clase) =>
    '<svg class="icon' + (clase ? ' ' + clase : '') + '" aria-hidden="true"><use href="#' + id + '"/></svg>';

  /* ── el video de la portada ──
     Clips de la destacada "Navidad" de Instagram, en su calidad original.
     Hay dos montajes porque la portada cubre TODA la pantalla y ningun
     video unico sirve para todas las formas:

       vertical  720x1560  el clip va entero en el centro, con bandas
                 desenfocadas arriba y abajo. Los telefonos de hoy son mas
                 alargados que el clip, asi que al cubrir la pantalla el
                 navegador recorta: que se coma el desenfoque y no a la gente.
       ancho    1280x720   tres clips verticales en columnas, cada uno a todo
                 lo alto. Al recortar de lado solo se ven menos columnas,
                 pero nadie queda cortado.

     El corte esta en 0.7: por debajo (telefono de pie) va el vertical; por
     encima (tablet, laptop, telefono acostado) va el ancho. Y se vuelve a
     elegir si giras el aparato. */
  const vid = document.getElementById('heroVideo');
  if (vid) {
    const anchoMQ = matchMedia('(min-aspect-ratio: 7/10)');
    let puesto = null;
    const pon = () => {
      const ancho = anchoMQ.matches;
      if (ancho === puesto) return;            // no recargar si no cambia
      puesto = ancho;
      const fuente = vid.querySelector('source');
      if (fuente) fuente.src = ancho ? 'assets/hero-navidad-ancho.mp4'
                                     : 'assets/hero-navidad.mp4';
      vid.poster = ancho ? 'assets/img/hero-navidad-poster-ancho.jpg'
                         : 'assets/img/hero-navidad-poster.jpg';
      vid.style.objectPosition = '50% 50%';
      vid.load();
      vid.play().catch(() => {});
    };
    pon();
    if (anchoMQ.addEventListener) anchoMQ.addEventListener('change', pon);
    else anchoMQ.addListener(pon);             // navegadores viejos
  }

  const quieto = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const movil = matchMedia('(max-width:720px)').matches;

  /* ═══════════════════════════════════════════════════════════════
     LUCES DE NAVIDAD

     Lo que separa una luz de Navidad de una pelota de color es que la
     bombilla EMITE. Cada una se pinta en cinco capas:

       1. el halo, en mezcla aditiva, que es la luz derramandose sobre
          el fondo. Sin esto parece una pegatina.
       2. el vidrio: una gota con degradado, saturado en el borde y
          encendido hacia el centro.
       3. el filamento, un punto casi blanco con el tono encima.
       4. el reflejo especular, una manchita clara arriba a la
          izquierda: es lo que hace que el vidrio parezca vidrio.
       5. el casquillo oscuro que la une al cable.

     El cable cuelga en arcos, como un cable de verdad, y las bombillas
     cuelgan de el por su propio peso. No parpadean encendido/apagado:
     laten, cada una a su ritmo, y algunas quedan mas apagadas que otras,
     que es como se ve una serie de verdad.
     ═══════════════════════════════════════════════════════════════ */
  const TONOS_LUZ = [
    [255, 58, 58],     // rojo
    [60, 220, 90],     // verde
    [64, 126, 255],    // azul
    [255, 186, 42],    // ambar
    [255, 70, 180],    // rosa, que es de la marca
  ];
  const CABLE = '#2b4a34';

  const cuerdas = [];

  const montaLuces = (donde, idx) => {
    if (!donde) return;
    const lienzo = document.createElement('canvas');
    lienzo.className = 'nv-luces';
    lienzo.setAttribute('aria-hidden', 'true');
    donde.prepend(lienzo);
    const cx = lienzo.getContext('2d');
    const cuerda = { el: lienzo, cx, bombillas: [], an: 0, al: 0, idx };
    cuerdas.push(cuerda);
    mideCuerda(cuerda);
    return cuerda;
  };

  function mideCuerda(c) {
    const caja = c.el.parentElement.getBoundingClientRect();
    const an = Math.max(320, Math.round(caja.width));
    const al = movil ? 56 : 76;
    const DPR = Math.min(devicePixelRatio || 1, 2);
    c.an = an; c.al = al;
    c.el.width = Math.round(an * DPR);
    c.el.height = Math.round(al * DPR);
    c.el.style.width = an + 'px';
    c.el.style.height = al + 'px';
    c.cx.setTransform(DPR, 0, 0, DPR, 0, 0);

    /* el cable se cuelga en arcos: cuantos quepan, de ancho parecido */
    const anchoArco = movil ? 150 : 215;
    const arcos = Math.max(2, Math.round(an / anchoArco));
    const paso = an / arcos;
    const caida = movil ? 15 : 20;
    const techo = movil ? 5 : 7;
    const sep = movil ? 19 : 23;

    c.arcos = [];
    c.bombillas = [];
    let n = 0;
    for (let i = 0; i < arcos; i++) {
      const x0 = i * paso, x1 = (i + 1) * paso;
      c.arcos.push({ x0, x1, techo, caida });
      const cuantas = Math.max(2, Math.round(paso / sep));
      for (let k = 1; k <= cuantas; k++) {
        const t = k / (cuantas + 1);
        c.bombillas.push({
          arco: i, t,
          tono: TONOS_LUZ[n % TONOS_LUZ.length],
          r: (movil ? 3.3 : 4.1) * (0.90 + Math.random() * 0.20),
          fase: Math.random() * 6.283,
          vel: 0.010 + Math.random() * 0.012,
          /* algunas nacen mas apagadas: una serie de verdad nunca tiene
             todas las bombillas igual de fuertes */
          fuerza: 0.72 + Math.random() * 0.28,
        });
        n++;
      }
    }
  }

  /* punto del arco y su inclinacion, para colgar la bombilla */
  const puntoArco = (a, t) => {
    const x = a.x0 + t * (a.x1 - a.x0);
    const y = a.techo + a.caida * Math.sin(Math.PI * t);
    const pend = (a.caida * Math.PI * Math.cos(Math.PI * t)) / (a.x1 - a.x0);
    return { x, y, ang: Math.atan(pend) };
  };

  function pintaBombilla(cx, x, y, r, tono, brillo, ang) {
    const [R, G, B] = tono;
    const rgb = (a) => 'rgba(' + R + ',' + G + ',' + B + ',' + a + ')';

    cx.globalCompositeOperation = 'lighter';

    /* 1a. el bloom: ancho y muy tenue. Es lo que una camara ve alrededor
       de una luz pequena, y lo que impide que parezca un punto pegado. */
    const bloom = cx.createRadialGradient(x, y, 0, x, y, r * 7.5);
    bloom.addColorStop(0, rgb(0.13 * brillo));
    bloom.addColorStop(1, rgb(0));
    cx.fillStyle = bloom;
    cx.beginPath(); cx.arc(x, y, r * 7.5, 0, 6.283); cx.fill();

    /* 1b. el halo ceñido: la luz pegada al vidrio */
    const halo = cx.createRadialGradient(x, y, 0, x, y, r * 3.1);
    halo.addColorStop(0, rgb(0.58 * brillo));
    halo.addColorStop(0.45, rgb(0.20 * brillo));
    halo.addColorStop(1, rgb(0));
    cx.fillStyle = halo;
    cx.beginPath(); cx.arc(x, y, r * 3.1, 0, 6.283); cx.fill();

    cx.globalCompositeOperation = 'source-over';

    cx.save();
    cx.translate(x, y);
    cx.rotate(ang * 0.42);          // cuelga casi a plomo

    /* 4. el casquillo, detras del vidrio */
    cx.fillStyle = 'rgba(26,32,26,.9)';
    cx.beginPath();
    cx.roundRect(-r * 0.38, -r * 2.05, r * 0.76, r * 0.85, r * 0.22);
    cx.fill();

    /* 2. el vidrio: una gota estrecha y alargada, como una luz de serie
       fina, no un bombillon redondo */
    const vidrio = cx.createRadialGradient(-r * 0.26, -r * 0.42, r * 0.08, 0, 0, r * 1.5);
    vidrio.addColorStop(0, 'rgba(255,255,255,' + (0.95 * brillo + 0.05) + ')');
    vidrio.addColorStop(0.34, rgb(0.98 * brillo + 0.02));
    vidrio.addColorStop(1, 'rgba(' + (R * 0.55 | 0) + ',' + (G * 0.55 | 0) + ',' + (B * 0.55 | 0) + ',' + (0.95 * brillo + 0.05) + ')');
    cx.fillStyle = vidrio;
    cx.beginPath();
    cx.ellipse(0, 0, r * 0.72, r * 1.38, 0, 0, 6.283);
    cx.fill();

    /* 3. el filamento: en pequeno es lo que manda, asi que va fuerte */
    cx.globalCompositeOperation = 'lighter';
    const nucleo = cx.createRadialGradient(0, -r * 0.12, 0, 0, -r * 0.12, r * 0.72);
    nucleo.addColorStop(0, 'rgba(255,253,246,' + (0.95 * brillo) + ')');
    nucleo.addColorStop(0.5, rgb(0.42 * brillo));
    nucleo.addColorStop(1, rgb(0));
    cx.fillStyle = nucleo;
    cx.beginPath(); cx.arc(0, -r * 0.12, r * 0.72, 0, 6.283); cx.fill();
    cx.globalCompositeOperation = 'source-over';

    /* 5. el reflejo del vidrio: pequeno pero presente */
    cx.fillStyle = 'rgba(255,255,255,' + (0.42 * brillo + 0.14) + ')';
    cx.beginPath();
    cx.ellipse(-r * 0.26, -r * 0.55, r * 0.17, r * 0.34, -0.45, 0, 6.283);
    cx.fill();

    cx.restore();
  }

  function pintaCuerda(c, t) {
    const cx = c.cx;
    cx.clearRect(0, 0, c.an, c.al);

    /* el cable primero, para que las bombillas vayan encima */
    cx.strokeStyle = CABLE;
    cx.lineWidth = movil ? 1.1 : 1.4;
    cx.lineCap = 'round';
    for (const a of c.arcos) {
      cx.beginPath();
      for (let i = 0; i <= 26; i++) {
        const p = puntoArco(a, i / 26);
        if (i) cx.lineTo(p.x, p.y); else cx.moveTo(p.x, p.y);
      }
      cx.stroke();
    }

    for (const b of c.bombillas) {
      const p = puntoArco(c.arcos[b.arco], b.t);
      /* late, no parpadea */
      const latido = 0.78 + 0.22 * Math.sin(t * b.vel * 60 + b.fase);
      pintaBombilla(cx, p.x, p.y + b.r * 1.1, b.r, b.tono, latido * b.fuerza, p.ang);
    }
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
    /* ── luces de Navidad desenfocadas ──
       Lo que de verdad dice "Navidad" en una foto de noche no es un adorno:
       son las bombillas del fondo, fuera de foco. Aqui no hay ningun objeto
       con silueta, asi que no hay nada con que chocar.

       Dos detalles importan:
       · El sprite lleva un ANILLO de lente (la parada de 0.80 brilla mas que
         la de 0.62). Eso es lo que hace que se lea como un desenfoque de
         camara y no como una mancha de color.
       · Se dibuja una sola vez en un lienzo aparte y luego se estampa. Nada
         de recalcular un degradado por cuadro. */
    const TONOS = [
      [255, 196, 107], [255, 196, 107], [255, 212, 150],   // oro de bombilla
      [255, 90, 74],                                        // rojo calido
      [82, 217, 154],                                       // verde pino
    ];
    const LADO = 128;
    const sellos = TONOS.map(([r, g, b]) => {
      const c = document.createElement('canvas');
      c.width = c.height = LADO;
      const cx = c.getContext('2d');
      const m = LADO / 2;
      const gr = cx.createRadialGradient(m, m, 0, m, m, m);
      const col = (a) => 'rgba(' + r + ',' + g + ',' + b + ',' + a + ')';
      gr.addColorStop(0, col(0.55));
      gr.addColorStop(0.62, col(0.42));
      gr.addColorStop(0.80, col(0.62));   // el anillo
      gr.addColorStop(1, col(0));
      cx.fillStyle = gr;
      cx.fillRect(0, 0, LADO, LADO);
      return c;
    });

    const TOPE = 0.10;                      // candado: por encima deja de ser bruma
    const luces = [];
    const naceLuz = () => {
      const i = (Math.random() * TONOS.length) | 0;
      return {
        sello: sellos[i], tono: TONOS[i],
        x: Math.random() * an, y: Math.random() * al,
        r: (movil ? 38 : 46) + Math.random() * (movil ? 54 : 84),
        a: 0.05 + Math.random() * 0.04,
        vx: (Math.random() < 0.5 ? -1 : 1) * (0.05 + Math.random() * 0.07),
        vy: -0.02 + Math.random() * 0.05,
        f: Math.random() * 6.283, vf: 0.0007 + Math.random() * 0.0008,
        k: 1, u: 0,                         // multiplicador y progreso de la campanada
      };
    };

    /* la campanada: cada 9-14 s una sola bombilla da un golpe de luz y se
       apaga despacio, con un aro que se abre. Es "usa campanas" resuelto
       como luz: el ataque seco y la cola larga SON la curva de una campana.
       Nunca dos a la vez. */
    let proxima = 4 + Math.random() * 4;

    medir();
    CAPAS.forEach((c) => { for (let i = 0; i < c.n; i++) copos.push(nace(c, false)); });
    for (let i = 0; i < (movil ? 4 : 7); i++) luces.push(naceLuz());

    /* ── efecto bola de nieve ──
       Al desplazar, la nieve se agita y se calma sola. Al cargar arranca
       sacudida, como un globo de nieve recien movido.
       El scroll SOLO guarda el valor; la cuenta va dentro del rAF. Leer
       layout en cada evento de scroll es justo lo que congela un telefono. */
    let rafaga = 1.1, yAnt = scrollY, yAhora = scrollY;
    addEventListener('scroll', () => { yAhora = scrollY; }, { passive: true });
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

    const pintaLuz = (L) => {
      const brillo = Math.min(TOPE, L.a * (0.78 + 0.22 * Math.sin(L.f))) * L.k;
      ctx.globalAlpha = brillo;
      ctx.drawImage(L.sello, L.x - L.r, L.y - L.r, L.r * 2, L.r * 2);
      ctx.globalAlpha = 1;
      if (L.k > 1.05) {                     // el aro de la campanada
        const rr = L.r * (1 + 2.2 * L.u);
        ctx.strokeStyle = 'rgba(' + L.tono[0] + ',' + L.tono[1] + ',' + L.tono[2] + ',' + (0.06 * (1 - L.u)) + ')';
        ctx.lineWidth = 1.5 * (1 - L.u);
        ctx.beginPath(); ctx.arc(L.x, L.y, rr, 0, 6.283); ctx.stroke();
      }
    };

    let vivo = true, lazo = 0, t = 0, antes = 0, saltar = false;
    const paso = (ahora) => {
      if (!vivo) return;
      /* freno: si un cuadro tarda demasiado, ese cuadro se queda sin luces.
         Lo primero que se cae siempre es la luz, nunca la nieve. */
      saltar = antes ? (ahora - antes) > 34 : false;
      antes = ahora;

      ctx.clearRect(0, 0, an, al);
      t += 0.006;

      const d = Math.abs(yAhora - yAnt); yAnt = yAhora;
      rafaga = Math.min(1.6, rafaga + Math.min(d, 60) * 0.006) * 0.955;
      const viento = Math.sin(t) * 0.22 + rafaga * 1.1;

      if (!saltar) {
        proxima -= 0.016;
        if (proxima <= 0 && !luces.some((L) => L.k > 1.02)) {
          const L = luces[(Math.random() * luces.length) | 0];
          if (L) { L.k = 2.4; L.u = 0; }
          proxima = 9 + Math.random() * 5;
        }
        ctx.globalCompositeOperation = 'lighter';
        for (let i = 0; i < luces.length; i++) {
          const L = luces[i];
          L.x += L.vx + viento * 0.25;
          L.y += L.vy;
          L.f += L.vf;
          if (L.k > 1) { L.k = 1 + (L.k - 1) * 0.978; L.u = Math.min(1, L.u + 0.012); }
          else { L.k = 1; L.u = 0; }
          if (L.x < -L.r) L.x = an + L.r; else if (L.x > an + L.r) L.x = -L.r;
          if (L.y < -L.r) L.y = al + L.r; else if (L.y > al + L.r) L.y = -L.r;
          pintaLuz(L);
        }
        ctx.globalCompositeOperation = 'source-over';
      }

      if (!saltar) for (let k = 0; k < cuerdas.length; k++) pintaCuerda(cuerdas[k], t * 60);

      for (let i = 0; i < copos.length; i++) {
        const c = copos[i];
        c.y += c.vy * (1 + rafaga * 0.3);
        c.fase += 0.009;
        c.x += c.vx + viento + Math.sin(c.fase) * c.amp;
        if (c.y - c.r > al) Object.assign(c, nace(c.capa, true));
        if (c.x < -20) c.x = an + 16;
        else if (c.x > an + 20) c.x = -16;
        pinta1(c);
      }
      lazo = requestAnimationFrame(paso);
    };
    paso(0);
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
      ['navidad/17.jpg', 800, 1200, 'Regalos de Navidad', 'Regalos'],
      ['navidad/13.jpg', 800, 1200, 'Santa y la Sra. Claus', 'Santa y Sra. Claus'],
      ['blanca-navidad/01.jpg', 750, 1000, 'Blanca Navidad bajo la nieve', 'Blanca Navidad'],
      ['navidad/10.jpg', 1200, 900, 'Santa, la galleta y los elfos', 'Santa y la galleta'],
      ['navidad/04.jpg', 912, 913, 'Soldados de juguete', 'Soldaditos'],
    ];
    const banda = document.createElement('section');
    banda.className = 'nv-banda';
    banda.innerHTML =
      '<div class="container nv-dentro">' +
        '<div class="nv-cab">' +
          '<span class="nv-eti">' + icono('i-campana') + 'Temporada navideña</span>' +
          '<h2>La Navidad de tu evento,<br><span class="thin">a lo grande</span></h2>' +
          '<p>Santa, el Grinch, la galleta, los Regalos, soldaditos y zancos. Montamos el ' +
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
    strip.after(banda);
    montaLuces(banda, 0);
  }

  /* si el equipo pide menos movimiento no hay bucle, asi que se pintan una
     sola vez y se quedan encendidas y quietas */
  if (quieto) cuerdas.forEach((c) => pintaCuerda(c, 0));

  addEventListener('resize', () => {
    cuerdas.forEach((c) => { mideCuerda(c); if (quieto) pintaCuerda(c, 0); });
  }, { passive: true });

  /* ── los adornos de fondo pasan a campanas ──
     No se añade nada: el hueco ya existe. La sección de destacados ya tenía
     bolas de disco y plumas flotando detrás; solo se cambia QUÉ flota. Por
     eso no choca: el sitio estaba hecho para eso. */
  const deco = document.querySelectorAll('.sec-deco .sd');
  deco.forEach((img) => { img.src = 'assets/img/deco/nv-campanas.webp'; });

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
  /* Las tres son retratos de estudio de 800x1200, o sea 2:3 exacto. Con la
     tarjeta puesta en 2/3 encajan clavadas: no se recorta ni un pixel, asi
     que es imposible que corten una cara. */
  const NAV = [
    { pack: 'nv-santa', img: 'navidad/13.jpg', t: 'Santa y la Sra. Claus',
      s: 'El clásico que nunca falla', c: '#d7263d',
      fotos: ['navidad/13.jpg', 'navidad/09.jpg', 'navidad/12.jpg', 'navidad/01.jpg', 'navidad/05.jpg'] },
    { pack: 'nv-regalos', img: 'navidad/17.jpg', t: 'Regalos',
      s: 'Las que levantan la fiesta', c: '#2f9e5f',
      fotos: ['navidad/17.jpg', 'navidad/16.jpg', 'navidad/20.jpg', 'navidad/21.jpg'] },
    { pack: 'nv-baston', img: 'navidad/18.jpg', t: 'Bastón de caramelo',
      s: 'Con la Sra. Claus de rojo', c: '#e8c37a',
      fotos: ['navidad/18.jpg', 'navidad/11.jpg', 'navidad/15.jpg', 'navidad/10.jpg'] },
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
    if (img) { img.src = T + '/' + d.img; img.style.objectPosition = '50% 50%'; img.alt = d.t; }
    const cov = el.querySelector('.feat-cover');
    if (cov) { cov.dataset.pack = d.pack; cov.setAttribute('aria-label', 'Ver todas las fotos de ' + d.t); }
    const h3 = el.querySelector('h3'), p = el.querySelector('.feat-bar p'), bar = el.querySelector('.feat-bar');
    if (h3) h3.textContent = d.t;
    if (p) p.textContent = d.s;
    if (bar) bar.style.setProperty('--fc', d.c);
  });

  const et = document.querySelector('#destacados .sec-label');
  if (et) et.innerHTML = icono('i-campana') + 'Navidad 2026';
  const h2 = document.querySelector('#destacados h2');
  if (h2) h2.textContent = 'Los shows de Navidad';
})();
