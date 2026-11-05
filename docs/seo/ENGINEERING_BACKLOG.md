# Backlog de ingeniería SEO — gogodevs.cl

La estrategia define las prioridades y el agente de ingeniería las implementa
**solo cuando Diego aprueba cada ítem**. La evidencia de cada problema está en
`SEO_AUDIT.md`.

## Reglas para quien implementa

1. **Commit sí, push no.** El push despliega por FTP; lo hace Diego.
2. **Los artículos se editan en `_blog/programados/`, no en `blog/`.** `publicar.py` regenera todo. Después se corre `python _blog/verificar.py` y se restaura `_blog/__pycache__/publicar.cpython-313.pyc`.
3. **Ventanas de medición abiertas.** Las URLs tocadas el 30-10, 02-11, 03-11 y 04-11 se miden el **16-11** y el **01-12**. Hasta esa fecha no se cambia su title, su H1 ni su description, **salvo los ítems P0**: lo legal y comercial pesa más que la medición. Si se toca una de esas URLs, se anota la fecha en `SEO_ROADMAP_90_DAYS.md`.
   Las URLs en medición son: home, /servicios/desarrollo-web/, /servicios/mantencion-web/, /servicios/integraciones/, /servicios/ecommerce/, /servicios/seo-tecnico/, /paginas-web-maipu/, /paginas-web-santiago/, los 2 rubros, y los artículos de mantención, Mercado Pago, catálogo y autoadministrable.
4. **Cada criterio de aceptación tiene una prueba**, y la prueba se comprueba **al revés**: con el cambio deshecho, tiene que fallar.
5. Nada de dependencias nuevas sin justificarlo en el ítem. Nada de secretos en el repo.

## Estado

| ID | Título | Prioridad | Depende de | Estado |
|---|---|---|---|---|
| ENG-01 | Oferta de mantención coherente (sin hosting incluido) | P0 | Texto aprobado por Diego | Pendiente de decisión |
| ENG-02 | Leads medidos de punta a punta | P0 | Autorización de Diego para un envío de prueba | Pendiente |
| ENG-03 | Entidad: página "Sobre", Diego como Person y schema unificado | P1 | Contenido y foto de Diego | Pendiente de contenido |
| ENG-04 | Plantilla de caso con datos y guarda de permiso | P1 | — | Listo para implementar |
| ENG-05 | Indexación de páginas comerciales y ritmo del blog | P1 | Decisión de ritmo (Diego) | Pendiente de decisión |
| ENG-06 | Fuentes servidas desde el sitio (CLS de los artículos y bloqueo de renderizado) | P2 | — | Listo |
| ENG-07 | LCP de la home: imagen del hero descubrible | P2 | — | Listo |
| ENG-08 | Caché de recursos estáticos | P2 | Confirmar nginx del hosting | Listo para probar |
| ENG-09 | Página 404 propia | P3 | — | Listo |
| ENG-10 | Quitar el marcado oculto del Cyber de octubre | P2 | Decisión de Diego | Pendiente de decisión |
| ENG-11 | Higiene de URLs (/index.html, /links/, /herramientas/) | P3 | — | Listo |
| ENG-12 | `lastmod` real en el sitemap | P3 | — | Listo |
| ENG-13 | Detalles on-page y de accesibilidad | P3 | Después del 01-12 para las URLs en medición | Listo |
| ENG-14 | Que el servicio se quede con "mantención web" | P1 | ENG-01 y medición del 16-11 | Bloqueado |
| ENG-15 | Core Web Vitals de campo hacia GA4 (opcional) | P3 | Decisión: suma una dependencia | Propuesto |

---

## ENG-01 — Oferta de mantención coherente · P0

- **Problema:** el sitio promete que la mantención incluye el hosting "pagado y administrado". Los Términos dicen que el dominio y el hosting van a nombre del cliente y son de su costo. La regla del 03-11 de Diego lo prohíbe.
- **Evidencia:** `SEO_AUDIT.md`, A-01:
  - /servicios/mantencion-web/: líneas 7, 20, 28, 167, 179, 201 y 215.
  - /servicios/: líneas 258 y 260.
  - /cuanto-cuesta-una-pagina-web-chile/: líneas 114, 275 y 457.
  - Menciones a revisar una por una en /paginas-web-maipu/, /paginas-web-santiago/, /blog/, y en los artículos de mantención (13), qué pedirle a una empresa (3), registrar dominio (4), cuánto cuesta una tienda, cuánto cuesta un sistema y página lenta.
- **Objetivo:** que ninguna página publique una oferta que el negocio no sostiene, y que la IA no la cite.
- **Requisito funcional:**
  - Reemplazar la oferta por el modelo de la regla del 03-11. La infraestructura (servidor, base de datos, correo y dominio) queda **a nombre del cliente** y se paga directo al proveedor, sin margen. Configurarla y monitorearla es parte de la mantención.
  - La mantención comienza al publicar, se cobra aparte y en UF.
  - Incluye monitoreo, respaldos, actualizaciones de seguridad, correcciones y pequeños ajustes. Las fallas críticas se atienden en 24 horas hábiles.
  - **El texto literal lo aprueba Diego.** La base está en la memoria `propuestas-hosting-y-dominio-nunca-regalados.md`.
  - Actualizar también la meta description, `og:description`, `twitter:description` y las respuestas de FAQPage en el JSON-LD, idénticas a lo visible.
  - Los artículos se editan en `_blog/programados/`.
- **Archivos:** los de la evidencia, más sus fuentes en `_blog/programados/`.
- **Criterios de aceptación:**
  1. 0 apariciones en el HTML público de: "hosting pagado", "No tienes que pagar ni renovar el hosting", "hosting incluido", "dominio incluido", "primer año", "a partir del segundo año", "hosting gratis" y "sin costo de servidor".
  2. Cada mención restante de "hosting" o "dominio" queda en una tabla en el mensaje del commit, con la URL y por qué es coherente con los Términos.
  3. Las respuestas de FAQPage coinciden con el texto visible.
  4. `verificar.py` queda en verde.
- **Validación:** sumar a `verificar.py` una guarda que falle si aparece cualquiera de las frases prohibidas. Comprobarla al revés restaurando la versión vieja de /servicios/mantencion-web/.
- **Riesgo:** bajo en lo técnico. En lo comercial, cambia lo que se le dice a quien ya leyó la oferta: revisar si algún cliente activo contrató creyendo que el hosting venía incluido.
- **Dependencias:** el texto aprobado por Diego. El artículo `_blog/en-pausa/2026-11-06-hosting-para-pagina-web-chile.html` sigue pausado hasta la misma decisión.

## ENG-02 — Leads medidos de punta a punta · P0

- **Problema:** la búsqueda orgánica no registra ningún evento clave en 90 días. Hubo 4 eventos `formulario_enviado_intento` y 0 `lead_formulario`. No se sabe si esos 4 envíos llegaron al correo.
- **Evidencia:** GA4, 90 días (`SEO_AUDIT.md`, A-02). El flujo es AJAX a `formsubmit.co/ajax/…` (`assets/js/main.js:241-283`), que dispara `gg:lead-formulario`, que `medicion.js:261` convierte en `lead_formulario`.
- **Objetivo:** cada cotización real se mide una sola vez y se puede atribuir a su canal. Sin esto el SEO no demuestra impacto comercial.
- **Requisito funcional:**
  1. Revisar en el código si `formsubmit.co` puede devolver `success` distinto de `"true"` estando activo. Por ejemplo, un formulario que nunca se confirmó desde el correo.
  2. **Prueba controlada, solo con autorización de Diego para esa corrida**, porque manda un correo real y dispara el Lead de Meta:
     - Un envío con el nombre "PRUEBA SEO <fecha>" y GA4 en modo depuración.
     - Resultado esperado: llega 1 correo, aparece 1 `lead_formulario` en DebugView y el formulario se limpia.
     - Anotar la fecha y hora para excluir la prueba de los informes de Meta y GA4.
  3. /cotizar/: confirmar si su formulario está cubierto. Si no lo está, agregar `lead_cotizador`, que se dispara solo cuando el envío se confirma.
  4. Agregar al formulario de contacto y al de cotización un campo opcional **"¿Cómo nos encontraste?"**, con las opciones Google, ficha de Google Maps, ChatGPT u otra IA, Instagram, LinkedIn, recomendación y otro. Va en el correo y como parámetro `origen_declarado` del evento.
  5. **Ningún dato personal** (nombre, correo o teléfono) viaja a GA4 ni a Meta.
  6. **Diego, en GA4 Admin:**
     - Marcar `lead_formulario` y `lead_cotizador` como eventos clave.
     - Agregar `formsubmit.co` a "Referencias no deseadas".
     - Revisar el filtro de tráfico interno.
- **Archivos:** `assets/js/main.js`, `assets/js/medicion.js`, `contacto/index.html`, `cotizar/index.html`, `assets/js/cotizador.js`.
- **Criterios de aceptación:**
  1. Un envío confirmado produce exactamente 1 evento de lead. Recargar la página no produce otro.
  2. Un envío fallido produce 0 leads y sigue ofreciendo el respaldo a WhatsApp.
  3. Sin consentimiento, no se manda ningún evento (Ley 21.719, tal como está hoy).
  4. Los parámetros no traen datos personales.
- **Validación:** una prueba en el navegador (Playwright) con `formsubmit.co` **simulado**, que cubra éxito, fallo y recarga, contando las llamadas a `gtag`. La prueba se comprueba al revés quitando el `dispatchEvent`. Después, la prueba real del punto 2.
- **Riesgo:** medio. La prueba real escribe en Meta y GA4. Sin la prueba simulada, un arreglo podría duplicar leads e inflar las campañas.
- **Dependencias:** la autorización de Diego para la corrida real.

## ENG-03 — Entidad: página "Sobre", Diego como Person y schema unificado · P1

- **Problema:** /sobre-gogodevs/ no nombra a nadie ("liderada por un Ingeniero en Informática") y Google no la indexa. El `sameAs` de Organization incluye el LinkedIn personal de Diego. ProfessionalService es un nodo aparte, sin `@id`. El autor de los artículos enlaza a LinkedIn y no a una página del sitio.
- **Evidencia:** `SEO_AUDIT.md`, A-05 y A-13.
- **Objetivo:** que Google y las IA entiendan quién es GoGoDevS, quién hace el trabajo y dónde están sus perfiles oficiales. También ayuda a separar la marca de "GOGODEV".
- **Requisito funcional:**
  1. **Contenido** (lo entrega o aprueba Diego):
     - Nombre, foto real, formación, desde cuándo hace proyectos.
     - Proyectos entregados, con la cifra del CRM.
     - Casos con enlace.
     - La razón social, que ya es pública en el pie.
     - Cómo trabaja, contacto y perfiles.
  2. **Schema:**
     - Un solo nodo `@id: https://www.gogodevs.cl/#organization`, con el tipo `ProfessionalService` (subtipo de Organization). Fusiona las propiedades que hoy están repartidas y saca el LinkedIn personal de su `sameAs`.
     - Agregar `founder: {"@id": "https://www.gogodevs.cl/sobre-gogodevs/#diego"}`.
     - En /sobre-gogodevs/, un nodo `Person` con ese `@id`: name, jobTitle, image, `worksFor` (la organización) y `sameAs` (su LinkedIn personal).
  3. **Plantilla del blog:**
     - `author: {"@id": ".../sobre-gogodevs/#diego", "name": "Diego Dinamarca", "url": "https://www.gogodevs.cl/sobre-gogodevs/"}`.
     - Una firma visible en cada artículo que enlace a /sobre-gogodevs/.
  4. Diego confirma que cada URL de `sameAs` es suya: Instagram, LinkedIn de la empresa, TikTok, YouTube @gogodevs y Facebook.
- **Archivos:** `sobre-gogodevs/index.html`, `index.html` (schema), el `<head>` común si el schema se repite, `_blog/plantilla_articulo.html` y `_blog/publicar.py`.
- **Criterios de aceptación:**
  1. El validador de Schema.org da 0 errores en la home, en /sobre-gogodevs/ y en un artículo.
  2. La Prueba de resultados enriquecidos reconoce la organización y el logo.
  3. Cada dato del schema aparece visible en la página.
  4. La página tiene al menos 600 palabras de contenido propio *(guía, no una meta de SEO)*.
- **Validación:** sumar a `verificar.py` una guarda que exija que `author` apunte a `#diego` en todos los artículos y que el `sameAs` de la organización no contenga `linkedin.com/in/`. Comprobarla al revés.
- **Riesgo:** bajo. La foto tiene que ser real: nada de imágenes de IA.
- **Dependencias:** el contenido de Diego.

## ENG-04 — Plantilla de caso con datos y guarda de permiso · P1

- **Problema:** los casos tienen entre 342 y 591 palabras y casi no traen datos verificables. Es la brecha principal frente a la competencia.
- **Evidencia:** `SEO_AUDIT.md`, A-06, y `SEO_COMPETITORS.md`.
- **Objetivo:** fichas de caso con información propia que se pueda citar, **sin publicar nada que el cliente no haya autorizado**.
- **Requisito funcional:**
  - Un bloque HTML reutilizable con las secciones de `SEO_CONTENT_PLAN.md`, sección 4: cliente, problema, qué se hizo, plazo y tramo, stack, resultado medido, qué no salió bien y llamada a la acción.
  - Clases CSS dentro del sistema visual actual.
  - Todo bloque de resultado o de cita del cliente lleva `data-permiso="AAAA-MM-DD"`, con la fecha del permiso escrito.
- **Archivos:** `proyectos/*/index.html`, `assets/css/style.css`, `_blog/sitio_comun.py` (si arma partes comunes de los casos), `_blog/verificar.py`.
- **Criterios de aceptación:**
  1. `verificar.py` falla si un caso tiene un bloque de resultado o de cita sin `data-permiso`.
  2. Los casos existentes no cambian de URL.
  3. Se ven bien a 390 y a 1440 px.
- **Validación:** la guarda comprobada al revés y capturas en escritorio y celular.
- **Riesgo:** bajo en lo técnico. El riesgo real es publicar un dato sin permiso, y la guarda lo frena.
- **Dependencias:** ninguna para la plantilla. El contenido de cada caso depende de cada cliente.

## ENG-05 — Indexación de páginas comerciales y ritmo del blog · P1

- **Problema:** 23 de 68 URLs no están indexadas, entre ellas /servicios/automatizacion-de-procesos/, /sobre-gogodevs/, /contacto/, /paginas-web-santiago/ y los 2 rubros. Se publica un artículo al día con indexación baja.
- **Evidencia:** `SEO_AUDIT.md`, A-03 y A-04.
- **Objetivo:** que las páginas que venden estén indexadas, y que el rastreo no se diluya en piezas sin información propia.
- **Requisito funcional:**
  1. **Diego**, en Search Console > Inspección de URLs: solicitar la indexación de las 6 páginas comerciales, unas pocas por día porque hay cuota.
  2. **Enlaces contextuales**, no solo en el pie, hacia esas 6 páginas desde páginas indexadas que se rastrean seguido: home, /servicios/, /servicios/integraciones/ y el artículo de Mercado Pago. Para la home y las URLs en medición esto va **después del 16-11**. /servicios/ no está en medición y puede ir ya.
  3. **Ritmo del blog**, cuando Diego lo decida. Cambiar las fechas de los archivos de `_blog/programados/` a dos por semana; por ejemplo, martes y viernes. `publicar.py` es idempotente y publica lo vencido. Verificar que ninguno quede con fecha pasada sin querer.
- **Archivos:** `servicios/index.html`, `index.html`, `servicios/integraciones/index.html`, `_blog/programados/*`.
- **Criterios de aceptación:**
  1. El calendario de `_blog/programados/` no tiene más de 2 fechas por semana.
  2. Las 6 páginas reciben al menos un enlace contextual desde una página indexada.
  3. Indicador de seguimiento (no es una promesa): estado de las 6 en la API de inspección, el 01-12 y el 15-12.
- **Validación:** `verificar.py` en verde y un script que cuente las fechas por semana.
- **Riesgo:** bajo.
- **Dependencias:** la decisión de ritmo de Diego (`SEO_CONTENT_PLAN.md`, sección 1).

## ENG-06 — Fuentes servidas desde el sitio · P2

- **Problema:** Google Fonts (Montserrat 400/600/700/900) bloquea el renderizado unos 765 ms en todas las páginas. En los artículos, el cambio de fuente mueve el título y la imagen: CLS de 0,284 en laboratorio.
- **Evidencia:** Lighthouse del 05-11 (`SEO_AUDIT.md`, A-08 y A-10).
- **Objetivo:** CLS bajo y una carga más rápida. De paso, no se envía la IP del visitante a Google Fonts, coherente con la Ley 21.719.
- **Requisito funcional:**
  - Servir Montserrat en WOFF2 desde `/assets/fonts/`, con el subconjunto latino. La licencia OFL lo permite.
  - Reducir los pesos a los que se usan de verdad (revisar el CSS).
  - `@font-face` con `font-display: swap` y una fuente de respaldo con métricas ajustadas (`size-adjust`, `ascent-override`), o `font-display: optional`.
  - `preload` solo para el peso del texto principal.
  - Quitar `fonts.googleapis.com` y `fonts.gstatic.com` de los 71 HTML y de las plantillas del blog.
- **Archivos:** el `<head>` de todos los HTML (con un script), `_blog/plantilla_articulo.html`, `_blog/plantilla_indice.html`, `assets/css/style.css`, `assets/fonts/` (nuevo).
- **Criterios de aceptación:**
  1. Ninguna petición a `fonts.googleapis.com` ni a `fonts.gstatic.com`.
  2. Lighthouse móvil, mediana de 3 corridas: CLS ≤ 0,1 en 3 artículos distintos.
  3. FCP sin empeorar en la home ni en /servicios/desarrollo-web/.
  4. Las capturas antes y después no muestran cambio visual de la tipografía.
- **Validación:** Lighthouse, capturas con Playwright, y `grep -r "fonts.googleapis" --include=*.html .` igual a 0.
- **Riesgo:** medio-bajo, porque toca todas las páginas. Hacerlo en un commit propio y reversible.
- **Dependencias:** ninguna.

## ENG-07 — LCP de la home: imagen del hero descubrible · P2

- **Problema:** el LCP de la home es de 3,1 s en laboratorio. El elemento LCP es `.hero-home__bg`, cuya imagen va en una variable CSS (`--hero-photo: url('/assets/img/home-hero-bg.webp')`): el navegador la descubre tarde y sin prioridad.
- **Evidencia:** Lighthouse del 05-11, `lcp-discovery-insight` (`SEO_AUDIT.md`, A-09).
- **Objetivo:** LCP ≤ 2,5 s en laboratorio. Es el umbral bueno de campo.
- **Requisito funcional:** `<link rel="preload" as="image" href="/assets/img/home-hero-bg.webp" fetchpriority="high">` en el `<head>` de `index.html`, con `imagesrcset` si existe una versión para celular; si no existe, evaluar crearla. La alternativa es un `<img fetchpriority="high">` con `object-fit`.
- **Archivos:** `index.html`, `assets/css/style.css` y, si hace falta, `assets/img/`.
- **Criterios de aceptación:**
  1. Lighthouse móvil, mediana de 3 corridas: LCP ≤ 2,5 s.
  2. `lcp-discovery-insight` sin advertencias.
  3. Sin cambio visual.
- **Validación:** Lighthouse y capturas.
- **Riesgo:** bajo. La home está en medición, pero esto no toca el title, el H1 ni el texto, así que puede ir ya.
- **Dependencias:** ninguna.

## ENG-08 — Caché de recursos estáticos · P2

- **Problema:** `/assets/*` (CSS, JS e imágenes) se sirve sin `Cache-Control` ni `Expires`; solo con ETag y Last-Modified.
- **Evidencia:** curl del 05-11 (`SEO_AUDIT.md`, A-11).
- **Objetivo:** que las visitas que vuelven no revaliden cada recurso.
- **Requisito funcional:**
  - Con `mod_expires` y `mod_headers` en `.htaccess`:
    - CSS y JS versionados con `?v=`: `Cache-Control: public, max-age=31536000, immutable`.
    - Imágenes y fuentes: `max-age=2592000` (30 días).
    - HTML: `no-cache`.
  - Antes, comprobar que **todas** las referencias a CSS y JS llevan `?v=`.
  - **Comprobar si el nginx que está delante respeta el `.htaccess`** para los estáticos. Si no lo respeta, se configura en el panel del hosting (VtoSur, DirectAdmin) y eso lo hace Diego.
- **Archivos:** `.htaccess` y, si hace falta, las referencias sin versión.
- **Criterios de aceptación:**
  1. `curl -sI https://www.gogodevs.cl/assets/css/style.css?v=…` muestra el `Cache-Control` esperado.
  2. Una imagen muestra `max-age=2592000`.
  3. El HTML muestra `no-cache`.
- **Validación:** curl después del despliegue, que hace Diego.
- **Riesgo:** medio. Si un CSS o JS cambia sin cambiar su `?v=`, el visitante ve la versión vieja hasta un año. Regla: cada cambio de CSS o JS sube su versión; `verificar.py` puede comprobarlo comparando el hash del archivo con su `?v=`.
- **Dependencias:** confirmar el comportamiento del nginx.

## ENG-09 — Página 404 propia · P3

- **Problema:** se ve la 404 por defecto de Apache. El servidor ya intenta usar un ErrorDocument que no existe.
- **Evidencia:** el cuerpo de la respuesta en vivo (`SEO_AUDIT.md`, A-15).
- **Requisito funcional:**
  - `404.html` en la raíz, con la cabecera y el pie del sitio.
  - H1 "No encontramos esta página" y enlaces a /servicios/, /proyectos/, /cuanto-cuesta…/ y /contacto/.
  - `<meta name="robots" content="noindex">`.
  - `ErrorDocument 404 /404.html` en `.htaccess`.
  - Queda fuera del sitemap, y `verificar.py` no la exige ahí.
- **Criterios de aceptación:** `curl -s -o /dev/null -w "%{http_code}" https://www.gogodevs.cl/no-existe/` devuelve **404** (nunca 200), y el cuerpo contiene "No encontramos esta página".
- **Riesgo:** bajo. Cuidado con que la respuesta no pase a 200 (sería un *soft 404*).

## ENG-10 — Quitar el marcado oculto del Cyber de octubre · P2

- **Problema:** casi todas las páginas conservan elementos `data-cyber` con `hidden`, con precios de campaña y el texto "Hasta el lunes 12". Por ejemplo, 31 en /cuanto-cuesta…/ y 15 en /servicios/desarrollo-web/.
- **Evidencia:** `SEO_AUDIT.md`, A-12.
- **Objetivo:** que ningún rastreador que lea el HTML crudo, como el de una IA, tome un precio que no rige (criterio G-01).
- **Requisito funcional:** si Diego confirma que no hay campaña activa, quitar los elementos `data-cyber` y la carga de `assets/js/cyber.js`. El código queda en el historial de git para la próxima campaña. Si se quiere conservar el mecanismo, los precios de la campaña salen del HTML y se inyectan solo mientras dure.
- **Criterios de aceptación:** `grep -rl "data-cyber" --include=index.html .` devuelve 0 archivos (o ninguno con texto de precio), y "Hasta el lunes" no aparece en el HTML público.
- **Riesgo:** bajo. Revisar que el CSS no dependa de esos elementos.
- **Dependencias:** la decisión de Diego. Ver la memoria `campana-cyber-gogodevs`.

## ENG-11 — Higiene de URLs · P3

- **Requisito funcional:**
  1. 301 de `/index.html` y `/<ruta>/index.html` a la URL de directorio, con una condición `THE_REQUEST` para no crear un bucle.
  2. `/links/`: `<meta name="robots" content="noindex, follow">` y un canonical a sí misma. Es una página de enlaces para la biografía de Instagram.
  3. Excluir `^herramientas/` del `mirror` en `deploy.yml` y en `blog-diario.yml`, y agregar `RedirectMatch 404 ^/herramientas/`. El `--exclude` no borra el archivo que ya está en el servidor, y la regla lo tapa.
  4. Opcional: preguntar al hosting si `http://gogodevs.cl` puede ir en un solo salto a `https://www`. Hoy el primer salto lo hace el nginx.
- **Criterios de aceptación:**
  1. `/index.html` devuelve 301 a `/`.
  2. `/links/` trae `noindex`.
  3. `/herramientas/refrescar_resenas.py` devuelve 404.
  4. La home sigue respondiendo 200.
- **Riesgo:** bajo. Una regla de reescritura mal escrita puede crear un bucle: probar con curl todas las rutas del sitemap.

## ENG-12 — `lastmod` real en el sitemap · P3

- **Problema:** 26 URLs dicen 07-10, aunque hubo cambios de contenido después. Por ejemplo, /servicios/desarrollo-web/ cambió su title y su H1 el 03-11.
- **Requisito funcional:** que `lastmod` refleje la fecha del último cambio del **contenido principal** (`<main>`), no del pie común. Una forma posible: guardar un hash del `<main>` por URL y actualizar la fecha solo cuando ese hash cambia, desde `sitio_comun.py --aplicar`.
- **Criterios de aceptación:** en 5 URLs elegidas al azar, `lastmod` coincide con la fecha del último commit que cambió su `<main>`.
- **Riesgo:** bajo.

## ENG-13 — Detalles on-page y de accesibilidad · P3

- **Requisito funcional:**
  - Títulos de ≤ 65 caracteres en /proyectos/fco-climatizacion/ (71), /proyectos/salon-amanda/ (71) y /proyectos/travesia-logistica/ (68). Los arma `sitio_comun.py`.
  - Description de ≤ 160 caracteres en /paginas-web-santiago/ (hoy 198). Va **después del 01-12**, porque la página está en medición.
  - En /proyectos/, cambiar el salto de H1 a H3 por un H2.
  - Accesibilidad según Lighthouse: contraste de color, `label-content-name-mismatch` (el `aria-label` tiene que contener el texto visible), `image-redundant-alt` y `link-in-text-block`.
- **Criterios de aceptación:**
  1. El script de auditoría no marca títulos de más de 65 caracteres ni descriptions de más de 160.
  2. Lighthouse de accesibilidad ≥ 98 en las 5 URLs de la línea base.
- **Riesgo:** bajo.

## ENG-14 — Que el servicio se quede con "mantención web" · P1 (bloqueado)

- **Problema:** unas 101 impresiones de "mantención web" (posición 10-20) caen en el artículo y no en la página de servicio.
- **Requisito funcional:**
  - **Después de ENG-01 y de la medición del 16-11:**
    - El title y el H1 del servicio contienen "Mantención web".
    - El artículo vuelve a la pregunta: "¿Qué incluye la mantención de una página web?".
  - El artículo enlaza al servicio con el texto "mantención web", y el servicio enlaza al artículo con el texto "qué incluye la mantención".
- **Criterios de aceptación:**
  1. Los títulos y H1 quedan según la especificación y los enlaces cruzados existen.
  2. Indicador de seguimiento a 4 semanas: qué URL muestra Search Console para "mantención web". No es una promesa.
- **Riesgo:** bajo-medio. Puede bajar temporalmente la posición del artículo.
- **Dependencias:** ENG-01 y el 16-11.

## ENG-15 — Core Web Vitals de campo hacia GA4 (opcional) · P3

- **Problema:** no hay datos de campo. CrUX no tiene volumen suficiente y PageSpeed sin clave responde 429.
- **Requisito funcional:** cargar la librería `web-vitals` (unos 2 KB, servida desde el propio sitio) y mandar LCP, INP y CLS a GA4 como eventos, **solo con consentimiento**.
- **Criterios de aceptación:** los eventos aparecen en DebugView con su valor, y nada se manda sin consentimiento.
- **Riesgo:** suma una dependencia y más eventos. **Decidir antes de implementar.**
