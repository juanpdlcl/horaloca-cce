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
  { id: 'robot-led',   img: 'assets/img/promo/robot-espejo.jpg',   pos: '50% 0%', name: 'Robot LED',              desc: 'Show futurista iluminado para el punto alto de la noche.' },
  { id: 'cabezones',   img: 'assets/img/promo/artistas.jpg',       pos: '50% 12%', name: 'Cabezones',              desc: 'Bad Bunny, Karol G y Daddy Yankee en versión gigante, animando la pista.' },
  { id: 'bailarines',  img: 'assets/img/promo/bailarinas-led.jpg', pos: '50% 35%', name: 'Bailarines adicionales', desc: 'Refuerza el cuerpo de baile de tu show.' },
];

/* temáticas de la Hora Loca (fotos reales del catálogo de Carolina).
   imgs[0] = portada; si hay más de una foto la tarjeta rota en slideshow.
   more:true = oculta hasta pulsar "Ver todas las temáticas". */
const T = 'assets/img/tematicas';
const seq = (dir, n) => Array.from({ length: n }, (_, i) => `${T}/${dir}/${String(i + 1).padStart(2, '0')}.jpg`);
const THEMES = [
  { id: 'gold', cat: 'brillo', tags: 'dorado oro gold show girls plumas',        name: 'Dorado',          imgs: ['assets/img/destacado/dorado-4.jpg', `${T}/dorado/06.jpg`, `${T}/dorado/04.jpg`, `${T}/dorado/05.jpg`, `${T}/dorado/07.jpg`, ...seq('dorado', 3)] },
  { id: 'led', cat: 'brillo', tags: 'espejos disco ball plateado bola',         name: 'Disco Ball',      imgs: [`${T}/espejos/main.jpg`, `${T}/espejos/09.jpg`, `${T}/espejos/10.jpg`, `${T}/espejos/11.jpg`, 'assets/img/destacado/plata-4.jpg', 'assets/img/destacado/plata-1.jpg', 'assets/img/destacado/plata-2.jpg', 'assets/img/destacado/plata-3.jpg', ...seq('espejos', 8)] },
  { id: 'brasil', cat: 'brillo', tags: 'brazil plateada plumas carnaval',      name: 'Brazil plateada', imgs: [...seq('brasil-plata', 3), 'assets/img/destacado/brasil-1.jpg'] },
  { id: 'brazil', cat: 'tropical', tags: 'brasil samba plumas carnaval rio',      name: 'Brazil',          imgs: [...seq('brazil', 6), { v: 'assets/video/brazil.mp4' }] },
  { id: 'vegas', cat: 'brillo', tags: 'casino show girls plumas host entrada',       name: 'Viva las Vegas',  desc: 'Show girls y host de entrada', imgs: [`${T}/vegas/05.jpg`, `${T}/vegas/06.jpg`, `${T}/vegas/07.jpg`, `${T}/vegas/08.jpg`, ...seq('vegas', 4)] },
  { id: 'dominicana', cat: 'dominicano', tags: 'bandera republica dominicana merengue',  name: 'Dominicana',      imgs: seq('dominicana', 5) },
  { id: 'neon', cat: 'luces', tags: 'fluorescente luces glow',        name: 'Neón',            imgs: [`${T}/neon/05.jpg`, `${T}/neon/06.jpg`, ...seq('neon', 4)] },
  { id: 'tropical', cat: 'tropical', tags: 'verano flores colores',    name: 'Tropical',        imgs: ['assets/img/ig/tropical-sunset.jpg', ...seq('tropical', 2)] },
  { id: 'gatsby', cat: 'epocas', tags: 'anos 20 vintage elegante charleston',      name: 'Gatsby',          imgs: seq('gatsby', 7) },
  { id: 'alas-led', cat: 'luces', tags: 'alas angel luces',    name: 'Alas LED',        imgs: seq('alas-led', 4) },
  { id: 'bar-neon', cat: 'luces', tags: 'bar neon bandeja canapes pasabocas hostess luces led mesa humana recibimiento', name: 'Bar Neón', desc: 'Hostess iluminada con bandeja de canapés', imgs: seq('bar-neon', 2), more: true },
  { id: 'shine-gold', cat: 'brillo', tags: 'dorado oro brillo',  name: 'Shine Gold',      imgs: seq('shine-gold', 1), more: true },
  { id: 'carnaval', cat: 'dominicano', tags: 'diablos cojuelos lechones vegano',    name: 'Carnaval Dominicano', desc: 'Con diablos cojuelos y lechones', imgs: [`${T}/carnaval/02.jpg`, 'assets/img/ig/carnaval.jpg', `${T}/carnaval/01.jpg`], more: true },
  { id: 'marchantas', cat: 'dominicano', tags: 'mercado tipico campo',  name: 'Marchantas',      imgs: seq('marchantas', 3), more: true },
  { id: 'samba', cat: 'tropical', tags: 'brasil rio plumas',       name: 'Samba',           imgs: seq('samba', 1), more: true },
  { id: 'africa', cat: 'tropical', tags: 'jungla safari selva animal print',      name: 'África',          imgs: seq('africa', 4), more: true },
  { id: 'tropical-cuba', cat: 'tropical', tags: 'cuba habana caribe', name: 'Tropical Cuba', imgs: seq('tropical-cuba', 3), more: true },
  { id: 'playa', cat: 'tropical', tags: 'verano mar arena',       name: 'Playa',           imgs: seq('playa', 1), more: true },
  { id: 'hawaii', cat: 'tropical', tags: 'hula isla verano',      name: 'Hawaii',          imgs: seq('hawaii', 1), more: true },
  { id: 'vaqueros', cat: 'epocas', tags: 'cowboy oeste western texas',    name: 'Vaqueros',        imgs: seq('vaqueros', 3), more: true },
  { id: 'porristas', cat: 'personajes', tags: 'cheerleaders animadoras deporte',   name: 'Porristas',       imgs: seq('porristas', 1), more: true },
  { id: 'ingenieros', cat: 'personajes', tags: 'construccion casco obra',  name: 'Ingenieros',      imgs: seq('ingenieros', 4), more: true },
  { id: 'cocineros-show', cat: 'personajes', tags: 'chef cocina comida', name: 'Cocineros',    imgs: seq('cocineros-show', 3), more: true },
  { id: 'bienvenida', cat: 'personajes', tags: 'recibimiento host entrada hostess',  name: 'Personajes para bienvenida', imgs: seq('bienvenida', 3), more: true },
  { id: 'corazon', cat: 'personajes', tags: 'amor san valentin recibimiento',     name: 'Personaje de corazón', imgs: seq('corazon', 1), more: true },
  { id: 'personaje-playa', cat: 'personajes', tags: 'playa verano recibimiento', name: 'Personaje de playa', imgs: seq('personaje-playa', 1), more: true },
  { id: 'hadas', cat: 'personajes', tags: 'hada fantasia alas',       name: 'Hadas',           imgs: seq('hadas', 1), more: true },
  { id: 'astronauta', cat: 'personajes', tags: 'espacio alien galaxia',  name: 'Astronauta y alien', imgs: seq('astronauta', 6), more: true },
  { id: 'pelota', cat: 'dominicano', tags: 'beisbol baseball deporte licey leones mascotas', name: 'Pelota dominicana', imgs: [`${T}/pelota/03.jpg`, ...seq('pelota', 2)], more: true },
  { id: 'zanqueros-rd', cat: 'dominicano', tags: 'zancos zanqueros bandera patria dominicana altura', name: 'Zancos dominicanos', desc: 'Con la bandera en alto', imgs: seq('zanqueros-rd', 1), more: true },
  { id: 'cabezones', cat: 'personajes', tags: 'bad bunny karol g daddy yankee artistas cabezas',   name: 'Cabezones',       desc: 'Bad Bunny, Karol G y Daddy Yankee', imgs: [`${T}/cabezones/main.jpg`, `${T}/cabezones/02.jpg`, 'assets/img/promo/artistas.jpg', `${T}/cabezones/01.jpg`], more: true },
  { id: 'robot-espejo', cat: 'luces', tags: 'robot espejo futurista', name: 'Robot LED espejo', imgs: [`${T}/robot-espejo/02.jpg`, `${T}/robot-espejo/01.jpg`, `${T}/robot-espejo/03.jpg`], more: true },
  { id: 'led-show', cat: 'luces', tags: 'led robots tambores zancos luces',    name: 'Led',             imgs: [...seq('led-show', 4), { v: 'assets/video/led-show.mp4' }], more: true },
  { id: 'neon-2000', cat: 'luces', tags: 'fluorescente 2000 retro',   name: 'Neon 2000',       imgs: seq('neon-2000', 3), more: true },
  { id: 'navidad', cat: 'navidad', tags: 'santa grinch galleta elfos diciembre navideno',     name: 'Navidad',         imgs: [`${T}/navidad/12.jpg`, `${T}/navidad/13.jpg`, `${T}/navidad/09.jpg`, `${T}/navidad/10.jpg`, `${T}/navidad/11.jpg`, `${T}/navidad/15.jpg`, `${T}/navidad/16.jpg`, `${T}/navidad/17.jpg`, `${T}/navidad/18.jpg`, `${T}/navidad/19.jpg`, ...seq('navidad', 8)], more: true },
  { id: 'feria-circo', cat: 'personajes', tags: 'payasos mimos circo feria carpa', name: 'Feria/Circo',     desc: 'Payasos y mimos', imgs: seq('feria-circo', 3), more: true },
  { id: 'blanca-navidad', cat: 'navidad', tags: 'navidad blanca invierno nieve', name: 'Blanca Navidad', imgs: seq('blanca-navidad', 1), more: true },
  { id: 'disco', cat: 'brillo', tags: 'setenta disco fiebre',       name: 'Disco',           imgs: seq('disco', 1), more: true },
  { id: 'anos-80', cat: 'epocas', tags: '80 ochenta retro',     name: 'Años 80',         imgs: seq('anos-80', 2), more: true },
  { id: 'anos-90', cat: 'epocas', tags: '90 noventa retro',     name: 'Años 90',         imgs: seq('anos-90', 1), more: true },
  { id: 'brigeston', cat: 'epocas', tags: 'bridgerton epoca vintage realeza',   name: 'Brigeston',       imgs: seq('brigeston', 1), more: true },
  { id: 'pilotos', cat: 'epocas', tags: 'formula 1 carreras autos f1',     name: 'Pilotos Formula 1', imgs: [`${T}/pilotos/01.jpg`, `${T}/pilotos/04.jpg`, `${T}/pilotos/03.jpg`, `${T}/pilotos/02.jpg`], more: true },
  { id: 'marineros', cat: 'epocas', tags: 'marinos barco nautico',   name: 'Marineros',       imgs: seq('marineros', 1), more: true },
  { id: 'mimos', cat: 'personajes', tags: 'mimo circo blanco',       name: 'Mimos',           imgs: seq('mimos', 1), more: true },
  { id: 'bienvenida-blanca', cat: 'personajes', tags: 'recibimiento bienvenida rosas flores blanca jaula host entrada', name: 'Bienvenida Blanca', desc: 'Recibimiento con rosas blancas', imgs: seq('bienvenida-blanca', 2), more: true },
  { id: 'bienvenida-roja', cat: 'personajes', tags: 'recibimiento bienvenida rosas flores roja jaula host entrada anfitriones lentejuelas rojo', name: 'Bienvenida Roja', desc: 'Recibimiento en rojo: rosas y anfitriones', imgs: [...seq('bienvenida-roja', 7), 'assets/img/rojo.jpg'], more: true },
  { id: 'safari', cat: 'tropical', tags: 'safari jungla exploradores aventura africa selva', name: 'Safari', desc: 'Exploradores', imgs: [`${T}/safari/03.jpg`, `${T}/safari/01.jpg`, `${T}/safari/02.jpg`], more: true },
  { id: 'catrinas', cat: 'epocas', tags: 'muertos mexico calaveras',    name: 'Catrinas',        imgs: ['assets/img/catrinas.jpg'], more: true },
  { id: 'venezia', cat: 'epocas', tags: 'venecia mascaras italia',     name: 'Venezia',         imgs: ['assets/img/ig/venetian.jpg'], more: true },
  { id: 'otra', tags: 'personalizada medida idea',        name: 'Otra / por definir', imgs: ['assets/img/ig/troupe.jpg'] },
];

const byId = (id) => SERVICES.find((s) => s.id === id);
const $ = (id) => document.getElementById(id);
/* swipe con el dedo para pasar fotos en los visores (teléfono) */
function conSwipe(el, siguiente, anterior) {
  let x0 = null, y0 = null;
  el.addEventListener('touchstart', (e) => {
    x0 = e.touches[0].clientX; y0 = e.touches[0].clientY;
  }, { passive: true });
  el.addEventListener('touchend', (e) => {
    if (x0 === null) return;
    const dx = e.changedTouches[0].clientX - x0;
    const dy = e.changedTouches[0].clientY - y0;
    x0 = null;
    if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy) * 1.5) (dx < 0 ? siguiente : anterior)();
  }, { passive: true });
}
/* miniatura ligera (t-*.jpg) para tarjetas y mosaico; el archivo completo
   queda para visores, destacados y links de WhatsApp */
const thumb = (p) => typeof p === 'string' ? p.replace(/([^/]+)\.(jpg|png)$/i, 't-$1.jpg') : p;

/* ─── PRELOADER (solo index) ───
   Se quita apenas el documento está listo (no espera videos ni fotos),
   con un tope duro de 2s: la página nunca se queda "cargando". */
if ($('preloader')) {
  const fuera = () => $('preloader').classList.add('done');
  if (document.readyState !== 'loading') setTimeout(fuera, 450);
  else document.addEventListener('DOMContentLoaded', () => setTimeout(fuera, 450));
  setTimeout(fuera, 2000);
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
      <span class="serv-img"><img src="${thumb(s.img)}" alt="" loading="lazy" style="object-position:${s.pos}"></span>
      <span class="serv-body">
        <h3>${s.name}</h3>
        <p>${s.desc}</p>
        <span class="serv-state state-off"><svg class="icon"><use href="#i-plus"/></svg> Agregar</span>
        <span class="serv-state state-on" hidden><svg class="icon"><use href="#i-check"/></svg> Agregado</span>
      </span>
    </button>
  `).join('');

  /* temáticas de la Hora Loca, visibles en la página */
  $('themePick').innerHTML = THEMES.map((t) => `
    <button class="pk" data-key="hora-loca:${t.id}" data-cat="${t.cat || ''}" data-buscar="${(t.name + ' ' + (t.desc || '') + ' ' + (t.tags || '')).toLowerCase()}" type="button" aria-pressed="false">
      <img class="pk-img on" src="${thumb(t.imgs[0])}" alt="" loading="lazy">
      <span class="pk-name">${t.name}${t.desc ? `<small>${t.desc}</small>` : ''}</span>
      <span class="pk-check"><svg class="icon"><use href="#i-check"/></svg></span>
    </button>
  `).join('');

  /* ─── BUSCADOR TIPO CATÁLOGO: escribe o filtra por estilo ─── */
  const buscar = $('temaBuscar');
  const cats = $('temaCats');
  const vacio = $('temaVacio');
  const contador = $('temaN');
  let catActiva = '';
  /* sin tildes ni mayúsculas: "neon" encuentra "Neón" */
  const limpia = (t) => t.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');

  function filtrar() {
    const q = limpia(buscar.value.trim());
    const palabras = q ? q.split(/\s+/) : [];
    let visibles = 0;
    document.querySelectorAll('#themePick .pk').forEach((card) => {
      const texto = limpia(card.dataset.buscar || '');
      const okCat = !catActiva || card.dataset.cat === catActiva;
      const okQ = palabras.every((p) => texto.includes(p));
      const ok = okCat && okQ;
      card.hidden = !ok;
      if (ok) visibles++;
    });
    vacio.hidden = visibles > 0;
    contador.textContent = visibles === THEMES.length
      ? `${THEMES.length} temáticas disponibles`
      : `${visibles} ${visibles === 1 ? 'temática' : 'temáticas'}`;
    $('temaLimpiar').hidden = !buscar.value;
  }

  buscar.addEventListener('input', filtrar);
  $('temaLimpiar').addEventListener('click', () => { buscar.value = ''; buscar.focus(); filtrar(); });
  cats.addEventListener('click', (e) => {
    const b = e.target.closest('.bcat');
    if (!b) return;
    catActiva = b.dataset.cat;
    cats.querySelectorAll('.bcat').forEach((x) => x.classList.toggle('on', x === b));
    filtrar();
  });
  filtrar();

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
        if (!r.visible || r.busy || r.card.hidden || now < r.next) return;
        if (r.card.matches(':hover, :focus')) return; // pausa mientras se mira
        r.busy = true;
        r.idx = (r.idx + 1) % r.imgs.length;
        const item = r.imgs[r.idx];
        const isVideo = typeof item === 'object';
        const layer = document.createElement(isVideo ? 'video' : 'img');
        layer.className = 'pk-img';
        const done = () => { r.busy = false; r.next = performance.now() + (isVideo ? STEP_VIDEO : STEP); };
        const show = () => {
          r.card.insertBefore(layer, r.card.querySelector('.pk-name'));
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
          r.card.insertBefore(layer, r.card.querySelector('.pk-name'));
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
          layer.src = thumb(item);
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

    /* botón flotante: aparece con la primera selección y siempre queda a mano */
    if ($('selFloat')) {
      $('selFloat').hidden = keys.length === 0;
      $('selFloatN').textContent = keys.length;
    }

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
          <img class="cart-item-thumb" src="${thumb(keyImg(key))}" alt="">
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

  /* tocar una temática abre su visor con las fotos en grande */
  const tv = $('tv');
  let tvTheme = null, tvIdx = 0;
  const tvItems = () => tvTheme.imgs;
  function tvShow() {
    const item = tvItems()[tvIdx];
    const esVideo = typeof item === 'object';
    $('tvImg').hidden = esVideo;
    $('tvVid').hidden = !esVideo;
    if (esVideo) {
      $('tvVid').src = item.v;
      $('tvVid').play().catch(() => {});
    } else {
      $('tvVid').pause();
      $('tvImg').src = item; // tamaño completo, no miniatura
    }
    $('tvName').textContent = tvTheme.name + (tvTheme.desc ? ` — ${tvTheme.desc}` : '');
    $('tvDots').innerHTML = tvItems().map((_, i) => `<i class="${i === tvIdx ? 'on' : ''}"></i>`).join('');
    const nav = tvItems().length > 1;
    $('tvPrev').hidden = !nav;
    $('tvNext').hidden = !nav;
    tvPintaBoton();
  }
  function tvPintaBoton() {
    const on = !!quote[`hora-loca:${tvTheme.id}`];
    $('tvAdd').textContent = on ? 'Quitar de mi cotización' : 'Agregar a mi cotización';
    $('tvAdd').classList.toggle('quitar', on);
  }
  function tvOpen(id) {
    tvTheme = THEMES.find((t) => t.id === id);
    if (!tvTheme) return;
    tvIdx = 0;
    tv.hidden = false;
    document.body.style.overflow = 'hidden';
    tvShow();
    $('tvClose').focus();
  }
  function tvCierra() {
    tv.hidden = true;
    $('tvVid').pause();
    document.body.style.overflow = '';
  }
  $('themePick').addEventListener('click', (e) => {
    const b = e.target.closest('.pk');
    if (!b) return;
    tvOpen(b.dataset.key.split(':')[1]);
  });
  $('tvClose').addEventListener('click', tvCierra);
  $('tvPrev').addEventListener('click', () => { tvIdx = (tvIdx - 1 + tvItems().length) % tvItems().length; tvShow(); });
  $('tvNext').addEventListener('click', () => { tvIdx = (tvIdx + 1) % tvItems().length; tvShow(); });
  tv.addEventListener('click', (e) => { if (e.target === tv || e.target.classList.contains('tv-stage')) tvCierra(); });
  $('tvAdd').addEventListener('click', () => {
    const key = `hora-loca:${tvTheme.id}`;
    if (quote[key]) { removeKey(key); tvPintaBoton(); }
    else { addKey(key); tvCierra(); }
  });
  document.addEventListener('keydown', (e) => {
    if (tv.hidden) return;
    if (e.key === 'Escape') tvCierra();
    if (e.key === 'ArrowLeft') $('tvPrev').click();
    if (e.key === 'ArrowRight') $('tvNext').click();
  });
  conSwipe(tv, () => $('tvNext').click(), () => $('tvPrev').click());

  /* panel: foco, inert y apertura */
  const background = () => [
    $('nav'),
    ...document.querySelectorAll('body > .strip, body > main, body > section, body > footer, body > .sel-float'),
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
  if ($('selFloat')) $('selFloat').addEventListener('click', openCart);
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
      `   Foto: ${new URL(it.img, document.baseURI).href}`,
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
      el.src = thumb(item); el.alt = '';
    }
    el.className = 'm-layer';
    return el;
  };

  mosaic.innerHTML = '';
  const brazilIdx = POOL.findIndex((p) => typeof p === 'object' && p.v.includes('brazil'));
  const pickFotoLibre = () => {
    let i;
    do { i = Math.floor(Math.random() * POOL.length); } while (showing.includes(i) || typeof POOL[i] === 'object');
    return i;
  };
  // al cargar, solo fotos ligeras: los videos entran cuando el mosaico se ve
  for (let t = 0; t < TILES; t++) {
    const tile = document.createElement('div');
    tile.className = 'm-tile';
    const idx = pickFotoLibre();
    showing[t] = idx;
    const layer = makeLayer(idx);
    layer.classList.add('on');
    tile.appendChild(layer);
    mosaic.appendChild(tile);
  }

  let mosaicVisible = true;
  let brazilPuesto = false;
  new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      mosaicVisible = en.isIntersecting;
      // el video de Brazil abre la sección: entra al primer cuadro
      // la primera vez que el mosaico aparece en pantalla
      if (en.isIntersecting && !brazilPuesto && brazilIdx >= 0) {
        brazilPuesto = true;
        const tile = mosaic.children[0];
        showing[0] = brazilIdx;
        const fresh = makeLayer(brazilIdx);
        tile.appendChild(fresh);
        requestAnimationFrame(() => requestAnimationFrame(() => {
          fresh.classList.add('on');
          const old = tile.querySelector('.m-layer.on');
          if (old && old !== fresh) old.classList.remove('on');
          setTimeout(() => { [...tile.querySelectorAll('.m-layer:not(.on)')].forEach((l) => l.remove()); }, 1000);
        }));
      }
    });
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
    plata:  { name: 'Disco Ball', imgs: ['assets/img/tematicas/espejos/main.jpg', 'assets/img/tematicas/espejos/09.jpg', 'assets/img/tematicas/espejos/10.jpg', 'assets/img/tematicas/espejos/11.jpg', 'assets/img/destacado/plata-4.jpg', 'assets/img/destacado/plata-1.jpg', 'assets/img/destacado/plata-2.jpg', 'assets/img/destacado/plata-3.jpg', 'assets/img/tematicas/espejos/01.jpg', 'assets/img/tematicas/espejos/02.jpg', 'assets/img/tematicas/espejos/03.jpg', 'assets/img/tematicas/espejos/04.jpg', 'assets/img/tematicas/espejos/05.jpg', 'assets/img/tematicas/espejos/06.jpg', 'assets/img/tematicas/espejos/07.jpg', 'assets/img/tematicas/espejos/08.jpg'] },
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
  conSwipe(lb, () => $('lbNext').click(), () => $('lbPrev').click());
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
