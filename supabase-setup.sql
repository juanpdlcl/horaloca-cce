-- ═══════════════════════════════════════════════════════════
-- CC Entertainment — Base de datos de cotizaciones (Supabase)
-- Pega TODO este archivo en: Supabase → SQL Editor → Run
-- ═══════════════════════════════════════════════════════════

create table if not exists public.tickets (
  id     text primary key,
  ts     timestamptz not null default now(),
  name   text not null,
  phone  text not null,
  type   text,
  place  text,
  date   text,
  items  jsonb not null default '[]',
  status text not null default 'nueva',
  quote  jsonb,
  manual boolean default false
);

alter table public.tickets enable row level security;

-- Los clientes (anónimos) SOLO pueden crear tickets: nunca leer ni tocar los de otros.
create policy "clientes crean tickets"
  on public.tickets for insert to anon with check (true);

-- Solo el dueño autenticado (tu usuario del panel) puede ver y gestionar.
create policy "dueno lee"    on public.tickets for select to authenticated using (true);
create policy "dueno edita"  on public.tickets for update to authenticated using (true);
create policy "dueno borra"  on public.tickets for delete to authenticated using (true);

-- ═══════════════════════════════════════════════════════════
-- DESPUÉS DE CORRER ESTO:
-- 1) Authentication → Users → Add user: crea tu usuario con tu
--    correo y una clave fuerte (ese será el login del panel).
-- 2) Project Settings → API: copia "Project URL" y "anon public key"
--    y pégalos en js/config.js del sitio.
-- ═══════════════════════════════════════════════════════════
