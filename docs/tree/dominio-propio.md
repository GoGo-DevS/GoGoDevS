# Tree con dominio propio: cómo servir `tunegocio.cl` sin que se vea gogodevs.cl

Investigación del 11-11-2026. Nada de esto está hecho: no se crearon cuentas, no
se compró nada y no se tocó ningún DNS. Es para que Diego elija.

## El problema

El Tree del cliente vive en `https://www.gogodevs.cl/t/<slug>/` (lo genera
`_tree/generar.py`). El plan de dominio propio promete que el cliente lo vea en
`tunegocio.cl`, sin GoGoDevS a la vista, con el dominio a su nombre y pagado
directo a NIC Chile.

Lo que condiciona las opciones:

- El DNS de gogodevs.cl **no** está en Cloudflare: está en VtoSur
  (`ns1/ns2.vsur2.vtosur.cl`), y el sitio es estático por FTP en un hosting
  compartido con DirectAdmin.
- NIC Chile registra el dominio, pero para que `tunegocio.cl` muestre algo hay
  que delegarlo a servidores de nombre de algún proveedor de DNS.
- El correo con dominio (parte del pack "Presencia sin web") ya se hace con
  Cloudflare Email Routing + Gmail en una cuenta de Cloudflare **a nombre del
  cliente** (memoria `correo-clientes-cloudflare-brevo`). Esa cuenta necesita
  que el dominio esté en Cloudflare.
- El Tree generado ya está preparado para el dominio propio: con
  `"plan": "dominio_propio"` usa rutas relativas para lo suyo (logo, foto) y
  URL absolutas de gogodevs.cl para lo compartido (medición, política), y no
  muestra el crédito de GoGoDevS.

## Opciones

| | Opción | Costo | Alta por cliente | Mantención | Pega con la regla "a nombre del cliente" |
|---|---|---|---|---|---|
| **A** | **Worker de Cloudflare en la cuenta del cliente** que hace de proxy hacia `/t/<slug>/` | $0 (Workers gratis: 100.000 peticiones al día, 10 ms de CPU por petición) | 20 a 30 min la primera vez | Casi nada: el script no cambia; los cambios del Tree llegan solos desde gogodevs.cl | Sí: dominio, DNS y Worker en la cuenta del cliente |
| B | Cloudflare for SaaS (custom hostnames) en una zona de GoGoDevS | 100 hostnames gratis, después USD 0,10 al mes c/u | 5 min (el cliente agrega un CNAME) | Un solo Worker central con la tabla dominio → slug | No del todo: el tráfico pasa por una cuenta de GoGoDevS |
| C | Dominio adicional en el hosting de VtoSur (DirectAdmin) + regla en `.htaccess` por dominio | $0 si el plan admite más dominios (revisar con VtoSur) | 20 min (panel + SSL + commit del `.htaccess`) | Cada dominio en el panel de GoGoDevS; SSL por dominio | No: el DNS del cliente queda dentro del hosting de GoGoDevS |
| D | Hosting estático aparte (Cloudflare Pages o GitHub Pages) con una copia del Tree | $0 | 20 min | Alta: cada cambio de plantilla o de skin hay que volver a subirlo cliente por cliente | Depende de la cuenta |
| E | Plan B: redirección 301 de `tunegocio.cl` a `gogodevs.cl/t/<slug>/` | $0 | 10 min | Ninguna | Sí, pero **se ve gogodevs.cl** en la barra |

Detalles que pesan:

- **B** exige una zona de GoGoDevS en Cloudflare: mover el DNS de gogodevs.cl a
  Cloudflare o comprar un dominio aparte para esto. Además el dominio raíz
  (`tunegocio.cl` sin www) no se puede apuntar en los planes Free, Pro ni
  Business (el "apex proxying" es un extra de Enterprise), así que el cliente
  igual necesita un DNS propio para redirigir la raíz al www. Conviene recién
  con muchos clientes (30 o más), cuando administrar 30 cuentas de Cloudflare
  pese más que la dependencia central.
- **C** choca con el correo: si el DNS del cliente vive en VtoSur, no puede usar
  Cloudflare Email Routing, que es el modelo de correo vigente. Y si el cliente
  se va, hay que sacarle el DNS del hosting de GoGoDevS.
- **D** duplica el Tree: el día que se mejore la plantilla o la medición, hay
  que actualizar cada copia a mano.
- **E** no cumple lo que se vende ("sin GoGoDevS a la vista"). Sirve si el
  cliente solo quiere que su dominio lleve a su Tree y no le importa la barra.
  En ese caso se cobra como el plan de gogodevs.cl, no como dominio propio.

## Recomendación: opción A (Worker en la cuenta del cliente)

1. **$0 de costo recurrente** para GoGoDevS, coherente con el precio
   (0,5 UF/año).
2. **Todo a nombre del cliente**: el dominio en NIC Chile, el DNS y el Worker en
   su cuenta de Cloudflare. Igual que la regla de infraestructura de las
   propuestas.
3. **La misma cuenta sirve para el correo** del pack: Email Routing vive en esa
   zona. Una sola alta para Tree con dominio + correo.
4. **Cero mantención por cliente**: el Worker solo reenvía. Cuando se regenera
   el Tree en gogodevs.cl, el dominio del cliente lo muestra solo (con un caché
   de 5 minutos).
5. **SSL automático**: al agregar el dominio al Worker, Cloudflare crea el
   registro DNS y el certificado.

El script está en `docs/tree/worker-tree.js` y se probó con Node contra el
servidor local, con 8 casos: portada, logo, www → raíz con 301, intento de salir
de la carpeta (404), archivo inexistente (404 propio, sin la página de error de
GoGoDevS) y POST (405).

### Qué tendría que hacer Diego, por cliente (la primera vez, unos 30 min)

1. **Dominio**: que el cliente lo registre a su nombre en NIC Chile (lo paga
   él). Guía para mandarle: `/blog/registrar-dominio-cl-nic-chile/`.
2. **Cuenta de Cloudflare a nombre del cliente** (plan Free), con su correo. Si
   Diego la crea con el cliente al lado, que el cliente agregue a
   `contacto@gogodevs.cl` como miembro para poder administrarla. Revisar al
   hacer el primero que la cuenta gratis permite miembros.
3. **Agregar el dominio** a Cloudflare (Add a site → Free) y copiar los dos
   servidores de nombre que entrega.
4. **En NIC Chile**, cambiar los servidores de nombre del dominio por los de
   Cloudflare (lo hace el titular, o Diego con su acceso). Puede tardar unas
   horas en propagarse.
5. **Crear el Worker** (Workers & Pages → Create → Hello World), pegar
   `docs/tree/worker-tree.js` y cambiar `SLUG` por el del cliente. Deploy.
6. **Settings → Domains & Routes → Add → Custom domain**: `tunegocio.cl` y
   también `www.tunegocio.cl` (el script redirige el www a la raíz).
7. **Probar**: abrir `https://tunegocio.cl` en el celular, revisar que no se vea
   GoGoDevS y tocar el botón de WhatsApp.
8. En el JSON del negocio: `"plan": "dominio_propio"` y `"dominio": "tunegocio.cl"`,
   regenerar y publicar (`docs/tree/alta.md`).

Si después compra la web: el dominio ya es suyo; se borra el Worker y el
dominio apunta a la web nueva, donde el Tree pasa a ser su `/links/`.

## Decisiones pendientes de Diego

1. **Aprobar la opción A**, o elegir otra.
2. **¿Cuenta de Cloudflare del cliente o de GoGoDevS?** La recomendación es la
   del cliente (regla de infraestructura y correo). La de GoGoDevS es más cómoda
   para administrar, pero deja la infraestructura del cliente en manos de
   GoGoDevS.
3. **¿Indexar el dominio propio en Google?** Hoy todos los Tree van con
   `noindex, follow`, para no llenar gogodevs.cl de páginas delgadas. En el
   dominio propio podría convenirle al cliente aparecer cuando lo buscan por su
   nombre. Se puede hacer: el Worker cambia el `noindex` por `index` con
   `HTMLRewriter` solo en su dominio, y la copia de gogodevs.cl sigue con
   `noindex`. No está hecho.
4. **Privacidad en el dominio propio**: el aviso de cookies enlaza a la política
   de gogodevs.cl, porque la medición va a la propiedad GA4 de GoGoDevS
   (parámetro `negocio`). Con la Ley 21.719 vigente desde el 01-12-2026,
   conviene que la política diga que GoGoDevS mide los Tree de sus clientes
   como encargado, o que cada Tree con dominio propio tenga su `politica_url`.
5. **El plan B (redirección)**: si se ofrece, a qué precio. La propuesta es el
   del plan de gogodevs.cl (0,5 UF), porque no oculta GoGoDevS.

## Fuentes revisadas (11-11-2026)

- Límites de Workers: https://developers.cloudflare.com/workers/platform/limits/
- Custom domains de Workers: https://developers.cloudflare.com/workers/configuration/routing/custom-domains/
- Planes de Cloudflare for SaaS: https://developers.cloudflare.com/cloudflare-for-platforms/cloudflare-for-saas/plans/
