/* ═══ Mantiene despierta la base de datos ═══
   Supabase (plan gratis) pausa un proyecto tras ~7 dias sin actividad y,
   al pausarlo, le quita el dominio: la web deja de guardar cotizaciones.
   Vercel llama a esta funcion una vez al dia (ver "crons" en vercel.json)
   y la consulta cuenta como actividad, asi que el proyecto nunca se pausa.

   La consulta es minima y no expone nada: anon no puede leer tickets
   (RLS lo impide), asi que la respuesta siempre es una lista vacia.
   La key es la publishable, que ya es publica por diseno.
   CommonJS a proposito: el repo no tiene package.json, asi que Vercel
   trata los .js de api/ como CommonJS. */
const SUPABASE = 'https://ovsnjriqopsyboxyqaoz.supabase.co';
const KEY = 'sb_publishable_G5Z6TqEay-PZ8w0TWiq9dA_J64WLawK';

module.exports = async (req, res) => {
  const t0 = Date.now();
  try {
    const r = await fetch(`${SUPABASE}/rest/v1/tickets?select=id&limit=1`, {
      headers: { apikey: KEY, Accept: 'application/json' },
    });
    const ok = r.status === 200;
    res.status(ok ? 200 : 503).json({
      ok,
      status: r.status,
      ms: Date.now() - t0,
      cuando: new Date().toISOString(),
    });
  } catch (e) {
    res.status(503).json({ ok: false, error: String(e), cuando: new Date().toISOString() });
  }
};
