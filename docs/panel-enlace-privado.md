# Panel administrativo: enlace privado

El panel (`/admin`) no pide contraseña: se abre con un **enlace privado**.

    https://horaloca-cce.vercel.app/admin#k=<secreto>

## Por qué es distinto de como estaba antes

Antes la clave estaba **escrita dentro de `admin/index.html`**, que es una
página pública: cualquiera que abriera el código fuente la leía. Ese era el
fallo, no el hecho de tener un enlace.

Ahora el secreto vive en dos sitios y en ninguno más:

1. En la tabla `admin_config` de Supabase, que no es consultable por la API
   (RLS activo y forzado, y sin permisos para `anon` ni `authenticated`).
2. En el enlace que guarda el dueño.

En el código **no está**. Quien abra `/admin` sin el enlace no ve nada.

El secreto viaja después de la almohadilla (`#`), que el navegador **no manda
al servidor**: no queda en los registros de Vercel ni de ningún intermediario.
La primera vez se guarda en ese dispositivo y se borra de la barra de
direcciones, así que después basta con abrir `/admin`.

## Lo que hay que tener claro

- **Quien tenga el enlace, entra.** No se puede dar acceso a una persona y
  quitárselo solo a ella: el secreto es uno solo.
- Si se reenvía por WhatsApp, se comparte la pantalla o se sincroniza el
  historial del navegador, el acceso se va con él.
- No hay registro de quién entró ni cuándo.

Si algún día hace falta cerrar el acceso a alguien en concreto, el paso es
pasar a inicio de sesión con correo y contraseña (Supabase Authentication).

## Cambiar el secreto

Si el enlace se filtra, se cambia en un minuto desde el editor SQL de
Supabase y el enlace viejo deja de servir al instante:

```sql
delete from public.admin_config;
insert into public.admin_config (secret) values ('<secreto-nuevo-largo>');
```

Genera el secreto nuevo con algo que no sea adivinable, por ejemplo:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Cómo está montado

- `admin/index.html` lee el secreto de `location.hash`, lo guarda en
  `localStorage` (`cce-panel-k`) y limpia la URL.
- Todas las operaciones pasan por funciones `SECURITY DEFINER` que comprueban
  el secreto contra `admin_config`: `admin_tickets`, `admin_insert_ticket`,
  `admin_update_ticket`, `admin_delete_ticket`.
- La tabla `tickets` no es accesible directamente: `anon` solo puede
  **insertar** (el cotizador público). Leer, editar y borrar exige el secreto.
- Un 400/401/403 borra el secreto guardado y devuelve al aviso de acceso
  privado.
