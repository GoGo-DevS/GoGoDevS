# Auditoría SEO de gogodevs.cl — 05-11-2026

Línea base y hallazgos con evidencia. Si un dato no se pudo medir, se dice.
Estrategia: `SEO_STRATEGY_CHILE.md`. Arreglos técnicos: `ENGINEERING_BACKLOG.md`.

## 0. Fuentes y acceso real

| Fuente | Acceso | Qué se usó |
|---|---|---|
| Search Console (`sc-domain:gogodevs.cl`) | Sí, por API, cuenta de servicio de solo lectura | Rendimiento de 90 días (05-08 a 02-11) y de 28 días (06-10 a 02-11), consulta × página, dispositivo y país |
| Inspección de URLs (API de Search Console) | Sí | Estado de indexación de las 68 URLs del sitemap, consultado el 05-11 |
| GA4 (propiedad 555307318) | Sí, por API de solo lectura | 90 días: canales, fuentes, eventos y landings orgánicas |
| Sitio en vivo | Sí (curl) | Códigos HTTP, redirecciones, cabeceras, 404 y archivos expuestos |
| Repositorio `GoGo-DevS/GoGoDevS` | Sí, `main` en `ef71d6c` | 71 HTML auditados con un script: metadatos, encabezados, schema, imágenes y enlaces |
| Core Web Vitals de campo (CrUX) | **No.** PageSpeed Insights respondió 429 (cuota sin clave) y el sitio probablemente no tiene tráfico suficiente para CrUX | — |
| Rendimiento de laboratorio | Sí, Lighthouse 12 local, móvil simulado, **una corrida por URL** | 5 URLs |
| Informe de IA generativa de Search Console, Bing Webmaster Tools, Clarity | **No revisados.** La API no los expone y no hay acceso a los paneles desde aquí | Tarea de Diego (roadmap, semana 1) |
| SERP de Google.cl | **No.** Google bloquea la navegación automatizada; se usó un buscador web desde EE. UU. | Ver los límites en `SEO_COMPETITORS.md` |

## 1. Línea base

### Search Console

| Ventana | Clics | Impresiones | Posición media |
|---|---|---|---|
| 90 días (05-08 a 02-11) | 17 | 2.065 | 9,9 |
| 28 días (06-10 a 02-11) | 4 | 1.192 | 10,1 |

- Chile: 1.720 de las 2.065 impresiones (90 días).
- Por dispositivo (90 días): escritorio 10 clics, 1.014 impresiones, posición 12,2; móvil 7 clics, 1.046 impresiones, posición 7,7.

**De dónde vienen las impresiones** (90 días, filas con la consulta visible, 1.178 impresiones):

| Tipo de consulta | Impresiones | % | Lectura |
|---|---|---|---|
| Marcas de clientes (medina 4x4, púas, AZA…) | 637 | 54 % | Esa gente busca al cliente, no a GoGoDevS. No es demanda propia |
| Prompts largos tipo asistente de IA ("¿qué plataforma de checkout conviene…? entrégame las URLs de Chile") | 217 | 18 % | Llegan a /servicios/integraciones/, /servicios/ecommerce/ y al artículo de Mercado Pago, en posición 6-10 |
| Consultas propias sin marca | 324 | 28 % | **0 clics en 90 días** |

**Consultas propias con más impresiones (90 días):**

| Grupo | Impresiones | Posición | Página que Google muestra |
|---|---|---|---|
| mantención web, mantención de páginas web y variantes (8 en total) | ~101 | 10-20 | El artículo del blog, no la página de servicio |
| sistemas a medida | 23 | 54 | /servicios/sistemas-a-medida/ |
| alternativa a webpay | 22 | 23 | Artículo de Mercado Pago |
| autoadministrable y variantes | ~42 | 20-53 | Artículo autoadministrable. También aparece /proyectos/puas-tatuajes/ en posición 74-84 (canibalización menor) |
| seo técnico chile | 12 | 18 | /servicios/seo-tecnico/ |
| mercado pago es webpay | 10 | 4,2 | Artículo de Mercado Pago |
| servicios de desarrollo web / desarrollo web empresarial / para empresas | 8 / 8 / 4 | 16 / 24 / 31 | /servicios/desarrollo-web/ |
| desarrollo de páginas web (en) chile | 11 | 61-63 | — |

**Páginas con más impresiones (90 días):** /proyectos/medina4x4/ 624 (búsquedas de la marca) · artículo de Mercado Pago 238 · /servicios/integraciones/ 171 · /proyectos/sindicato-aza/ 142 · /proyectos/puas-tatuajes/ 117 · artículo de mantención 113 · /servicios/desarrollo-web/ 79 (posición 20,6) · home 63 en www (posición 2,9, 6 clics) más 66 en `https://gogodevs.cl/` (la URL que tiene la ficha de Google).

### GA4 (90 días, 07-08 a 04-11)

| Canal | Sesiones | Sesiones con interacción | Eventos clave |
|---|---|---|---|
| Directo | 103 | 54 | 1 |
| Social orgánico | 70 | 44 | 0 |
| Búsqueda orgánica | 61 | 40 | **0** |
| Referencias | 57 | 27 | 0 |

- **Eventos (90 días):** chat_abierto 26 · chat_mensaje 7 · contacto_whatsapp 4 · formulario_enviado_intento 4 (2 desde orgánico) · form_submit 1 · **lead_formulario 0**.
- **Referencias de asistentes de IA** (chatgpt.com, perplexity, claude, gemini, copilot): **0 sesiones en 90 días.**
- Hay ruido de bots en las ciudades (Luleå, Prineville, Independence, Forest City).
- **Desde el 01-11, GA4 mide solo con consentimiento** (banner de la Ley 21.719). Las sesiones van a bajar aunque no baje el tráfico real.

### Indexación (API de inspección, 05-11, 68 URLs del sitemap)

| Estado | URLs |
|---|---|
| Enviada e indexada | **45** |
| Descubierta: actualmente sin indexar | **9**: /contacto/, /sobre-gogodevs/ y 7 artículos (migrar sitio, tienda de ropa, landing o sitio, WhatsApp en tu sitio, Mercado Libre o tienda propia, climatización, pastelería) |
| Google no reconoce esta URL | **14**: /servicios/automatizacion-de-procesos/, /paginas-web-santiago/ (04-11), /paginas-web-por-rubro/inmobiliarias/ y /peluquerias-y-salones/ (03-11), y 10 artículos publicados entre el 25-10 y el 04-11 |

**Blog: 12 de 29 artículos indexados (41 %).** Las fechas del último rastreo de las páginas indexadas van del 04-09 al 05-11: Google vuelve a pasar por cada página cada varias semanas, no a diario.

## 2. Lo que está sano (no volver a auditarlo)

- Las 68 URLs del sitemap responden 200. Tiempo hasta el primer byte: 44 ms de media y 62 ms de máximo, medido desde Chile en una sola pasada.
- Hay una sola versión del dominio: http → https y sin www → www, con 301. Todas las páginas indexables tienen un canonical absoluto y correcto.
- `robots.txt` permite todo y declara el sitemap. No hay `noindex` accidentales: solo llevan noindex los dos archivos viejos que ya redirigen con 301.
- 71 HTML: títulos únicos, una sola H1 por página, 0 enlaces internos rotos, `lang` y `viewport` presentes. HTML estático, así que el contenido principal llega sin JavaScript.
- Ningún archivo interno sensible queda expuesto: `.git`, `.env`, `.htaccess`, `_blog/`, `README.md` e `index-v2.html` dan 403 o 404 en vivo.
- Schema en JSON-LD válido en todas las páginas: Organization, WebSite, ProfessionalService, BlogPosting, BreadcrumbList, Service y FAQPage. No hay `AggregateRating` propio, ni dirección inventada, ni horarios.
- Lighthouse SEO: 100 en las 5 URLs medidas.

## 3. Hallazgos

Severidad: **Crítica** (cuesta plata o expone al negocio) · **Alta** · **Media** · **Baja**.
Cada hallazgo técnico tiene su especificación en el backlog (columna ENG).

| ID | Hallazgo | Evidencia | Severidad | Impacto SEO o negocio | Dificultad | Archivos | Acción | ENG |
|---|---|---|---|---|---|---|---|---|
| A-01 | **El sitio publica que la mantención incluye el hosting**, lo que contradice los Términos y la regla del 03-11 | /servicios/mantencion-web/: meta description, hero y la tarjeta "Hosting: el servidor donde vive tu sitio, pagado y administrado. No tienes que pagar ni renovar el hosting por tu cuenta". /servicios/: "Hosting pagado y administrado". /cuanto-cuesta…/: fila de mantención. FAQ "¿Incluye dominio y hosting?" ambigua. Hay menciones en 6 artículos. /legal/terminos/ dice lo contrario | **Crítica** | Una oferta publicada que el negocio no puede sostener: es un costo recurrente que pagaría Diego. Además, las IA leen y citan esa página | Baja (son textos), pero hay que editar las fuentes `_blog/programados/` | ver ENG-01 | Diego decide el texto y después se corrigen todas las menciones | ENG-01 |
| A-02 | **La búsqueda orgánica no tiene ningún lead medido**, y el lead confirmado del formulario nunca aparece | GA4, 90 días: búsqueda orgánica con 0 eventos clave; formulario_enviado_intento 4 y lead_formulario 0 (el evento se arregló el 30-10). No se sabe si esos 4 envíos llegaron al correo | **Crítica** | Sin esto no se puede demostrar que el SEO trae clientes, que es el objetivo final | Media | `assets/js/main.js`, `medicion.js`, `/cotizar/` y la configuración de GA4 | Prueba controlada con OK de Diego, cruzar con el correo y marcar los eventos clave | ENG-02 |
| A-03 | **23 de 68 URLs sin indexar**, entre ellas páginas comerciales y de confianza | Ver la tabla de indexación. /servicios/automatizacion-de-procesos/ está enlazada desde todo el sitio y Google "no la reconoce" | **Alta** | Una página que no está indexada no puede rankear ni ser citada por una IA | Baja: solicitar indexación y reforzar enlaces | sitemap y enlaces internos | Solicitar indexación de las 6 páginas comerciales, priorizar enlaces y bajar el ritmo del blog (A-04) | ENG-05 |
| A-04 | **Se publica un artículo al día y Google indexa menos de la mitad** | 29 artículos en ~29 días, casi todos de ~1.000 palabras con la misma estructura y FAQ; 12 indexados. Quedan 10 programados entre el 11 y el 20-11 | **Alta** (riesgo) | La guía de Google (15-05-2026) llama spam al contenido a escala (*scaled content*). Esto **no prueba una penalización**: es una señal de baja prioridad de rastreo en un sitio con poca autoridad, y el riesgo crece con cada página igual | Baja | `_blog/programados/`, `blog-diario.yml` | Bajar a 1 o 2 por semana y publicar solo con información propia (ver `SEO_CONTENT_PLAN.md`) | ENG-05 |
| A-05 | **"Sobre GoGoDevS" no dice quién está detrás**, y Google no la indexa | El texto dice "liderada por un Ingeniero en Informática", sin nombre, años, clientes ni perfiles. Estado: descubierta, sin indexar. El autor de los artículos (`Person` "Diego Dinamarca") enlaza a LinkedIn, no a una página del sitio | **Alta** | Es la señal de entidad y experiencia más barata que hay. "GOGODEVS" choca con "GOGODEV" (YouTube, 23,6 mil suscriptores) | Media: el contenido lo da Diego | `sobre-gogodevs/index.html`, plantilla del blog | Página de entidad con Diego, la razón social ya pública, casos y perfiles, más `Person` en el schema | ENG-03 |
| A-06 | **Los casos son cortos y casi no tienen datos verificables** | /proyectos/*: entre 342 y 591 palabras. Son el contenido diferencial frente a la competencia (ver `SEO_COMPETITORS.md`) | **Alta** | Información original (*information gain*) y confianza para quien compara agencias | Media: datos y permisos de cada cliente | `proyectos/*`, `_blog/sitio_comun.py` | Plantilla de caso con problema, alcance, plazo, tramo, stack y resultado, solo con permiso escrito | ENG-04 |
| A-07 | **Lo que más busca la gente propia (mantención web) cae en el blog**, no en la página de servicio | ~101 impresiones en posición 10-20, todas al artículo | Media | Es el grupo comercial más grande; la página de servicio no capta su demanda | Baja | mantención (servicio y artículo) | **Después de A-01 y de la medición del 16-11**: el servicio se queda con "mantención web" y el artículo responde "qué incluye" | ENG-14 |
| A-08 | **Los artículos se mueven al cargar (CLS 0,284 en laboratorio)** | Lighthouse móvil, artículo de Mercado Pago: el `figure` se desplaza 0,284 cuando carga la fuente Montserrat (`display=swap`) y cambia la altura del título. La plantilla es la misma para los 29 artículos | Media | La CLS es parte de la experiencia de página. El umbral bueno es 0,1 en el percentil 75 **de campo**, y eso no se pudo medir | Media | `_blog/plantilla_articulo.html`, CSS y fuentes | Fuentes servidas desde el propio sitio con *fallback* ajustado, o `font-display: optional` | ENG-06 |
| A-09 | **El LCP de la home es de 3,1 s en laboratorio**, por una imagen de fondo que el navegador descubre tarde | El elemento LCP es `.hero-home__bg` con la imagen dentro de una variable CSS: no está en el HTML inicial ni lleva `fetchpriority`. Las otras 4 URLs miden entre 2,4 y 2,6 s | Media | El umbral bueno es 2,5 s (de campo) | Baja | `index.html`, CSS | Precargar la imagen del hero con `fetchpriority="high"` o usar un `<img>` | ENG-07 |
| A-10 | **Google Fonts bloquea el renderizado en todas las páginas** | Lighthouse: unos 765 ms de bloqueo por `fonts.googleapis.com` y unos 310 ms por `style.css` (107 KB sin minificar). FCP de 2,4 a 2,6 s en las 5 URLs | Media | Afecta a todas las métricas de carga | Media | `<head>` común, `assets/css/style.css` | Servir las fuentes desde el sitio y minificar el CSS | ENG-06 |
| A-11 | **Los recursos estáticos no tienen caché del navegador** | Las cabeceras de `/assets/*.css`, `.js` y `.png` traen solo ETag y Last-Modified, sin `Cache-Control` ni `Expires`. El CSS ya se versiona con `?v=` | Media | Cada visita vuelve a validar cada recurso | Baja, pero hay que comprobar si el nginx del hosting respeta el `.htaccess` | `.htaccess` | Caché larga para `/assets/` | ENG-08 |
| A-12 | **El HTML conserva el marcado oculto del Cyber de octubre, con precios rebajados** | Atributos `data-cyber` con `hidden` en casi todas las páginas (31 en /cuanto-cuesta…/) y el texto "Hasta el lunes 12" | Media | Un rastreador que lee el HTML crudo puede extraer un precio que ya no rige. Riesgo de **precio mal citado** (criterio G-01) | Baja | HTML, `assets/js/cyber.js` | Diego decide si se borra; si no hay campaña, se borra | ENG-10 |
| A-13 | **El schema de la entidad tiene inconsistencias** | El `sameAs` de Organization incluye el LinkedIn **personal** de Diego. ProfessionalService no comparte `@id` con Organization, así que se declaran dos entidades para un mismo negocio | Baja-Media | Claridad de la entidad para Google y las IA | Baja | `index.html`, `<head>` común | Unificar con `@id` y mover el LinkedIn personal a una `Person` | ENG-03 |
| A-14 | **FAQPage en más de 45 páginas: es válido, pero ya no genera resultados enriquecidos** | Desde agosto de 2023, Google muestra las FAQ enriquecidas solo en sitios gubernamentales y de salud con autoridad | Baja | No hace daño, pero no esperar estrellas ni desplegables. Sigue siendo coherente porque las preguntas son visibles | — | — | Mantenerlo. No venderlo como "rich results" | — |
| A-15 | **La página 404 es la de Apache por defecto**, y el servidor ya busca un ErrorDocument que no existe | Cuerpo en vivo: "Additionally, a 404 Not Found error was encountered while trying to use an ErrorDocument" | Baja | Quien llega a un enlace roto se va sin navegación | Baja | `404.html` nuevo, `.htaccess` | 404 propia que siga respondiendo 404 | ENG-09 |
| A-16 | **Higiene de URLs** | `/index.html` responde 200 (duplicada; el canonical la mitiga). `http://gogodevs.cl/` hace 2 saltos. `/links/` es indexable sin canonical. `/herramientas/refrescar_resenas.py` se descarga en vivo (no tiene secretos) | Baja | Menor | Baja | `.htaccess`, `links/`, `deploy.yml` | Ver la especificación | ENG-11 |
| A-17 | **El `lastmod` del sitemap no refleja los cambios de contenido** | /servicios/desarrollo-web/ cambió su title y su H1 el 03-11 y el sitemap sigue diciendo 07-10. 26 URLs tienen la misma fecha, 07-10 | Baja | Google usa `lastmod` solo si es confiable | Baja | `sitemap.xml`, `_blog/sitio_comun.py` | `lastmod` por cambio del contenido principal, no del pie | ENG-12 |
| A-18 | **Detalles on-page** | 3 títulos de casos de 68 a 71 caracteres; la description de /paginas-web-santiago/ tiene 198; /proyectos/ salta de H1 a H3; Lighthouse marca contraste de color, `label-content-name-mismatch` e `image-redundant-alt` | Baja | Menor | Baja | varios | Ver la especificación | ENG-13 |
| A-19 | **El tráfico de la ficha de Google no se puede separar** | La ficha apunta a `https://gogodevs.cl/` sin UTM, y GA4 lo cuenta como google/orgánico | Baja | No se sabe cuánto aporta la ficha | Baja (la hace Diego) | Panel de la ficha | URL www con UTM | — |

## 4. Rendimiento (laboratorio, no campo)

Lighthouse 12, móvil simulado, una corrida por URL el 05-11. **Estas cifras no son Core Web Vitals reales ni garantizan nada en el ranking.**

| URL | Perf. | LCP | CLS | TBT | FCP | SEO | Accesibilidad |
|---|---|---|---|---|---|---|---|
| / | 89 | **3,1 s** | 0 | 70 ms | 2,6 s | 100 | 96 |
| /servicios/desarrollo-web/ | 94 | 2,4 s | 0,006 | 0 | 2,4 s | 100 | 92 |
| /cuanto-cuesta-una-pagina-web-chile/ | 94 | 2,4 s | 0,003 | 0 | 2,4 s | 100 | 96 |
| /blog/mercado-pago-o-webpay-tienda-online/ | 79 | 2,5 s | **0,284** | 0 | 2,5 s | 100 | 96 |
| /proyectos/medina4x4/ | 93 | 2,6 s | 0,003 | 0 | 2,5 s | 100 | 92 |

La interacción (INP) no se mide en laboratorio, y un TBT de 0-70 ms sugiere que no hay problema. Para tener datos de campo, ver ENG-02 (web-vitals hacia GA4, opcional) o esperar a que CrUX tenga datos suficientes.

## 5. Confianza y contenido

- **A favor (verificable):** 16 reseñas de Google con 5,0, todas respondidas; precios públicos en UF (9/14/18/25); 15 casos con enlace al sitio del cliente en vivo; la razón social en el pie; reseñas reales en la home sin `AggregateRating` propio; créditos "Desarrollo web por GoGoDevS" en unos 15 sitios de clientes.
- **En contra:** no hay una persona con nombre detrás del trabajo (A-05); los casos casi no tienen datos (A-06); el blog tiene volumen sin información propia (A-04); la oferta de mantención es incoherente (A-01).
- **Lo que la competencia no tiene** y GoGoDevS sí: casos con nombre y sitio en vivo junto con precios publicados (ver `SEO_COMPETITORS.md`).

## 6. Cómo repetir esta auditoría

Los scripts están en el scratchpad de la sesión del 05-11 y aquí queda el método:

1. `audit_repo.py`: recorre los HTML versionados (title, description, canonical, H1, saltos de encabezado, JSON-LD y FAQ visible, imágenes, enlaces rotos y sitemap).
2. `curl` con un User-Agent de Chrome completo a cada URL del sitemap, más la prueba de 404, de redirecciones y de cabeceras. El sitio le responde 403 a "Mozilla/5.0" a secas.
3. `gsc_gogodevs.py`: Search Console de 90 y 28 días, inspección de las URLs del sitemap y GA4. Usa la cuenta de servicio de solo lectura de `GoGoCRM/scripts/extraer_seo_api.py`.
4. `npx lighthouse@12 <url> --output=json`, 3 corridas por URL, quedándose con la mediana.

Próxima pasada: **01-12-2026**, comparando contra esta línea base.
