/* ═══ Conexión a Supabase (base de datos de cotizaciones) ═══
   Mientras esté vacío, todo funciona en modo local (mismo navegador).
   Para activar la nube: crea el proyecto gratis en supabase.com,
   corre supabase-setup.sql y pega aquí los dos valores de
   Project Settings → API. */
window.CCE_SUPABASE = {
  url: '',   // ej. 'https://abcdefgh.supabase.co'
  key: '',   // la "anon public" key
};
