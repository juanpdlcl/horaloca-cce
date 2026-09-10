-- ═══════════════════════════════════════════════════════════════════════════
-- CC Entertainment (horaloca-cce) — RECREACIÓN COMPLETA DE LA BASE DE DATOS
-- Para pegar tal cual en el editor SQL de un proyecto NUEVO de Supabase.
--
-- Es IDEMPOTENTE: se puede correr varias veces sin romper nada.
--
-- Qué hace:
--   PARTE 1 — Extensiones y tabla admin_config (clave del panel).
--   PARTE 2 — Tabla public.tickets con todas las columnas que usa la app.
--   PARTE 3 — Defensas de datos (CHECKs de forma, dominio y tamaño).
--   PARTE 4 — RLS + privilegios por columna: anon SOLO puede insertar
--             cotizaciones "limpias" y solo en las columnas del formulario.
--   PARTE 5 — Trigger de guardia: fuerza en el servidor lo que anon no debe
--             poder decidir (status, quote, manual) + freno anti-inundación.
--   PARTE 6 — Las 3 funciones RPC del panel (admin_tickets,
--             admin_update_ticket, admin_delete_ticket), con las MISMAS
--             firmas y nombres de parámetro que espera admin/index.html.
--   PARTE 7 — Siembra de la clave del panel (¡EDITAR!) y recarga de PostgREST.
--   PARTE 8 — Verificación.
--   PARTE 9 — OPCIONAL (todo comentado): endurecimientos que EXIGEN tocar
--             el HTML del panel. No se ejecutan.
--
-- ANTES DE CORRER, EDITAR:
--   · PARTE 7: el valor de la clave del panel.
-- DESPUÉS DE CORRER, EN EL PROYECTO:
--   · js/config.js  → url y publishable key del proyecto NUEVO.
--   · admin/index.html:641 → PANEL_KEY = la clave que sembraste aquí.
--   · admin/index.html:755 → el ref viejo (ovsnjriqopsyboxyqaoz) del aviso.
--   · sw.js:6 → subir VERSION (hoy 'cce-v2') para invalidar el caché
--     que precachea js/config.js con las credenciales viejas.
--   · vercel.json ya permite connect-src https://*.supabase.co: no se toca.
--
-- Modelo de seguridad (el mismo de siempre, pero cerrado de verdad):
--   · anon (publishable key, pública por diseño) SOLO puede crear tickets,
--     y solo con la forma que produce el formulario público.
--   · Leer / editar / borrar pasa por funciones SECURITY DEFINER que
--     validan la clave del panel contra admin_config.
--   · LIMITACIÓN CONOCIDA Y ACEPTADA HOY: la clave del panel está embebida
--     en admin/index.html, que es público. Quien tenga la URL /admin tiene
--     acceso total a los tickets. Cerrar eso es la PARTE 9 (opcional).
-- ═══════════════════════════════════════════════════════════════════════════


-- ═══════════════════════════════════════════════════════════════════════════
-- PARTE 1 · Extensiones y tabla de la clave del panel
-- ═══════════════════════════════════════════════════════════════════════════

-- gen_random_bytes / gen_random_uuid (Supabase la instala en el esquema
-- "extensions"; si ya existe, este create no hace nada).
create extension if not exists pgcrypto with schema extensions;

-- Guarda la clave del panel. RLS activo y SIN NINGUNA POLICY = inaccesible
-- por la API REST. Solo la leen las funciones SECURITY DEFINER de la PARTE 6.
create table if not exists public.admin_config (
  secret text primary key
);

alter table public.admin_config enable row level security;
-- force: ni siquiera el dueño de la tabla se salta RLS al consultarla
-- por la API (las funciones SECURITY DEFINER sí, porque corren como dueño
-- del objeto y el bypass de RLS del owner sigue vigente dentro de ellas).
alter table public.admin_config force row level security;

-- Nadie que venga por la API puede tocarla, ni siquiera para contar filas.
revoke all on public.admin_config from public, anon, authenticated;


-- ═══════════════════════════════════════════════════════════════════════════
-- PARTE 2 · Tabla de cotizaciones (tickets)
--
-- Contrato exacto que consumen js/main.js y admin/index.html. NO cambiar
-- tipos ni nombres sin tocar el front:
--   id     text PK  → código corto que genera el cliente (base36, 6 chars)
--                     y que se imprime en el WhatsApp: "COTIZACIÓN #ABC123".
--   ts     timestamptz → el cliente SIEMPRE manda new Date().toISOString().
--   name   text not null
--   phone  text not null
--   "type" text  → 'Boda' | 'Cumpleaños' | 'XV años' | 'Empresa' | 'Otro'
--                  | 'Por definir'. Va entrecomillada: palabra reservada.
--   place  text  → texto libre, fallback 'Por definir'.
--   "date" text  → ¡TEXTO LIBRE, NO tipo date! Guarda "15 de octubre" o
--                  "Por definir". La fecha real de agenda vive en
--                  quote->'evento'->>'fecha' como 'YYYY-MM-DD'.
--   items  jsonb → array de {id, name, qty, img, note}. Renombrar cualquier
--                  clave rompe el panel.
--   status text  → SOLO 'nueva' | 'atendida'. Se inyecta crudo como clase
--                  CSS en el panel; un tercer valor descuadra la lista.
--   quote  jsonb → la escribe SOLO el panel:
--                  {rows:[{d,n,q,p}], disc, terms, place, pago, evento:{fecha,hora}}
--   manual boolean → true = cotización creada a mano desde el panel.
-- ═══════════════════════════════════════════════════════════════════════════

create table if not exists public.tickets (
  id      text primary key,
  ts      timestamptz not null default now(),
  name    text not null,
  phone   text not null,
  "type"  text,
  place   text,
  "date"  text,
  items   jsonb   not null default '[]'::jsonb,
  status  text    not null default 'nueva',
  quote   jsonb,
  manual  boolean not null default false
);

-- Por si la tabla ya existía de una corrida anterior incompleta.
alter table public.tickets add column if not exists ts      timestamptz not null default now();
alter table public.tickets add column if not exists "type"  text;
alter table public.tickets add column if not exists place   text;
alter table public.tickets add column if not exists "date"  text;
alter table public.tickets add column if not exists items   jsonb   not null default '[]'::jsonb;
alter table public.tickets add column if not exists status  text    not null default 'nueva';
alter table public.tickets add column if not exists quote   jsonb;
alter table public.tickets add column if not exists manual  boolean not null default false;

-- created_at: reloj DEL SERVIDOR, que el cliente no puede falsear.
-- Hoy el panel ordena y archiva por ts (que sí manda el cliente); esta
-- columna queda lista para cuando se migre el JS, y sirve para el freno
-- anti-inundación de la PARTE 5 sin depender de un ts inventado.
alter table public.tickets add column if not exists created_at timestamptz not null default now();

-- El panel lee todo ordenado por ts desc; el índice lo hace barato.
create index if not exists tickets_ts_idx         on public.tickets (ts desc);
create index if not exists tickets_created_at_idx on public.tickets (created_at desc);
create index if not exists tickets_status_idx     on public.tickets (status);

comment on table  public.tickets        is 'Cotizaciones de CC Entertainment. Las crea el cotizador público; las edita el panel vía RPC.';
comment on column public.tickets."date" is 'TEXTO LIBRE tal como lo escribió el cliente ("15 de octubre", "Por definir"). NO es tipo date. La fecha de agenda está en quote->evento->fecha.';
comment on column public.tickets.ts     is 'Lo manda el cliente (new Date().toISOString()). Para orden confiable usar created_at.';


-- ═══════════════════════════════════════════════════════════════════════════
-- PARTE 3 · Defensas de datos: forma, dominio y tamaño
--
-- Todos los CHECKs están calculados para NO rechazar nada de lo que hoy
-- envían la página pública (js/main.js:541-550) ni el alta manual del panel
-- (admin/index.html:1289-1295). Se crean NOT VALID y se validan al final:
-- así la corrida nunca falla aunque la tabla ya tuviera filas viejas.
--
-- OJO: el POST del cliente es fire-and-forget (js/main.js:570 traga el
-- error), así que un CHECK demasiado estricto haría desaparecer cotizaciones
-- EN SILENCIO. Por eso los márgenes son anchos y NO hay CHECK sobre ts
-- (relojes de teléfono desfasados romperían inserciones legítimas).
-- ═══════════════════════════════════════════════════════════════════════════

do $$
begin
  -- ── Forma de los jsonb ────────────────────────────────────────────────
  -- items debe ser array: si llega un número, el panel imprime
  -- "undefined elementos" y openDoc revienta en (current.items||[]).map().
  if not exists (select 1 from pg_constraint where conname = 'tickets_items_es_array') then
    alter table public.tickets add constraint tickets_items_es_array
      check (jsonb_typeof(items) = 'array') not valid;
  end if;

  if not exists (select 1 from pg_constraint where conname = 'tickets_items_max') then
    alter table public.tickets add constraint tickets_items_max
      check (jsonb_array_length(items) <= 60) not valid;
  end if;

  -- quote debe ser objeto o NULL: un quote escalar tumba el panel.
  if not exists (select 1 from pg_constraint where conname = 'tickets_quote_es_objeto') then
    alter table public.tickets add constraint tickets_quote_es_objeto
      check (quote is null or jsonb_typeof(quote) = 'object') not valid;
  end if;

  -- quote.rows, si viene, debe ser array: openDoc hace q.rows.map() sin defensa.
  if not exists (select 1 from pg_constraint where conname = 'tickets_quote_rows_array') then
    alter table public.tickets add constraint tickets_quote_rows_array
      check (
        quote is null
        or quote->'rows' is null
        or jsonb_typeof(quote->'rows') = 'array'
      ) not valid;
  end if;

  -- quote.evento.fecha, si viene, debe ser 'YYYY-MM-DD': el calendario hace
  -- e.fecha.slice(0,4) y revienta si no es string.
  if not exists (select 1 from pg_constraint where conname = 'tickets_quote_fecha_fmt') then
    alter table public.tickets add constraint tickets_quote_fecha_fmt
      check (
        quote is null
        or quote #> '{evento,fecha}' is null
        or (jsonb_typeof(quote #> '{evento,fecha}') = 'string'
            and quote #>> '{evento,fecha}' ~ '^\d{4}-\d{2}-\d{2}$')
      ) not valid;
  end if;

  -- ── Dominios cerrados ─────────────────────────────────────────────────
  -- status se inyecta CRUDO como clase CSS (admin/index.html:794) y alimenta
  -- los chips de filtro: solo estos dos valores.
  if not exists (select 1 from pg_constraint where conname = 'tickets_status_dominio') then
    alter table public.tickets add constraint tickets_status_dominio
      check (status in ('nueva','atendida')) not valid;
  end if;

  -- quote.pago se inyecta crudo como clase CSS (.ev-avance / .ev-pagado):
  -- un cuarto valor entra al calendario sin estilo.
  if not exists (select 1 from pg_constraint where conname = 'tickets_quote_pago_dominio') then
    alter table public.tickets add constraint tickets_quote_pago_dominio
      check (
        quote is null
        or quote->'pago' is null
        or quote->>'pago' in ('','avance','pagado')
      ) not valid;
  end if;

  -- ── Tamaños: evitan que un solo POST llene los 500 MB del plan Free ───
  -- Rangos amplios a propósito: el id real son 6 chars base36 en mayúscula.
  if not exists (select 1 from pg_constraint where conname = 'tickets_id_fmt') then
    alter table public.tickets add constraint tickets_id_fmt
      check (id ~ '^[A-Za-z0-9_-]{3,24}$') not valid;
  end if;

  if not exists (select 1 from pg_constraint where conname = 'tickets_name_len') then
    alter table public.tickets add constraint tickets_name_len
      check (char_length(name) between 1 and 120) not valid;
  end if;

  -- El formulario ya limpia el teléfono a dígitos y '+', con mínimo 8.
  -- Aquí acepto también espacios y paréntesis por el alta manual del panel,
  -- que puede mandar '—' (por eso el mínimo es 1, no 8: no quiero que una
  -- cotización manual falle en silencio).
  if not exists (select 1 from pg_constraint where conname = 'tickets_phone_len') then
    alter table public.tickets add constraint tickets_phone_len
      check (char_length(phone) between 1 and 40) not valid;
  end if;

  if not exists (select 1 from pg_constraint where conname = 'tickets_type_len') then
    alter table public.tickets add constraint tickets_type_len
      check ("type" is null or char_length("type") <= 60) not valid;
  end if;

  if not exists (select 1 from pg_constraint where conname = 'tickets_place_len') then
    alter table public.tickets add constraint tickets_place_len
      check (place is null or char_length(place) <= 200) not valid;
  end if;

  if not exists (select 1 from pg_constraint where conname = 'tickets_date_len') then
    alter table public.tickets add constraint tickets_date_len
      check ("date" is null or char_length("date") <= 120) not valid;
  end if;

  -- length(x::text) y no pg_column_size(): el cast de jsonb a text es
  -- inmutable y por tanto seguro dentro de un CHECK.
  if not exists (select 1 from pg_constraint where conname = 'tickets_items_size') then
    alter table public.tickets add constraint tickets_items_size
      check (octet_length(items::text) <= 32768) not valid;
  end if;

  if not exists (select 1 from pg_constraint where conname = 'tickets_quote_size') then
    alter table public.tickets add constraint tickets_quote_size
      check (quote is null or octet_length(quote::text) <= 65536) not valid;
  end if;
end $$;

-- Validación de los CHECKs sobre las filas existentes. En una base recién
-- creada pasa siempre. Si alguna fallara por datos viejos sucios, la corrida
-- NO se detiene: se avisa por NOTICE y el CHECK queda igual activo para
-- todas las filas NUEVAS (que es lo que importa).
do $$
declare c record;
begin
  for c in
    select conname
      from pg_constraint
     where conrelid = 'public.tickets'::regclass
       and contype = 'c'
       and not convalidated
  loop
    begin
      execute format('alter table public.tickets validate constraint %I', c.conname);
    exception when others then
      raise notice 'CHECK % no pudo validarse sobre filas existentes (%). Queda activo para filas nuevas.', c.conname, sqlerrm;
    end;
  end loop;
end $$;


-- ═══════════════════════════════════════════════════════════════════════════
-- PARTE 4 · RLS y privilegios: qué puede hacer el cliente anónimo
--
-- Dos capas distintas y ambas necesarias:
--   · GRANTS por columna → deciden QUÉ COLUMNAS puede nombrar el POST.
--     (Supabase por defecto le da a anon "grant all on tables", así que
--      sin esto anon podría escribir quote, manual, status, ts e id.)
--   · POLICY with check → decide qué FILAS son aceptables.
-- ═══════════════════════════════════════════════════════════════════════════

alter table public.tickets enable row level security;

-- Punto de partida limpio: se le quita todo a los roles de la API.
revoke all on public.tickets from public, anon, authenticated;

-- anon SOLO puede insertar, y solo las columnas que el formulario público
-- realmente envía (js/main.js:541-550). Fíjate en lo que NO está:
--   quote  → el presupuesto lo arma únicamente el panel;
--   manual → nadie se hace pasar por cotización creada a mano;
--   created_at → reloj del servidor, intocable.
-- Sí dejo id y ts porque el cliente los manda hoy y quitarlos rompería el
-- sitio (el id es el número que sale en el WhatsApp).
grant insert (id, ts, name, phone, "type", place, "date", items, status)
  on public.tickets to anon;

-- Ojo: el alta manual del panel (admin/index.html:1289-1295) entra por esta
-- MISMA puerta anon y manda manual:true. El trigger de la PARTE 5 lo
-- resuelve sin romperlo (ver nota allí).

drop policy if exists "clientes crean tickets" on public.tickets;
create policy "clientes crean tickets"
on public.tickets
for insert to anon
with check (
      status = 'nueva'                     -- ninguna cotización nace atendida
  and quote is null                        -- nadie se auto-agenda como pagado
  and jsonb_typeof(items) = 'array'
  and char_length(id)    between 3 and 24
  and char_length(name)  between 1 and 120
  and char_length(phone) between 1 and 40
  and coalesce(char_length("type"), 0) <= 60
  and coalesce(char_length(place),  0) <= 200
  and coalesce(char_length("date"), 0) <= 120
);

-- No hay policy de SELECT, UPDATE ni DELETE para anon: leer, editar y borrar
-- pasa obligatoriamente por las funciones de la PARTE 6.
-- Por eso el POST del sitio manda 'Prefer: return=minimal' (js/main.js:567):
-- pedir return=representation fallaría, porque anon no tiene SELECT.

-- authenticated no se usa hoy (no hay Supabase Auth en el proyecto):
-- queda sin ningún privilegio sobre tickets, a propósito.


-- ═══════════════════════════════════════════════════════════════════════════
-- PARTE 5 · Trigger de guardia + freno anti-inundación
--
-- Cinturón y tirantes: aunque mañana alguien vuelva a otorgar grants de más
-- desde el dashboard, este trigger reescribe en el servidor lo que el
-- cliente anónimo no debe decidir.
--
-- SECURITY INVOKER a propósito: dentro de un SECURITY DEFINER, current_user
-- sería el dueño de la función y el filtro por rol no distinguiría nada.
-- ═══════════════════════════════════════════════════════════════════════════

-- Contador global de inserciones por ventana. RLS activo y sin policies:
-- invisible por la API.
create table if not exists public.rl_hits (
  minuto timestamptz primary key,
  n      integer not null default 0
);
alter table public.rl_hits enable row level security;
revoke all on public.rl_hits from public, anon, authenticated;

-- SECURITY DEFINER obligatorio aquí: si fuera INVOKER, el conteo correría
-- como 'anon' bajo RLS, devolvería 0 SIEMPRE y el freno sería decorativo.
create or replace function public.rl_check()
returns void
language plpgsql
security definer
set search_path = public, pg_temp
as $$
declare
  v_min integer;
  v_hora integer;
begin
  insert into public.rl_hits (minuto, n)
  values (date_trunc('minute', now()), 1)
  on conflict (minuto) do update set n = public.rl_hits.n + 1
  returning n into v_min;

  -- Topes globales holgados: una fiesta real nunca genera 40 cotizaciones
  -- en un minuto, pero un script sí. Contrapartida honesta: quien sature el
  -- cupo también bloquea inserciones legítimas durante esa ventana; eso se
  -- recupera, llenar la base no.
  if v_min > 40 then
    raise exception 'Demasiadas solicitudes. Intenta de nuevo en un minuto.'
      using errcode = '53400';
  end if;

  select coalesce(sum(n), 0) into v_hora
    from public.rl_hits
   where minuto > now() - interval '1 hour';

  if v_hora > 400 then
    raise exception 'Servicio temporalmente saturado.' using errcode = '53400';
  end if;

  -- Tope absoluto de la tabla: protege la cuota del plan Free.
  if (select count(*) from public.tickets) > 50000 then
    raise exception 'Capacidad alcanzada.' using errcode = '53400';
  end if;

  -- Limpieza perezosa del contador (1 de cada 100 inserciones).
  if random() < 0.01 then
    delete from public.rl_hits where minuto < now() - interval '2 days';
  end if;
end $$;

revoke all on function public.rl_check() from public;
grant execute on function public.rl_check() to anon;

create or replace function public.tickets_guard()
returns trigger
language plpgsql
as $$
begin
  -- Solo vigilamos al rol anónimo. Las inserciones hechas desde el editor
  -- SQL, desde las funciones del panel o con service_role pasan intactas.
  if current_user <> 'anon' then
    return new;
  end if;

  -- Reloj del servidor, no negociable.
  new.created_at := now();

  -- El público nunca crea cotizaciones ya atendidas ni con presupuesto.
  new.status := 'nueva';
  new.quote  := null;

  -- manual: el alta manual del panel entra por esta misma puerta anon y
  -- manda manual:true. NO lo forzamos a false para no romper ese botón:
  -- solo garantizamos que no sea NULL. (Cerrar esto de verdad exige mover
  -- dbInsert a una RPC → ver PARTE 9.)
  new.manual := coalesce(new.manual, false);

  -- Red de seguridad por si faltaran datos.
  if new.id is null or new.id = '' then
    new.id := upper(encode(extensions.gen_random_bytes(5), 'hex'));
  end if;
  if new.ts is null then
    new.ts := now();
  end if;
  if new.items is null then
    new.items := '[]'::jsonb;
  end if;

  perform public.rl_check();
  return new;
end $$;

drop trigger if exists tickets_guard on public.tickets;
create trigger tickets_guard
before insert on public.tickets
for each row execute function public.tickets_guard();


-- ═══════════════════════════════════════════════════════════════════════════
-- PARTE 6 · Funciones RPC del panel
--
-- FIRMAS INTOCABLES: PostgREST enruta por NOMBRE de argumento leído del
-- cuerpo JSON. Renombrar p_secret / p_id / p_patch rompe las tres llamadas
-- de admin/index.html (líneas 670, 684, 688, 717).
--
-- Las tres son SECURITY DEFINER: se saltan RLS a propósito, y por eso lo
-- primero que hacen es validar la clave contra admin_config y LANZAR
-- EXCEPCIÓN si no coincide. El panel depende de ese error: rpc() lanza si
-- !r.ok (línea 661) y el login lo convierte en "Clave incorrecta o sin
-- conexión" (línea 725). Si devolvieran 200 con array vacío, cualquier
-- clave dejaría entrar.
-- ═══════════════════════════════════════════════════════════════════════════

-- Validador común de la clave del panel.
create or replace function public.admin_check(p_secret text)
returns void
language plpgsql
stable
security definer
set search_path = public, pg_temp
as $$
begin
  if p_secret is null
     or not exists (select 1 from public.admin_config where secret = p_secret) then
    raise exception 'unauthorized' using errcode = '42501';
  end if;
end $$;

revoke all on function public.admin_check(text) from public, anon, authenticated;
-- Nadie la llama desde fuera: solo la usan las otras funciones (como
-- SECURITY DEFINER, corren con los privilegios de su dueño).


-- ── admin_tickets ──────────────────────────────────────────────────────────
-- Devuelve JSONB (un array agregado), NO 'setof tickets'.
-- MOTIVO: PostgREST aplica su tope db-max-rows (1000 en Supabase) a las
-- funciones que devuelven conjuntos, y lo hace SIN error: recorta y responde
-- 200. Con 'order by ts desc' lo que se perdería es justo el archivo
-- histórico, sin ningún aviso. Un jsonb es UNA sola fila: no se puede
-- recortar.
-- COMPATIBLE CON EL JS ACTUAL SIN TOCAR UNA LÍNEA: rpc() hace
-- JSON.parse(await r.text()) (admin/index.html:662-663) y sigue obteniendo
-- un array; con la tabla vacía devuelve [].
drop function if exists public.admin_tickets(text);

create or replace function public.admin_tickets(p_secret text)
returns jsonb
language plpgsql
stable
security definer
set search_path = public, pg_temp
as $$
declare v jsonb;
begin
  perform public.admin_check(p_secret);

  select coalesce(jsonb_agg(to_jsonb(t) order by t.ts desc), '[]'::jsonb)
    into v
    from public.tickets t;

  return v;
end $$;


-- ── admin_update_ticket ────────────────────────────────────────────────────
-- Parche PARCIAL por coalesce. Solo aplica name, phone, type, place, date,
-- status y quote; cualquier otra clave del patch se ignora en silencio
-- (el panel nunca manda items, manual, id ni ts).
-- NOTA: quote se REEMPLAZA entero, no se hace merge profundo. Por eso
-- collectQuote() en el panel hace spread de current.quote primero
-- (admin/index.html:1220), para no perder pago ni evento.
create or replace function public.admin_update_ticket(p_secret text, p_id text, p_patch jsonb)
returns void
language plpgsql
security definer
set search_path = public, pg_temp
as $$
begin
  perform public.admin_check(p_secret);

  update public.tickets set
    name   = coalesce(p_patch->>'name',   name),
    phone  = coalesce(p_patch->>'phone',  phone),
    "type" = coalesce(p_patch->>'type',   "type"),
    place  = coalesce(p_patch->>'place',  place),
    "date" = coalesce(p_patch->>'date',   "date"),
    status = coalesce(p_patch->>'status', status),
    quote  = coalesce(p_patch->'quote',   quote)
  where id = p_id;
end $$;


-- ── admin_delete_ticket ────────────────────────────────────────────────────
create or replace function public.admin_delete_ticket(p_secret text, p_id text)
returns void
language plpgsql
security definer
set search_path = public, pg_temp
as $$
begin
  perform public.admin_check(p_secret);
  delete from public.tickets where id = p_id;
end $$;


-- ── Privilegios de las tres funciones ──────────────────────────────────────
-- IMPORTANTE: en PostgreSQL, "create function" concede EXECUTE a PUBLIC
-- automáticamente. El script viejo nunca lo revocaba, así que cualquier rol
-- presente o futuro podía invocarlas. Aquí se revoca primero y se concede
-- después, solo a anon (que es el rol con el que habla el panel).
revoke all on function public.admin_tickets(text)                    from public, anon, authenticated;
revoke all on function public.admin_update_ticket(text, text, jsonb) from public, anon, authenticated;
revoke all on function public.admin_delete_ticket(text, text)        from public, anon, authenticated;

grant execute on function public.admin_tickets(text)                    to anon;
grant execute on function public.admin_update_ticket(text, text, jsonb) to anon;
grant execute on function public.admin_delete_ticket(text, text)        to anon;


-- ═══════════════════════════════════════════════════════════════════════════
-- PARTE 7 · Clave del panel  ←←← EDITAR ESTA LÍNEA ANTES DE CORRER
--
-- Sin esta fila, las tres RPC responden siempre 'unauthorized' y el panel
-- se abre vacío mostrando el aviso de "base de datos apagada".
--
-- La clave debe coincidir EXACTAMENTE con admin/index.html:641 (PANEL_KEY).
-- Como ese HTML es público y está en un repo público, la clave vieja
-- 'CCE-IaRvRdOMLumAX9tH' está QUEMADA: no la reutilices. Genera una nueva,
-- larga y aleatoria, y cámbiala también en el HTML antes de desplegar.
-- ═══════════════════════════════════════════════════════════════════════════

insert into public.admin_config (secret)
values ('CCE-CAMBIAR-POR-CLAVE-NUEVA-LARGA-Y-ALEATORIA')
on conflict (secret) do nothing;

-- Si estás rotando la clave: primero inserta la nueva (arriba), verifica que
-- el panel entra, y recién entonces borra la vieja:
-- delete from public.admin_config where secret = 'CCE-IaRvRdOMLumAX9tH';

-- PostgREST cachea el esquema: esto le dice que lo recargue ya.
notify pgrst, 'reload schema';


-- ═══════════════════════════════════════════════════════════════════════════
-- PARTE 8 · Verificación (solo lectura, no cambia nada)
-- ═══════════════════════════════════════════════════════════════════════════

-- Debe devolver exactamente 1. Si da 0, el panel NO va a poder entrar.
select count(*) as claves_del_panel from public.admin_config;

-- Debe listar SOLO 'INSERT' para anon, y solo sobre las 9 columnas
-- del formulario (id, ts, name, phone, type, place, date, items, status).
select grantee, privilege_type, column_name
  from information_schema.column_privileges
 where table_schema = 'public'
   and table_name   = 'tickets'
   and grantee in ('anon','authenticated','PUBLIC')
 order by grantee, privilege_type, column_name;

-- Debe listar solo la policy de INSERT para anon.
select policyname, cmd, roles
  from pg_policies
 where schemaname = 'public' and tablename = 'tickets';

-- Las 3 funciones deben existir con estas firmas exactas.
select p.proname,
       pg_get_function_identity_arguments(p.oid) as firma,
       p.prosecdef as security_definer
  from pg_proc p
  join pg_namespace n on n.oid = p.pronamespace
 where n.nspname = 'public'
   and p.proname in ('admin_tickets','admin_update_ticket','admin_delete_ticket')
 order by p.proname;

-- Prueba de humo desde la terminal (reemplaza <ref> y <publishable-key>):
--
-- curl -s -X POST "https://<ref>.supabase.co/rest/v1/rpc/admin_tickets" \
--   -H "apikey: <publishable-key>" -H "Content-Type: application/json" \
--   -d '{"p_secret":"LA-CLAVE-QUE-SEMBRASTE"}'
--   → esperado: []   (con clave mala: 'unauthorized', HTTP 400)
--
-- curl -s -X POST "https://<ref>.supabase.co/rest/v1/tickets" \
--   -H "apikey: <publishable-key>" -H "Content-Type: application/json" \
--   -H "Prefer: return=minimal" \
--   -d '{"id":"TEST01","ts":"2026-09-10T12:00:00Z","name":"Prueba","phone":"8095551234","type":"Boda","place":"Por definir","date":"Por definir","items":[],"status":"nueva"}'
--   → esperado: HTTP 201 sin cuerpo. Luego bórralo con admin_delete_ticket.


-- ═══════════════════════════════════════════════════════════════════════════
-- ═══════════════════════════════════════════════════════════════════════════
--
--   PARTE 9 · OPCIONAL — NO SE EJECUTA (todo comentado)
--
--   Endurecimientos que SÍ exigen cambiar el HTML del panel. Cada bloque
--   dice en una línea qué cambio de HTML haría falta. No descomentar nada
--   sin hacer el cambio de HTML EN LA MISMA VENTANA, o el panel deja de
--   funcionar (y falla en silencio: dbInsert y dbUpdate no revisan r.ok).
--
-- ═══════════════════════════════════════════════════════════════════════════
-- ═══════════════════════════════════════════════════════════════════════════


-- ── OPCIONAL 9.A · Sacar el alta manual del panel de la puerta anon ────────
-- PROBLEMA: el botón "+ Nueva cotización" hace un POST directo a
-- /rest/v1/tickets con la key pública (admin/index.html:673-678), o sea que
-- depende de que la puerta de anon siga abierta. Con una RPC propia, la
-- policy pública puede cerrarse del todo (incluido forzar manual := false).
-- CAMBIO DE HTML: en dbInsert (admin/index.html:672), reemplazar el fetch por
--   await rpc('admin_insert_ticket', { p_secret: sbSecret, p_ticket: k });
--
-- create or replace function public.admin_insert_ticket(p_secret text, p_ticket jsonb)
-- returns text
-- language plpgsql security definer set search_path = public, pg_temp as $$
-- declare v_id text;
-- begin
--   perform public.admin_check(p_secret);   -- no pasa por rl_check
--   insert into public.tickets (id, ts, name, phone, "type", place, "date", items, status, quote, manual)
--   values (coalesce(nullif(p_ticket->>'id',''), upper(encode(extensions.gen_random_bytes(5),'hex'))),
--           coalesce((p_ticket->>'ts')::timestamptz, now()),
--           left(coalesce(p_ticket->>'name','Sin nombre'), 120),
--           left(coalesce(p_ticket->>'phone','—'), 40),
--           left(nullif(p_ticket->>'type',''), 60),
--           left(nullif(p_ticket->>'place',''), 200),
--           left(nullif(p_ticket->>'date',''), 120),
--           coalesce(p_ticket->'items', '[]'::jsonb),
--           coalesce(nullif(p_ticket->>'status',''), 'nueva'),
--           p_ticket->'quote',
--           true)
--   returning id into v_id;
--   return v_id;
-- end $$;
-- revoke all on function public.admin_insert_ticket(text, jsonb) from public, authenticated;
-- grant execute on function public.admin_insert_ticket(text, jsonb) to anon;
--
-- -- y recién entonces, endurecer la policy pública:
-- -- drop policy if exists "clientes crean tickets" on public.tickets;
-- -- create policy "clientes crean tickets" on public.tickets for insert to anon
-- --   with check (status = 'nueva' and quote is null and manual is false
-- --               and jsonb_typeof(items) = 'array');
-- -- y en tickets_guard() cambiar la línea de manual por:  new.manual := false;
-- notify pgrst, 'reload schema';


-- ── OPCIONAL 9.B · Que el id lo genere el servidor (id impredecible) ───────
-- PROBLEMA: el id es Date.now() en base36 recortado (js/main.js:542), o sea
-- determinista. Alguien puede pre-insertar los ids de los próximos minutos;
-- cada cotización real choca con 409 duplicate key y js/main.js:570 se lo
-- traga: el cliente ve "Ticket creado" y la cotización nunca llega.
-- CAMBIO DE HTML: js/main.js debe dejar de mandar `id` y leer el id que
-- devuelve la base (Prefer: return=representation + policy de select propia,
-- o una RPC create_ticket), y admin/index.html:1291 igual. El número que se
-- imprime en el WhatsApp (js/main.js:579) pasa a venir de la respuesta.
--
-- alter table public.tickets alter column id set default upper(encode(extensions.gen_random_bytes(5), 'hex'));
-- revoke insert (id) on public.tickets from anon;
-- -- Alternativa sin tocar el WhatsApp: conservar el código corto del cliente
-- -- en una columna aparte que NO sea la PK (chocar ahí no rompe el insert):
-- -- alter table public.tickets add column if not exists ref text;
-- -- alter table public.tickets add constraint tickets_ref_fmt check (ref is null or ref ~ '^[A-Z0-9]{4,10}$');
-- -- create index if not exists tickets_ref_idx on public.tickets (ref);
-- -- grant insert (ref) on public.tickets to anon;


-- ── OPCIONAL 9.C · Que el cliente no pueda falsear ts (orden de la lista) ──
-- PROBLEMA: anon manda ts, y el panel ordena por ts desc y archiva por
-- antigüedad. Un ts en 2090 clava filas basura arriba; uno de hace 40 días
-- las entierra en Historial.
-- CAMBIO DE HTML: en admin/index.html, esHistorial() (líneas 768-771), la
-- fecha de la lista (792) y la del documento (1141) deben usar k.created_at
-- en vez de k.ts; y admin_tickets debe ordenar por created_at desc.
--
-- revoke insert (ts) on public.tickets from anon;
-- alter table public.tickets alter column ts set default now();
-- -- y en tickets_guard():  new.ts := now();
-- -- y en admin_tickets(): order by t.created_at desc


-- ── OPCIONAL 9.D · Paginación real en admin_tickets ────────────────────────
-- La versión de la PARTE 6 ya evita el corte silencioso a 1000 filas, pero
-- sigue bajando la tabla entera en cada apertura del panel (egress + un
-- innerHTML gigante en el teléfono de la dueña).
-- CAMBIO DE HTML: rpc('admin_tickets', { p_secret, p_limit: 200, p_offset: 0 })
-- y un botón "cargar más" en la lista.
--
-- create or replace function public.admin_tickets(p_secret text, p_limit int default 200, p_offset int default 0)
-- returns jsonb
-- language plpgsql stable security definer set search_path = public, pg_temp as $$
-- declare v jsonb;
-- begin
--   perform public.admin_check(p_secret);
--   select coalesce(jsonb_agg(to_jsonb(t) order by t.created_at desc), '[]'::jsonb) into v
--     from (select * from public.tickets
--            order by created_at desc
--            limit least(coalesce(p_limit,200), 500)
--           offset greatest(coalesce(p_offset,0), 0)) t;
--   return v;
-- end $$;
-- grant execute on function public.admin_tickets(text, int, int) to anon;


-- ── OPCIONAL 9.E · Clave del panel hasheada y fuera del esquema public ─────
-- PROBLEMA: admin_config.secret está en texto plano, así que cualquier
-- backup, export o vista del dashboard la entrega tal cual; y la comparación
-- no es de tiempo constante.
-- CAMBIO DE HTML: ninguno si se mantiene el mismo p_secret (solo cambia la
-- verificación por dentro). Es el paso barato antes de 9.F.
--
-- create schema if not exists private;
-- revoke all on schema private from public, anon, authenticated;
-- alter table public.admin_config set schema private;
-- alter table private.admin_config add column if not exists secret_hash text;
-- update private.admin_config set secret_hash = extensions.crypt(secret, extensions.gen_salt('bf', 10));
-- alter table private.admin_config drop column if exists secret;
-- create or replace function public.admin_check(p_secret text) returns void
-- language plpgsql stable security definer set search_path = private, extensions, pg_temp as $$
-- begin
--   if not exists (select 1 from private.admin_config c
--                   where c.secret_hash = extensions.crypt(coalesce(p_secret,''), c.secret_hash)) then
--     raise exception 'unauthorized' using errcode = '42501';
--   end if;
-- end $$;


-- ── OPCIONAL 9.F · ARREGLO DE FONDO: Supabase Auth en vez de clave ─────────
-- PROBLEMA REAL Y CRÍTICO: PANEL_KEY está en admin/index.html:641, que Vercel
-- sirve público (y está en el historial de git). Cualquiera que haga
-- `curl https://sitio/admin` obtiene la clave, y con la publishable key —que
-- está en js/config.js— llama admin_tickets y se lleva nombre y WhatsApp de
-- TODOS los clientes, o llama admin_delete_ticket y borra el CRM entero.
-- Rotar la clave no arregla nada mientras se vuelva a hornear en el HTML:
-- el único modelo que no exige un secreto en un archivo público es un login
-- de verdad.
-- CAMBIO DE HTML (varios puntos de admin/index.html):
--   · sbHeaders() (652): apikey sigue siendo la publishable, pero
--     Authorization: 'Bearer ' + access_token del usuario logueado.
--   · login (711-725): POST /auth/v1/token?grant_type=password {email,password},
--     distinguiendo 400 (credenciales malas) de fallo de red; guardar y
--     renovar el refresh_token.
--   · rpc(): dejar de mandar p_secret en las tres llamadas.
--   · borrar PANEL_KEY (641) y el auto-login por hash (643-649).
--   · manejar 401 volviendo al login, no al aviso de "base de datos apagada".
--
-- create schema if not exists private;
-- revoke all on schema private from public, anon, authenticated;
-- create table if not exists private.admins (
--   user_id uuid primary key references auth.users(id) on delete cascade,
--   created_at timestamptz not null default now()
-- );
-- revoke all on all tables in schema private from public, anon, authenticated;
--
-- -- Crear antes el usuario en Authentication → Users, y poner aquí su correo:
-- insert into private.admins (user_id)
-- select id from auth.users where email = lower('CORREO-DEL-PANEL@ejemplo.com')
-- on conflict do nothing;
--
-- create or replace function public.is_admin() returns boolean
-- language sql stable security definer set search_path = private, pg_temp as $$
--   select exists (select 1 from private.admins a where a.user_id = auth.uid());
-- $$;
-- revoke all on function public.is_admin() from public, anon;
-- grant execute on function public.is_admin() to authenticated;
--
-- -- El panel autenticado trabaja con RLS normal, sin ninguna RPC secreta:
-- create policy "admin lee tickets"    on public.tickets for select to authenticated using (public.is_admin());
-- create policy "admin edita tickets"  on public.tickets for update to authenticated using (public.is_admin()) with check (public.is_admin());
-- create policy "admin borra tickets"  on public.tickets for delete to authenticated using (public.is_admin());
-- create policy "admin crea tickets"   on public.tickets for insert to authenticated with check (public.is_admin());
-- grant select, insert, update, delete on public.tickets to authenticated;
--
-- -- Y una vez migrado y probado el panel, cerrar la puerta vieja del todo:
-- -- revoke execute on function public.admin_tickets(text)                    from anon;
-- -- revoke execute on function public.admin_update_ticket(text, text, jsonb) from anon;
-- -- revoke execute on function public.admin_delete_ticket(text, text)        from anon;
-- -- drop function if exists public.admin_tickets(text);
-- -- drop function if exists public.admin_update_ticket(text, text, jsonb);
-- -- drop function if exists public.admin_delete_ticket(text, text);
-- -- drop table if exists public.admin_config;
-- notify pgrst, 'reload schema';


-- ── OPCIONAL 9.G · Papelera en vez de borrado duro ─────────────────────────
-- admin_delete_ticket borra sin log y sin vuelta atrás; en el plan Free no
-- hay backups descargables ni point-in-time recovery.
-- CAMBIO DE HTML: ninguno si admin_tickets filtra deleted_at is null y
-- admin_delete_ticket pasa a marcar en vez de borrar (el panel ni se entera).
--
-- alter table public.tickets add column if not exists deleted_at timestamptz;
-- create or replace function public.admin_delete_ticket(p_secret text, p_id text)
-- returns void language plpgsql security definer set search_path = public, pg_temp as $$
-- begin
--   perform public.admin_check(p_secret);
--   update public.tickets set deleted_at = now() where id = p_id and deleted_at is null;
-- end $$;
-- -- y en admin_tickets():  from public.tickets t where t.deleted_at is null


-- ── OPCIONAL 9.H · Fuera de SQL, pero del mismo problema ───────────────────
-- · vercel.json: cerrar el comodín de la CSP —
--   connect-src 'self' https://<ref-nuevo>.supabase.co
--   (hoy https://*.supabase.co autoriza exfiltrar a CUALQUIER proyecto).
-- · vercel.json: añadir a /admin → Cross-Origin-Opener-Policy: same-origin.
-- · Vercel → Settings → Deployment Protection → Password Protection sobre
--   /admin, o desplegar admin/ como proyecto aparte.
-- · Repo público en GitHub: la clave vieja queda en el historial aunque se
--   cambie el archivo. Rotarla es obligatorio, no opcional.
-- ═══════════════════════════════════════════════════════════════════════════

