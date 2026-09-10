-- ═══════════════════════════════════════════════════════════════════════
-- CC Entertainment — CERRAR EL PANEL CON LOGIN DE VERDAD
--
-- Qué arregla: hoy la clave del panel viaja dentro de admin/index.html,
-- que es una página pública. Cualquiera que abra el código fuente de
-- horaloca-cce.vercel.app/admin la lee y puede ver, editar y borrar TODAS
-- las cotizaciones. Este script quita esa puerta y la sustituye por un
-- inicio de sesión con correo y contraseña.
--
-- Es idempotente: se puede correr varias veces sin romper nada.
--
-- ANTES de correrlo: crea el usuario en Supabase
--   Authentication → Users → Add user → correo + contraseña → Create user
--   (marca "Auto Confirm User" para no tener que confirmar por correo)
--
-- DESPUÉS de correrlo: entra a /admin con ese correo y esa contraseña.
-- ═══════════════════════════════════════════════════════════════════════


-- ─── 1. Quién puede entrar al panel ────────────────────────────────────
-- Lista blanca de correos. Aunque alguien logre registrarse por su cuenta,
-- si su correo no está aquí no ve ni una cotización.
-- EDITA ESTOS CORREOS con los que uses de verdad.
create or replace function public.es_panel()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select coalesce(auth.jwt() ->> 'email', '') in (
    'carolina.caba95@gmail.com',
    'marcomercedes@grupocjc.com'
  )
$$;

comment on function public.es_panel() is
  'Lista blanca del panel. Para dar o quitar acceso, edita los correos y vuelve a correr este create or replace.';


-- ─── 2. Fuera la puerta vieja ──────────────────────────────────────────
-- Las tres funciones aceptaban la clave que estaba escrita en el HTML
-- público. Aunque alguien ya la haya copiado, a partir de aquí no sirve.
revoke execute on function public.admin_tickets(text)              from anon, authenticated, public;
revoke execute on function public.admin_update_ticket(text, text, jsonb) from anon, authenticated, public;
revoke execute on function public.admin_delete_ticket(text, text)  from anon, authenticated, public;

drop function if exists public.admin_tickets(text);
drop function if exists public.admin_update_ticket(text, text, jsonb);
drop function if exists public.admin_delete_ticket(text, text);

-- La clave quemada ya no vale para nada: se borra.
delete from public.admin_config;


-- ─── 3. Permisos por rol ───────────────────────────────────────────────
-- anon  = cualquier visitante de la web. Solo puede CREAR cotizaciones.
-- authenticated = quien inició sesión. Solo si su correo está en la lista.
revoke all on public.tickets from anon, authenticated;
grant insert on public.tickets to anon;
grant select, insert, update, delete on public.tickets to authenticated;

alter table public.tickets enable row level security;

drop policy if exists "clientes crean tickets" on public.tickets;
drop policy if exists "panel lee"             on public.tickets;
drop policy if exists "panel crea"            on public.tickets;
drop policy if exists "panel edita"           on public.tickets;
drop policy if exists "panel borra"           on public.tickets;

-- El cotizador público: solo insertar, nunca leer.
create policy "clientes crean tickets"
  on public.tickets for insert to anon
  with check (true);

-- El panel: todo, pero solo para los correos de la lista.
create policy "panel lee"
  on public.tickets for select to authenticated
  using (public.es_panel());

create policy "panel crea"
  on public.tickets for insert to authenticated
  with check (public.es_panel());

create policy "panel edita"
  on public.tickets for update to authenticated
  using (public.es_panel())
  with check (public.es_panel());

create policy "panel borra"
  on public.tickets for delete to authenticated
  using (public.es_panel());


-- ─── 4. Comprobación ───────────────────────────────────────────────────
-- Debe devolver: las 4 políticas de arriba, y ninguna función admin_*.
select policyname, cmd, roles
  from pg_policies
 where schemaname = 'public' and tablename = 'tickets'
 order by policyname;

select count(*) as funciones_admin_que_quedan
  from pg_proc p join pg_namespace n on n.oid = p.pronamespace
 where n.nspname = 'public' and p.proname like 'admin\_%';

-- Refrescar la caché de PostgREST para que los cambios se vean al instante.
notify pgrst, 'reload schema';
