# Alta de un GoGoDevS Tree (negocio sin web)

Meta: **15 minutos de trabajo** desde que el cliente mandó sus datos hasta el
commit. El plan de dominio propio suma unos 30 minutos la primera vez
(`docs/tree/dominio-propio.md`).

Precios (memoria `precios-en-uf`, 11-11-2026): en gogodevs.cl 0,5 UF + 0,5 UF
al año desde que se publica · con dominio propio 1 UF + 0,5 UF al año (el
dominio a nombre del cliente, pagado directo a NIC Chile) · skin extra 0,25 UF
· pack Presencia sin web 3 UF.

## Antes de empezar (lo pide Diego por WhatsApp)

- Nombre del negocio (hasta 40 caracteres) y una frase de lo que vende (hasta 140).
- Logo cuadrado (PNG, SVG o WebP). Si no tiene, van sus iniciales en un círculo de su color.
- Color principal (el de su marca, en `#RRGGBB`).
- Los enlaces: número de WhatsApp y el mensaje con que quiere que le escriban,
  Instagram, catálogo, ubicación en Google Maps, reseñas, etc. (hasta 8).
- Horario, si quiere mostrarlo.
- Plan (gogodevs.cl o dominio propio) y skin (base, oscura o foto). Para la
  skin de foto: una foto horizontal del negocio.
- El pago registrado en el CRM (`core.Pago`), con la renovación anual a la fecha de publicación.

## Pasos

| # | Paso | Tiempo |
|---|---|---|
| 1 | Elegir el slug (minúsculas y guiones, ej. `barberia-don-luis`). Es la dirección: `gogodevs.cl/t/barberia-don-luis/`. | 1 min |
| 2 | Logo a WebP cuadrado, 512 px, bajo 200 KB (comando abajo) en `_tree/negocios/<slug>/logo.webp`. Igual para `fondo.webp` si la skin es foto (1200 px de ancho). | 2 min |
| 3 | Copiar `_tree/negocios/ejemplo.json` a `_tree/negocios/<slug>.json`, **borrar `aviso`** (es solo para la muestra) y completar con los datos del cliente. En `nota`, la fecha de pago y de renovación. | 5 min |
| 4 | `python _tree/generar.py`. Si algo está mal (color sin contraste, enlace sin https, WhatsApp sin código de país), lo dice con el arreglo. | 1 min |
| 5 | Mirarlo: `python -m http.server 8000` en la raíz y abrir `http://127.0.0.1:8000/t/<slug>/` en vista de celular. Tocar cada botón. | 3 min |
| 6 | Mandarle la captura al cliente para que apruebe. | (espera) |
| 7 | `python _blog/verificar.py`, que tiene que decir `OK: sin errores`. | 1 min |
| 8 | Commit con rutas explícitas: `git add _tree/negocios/<slug>.json _tree/negocios/<slug>/ t/<slug>/` y `git commit -m "tree: <negocio>"`. | 1 min |
| 9 | Publicar (`git push origin main`, que despliega solo por FTP) y abrir `https://www.gogodevs.cl/t/<slug>/` en el celular. | 1 min |

Comando para el logo (Pillow):

    python -c "from PIL import Image; im=Image.open('logo-original.png').convert('RGBA'); im.thumbnail((512,512)); im.save('_tree/negocios/<slug>/logo.webp', quality=85)"

## Campos del JSON

| Campo | Obligatorio | Qué es |
|---|---|---|
| `plan` | no (`gogodevs`) | `gogodevs` o `dominio_propio` |
| `dominio` | con dominio propio | `tunegocio.cl` |
| `credito_gogodevs` | no | En `gogodevs` va siempre en `true`. En dominio propio va en `false` por defecto (sin GoGoDevS a la vista). |
| `nombre` | sí | Hasta 40 caracteres. Es el título de la página. |
| `descripcion` | sí | Hasta 140 caracteres. |
| `logo` | no | Nombre del archivo en `_tree/negocios/<slug>/`. Sin logo, van las iniciales. |
| `colores.principal` | sí | `#RRGGBB`. El texto encima se elige solo (blanco o negro); si ninguno llega a contraste 4,5, el generador lo rechaza. |
| `colores.fondo` | no | Solo en la skin base. Si no se indica, es un tinte claro del principal. |
| `skin` | no (`base`) | `base`, `oscura` o `foto`. |
| `fondo` | con skin foto | `fondo.webp` en la carpeta del negocio. |
| `horario` | no | Hasta 50 caracteres. |
| `botones` | sí | De 1 a 8. Cada uno: `texto` (hasta 48), `detalle` (opcional), `icono` y UNO de `url` (https), `whatsapp` (`{"numero": "569...", "mensaje": "..."}`), `telefono` (`+569...`) o `correo`. Uno solo puede llevar `"destacado": true`. |
| `politica_url` | no | Política de privacidad propia del cliente (https). |
| `aviso` | no | Franja de arriba. Solo para los Tree de muestra. |
| `nota` | no | Notas internas: no se publican. |

Iconos: whatsapp, instagram, facebook, tiktok, youtube, mapa, catalogo, tienda,
carta, calendario, estrella, web, telefono, correo, enlace.

## Cambios, renovación y baja

- **Cambio de enlaces o colores**: se edita el JSON, `python _tree/generar.py`,
  verificar, commit y push. Nunca se edita `t/` a mano: `verificar.py` lo rechaza.
- **Renovación anual**: recordatorio en el CRM a la fecha de publicación.
- **Baja** (no renovó): borrar `_tree/negocios/<slug>.json`, su carpeta y
  `t/<slug>/`, correr `python _tree/generar.py` y `verificar.py`, y commit. Si
  tenía dominio propio, avisarle que el dominio sigue siendo suyo y borrar el
  Worker de su cuenta de Cloudflare.

## Medición

Cada botón manda a GA4 (propiedad de gogodevs.cl) el evento `tree_click` con
`destino`, `texto_boton` y `negocio` (el slug). Solo se mide a quien acepta las
cookies. Para leer `negocio` en los informes hay que registrarlo una vez como
dimensión personalizada de evento en GA4 (como ya están `destino` y
`texto_boton`). El indicador para el cliente: de cada 100 que abren su Tree,
cuántos tocan WhatsApp.
