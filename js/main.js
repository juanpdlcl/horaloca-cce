/* ═══════════════════════════════════════════
   CC ENTERTAINMENT — Horas Locas
   JS compartido entre index.html y cotiza.html
   (cada bloque comprueba si sus elementos existen).
   Cotización a la medida: sin precios fijos.
   ═══════════════════════════════════════════ */

const WHATSAPP = '18293435460';

/* pos = object-position del recorte (sube o baja el encuadre de la foto)
   themed = al agregarlo se elige la temática */
const SERVICES = [
  { id: 'hora-loca',   img: 'assets/img/destacado/dorado-4.jpg', pos: '50% 40%', themed: true, name: 'Hora Loca', desc: 'Personajes, cotillón y 45–60 minutos de pura energía. Elige tu temática.' },
  { id: 'coreografia', img: 'assets/img/destacado/plata-1.jpg',  pos: '50% 25%', name: 'Coreografía personalizada', desc: 'Montaje profesional para tu entrada, apertura o sorpresa.' },
  { id: 'zanqueros',   img: 'assets/img/ig/gold-zanqueros.jpg',pos: '50% 30%', name: 'Zanqueros',                 desc: 'Altura y espectáculo que llenan la pista.' },
  { id: 'percusion',   img: 'assets/img/promo/musicos.jpg',        pos: '50% 42%', name: 'Percusión en vivo',      desc: 'Tambora, güira y tambores LED que encienden la fiesta junto al DJ.' },
  { id: 'robot-led',   img: 'assets/img/promo/robot-espejo.jpg',   pos: '50% 25%', name: 'Robot LED',              desc: 'Show futurista iluminado para el punto alto de la noche.' },
  { id: 'cabezones',   img: 'assets/img/promo/artistas.jpg',       pos: '50% 30%', name: 'Cabezones',              desc: 'Tus artistas favoritos en versión gigante, animando la pista.' },
  { id: 'bailarines',  img: 'assets/img/promo/bailarinas-led.jpg', pos: '50% 35%', name: 'Bailarines adicionales', desc: 'Refuerza el cuerpo de baile de tu show.' },
];

/* temáticas disponibles para la Hora Loca (fotos reales del catálogo) */
const THEMES = [
  { id: 'gold',     name: 'Gold',                img: 'assets/img/destacado/dorado-2.jpg' },
  { id: 'led',      name: 'Led Party',           img: 'assets/img/destacado/plata-2.jpg' },
  { id: 'carnaval', name: 'Carnaval Dominicano', img: 'assets/img/ig/carnaval.jpg' },
  { id: 'tropical', name: 'Tropical',            img: 'assets/img/ig/tropical-sunset.jpg' },
  { id: 'rouge',    name: 'Rouge Royal',         img: 'assets/img/rojo.jpg' },
  { id: 'catrinas', name: 'Catrinas',            img: 'assets/img/catrinas.jpg' },
  { id: 'venezia',  name: 'Venezia',             img: 'assets/img/ig/venetian.jpg' },
  { id: 'vegas',    name: 'Viva Las Vegas',      img: 'assets/img/ig/vegas-hd.jpg' },
  { id: 'otra',     name: 'Otra / por definir',  img: 'assets/img/ig/troupe.jpg' },
];

const byId = (id) => SERVICES.find((s) => s.id === id);
const $ = (id) => document.getElementById(id);

/* ─── PRELOADER (solo index) ─── */
if ($('preloader')) {
  window.addEventListener('load', () => {
    setTimeout(() => $('preloader').classList.add('done'), 800);
  });
}

/* ─── SELECCIÓN (id -> cantidad), compartida entre páginas ─── */
let quote = {};
try { quote = JSON.parse(localStorage.getItem('cce-quote') || '{}'); } catch (_) { quote = {}; }
if (!quote || typeof quote !== 'object' || Array.isArray(quote)) quote = {};
Object.keys(quote).forEach((key) => {
  const [sid, tid] = key.split(':');
  const okService = !!byId(sid);
  const okTheme = !tid || THEMES.some((t) => t.id === tid);
  if (!okService || !okTheme || !Number.isInteger(quote[key]) || quote[key] < 1) delete quote[key];
});

function save() { localStorage.setItem('cce-quote', JSON.stringify(quote)); }
function totalItems() { return Object.keys(quote).length; }

/* ─── COTIZADOR (solo cotiza.html) ─── */
const servGrid = $('servGrid');
if (servGrid) {
  const cartCount = $('cartCount');
  const cartItems = $('cartItems');
  const cartDrawer = $('cartDrawer');
  const cartOverlay = $('cartOverlay');
  const toast = $('toast');
  let toastTimer;
  let lastFocus = null;

  servGrid.innerHTML = SERVICES.map((s) => `
    <button class="serv" data-id="${s.id}" type="button" aria-pressed="false">
      <span class="serv-check"><svg class="icon"><use href="#i-check"/></svg></span>
      <span class="serv-img"><img src="${s.img}" alt="" loading="lazy" style="object-position:${s.pos}"></span>
      <span class="serv-body">
        <h3>${s.name}</h3>
        <p>${s.desc}</p>
        <span class="serv-state state-off"><svg class="icon"><use href="#i-plus"/></svg> ${s.themed ? 'Elegir temática' : 'Agregar'}</span>
        <span class="serv-state state-on" hidden><svg class="icon"><use href="#i-check"/></svg> Agregado</span>
      </span>
    </button>
  `).join('');

  /* claves del carrito: "servicio" o "servicio:tematica" */
  const parseKey = (key) => {
    const [sid, tid] = key.split(':');
    return { sid, tid, service: byId(sid), theme: THEMES.find((t) => t.id === tid) || null };
  };
  const keyName = (key) => {
    const { service, theme } = parseKey(key);
    return service.name + (theme ? ` — ${theme.name}` : '');
  };
  const keyImg = (key) => {
    const { service, theme } = parseKey(key);
    return (theme && theme.img) || service.img;
  };

  function showToast(msg) {
    $('toastMsg').textContent = msg;
    toast.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove('show'), 2100);
  }

  function syncUI() {
    const keys = Object.keys(quote);
    cartCount.textContent = keys.length;
    cartCount.classList.toggle('on', keys.length > 0);

    document.querySelectorAll('.serv').forEach((card) => {
      const sid = card.dataset.id;
      const mine = keys.filter((k) => parseKey(k).sid === sid);
      const on = mine.length > 0;
      card.classList.toggle('on', on);
      card.setAttribute('aria-pressed', on);
      card.querySelector('.state-off').hidden = on;
      const stateOn = card.querySelector('.state-on');
      stateOn.hidden = !on;
      if (on) {
        stateOn.innerHTML = `<svg class="icon"><use href="#i-check"/></svg> Agregado${mine.length > 1 ? ` ×${mine.length}` : ''}`;
      }
    });

    $('quoteHint').innerHTML = keys.length === 0
      ? 'Selecciona los elementos que quieras incluir'
      : `<strong>${keys.length}</strong> ${keys.length === 1 ? 'elemento seleccionado' : 'elementos seleccionados'}`;

    if (!keys.length) {
      cartItems.innerHTML = `
        <div class="cart-empty">
          <svg class="icon"><use href="#i-cart"/></svg>
          Aún no has seleccionado nada.<br>Elige los elementos de tu show.
        </div>`;
      return;
    }
    cartItems.innerHTML = keys.map((key) => `
      <div class="cart-item">
        <img class="cart-item-thumb" src="${keyImg(key)}" alt="">
        <div class="cart-item-info"><strong>${keyName(key)}</strong></div>
        <div class="cart-qty">
          <button data-dec="${key}" aria-label="Quitar uno"><svg class="icon"><use href="#i-minus"/></svg></button>
          <span>${quote[key]}</span>
          <button data-inc="${key}" aria-label="Agregar uno"><svg class="icon"><use href="#i-plus"/></svg></button>
        </div>
        <button class="cart-item-del" data-del="${key}" aria-label="Eliminar"><svg class="icon"><use href="#i-trash"/></svg></button>
      </div>`).join('');
  }

  function addKey(key) {
    quote[key] = (quote[key] || 0) + 1;
    cartCount.classList.remove('bump');
    void cartCount.offsetWidth;
    cartCount.classList.add('bump');
    showToast(`${keyName(key)} agregado`);
    save();
    syncUI();
  }
  function removeKey(key) {
    delete quote[key];
    showToast(`${keyName(key)} quitado`);
    save();
    syncUI();
  }

  /* ── selector de temáticas (para Hora Loca) ── */
  const picker = $('picker');
  let pickerSid = null;
  function openPicker(sid) {
    pickerSid = sid;
    $('pickerGrid').innerHTML = THEMES.map((t) => {
      const key = `${sid}:${t.id}`;
      const on = !!quote[key];
      return `
        <button class="pk ${on ? 'on' : ''}" data-theme="${t.id}" type="button">
          <img src="${t.img}" alt="" loading="lazy">
          <span class="pk-name">${t.name}</span>
          <span class="pk-check"><svg class="icon"><use href="#i-check"/></svg></span>
        </button>`;
    }).join('');
    picker.hidden = false;
    document.body.style.overflow = 'hidden';
  }
  function closePicker() {
    picker.hidden = true;
    document.body.style.overflow = '';
    pickerSid = null;
  }
  $('pickerGrid').addEventListener('click', (e) => {
    const b = e.target.closest('.pk');
    if (!b) return;
    const key = `${pickerSid}:${b.dataset.theme}`;
    if (quote[key]) removeKey(key); else addKey(key);
    b.classList.toggle('on', !!quote[key]);
  });
  $('pickerClose').addEventListener('click', closePicker);
  $('pickerDone').addEventListener('click', closePicker);
  picker.addEventListener('click', (e) => { if (e.target === picker) closePicker(); });

  /* panel: foco, inert y apertura */
  const background = () => [
    $('nav'),
    ...document.querySelectorAll('body > .strip, body > main, body > section, body > footer'),
  ];
  cartDrawer.inert = true; // cerrado al cargar: fuera del orden de tabulación
  function openCart() {
    lastFocus = document.activeElement;
    cartDrawer.inert = false;
    cartDrawer.classList.add('open');
    cartOverlay.classList.add('open');
    document.body.style.overflow = 'hidden';
    background().forEach((el) => { el.inert = true; });
    $('cartBtn').setAttribute('aria-expanded', 'true');
    $('cartClose').focus();
  }
  function closeCart() {
    cartDrawer.inert = true;
    cartDrawer.classList.remove('open');
    cartOverlay.classList.remove('open');
    document.body.style.overflow = '';
    background().forEach((el) => { el.inert = false; });
    $('cartBtn').setAttribute('aria-expanded', 'false');
    if (lastFocus && document.contains(lastFocus)) lastFocus.focus();
  }

  document.addEventListener('click', (ev) => {
    const card = ev.target.closest('.serv');
    if (card) {
      const s = byId(card.dataset.id);
      if (s.themed) { openPicker(s.id); return; }
      if (quote[s.id]) removeKey(s.id); else addKey(s.id);
      return;
    }

    const btn = ev.target.closest('[data-inc],[data-dec],[data-del]');
    if (!btn) return;
    if (btn.dataset.inc) {
      // actualizar solo la cantidad, sin re-render (conserva el foco del teclado)
      quote[btn.dataset.inc]++;
      btn.closest('.cart-qty').querySelector('span').textContent = quote[btn.dataset.inc];
      save();
      return;
    }
    if (btn.dataset.dec) {
      const key = btn.dataset.dec;
      quote[key]--;
      if (quote[key] >= 1) {
        btn.closest('.cart-qty').querySelector('span').textContent = quote[key];
        save();
        return;
      }
      delete quote[key];
    }
    if (btn.dataset.del) delete quote[btn.dataset.del];
    save();
    syncUI();
    // el botón enfocado fue destruido por el re-render: devolver el foco al panel
    if (cartDrawer.classList.contains('open')) {
      (cartItems.querySelector('button') || $('cartClose')).focus();
    }
  });

  $('cartBtn').addEventListener('click', openCart);
  $('quoteReview').addEventListener('click', () => {
    if (!Object.keys(quote).length) { showToast('Selecciona al menos un elemento'); return; }
    openCart();
  });
  $('cartClose').addEventListener('click', closeCart);
  cartOverlay.addEventListener('click', closeCart);
  document.addEventListener('keydown', (e) => {
    if (e.key !== 'Escape') return;
    if (!picker.hidden) { closePicker(); return; }
    closeCart();
  });

  /* ordenar: valida, crea el ticket y abre WhatsApp con fotos */
  $('cartOrder').addEventListener('click', () => {
    const keys = Object.keys(quote);
    if (!keys.length) { showToast('Selecciona al menos un elemento'); return; }

    const name = $('qName').value.trim();
    const phone = $('qPhone').value.replace(/[^\d+]/g, '');
    $('qName').classList.toggle('invalid', !name);
    $('qPhone').classList.toggle('invalid', phone.length < 8);
    if (!name) { showToast('Escribe tu nombre'); $('qName').focus(); return; }
    if (phone.length < 8) { showToast('Escribe un teléfono válido'); $('qPhone').focus(); return; }

    const date = $('qDate').value.trim();
    const place = $('qPlace').value.trim();
    const items = keys.map((key) => ({
      id: key,
      name: keyName(key),
      qty: quote[key],
      img: keyImg(key),
    }));

    // ticket para el panel administrativo
    const ticket = {
      id: Date.now().toString(36).toUpperCase().slice(-6),
      ts: new Date().toISOString(),
      name, phone,
      type: eventType || 'Por definir',
      date: date || 'Por definir',
      place: place || 'Por definir',
      items,
      status: 'nueva',
    };
    try {
      const all = JSON.parse(localStorage.getItem('cce-tickets') || '[]');
      all.unshift(ticket);
      localStorage.setItem('cce-tickets', JSON.stringify(all));
    } catch (_) { /* almacenamiento lleno o bloqueado: el WhatsApp sale igual */ }

    // si Supabase está configurado, el ticket también viaja a la nube
    const SB = window.CCE_SUPABASE || {};
    if (SB.url && SB.key) {
      fetch(`${SB.url}/rest/v1/tickets`, {
        method: 'POST',
        headers: {
          apikey: SB.key,
          Authorization: `Bearer ${SB.key}`,
          'Content-Type': 'application/json',
          Prefer: 'return=minimal',
        },
        body: JSON.stringify(ticket),
      }).catch(() => {});
    }

    const lines = items.map((it, i) => [
      `${i + 1}) ${it.name}${it.qty > 1 ? ` ×${it.qty}` : ''}`,
      `   Foto: ${new URL(it.img, location.href).href}`,
    ].join('\n'));
    const msg = [
      `*COTIZACIÓN #${ticket.id}* — CC Entertainment`,
      '',
      `*Nombre:* ${name}`,
      `*WhatsApp:* ${phone}`,
      `*Tipo de evento:* ${ticket.type}`,
      `*Lugar:* ${ticket.place}`,
      `*Fecha:* ${ticket.date}`,
      '',
      '*Mi selección:*',
      ...lines,
      '',
      'Enviado desde la página web.',
    ].join('\n');
    const url = `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(msg)}`;

    // limpiar la selección: el ticket ya quedó guardado
    quote = {};
    save();
    syncUI();
    closeCart();
    showToast(`Ticket #${ticket.id} creado`);

    // en in-app browsers (Instagram/Facebook) window.open devuelve null
    const win = window.open(url, '_blank', 'noopener');
    if (!win) location.href = url;
  });

  /* chips de tipo de evento (selección única) */
  let eventType = '';
  $('qType').addEventListener('click', (ev) => {
    const b = ev.target.closest('button[data-type]');
    if (!b) return;
    const on = !b.classList.contains('on');
    $('qType').querySelectorAll('button').forEach((x) => x.classList.remove('on'));
    b.classList.toggle('on', on);
    eventType = on ? b.dataset.type : '';
  });

  syncUI();
}

/* ─── NAVBAR ─── */
const nav = $('nav');
const navLinks = $('navLinks');
const navBurger = $('navBurger');
if (!document.body.classList.contains('page-cotiza')) {
  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 40);
  }, { passive: true });
}
navBurger.addEventListener('click', () => {
  const open = navLinks.classList.toggle('open');
  navBurger.classList.toggle('open', open);
  navBurger.setAttribute('aria-expanded', open);
});
navLinks.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => {
  navLinks.classList.remove('open');
  navBurger.classList.remove('open');
  navBurger.setAttribute('aria-expanded', 'false');
}));

/* link activo según sección visible (solo index) */
const linkFor = {};
navLinks.querySelectorAll('a[href^="#"]').forEach((a) => { linkFor[a.getAttribute('href').slice(1)] = a; });
document.querySelectorAll('section[id], footer[id]').forEach((s) => {
  new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (en.isIntersecting && linkFor[en.target.id]) {
        navLinks.querySelectorAll('a').forEach((a) => a.classList.remove('active'));
        linkFor[en.target.id].classList.add('active');
      }
    });
  }, { rootMargin: '-40% 0px -55% 0px' }).observe(s);
});

/* ─── REVEAL ON SCROLL ─── */
const revealObs = new IntersectionObserver((entries) => {
  entries.forEach((en) => {
    if (en.isIntersecting) {
      en.target.classList.add('in');
      revealObs.unobserve(en.target);
    }
  });
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach((el) => revealObs.observe(el));

/* ─── CONTADORES ─── */
const statObs = new IntersectionObserver((entries) => {
  entries.forEach((en) => {
    if (!en.isIntersecting) return;
    const el = en.target;
    statObs.unobserve(el);
    const target = +el.dataset.count;
    const dur = 1500;
    const t0 = performance.now();
    (function tick(now) {
      const p = Math.min((now - t0) / dur, 1);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(tick);
    })(t0);
  });
}, { threshold: 0.6 });
document.querySelectorAll('[data-count]').forEach((el) => statObs.observe(el));

/* ─── MOSAICO VIVO (temáticas, solo index): todo el contenido de IG rotando ─── */
const mosaic = $('mosaic');
if (mosaic) {
  const POOL = [
    'assets/img/ig/gold-duo.jpg', 'assets/img/ig/gold-zanqueros.jpg', 'assets/img/ig/gold-show.jpg',
    'assets/img/ig/gold-discoball.jpg', 'assets/img/ig/troupe.jpg', 'assets/img/ig/mirror-duo.jpg',
    'assets/img/ig/mirror-arch.jpg', 'assets/img/ig/led-tron.jpg', 'assets/img/ig/led-floor.jpg',
    'assets/img/ig/carnaval.jpg', 'assets/img/ig/carnaval-2.jpg', 'assets/img/ig/cabezon.jpg',
    'assets/img/ig/badbunny.jpg', 'assets/img/ig/tropical.jpg', 'assets/img/ig/tropical-sunset.jpg',
    'assets/img/ig/vegas-hd.jpg', 'assets/img/ig/white-dancers.jpg', 'assets/img/ig/venetian.jpg',
    'assets/img/ig/venetian-2.jpg', 'assets/img/ig/coreografia.jpg', 'assets/img/ig/zancos-color.jpg',
    'assets/img/rojo.jpg', 'assets/img/catrinas.jpg',
    { v: 'assets/video/finale.mp4' }, { v: 'assets/video/rojo.mp4' }, { v: 'assets/video/tambora.mp4' },
  ];
  const TILES = 6;
  const showing = new Array(TILES).fill(-1);
  const pickFree = () => {
    let i;
    do { i = Math.floor(Math.random() * POOL.length); } while (showing.includes(i));
    return i;
  };
  const makeLayer = (idx) => {
    const item = POOL[idx];
    let el;
    if (typeof item === 'object') {
      el = document.createElement('video');
      el.src = item.v; el.muted = true; el.loop = true; el.autoplay = true; el.playsInline = true;
      el.play().catch(() => {});
    } else {
      el = document.createElement('img');
      el.src = item; el.alt = '';
    }
    el.className = 'm-layer';
    return el;
  };

  mosaic.innerHTML = '';
  for (let t = 0; t < TILES; t++) {
    const tile = document.createElement('div');
    tile.className = 'm-tile';
    const idx = pickFree();
    showing[t] = idx;
    const layer = makeLayer(idx);
    layer.classList.add('on');
    tile.appendChild(layer);
    mosaic.appendChild(tile);
  }

  let mosaicVisible = true;
  new IntersectionObserver((entries) => {
    entries.forEach((en) => { mosaicVisible = en.isIntersecting; });
  }, { threshold: 0.05 }).observe(mosaic);

  let turn = 0;
  setInterval(() => {
    if (!mosaicVisible || document.hidden) return;
    const t = turn % TILES; // rota por turnos para que todas cambien parejo
    turn++;
    const tile = mosaic.children[t];
    const idx = pickFree();
    showing[t] = idx;
    const fresh = makeLayer(idx);
    tile.appendChild(fresh);
    requestAnimationFrame(() => requestAnimationFrame(() => {
      fresh.classList.add('on');
      const old = tile.querySelector('.m-layer.on');
      if (old && old !== fresh) old.classList.remove('on');
      setTimeout(() => {
        [...tile.querySelectorAll('.m-layer:not(.on)')].forEach((l) => l.remove());
      }, 1000);
    }));
  }, 2600);
}

/* ─── VISOR DE PAQUETES DESTACADOS (solo index) ─── */
const lb = $('lb');
if (lb && document.querySelector('.feat-cover')) {
  const PACKS = {
    dorado: { name: 'Gold', imgs: ['assets/img/destacado/dorado-4.jpg', 'assets/img/destacado/dorado-2.jpg', 'assets/img/destacado/dorado-3.jpg', 'assets/img/destacado/dorado-1.jpg'] },
    plata:  { name: 'Led Party', imgs: ['assets/img/destacado/plata-4.jpg', 'assets/img/destacado/plata-1.jpg', 'assets/img/destacado/plata-2.jpg', 'assets/img/destacado/plata-3.jpg'] },
  };
  let pack = null, idx = 0;

  function lbShow() {
    $('lbImg').src = pack.imgs[idx];
    $('lbName').textContent = pack.name;
    $('lbDots').innerHTML = pack.imgs.map((_, i) => `<i class="${i === idx ? 'on' : ''}"></i>`).join('');
  }
  function lbOpen(key) {
    pack = PACKS[key]; idx = 0;
    lb.hidden = false;
    document.body.style.overflow = 'hidden';
    lbShow();
    $('lbClose').focus();
  }
  function lbClose() {
    lb.hidden = true;
    document.body.style.overflow = '';
  }
  document.querySelectorAll('.feat-cover').forEach((b) =>
    b.addEventListener('click', () => lbOpen(b.dataset.pack)));
  $('lbClose').addEventListener('click', lbClose);
  $('lbPrev').addEventListener('click', () => { idx = (idx - 1 + pack.imgs.length) % pack.imgs.length; lbShow(); });
  $('lbNext').addEventListener('click', () => { idx = (idx + 1) % pack.imgs.length; lbShow(); });
  lb.addEventListener('click', (e) => { if (e.target === lb) lbClose(); });
  document.addEventListener('keydown', (e) => {
    if (lb.hidden) return;
    if (e.key === 'Escape') lbClose();
    if (e.key === 'ArrowLeft') $('lbPrev').click();
    if (e.key === 'ArrowRight') $('lbNext').click();
  });
}

/* ─── VIDEOS: reanudar al volver a la pestaña (Chrome los pausa en background) ─── */
document.addEventListener('visibilitychange', () => {
  if (document.hidden || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  document.querySelectorAll('video[autoplay]').forEach((v) => {
    if (v.paused) v.play().catch(() => {});
  });
});

/* ─── GALERÍA: pausar los loops fuera de vista ─── */
document.querySelectorAll('.gallery video').forEach((v) => {
  new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (en.isIntersecting) v.play().catch(() => {});
      else v.pause();
    });
  }, { threshold: 0.1 }).observe(v);
});

/* ─── VIDEO (solo index): loop continuo, pausa solo fuera de vista ─── */
const heroVideo = $('heroVideo');
if (heroVideo) {
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reducedMotion) heroVideo.pause();
  new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (en.isIntersecting && !reducedMotion) heroVideo.play().catch(() => {});
      else heroVideo.pause();
    });
  }, { threshold: 0.05 }).observe($('inicio'));
}
