# Estrategia SEO y comercial de GoGoDevS en Chile — 05-11-2026

Evidencia: `SEO_AUDIT.md`. Palabras clave: `KEYWORD_MAP.md`. Competencia: `SEO_COMPETITORS.md`.
Este documento decide **qué** se hace y **por qué**. El **cuándo** está en
`SEO_ROADMAP_90_DAYS.md` y el **cómo técnico** en `ENGINEERING_BACKLOG.md`.

## 1. Diagnóstico en un párrafo

Lo técnico de gogodevs.cl está sano y no es lo que frena. Lo que frena son cuatro cosas medibles:

1. **Autoridad baja.** Unos 15 dominios lo enlazan, casi todos de clientes.
2. **Una entidad difusa.** No hay una persona con nombre detrás, y "GOGODEVS" se confunde con "GOGODEV".
3. **Mucho contenido sin información propia.** De 29 artículos, Google indexó 12.
4. **Cero medición comercial.** La búsqueda orgánica no registra ningún lead en 90 días.

Además, el sitio publica una oferta (el hosting dentro de la mantención) que el negocio no puede sostener. Con unas 324 impresiones propias en 90 días, la meta realista no es "desarrollo web chile". La meta es **ganar búsquedas de nicho con intención de compra y ser la fuente que se cita en los temas donde GoGoDevS tiene experiencia demostrable.**

## 2. Las 10 oportunidades de mayor valor

Están ordenadas por valor comercial y urgencia, no por facilidad.

| # | Oportunidad | Por qué vale (evidencia) | Quién la mueve | Prioridad |
|---|---|---|---|---|
| 1 | **Corregir la oferta de mantención** | El sitio dice "hosting pagado y administrado"; los Términos y la regla del 03-11 dicen lo contrario (A-01). Un precio u oferta mal publicada es el defecto más caro | Diego decide el texto → ENG-01 | P0 |
| 2 | **Medir leads de punta a punta** | Búsqueda orgánica: 0 eventos clave. lead_formulario: 0. Hubo 4 intentos de envío sin confirmar (A-02). Sin esto el SEO no demuestra impacto | ENG-02, más Diego en GA4 | P0 |
| 3 | **Indexar lo comercial y bajar el ritmo del blog** | 23 de 68 URLs sin indexar, entre ellas /contacto/, /sobre-gogodevs/ y /servicios/automatizacion-de-procesos/ (A-03, A-04) | Diego (solicitar indexación) → ENG-05 | P1 |
| 4 | **Entidad: Diego y GoGoDevS con nombre y prueba** | Ningún competidor serio, salvo dos, muestra a la persona. La página "Sobre" es genérica y no está indexada (A-05, A-13) | Diego (contenido) → ENG-03 | P1 |
| 5 | **Casos con datos verificables** | Es la brecha número 1 de la competencia: casos anónimos o cifras sin línea base (`SEO_COMPETITORS.md`). Hoy los casos tienen entre 342 y 591 palabras | Diego (permisos y datos) → ENG-04 | P1 |
| 6 | **Que la página de servicio se quede con "mantención web"** | Unas 101 impresiones en posición 10-20, el grupo propio más grande (A-07) | Después de #1 y del 16-11 → ENG-14 | P1 |
| 7 | **Autoridad en cobros y checkout en Chile** | 238 + 171 impresiones; las IA ya leen esas páginas para responder sobre checkout y cobros recurrentes; "mercado pago es webpay" está en posición 4,2 | Contenido con datos propios de integraciones reales | P2 |
| 8 | **"Desarrollo web para empresas"** en /servicios/desarrollo-web/ | Posición 16-31 en "servicios de desarrollo web", "empresarial" y "para empresas"; la página se retituló el 03-11 | Medir el 01-12 y después reforzarla con casos | P2 |
| 9 | **Sistemas a medida con precio de entrada y un caso con nombre** | El servicio de más valor tiene la página más débil (posición 54). Codelan esconde sus precios y desarrollosoftwarechile.cl no tiene clientes con nombre | Diego (precio de entrada y caso) | P2 |
| 10 | **Experiencia de página e higiene técnica** | CLS de 0,284 en los artículos, LCP de 3,1 s en la home, fuentes que bloquean, sin caché, marcado del Cyber oculto con precios viejos (A-08 a A-12) | ENG-06 a ENG-12 | P2-P3 |

**Lo que NO se hace, y por qué:**
- **Páginas por comuna fuera de Santiago y Maipú.** El autocompletado del 02-11 no dio ninguna sugerencia comercial para las comunas vecinas, y sería *doorway*.
- **Atacar "desarrollo web chile" o "software para pymes chile" de frente.** La primera la dominan agencias con mucha más autoridad. La segunda tiene intención de comprar un SaaS.
- **llms.txt o "marcado para IA".** Google lo desmiente oficialmente.
- **Comprar enlaces o reseñas.**

## 3. Posicionamiento y diferenciación

Diferencias que GoGoDevS **puede probar hoy**. Cada una lleva su evidencia; sin evidencia no se publica.

| Diferencia | Evidencia que la sostiene | Contra quién pesa |
|---|---|---|
| **Precios publicados en UF** (9/14/18/25) | /cuanto-cuesta-una-pagina-web-chile/ | Codelan, crea7ive y grouty (en sistemas) no publican precios o solo dan rangos |
| **Hablas con quien hace el trabajo** | Diego es el desarrollador (hay que mostrarlo, #4) | Agencias con equipo anónimo |
| **Casos con nombre y sitio en vivo** | 15 casos enlazados a su dominio | Casos anónimos (Codelan), solo logos (grouty), cifras sin línea base (Best Solution) |
| **Tu dominio, tu servidor y tu código, a tu nombre** | Los Términos ya lo dicen. Falta alinear el resto del sitio (#1) | crea7ive y tecreamos venden el hosting incluido, que amarra al cliente |
| **Sistemas propios en Django y Postgres, no solo WordPress** | Stack de los proyectos reales | Best Solution, tecreamos, crea7ive |
| **Medición real** | Search Console y GA4 conectados, con datos propios publicables | Agencias que venden "SEO para IA" con llms.txt |

**Propuesta de valor por servicio.** El texto final lo aprueba Diego y la base es la de arriba:

| Servicio | Problema del cliente | Promesa sostenible | Prueba a mostrar |
|---|---|---|---|
| Desarrollo web para empresas | "Tengo una web que no me trae consultas" | Un sitio rápido, medible y a tu nombre, con un precio conocido de antemano | Casos FCO, Max y Púas, más la tabla de precios |
| E-commerce | "Vendo por Instagram o Mercado Libre y no escalo" | Una tienda propia con el cobro integrado | Medina4x4: vendía solo por Mercado Libre y hoy cobra con tarjeta en su propia tienda |
| Sistemas a medida | "Lo llevo en planillas y WhatsApp" | Un sistema hecho a la operación real, que crece por etapas | Un caso con permiso (a definir con Diego) |
| Integraciones y pagos | "¿Mercado Pago, Webpay o Flow?" | Te integramos el checkout que conviene a tu caso | Integraciones reales y datos de comisión verificados |
| Mantención web | "Nadie me responde cuando algo falla" | Monitoreo, respaldos, actualizaciones y ajustes, con fallas críticas en 24 horas hábiles; la infraestructura queda a tu nombre | Modelo SINAIL (regla del 03-11) |

## 4. SEO local (Chile, Santiago y Maipú)

Estado verificado: la ficha de Google existe, está verificada, es de **área de servicio sin dirección pública**, tiene categoría "Diseñador de sitios web", 16 reseñas con 5,0 (todas respondidas), 15 fotos y la primera publicación del 30-10.

1. **Coherencia NAP.** El nombre se escribe "GoGoDevS" en todas partes y el teléfono es siempre +56 9 5639 2509. **No se publica dirección** (no hay oficina). La comuna, Maipú, solo aparece donde ya es pública.
2. **La ficha** (Diego, 15 minutos):
   - Cambiar el sitio a `https://www.gogodevs.cl/?utm_source=google&utm_medium=organic&utm_campaign=ficha` para medirla aparte (A-19).
   - Revisar en el panel las categorías secundarias que existan para desarrollo de software y comercio electrónico, y elegir **solo las que describen servicios reales**.
   - Revisar que las áreas de servicio sean las reales.
   - Una publicación al mes y fotos de cada entrega real (nunca imágenes hechas con IA).
3. **Reseñas auténticas.** Pedirlas al entregar cada proyecto, de una en una, con el enlace directo `g.page/r/CRH_9v1iEamGECE/review`. Nunca incentivadas ni masivas. Responder todas, con tú y sin voseo.
4. **Páginas locales.** Hay exactamente dos y se quedan así: /paginas-web-santiago/ (04-11, todavía sin indexar) y /paginas-web-maipu/ (30-10). Se miden; **no se crean más comunas**.
5. **Menciones legítimas.**
   - Los créditos "Desarrollo web por GoGoDevS" en unos 15 sitios de clientes (ya hechos).
   - Casos publicados en conjunto con el cliente, con permiso.
   - Perfiles completos y consistentes en LinkedIn (empresa y Diego).
   - Directorios B2B con reseñas verificables, **solo si son reales y moderados**. A evaluar uno por uno: no se registra nada sin revisarlo antes.

## 5. Búsqueda con IA: qué está documentado y qué es hipótesis

**Documentado por Google** (ai-features; guía de optimización del 15-05-2026; post "succeeding in AI search" del 21-05-2025):

- AI Overviews y AI Mode usan **los mismos sistemas de búsqueda**. Basta con estar indexado y ser elegible para mostrarse con snippet; no hay requisitos técnicos extra.
- No hacen falta archivos especiales, ni llms.txt, ni un schema para IA, ni partir el texto en fragmentos (*chunking*). La guía de 2026 los trata como **mitos**.
- Lo que sí piden: contenido único y no genérico, con experiencia propia; contenido importante en texto HTML; datos estructurados iguales a lo visible; buena experiencia de página; ficha de Google al día; medir el valor de la visita y no solo los clics.
- El contenido creado a escala para posicionar es spam (*scaled content*).
- Search Console tiene desde el 31-08-2026 un **informe de rendimiento de IA generativa**. Muestra solo impresiones y aparece solo si el sitio tiene volumen suficiente. Los clics siguen mezclados en "Web".

**Documentado por otros:**
- Bing Webmaster Tools tiene "AI Performance" (citas en Copilot) desde el 10-02-2026.
- Clarity tiene "AI Visibility > Bot Activity", que mide la visita de bots, **no las citas**.
- OAI-SearchBot, Claude-SearchBot y PerplexityBot controlan la aparición en las búsquedas de cada IA. GPTBot y ClaudeBot son de entrenamiento.

**Hipótesis de la industria (no se venden como hechos):**
- Que las menciones en Reddit, YouTube o LinkedIn suban las citas.
- Que ChatGPT se apoye en el índice de Bing.
- Que poner una fecha de "última actualización" ayude. Solo vale si la actualización es real.

**Qué hace GoGoDevS:**
1. Mantener `robots.txt` abierto a los buscadores con IA (hoy permite todo). Diego decide aparte si permite los rastreadores **de entrenamiento**, pero eso no afecta las citas.
2. Información propia en los temas con evidencia: cobros y checkout en Chile, mantención, migraciones sin perder Google y casos.
3. Entidad clara (#4).
4. **Medir en vez de prometer:**
   - El informe de IA de Search Console, si aparece.
   - Bing AI Performance (hay que verificar el sitio en Bing).
   - GA4 con las fuentes chatgpt.com, perplexity.ai, claude.ai, gemini.google.com y copilot (hoy: 0).
   - Una auditoría de prompts al mes, con el protocolo de abajo.

**Protocolo de auditoría de prompts** (mensual, 20 minutos):
- 10 preguntas fijas de cliente, por ejemplo "¿qué empresa hace páginas web para pymes en Santiago con precios claros?" o "¿Mercado Pago o Webpay para mi tienda?".
- Hacerlas en ChatGPT, Gemini, Claude, Perplexity y Google con modo IA, cada vez en un chat nuevo o en modo incógnito.
- Registrar en una planilla si aparece GoGoDevS, qué URL cita y quién aparece en su lugar.
- Es un muestreo: las respuestas varían de una vez a otra.

## 6. Marketing y conversión

**Objetivo:** cotizaciones calificadas, no visitas.

1. **Captación orgánica por intención:**
   - Precio: /cuanto-cuesta…/.
   - Servicio: desarrollo web, ecommerce, sistemas, mantención.
   - Rubro: inmobiliarias, salones, repuestos.
   - Comparación: Mercado Pago o Webpay, tienda propia o SaaS.
   - Local: Santiago y Maipú.
   Cada página termina en **una** llamada a la acción principal.
2. **Llamadas a la acción:**
   - Principal: "Cotizar mi proyecto" (/cotizar/).
   - Secundaria: WhatsApp, con el mensaje prellenado según la página.
   - En el contenido educativo, una sola llamada a la acción contextual al servicio que corresponde, no tres.
3. **Formularios:**
   - Pocos campos obligatorios (nombre, contacto, tipo de proyecto).
   - Agregar el campo opcional **"¿Cómo nos encontraste?"**. Es la atribución más robusta ahora que GA4 mide solo con consentimiento.
   - Mantener el respaldo a WhatsApp cuando falla el envío (ya existe).
4. **Flujo de cotización:**
   - Lead → respuesta en menos de 24 horas hábiles → registro en el CRM con el **origen** (orgánico, ficha, IA, referido o redes) → propuesta → cierre.
   - Así el SEO se mide en clientes y no solo en clics.
5. **Medición** (ENG-02):

   | Evento | Qué significa | Tipo |
   |---|---|---|
   | `lead_formulario` | Envío confirmado del formulario | Clave |
   | `lead_cotizador` | Cotización enviada desde /cotizar/ | Clave |
   | `contacto_whatsapp` | Clic en WhatsApp | Clave secundario (es intención, no lead) |
   | `chat_mensaje` | Mensaje en el chat | Normal |

   - Excluir `formsubmit.co` como referencia no deseada.
   - Cada mes, cruzar los leads de GA4 contra los correos y el CRM. Si no calzan, el número no se informa.
6. **Confianza:**
   - Reseñas reales visibles (ya están).
   - Casos con datos (#5).
   - Diego con nombre y foto real (#4).
   - Los Términos y la oferta de mantención coherentes (#1).
   - **Nada de testimonios inventados ni resultados sin permiso escrito.**

## 7. Investigación de fuentes (Misión 1)

| Video | Qué se pudo verificar | Uso |
|---|---|---|
| [AI SEO for Beginners 2026](https://www.youtube.com/watch?v=XzDl3otai1Y), Reliablesoft Academy, 05-10-2026, 14 min | **Transcripción entregada por Diego.** Coincide con Google en que el SEO de IA es SEO, que no hay marcado especial, que el contenido va en HTML, que hay que aportar información propia y que el schema debe coincidir con lo visible. Los informes de Search Console (IA generativa), Bing (AI Performance) y Clarity (bots) existen y se verificaron. **No verificado:** "1.200 millones de usuarios semanales de ChatGPT", el estudio de SERP Interactive (el doble de clics) y que Reddit, YouTube, Wikipedia y LinkedIn sean los más citados. **Hay que matizar** dos recomendaciones: escribir encabezados como preguntas está bien para la persona, pero Google pide no reescribir "para la IA"; y la fecha de "última actualización" solo vale si hubo un cambio real | Marco de las secciones 5 y 6 |
| [Dame 34 Minutos y Te Doy 1000 Horas De Conocimiento Sobre Claude](https://www.youtube.com/watch?v=Ra3GIwwT4Yc), Adrián Sáenz, 01-09-2026, 35 min | Solo el título y la descripción: promoción de "skills" para crear webs y un enlace de afiliado de Hostinger. Tiene únicamente subtítulos automáticos y **no hay transcripción entregada** | Sin analizar. Es sobre herramientas de IA, no sobre SEO |
| [30 años de marketing digital en 53 minutos](https://www.youtube.com/watch?v=Qqky0A0I-Gs), canal MENTE EMPRESARIAL, 26-04-2025, 53 min | Según su descripción, es una **traducción hecha por un fan** de contenido de Simon Squibb, no el canal original. Solo tiene subtítulos automáticos y **no hay transcripción entregada** | Sin analizar. Si se usa, citar la fuente original |

**Para analizar los videos 2 y 3:** abrir cada video en YouTube, entrar a "Más" > "Mostrar transcripción", copiarla y pegármela. No se resumen videos que no se pudieron leer.
