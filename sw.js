/* ═══════════════════════════════════════════
   CC ENTERTAINMENT — modo a prueba de fallos
   La página queda guardada en el dispositivo:
   si el servidor o el internet fallan, igual abre.
   ═══════════════════════════════════════════ */
const VERSION = 'cce-v1';
const SHELL = `${VERSION}-shell`;
const MEDIA = `${VERSION}-media`;

/* lo mínimo para que la página abra sin internet */
const BASE = [
  '/',
  '/cotiza',
  '/css/styles.css?v=19',
  '/js/main.js?v=19',
  '/js/config.js',
  '/assets/img/logo-mark-glow.png',
  '/assets/img/hero-feathers.png',
  '/assets/img/hero-poster.jpg',
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(SHELL)
      .then((c) => Promise.allSettled(BASE.map((u) => c.add(u))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((ks) => Promise.all(ks.filter((k) => !k.startsWith(VERSION)).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) return;      // Supabase y fuentes: directo a la red
  if (url.pathname.startsWith('/admin')) return;   // el panel siempre en vivo

  /* fotos, videos y PDFs: del dispositivo primero (vuelan), y se guardan al vuelo */
  if (url.pathname.startsWith('/assets/') || url.pathname.endsWith('.pdf')) {
    e.respondWith(
      caches.match(req).then((hit) => hit || fetch(req).then((res) => {
        if (res.ok) {
          const copia = res.clone();
          caches.open(MEDIA).then((c) => c.put(req, copia));
        }
        return res;
      }).catch(() => hit))
    );
    return;
  }

  /* páginas, CSS y JS: siempre lo más nuevo; si no hay red, lo guardado */
  e.respondWith(
    fetch(req).then((res) => {
      if (res.ok) {
        const copia = res.clone();
        caches.open(SHELL).then((c) => c.put(req, copia));
      }
      return res;
    }).catch(() =>
      caches.match(req).then((hit) => hit
        || caches.match(req.mode === 'navigate' ? '/' : req)
        || new Response('', { status: 504 }))
    )
  );
});
