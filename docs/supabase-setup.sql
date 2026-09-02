-- ═══════════════════════════════════════════════════════════
-- CC Entertainment — Base de datos de cotizaciones (Supabase)
-- YA EJECUTADO en el proyecto horaloca-cce (ago 2026).
-- Se guarda aquí como respaldo/documentación.
--
-- Modelo de seguridad:
--  · Los clientes (anon) SOLO pueden crear tickets.
--  · Leer/editar/borrar requiere la clave del panel, que vive
--    únicamente en la tabla admin_config (inaccesible por API)
--    y se verifica dentro de funciones SECURITY DEFINER.
-- ═══════════════════════════════════════════════════════════

create table if not exists public.tickets (
  id text primary key,
  ts timestamptz not null default now(),
  name text not null,
  phone text not null,
  "type" text,
  place text,
  "date" text,
  items jsonb not null default '[]',
  status text not null default 'nueva',
  quote jsonb,
  manual boolean default false
);
alter table public.tickets enable row level security;
drop policy if exists "clientes crean tickets" on public.tickets;
create policy "clientes crean tickets" on public.tickets for insert to anon with check (true);

create table if not exists public.admin_config (secret text primary key);
alter table public.admin_config enable row level security;
-- insert into public.admin_config (secret) values ('<CLAVE-DEL-PANEL>');

create or replace function public.admin_tickets(p_secret text)
returns setof public.tickets language plpgsql security definer set search_path = public as $$
begin
  if not exists (select 1 from admin_config where secret = p_secret) then
    raise exception 'unauthorized';
  end if;
  return query select * from tickets order by ts desc;
end $$;

create or replace function public.admin_update_ticket(p_secret text, p_id text, p_patch jsonb)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not exists (select 1 from admin_config where secret = p_secret) then
    raise exception 'unauthorized';
  end if;
  update tickets set
    name   = coalesce(p_patch->>'name', name),
    phone  = coalesce(p_patch->>'phone', phone),
    "type" = coalesce(p_patch->>'type', "type"),
    place  = coalesce(p_patch->>'place', place),
    "date" = coalesce(p_patch->>'date', "date"),
    status = coalesce(p_patch->>'status', status),
    quote  = coalesce(p_patch->'quote', quote)
  where id = p_id;
end $$;

create or replace function public.admin_delete_ticket(p_secret text, p_id text)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not exists (select 1 from admin_config where secret = p_secret) then
    raise exception 'unauthorized';
  end if;
  delete from tickets where id = p_id;
end $$;

grant execute on function public.admin_tickets(text) to anon;
grant execute on function public.admin_update_ticket(text, text, jsonb) to anon;
grant execute on function public.admin_delete_ticket(text, text) to anon;
