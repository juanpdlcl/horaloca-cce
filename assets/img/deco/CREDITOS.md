# Origen de las imágenes de decoración

## assets/img/navidad-adornos/ — adornos navideños de CC

Salen todos de **`NAVIDAD CC.png`**, el pliego de adornos que mandó el cliente:
pino con lazos magenta y plumas turquesa, moradas y doradas, o sea los colores
del logo. Es material propio de CC Entertainment.

`tools/extraer_cc.py` separa el pliego en sus piezas sueltas: agrupa por canal
alfa (dilatando un poco la máscara para que el follaje ralo de una misma pieza
quede unido), recorta cada grupo con el alfa **original** y borra lo que se cuele
de la pieza vecina dentro de la misma caja. Salen 11 piezas, de `p01` a `p11`.

Las que usa la página:

| Pieza | Qué es | Dónde se usa |
|-------|--------|--------------|
| `p01` | Guirnalda larga con lazo central | Cuelga bajo la barra, sobre la portada |
| `p04` | Corona grande | Fondo tenue de la franja navideña |
| `p06` | Lazo chico | Delante de la etiqueta «Navidad 2026» |
| `p09` | Cinta con lazo | Separa el mosaico de «Los personajes» |
| `p10` | Ramo con lazo | Encima del título de la franja |
| `p11` | Guirnalda con dos lazos | Remate al pie de la franja |

`p02`, `p03`, `p05`, `p07` y `p08` están extraídas y guardadas, pero la página no
las carga todavía. Quedan ahí para cuando hagan falta.

> La guirnalda anterior era una foto de Unsplash. Se quitó al llegar este pliego,
> que es material propio y además va en los colores de la marca.

## El resto

- `disco-ball`, `pluma`, `rosa`, `tambora`: fotos propias de CC Entertainment.
- `assets/img/navidad-personajes/*`: recortes de la sesión de estudio navideña
  (`assets/img/tematicas/navidad/`), generados con `tools/retratos.py`.
