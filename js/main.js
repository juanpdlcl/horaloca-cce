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
  { id: 'zanqueros',   img: 'assets/img/promo/zancos.jpg',     pos: '50% 20%', name: 'Zanqueros',                 desc: 'Altura y espectáculo que llenan la pista.' },
  { id: 'percusion',   img: 'assets/img/promo/musicos.jpg',        pos: '50% 42%', name: 'Percusión en vivo',      desc: 'Tambores en vivo que encienden la fiesta junto al DJ.' },
  { id: 'robot-led',   img: 'assets/img/promo/robot-espejo.jpg',   pos: '50% 25%', name: 'Robot LED',              desc: 'Show futurista iluminado para el punto alto de la noche.' },
  { id: 'cabezones',   img: 'assets/img/promo/artistas.jpg',       pos: '50% 30%', name: 'Cabezones',              desc: 'Bad Bunny, Karol G y Daddy Yankee en versión gigante, animando la pista.' },
  { id: 'bailarines',  img: 'assets/img/promo/bailarinas-led.jpg', pos: '50% 35%', name: 'Bailarines adicionales', desc: 'Refuerza el cuerpo de baile de tu show.' },
];

/* temáticas de la Hora Loca (fotos reales del catálogo de Carolina).
   imgs[0] = portada; si hay más de una foto la tarjeta rota en slideshow.
   more:true = oculta hasta pulsar "Ver todas las temáticas". */
const T = 'assets/img/tematicas';
const seq = (dir, n) => Array.from({ length: n }, (_, i) => `${T}/${dir}/${String(i + 1).padStart(2, '0')}.jpg`);
const THEMES = [
  { id: 'gold',        name: 'Dorado',          imgs: ['assets/img/destacado/dorado-4.jpg', ...seq('dorado', 3)] },
  { id: 'led',         name: 'Disco Ball',      imgs: ['assets/img/destacado/plata-4.jpg', ...seq('espejos', 8)] },
  { id: 'brasil',      name: 'Brazil plateada', imgs: [...seq('brasil-plata', 3), 'assets/img/destacado/brasil-1.jpg'] },
  { id: 'brazil',      name: 'Brazil',          imgs: [...seq('brazil', 7), { v: 'assets/video/brazil.mp4' }] },
  { id: 'vegas',       name: 'Viva las Vegas',  imgs: seq('vegas', 4) },
  { id: 'dominicana',  name: 'Dominicana',      imgs: seq('dominicana', 5) },
  { id: 'neon',        name: 'Neón',            imgs: seq('neon', 4) },
  { id: 'tropical',    name: 'Tropical',        imgs: ['assets/img/ig/tropical-sunset.jpg', ...seq('tropical', 2)] },
  { id: 'gatsby',      name: 'Gatsby',          imgs: seq('gatsby', 6) },
  { id: 'alas-led',    name: 'Alas LED',        imgs: seq('alas-led', 4) },
  { id: 'carnaval',    name: 'Carnaval Dominicano', desc: 'Con sus diablos cojuelos', imgs: ['assets/img/ig/carnaval.jpg', `${T}/carnaval/01.jpg`], more: true },
  { id: 'marchantas',  name: 'Marchantas',      imgs: seq('marchantas', 3), more: true },
  { id: 'samba',       name: 'Samba',           imgs: seq('samba', 1), more: true },
  { id: 'vaqueros',    name: 'Vaqueros',        imgs: seq('vaqueros', 3), more: true },
  { id: 'porristas',   name: 'Porristas',       imgs: seq('porristas', 1), more: true },
  { id: 'bienvenida',  name: 'Personajes para bienvenida', imgs: seq('bienvenida', 3), more: true },
  { id: 'hadas',       name: 'Hadas',           imgs: seq('hadas', 1), more: true },
  { id: 'astronauta',  name: 'Astronauta y alien', imgs: seq('astronauta', 2), more: true },
  { id: 'pelota',      name: 'Pelota dominicana', imgs: seq('pelota', 2), more: true },
  { id: 'cabezones',   name: 'Cabezones',       desc: 'Bad Bunny, Karol G y Daddy Yankee', imgs: [`${T}/cabezones/main.jpg`, `${T}/cabezones/02.jpg`, 'assets/img/promo/artistas.jpg', `${T}/cabezones/01.jpg`], more: true },
  { id: 'robot-espejo', name: 'Robot LED espejo', imgs: [`${T}/robot-espejo/02.jpg`, `${T}/robot-espejo/01.jpg`, `${T}/robot-espejo/03.jpg`], more: true },
  { id: 'led-show',    name: 'Led',             imgs: [...seq('led-show', 2), { v: 'assets/video/led-show.mp4' }], more: true },
  { id: 'navidad',     name: 'Navidad',         imgs: seq('navidad', 6), more: true },
  { id: 'disco',       name: 'Disco',           imgs: seq('disco', 1), more: true },
  { id: 'anos-90',     name: 'Años 90',         imgs: seq('anos-90', 1), more: true },
  { id: 'pilotos',     name: 'Pilotos Formula 1', imgs: seq('pilotos', 2), more: true },
  { id: 'marineros',   name: 'Marineros',       imgs: seq('marineros', 1), more: true },
  { id: 'mimos',       name: 'Mimos',           imgs: seq('mimos', 1), more: true },
  { id: 'rouge',       name: 'Rouge Royal',     imgs: ['assets/img/rojo.jpg'], more: true },
  { id: 'catrinas',    name: 'Catrinas',        imgs: ['assets/img/catrinas.jpg'], more: true },
  { id: 'venezia',     name: 'Venezia',         imgs: ['assets/img/ig/venetian.jpg'], more: true },
  { id: 'otra',        name: 'Otra / por definir', imgs: ['assets/img/ig/troupe.jpg'] },
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

/* notas específicas por elemento ("quiero el cabezón de Bad Bunny", etc.) */
let quoteNotes = {};
try { quoteNotes = JSON.parse(localStorage.getItem('cce-notes') || '{}'); } catch (_) { quoteNotes = {}; }
if (!quoteNotes || typeof quoteNotes !== 'object' || Array.isArray(quoteNotes)) quoteNotes = {};
Object.keys(quoteNotes).forEach((k) => { if (!quote[k]) delete quoteNotes[k]; });
function saveNotes() { localStorage.setItem('cce-notes', JSON.stringify(quoteNotes)); }

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

  /* extras (todo lo que no es la Hora Loca temática) */
  servGrid.innerHTML = SERVICES.filter((s) => !s.themed).map((s) => `
    <button class="serv" data-id="${s.id}" type="button" aria-pressed="false">
      <span class="serv-check"><svg class="icon"><use href="#i-check"/></svg></span>
      <span class="serv-img"><img src="${s.img}" alt="" loading="lazy" style="object-position:${s.pos}"></span>
      <span class="serv-body">
        <h3>${s.name}</h3>
        <p>${s.desc}</p>
        <span class="serv-state state-off"><svg class="icon"><use href="#i-plus"/></svg> Agregar</span>
        <span class="serv-state state-on" hidden><svg class="icon"><use href="#i-check"/></svg> Agregado</span>
      </span>
    </button>
  `).join('');

  /* temáticas de la Hora Loca, visibles en la página */
  const countLabel = (t) => {
    const vids = t.imgs.filter((x) => typeof x === 'object').length;
    const fotos = t.imgs.length - vids;
    if (!vids) return `${fotos} fotos`;
    return fotos > 1 ? `${fotos} fotos + video` : 'Fotos + video';
  };
  $('themePick').innerHTML = THEMES.map((t) => `
    <button class="pk${t.more ? ' pk-hid' : ''}" data-key="hora-loca:${t.id}" type="button" aria-pressed="false">
      <img class="pk-img on" src="${t.imgs[0]}" alt="" loading="lazy">
      ${t.imgs.length > 1 ? `<span class="pk-count" aria-hidden="true">${countLabel(t)}</span>` : ''}
      <span class="pk-name">${t.name}${t.desc ? `<small>${t.desc}</small>` : ''}</span>
      <span class="pk-check"><svg class="icon"><use href="#i-check"/></svg></span>
    </button>
  `).join('');

  /* "Ver todas las temáticas": las menos pedidas quedan plegadas al entrar */
  const themesMore = $('themesMore');
  function setThemesExpanded(on) {
    $('themePick').classList.toggle('expanded', on);
    themesMore.setAttribute('aria-expanded', on);
    themesMore.textContent = on ? 'Ver menos temáticas' : `Ver todas las temáticas (${THEMES.length})`;
  }
  themesMore.addEventListener('click', () => {
    const on = !$('themePick').classList.contains('expanded');
    setThemesExpanded(on);
    if (!on) {
      const smooth = !matchMedia('(prefers-reduced-motion: reduce)').matches;
      $('themePick').scrollIntoView({ behavior: smooth ? 'smooth' : 'auto', block: 'start' });
    }
  });
  setThemesExpanded(THEMES.some((t) => t.more && quote[`hora-loca:${t.id}`]));

  /* slideshow: las tarjetas con varias fotos rotan estando a la vista */
  if (!matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const rotating = [];
    const rotObs = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        const r = rotating.find((x) => x.card === en.target);
        if (!r) return;
        r.visible = en.isIntersecting;
        const v = r.card.querySelector('video.pk-img.on');
        if (v) { if (en.isIntersecting) v.play().catch(() => {}); else v.pause(); }
      });
    }, { threshold: 0.25 });
    document.querySelectorAll('#themePick .pk').forEach((card, i) => {
      const t = THEMES.find((x) => `hora-loca:${x.id}` === card.dataset.key);
      if (!t || t.imgs.length < 2) return;
      const r = { card, imgs: t.imgs, idx: 0, visible: false, busy: false, next: (i % 7) * 620 };
      rotating.push(r);
      rotObs.observe(card);
    });
    const STEP = 3400;      // ms que se ve cada foto
    const STEP_VIDEO = 6500; // los clips en loop se quedan más tiempo
    setInterval(() => {
      if (document.hidden) return;
      const now = performance.now();
      rotating.forEach((r) => {
        if (!r.visible || r.busy || now < r.next) return;
        if (r.card.matches(':hover, :focus')) return; // pausa mientras se mira
        r.busy = true;
        r.idx = (r.idx + 1) % r.imgs.length;
        const item = r.imgs[r.idx];
        const isVideo = typeof item === 'object';
        const layer = document.createElement(isVideo ? 'video' : 'img');
        layer.className = 'pk-img';
        const done = () => { r.busy = false; r.next = performance.now() + (isVideo ? STEP_VIDEO : STEP); };
        const show = () => {
          r.card.insertBefore(layer, r.card.querySelector('.pk-count, .pk-name'));
          requestAnimationFrame(() => requestAnimationFrame(() => {
            const old = [...r.card.querySelectorAll('.pk-img.on')];
            layer.classList.add('on');
            old.forEach((l) => l.classList.remove('on'));
            setTimeout(() => { old.forEach((l) => l.remove()); done(); }, 950);
          }));
        };
        if (isVideo) {
          layer.muted = true; layer.loop = true; layer.playsInline = true; layer.preload = 'auto';
          // al DOM desde ya (invisible con opacity 0): un <video> suelto sin
          // referencias puede ser recolectado y sus eventos jamás disparan
          r.card.insertBefore(layer, r.card.querySelector('.pk-count, .pk-name'));
          const guard = setTimeout(() => {
            if (layer.oncanplay) { layer.oncanplay = null; layer.remove(); done(); }
          }, 6000);
          layer.onerror = () => { clearTimeout(guard); layer.oncanplay = null; layer.remove(); done(); };
          layer.oncanplay = () => {
            clearTimeout(guard);
            layer.oncanplay = null;
            layer.play().catch(() => {});
            show();
          };
          layer.src = item.v;
        } else {
          layer.alt = '';
          layer.onerror = done;
          layer.onload = show;
          layer.src = item;
        }
      });
    }, 350);
  }

  /* claves del carrito: "servicio" o "servicio:tematica" */
  const parseKey = (key) => {
    const [sid, tid] = key.split(':');
    return { sid, tid, service: byId(sid), theme: THEMES.find((t) => t.id === tid) || null };
  };
  /* la temática ES la hora loca: un solo nombre, sin servicio aparte */
  const keyName = (key) => {
    const { service, theme } = parseKey(key);
    if (!theme) return service.name;
    return theme.id === 'otra' ? 'Hora Loca (temática por definir)' : `Hora Loca ${theme.name}`;
  };
  const keyImg = (key) => {
    const { service, theme } = parseKey(key);
    return (theme && theme.imgs[0]) || service.img;
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
    document.querySelectorAll('.pk').forEach((p) => {
      const on = !!quote[p.dataset.key];
      p.classList.toggle('on', on);
      p.setAttribute('aria-pressed', on);
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
        <div class="cart-item-row">
          <img class="cart-item-thumb" src="${keyImg(key)}" alt="">
          <div class="cart-item-info"><strong>${keyName(key)}</strong></div>
          <div class="cart-qty">
            <button data-dec="${key}" aria-label="Quitar uno"><svg class="icon"><use href="#i-minus"/></svg></button>
            <span>${quote[key]}</span>
            <button data-inc="${key}" aria-label="Agregar uno"><svg class="icon"><use href="#i-plus"/></svg></button>
          </div>
          <button class="cart-item-del" data-del="${key}" aria-label="Eliminar"><svg class="icon"><use href="#i-trash"/></svg></button>
        </div>
        <input class="cart-item-note" data-note="${key}" placeholder="¿Algo específico? (opcional)" value="${(quoteNotes[key] || '').replace(/"/g, '&quot;')}">
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

  /* toggle de temáticas (a la vista en la página) */
  $('themePick').addEventListener('click', (e) => {
    const b = e.target.closest('.pk');
    if (!b) return;
    const key = b.dataset.key;
    if (quote[key]) removeKey(key); else addKey(key);
  });

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
    if (btn.dataset.del) { delete quote[btn.dataset.del]; delete quoteNotes[btn.dataset.del]; saveNotes(); }
    save();
    syncUI();
    // el botón enfocado fue destruido por el re-render: devolver el foco al panel
    if (cartDrawer.classList.contains('open')) {
      (cartItems.querySelector('button') || $('cartClose')).focus();
    }
  });

  /* guardar la nota específica de cada elemento mientras se escribe */
  cartItems.addEventListener('input', (e) => {
    const inp = e.target.closest('.cart-item-note');
    if (!inp) return;
    const v = inp.value.trim();
    if (v) quoteNotes[inp.dataset.note] = v;
    else delete quoteNotes[inp.dataset.note];
    saveNotes();
  });

  $('cartBtn').addEventListener('click', openCart);
  $('quoteReview').addEventListener('click', () => {
    if (!Object.keys(quote).length) { showToast('Selecciona al menos un elemento'); return; }
    openCart();
  });
  $('cartClose').addEventListener('click', closeCart);
  cartOverlay.addEventListener('click', closeCart);
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeCart();
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
      note: (quoteNotes[key] || '').trim(),
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
        keepalive: true, // sobrevive a la navegación a WhatsApp (in-app browsers)
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
      ...(it.note ? [`   Detalle: ${it.note}`] : []),
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
    quoteNotes = {};
    saveNotes();
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
    { v: 'assets/video/brazil.mp4' },
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
  const brazilIdx = POOL.findIndex((p) => typeof p === 'object' && p.v.includes('brazil'));
  for (let t = 0; t < TILES; t++) {
    const tile = document.createElement('div');
    tile.className = 'm-tile';
    // el video de Brazil abre la sección: siempre en el primer cuadro
    const idx = t === 0 && brazilIdx >= 0 ? brazilIdx : pickFree();
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
    dorado: { name: 'Gold', imgs: ['assets/img/destacado/dorado-4.jpg', 'assets/img/destacado/dorado-2.jpg', 'assets/img/destacado/dorado-3.jpg', 'assets/img/destacado/dorado-1.jpg', 'assets/img/tematicas/dorado/01.jpg', 'assets/img/tematicas/dorado/02.jpg', 'assets/img/tematicas/dorado/03.jpg'] },
    plata:  { name: 'Disco Ball', imgs: ['assets/img/tematicas/espejos/main.jpg', 'assets/img/destacado/plata-4.jpg', 'assets/img/destacado/plata-1.jpg', 'assets/img/destacado/plata-2.jpg', 'assets/img/destacado/plata-3.jpg', 'assets/img/tematicas/espejos/01.jpg', 'assets/img/tematicas/espejos/02.jpg', 'assets/img/tematicas/espejos/03.jpg', 'assets/img/tematicas/espejos/04.jpg', 'assets/img/tematicas/espejos/05.jpg', 'assets/img/tematicas/espejos/06.jpg', 'assets/img/tematicas/espejos/07.jpg', 'assets/img/tematicas/espejos/08.jpg'] },
    brasil: { name: 'Brasil Blanco con Plateado', imgs: ['assets/img/tematicas/brasil-plata/01.jpg', 'assets/img/tematicas/brasil-plata/02.jpg', 'assets/img/tematicas/brasil-plata/03.jpg', 'assets/img/destacado/brasil-1.jpg'] },
    cabezones: { name: 'Cabezones', imgs: ['assets/img/tematicas/cabezones/main.jpg', 'assets/img/promo/artistas.jpg', 'assets/img/tematicas/cabezones/01.jpg', 'assets/img/tematicas/cabezones/02.jpg'] },
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

  /* destacado que se alterna: Disco Ball ↔ Cabezones */
  const featAlt = $('featAlt');
  if (featAlt && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const STATES = [
      { pack: 'plata', title: 'Disco Ball', sub: 'El paquete plateado completo' },
      { pack: 'cabezones', title: 'Cabezones', sub: 'Bad Bunny, Karol G y Daddy Yankee' },
    ];
    const faImgs = featAlt.querySelectorAll('.fa-img');
    let alt = 0;
    setInterval(() => {
      if (document.hidden || featAlt.matches(':hover, :focus') || !lb.hidden) return;
      alt = 1 - alt;
      faImgs[alt].classList.add('on');
      faImgs[1 - alt].classList.remove('on');
      const s = STATES[alt];
      featAlt.dataset.pack = s.pack;
      featAlt.setAttribute('aria-label', `Ver todas las fotos del paquete ${s.title}`);
      $('faTitle').textContent = s.title;
      $('faSub').textContent = s.sub;
    }, 5000);
  }
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
document.querySelectorAll('.gallery video, .photo-main video').forEach((v) => {
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
