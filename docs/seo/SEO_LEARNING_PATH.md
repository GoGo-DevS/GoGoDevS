# Ruta de aprendizaje SEO: 12 semanas con datos de GoGoDevS

Cada semana tiene una idea central, una fuente oficial, un ejercicio sobre
gogodevs.cl con datos reales y una evaluación práctica. La regla: **no se
aprende un concepto sin aplicarlo a tu propio sitio y medirlo.**

Ritmo sugerido: unas 3 horas por semana (1 de lectura, 2 de ejercicio).

| Semana | Tema | Fuente oficial base | Ejercicio sobre GoGoDevS | Evaluación (aprobada si…) |
|---|---|---|---|---|
| 1 | **Cómo funciona un buscador** | [How Search works](https://developers.google.com/search/docs/fundamentals/how-search-works) | Lección 1, más abajo: tus 23 URLs sin indexar | Explicas, sin mirar, por qué /sobre-gogodevs/ no está indexada y qué harías |
| 2 | **Rastreo e indexación** | [Informe de indexación de páginas](https://support.google.com/webmasters/answer/7440203) · [Crawl budget](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget) | Leer `robots.txt`, `sitemap.xml` y el `.htaccess`, y predecir el código HTTP de 10 URLs (incluidas `/index.html`, `/servicios/sistemas-web/` y una que no existe) antes de comprobarlo con curl | Aciertas 9 de 10 y explicas cada error |
| 3 | **SEO técnico** | [Guía de inicio de SEO](https://developers.google.com/search/docs/fundamentals/seo-starter-guide) · [Canonicalización](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls) | Correr Lighthouse 3 veces sobre un artículo y explicar la CLS de 0,284 (ENG-06) con el panel "Performance" de Chrome | Identificas el elemento que se mueve y la causa, y propones la corrección |
| 4 | **Search Console a fondo** | [Informe de rendimiento](https://support.google.com/webmasters/answer/7576553) · [Informe de IA generativa](https://support.google.com/webmasters/answer/16984139) | Filtrar las consultas sin marca: excluir medina, púas, AZA, dulcecita y las que tengan "gogodevs". Comparar 28 días contra los 28 anteriores | Separas, con números, demanda propia, de marca de clientes y de prompts de IA |
| 5 | **Investigación de palabras clave** | [Planificador de palabras clave](https://support.google.com/google-ads/answer/7337243) | Observar a mano en Google.cl (incógnito) las 7 consultas pendientes de `KEYWORD_MAP.md`, sección 4. Si tienes acceso, bajar el CSV del Planificador | Completas la sección 4 con 10 resultados por consulta y su tipo de página |
| 6 | **Intención de búsqueda** | [Directrices para evaluadores de calidad](https://services.google.com/fh/files/misc/hsw-sqrg.pdf) (sección "Needs Met") | Clasificar las 45 consultas propias de la auditoría por intención (precio, servicio, comparar, aprender o navegar) | Tu clasificación coincide con el tipo de página que hoy rankea en el 80 % de los casos |
| 7 | **Arquitectura de contenidos** | [Enlaces](https://developers.google.com/search/docs/crawling-indexing/links-crawlable) · [Políticas de spam](https://developers.google.com/search/docs/essentials/spam-policies) (contenido a escala, *doorways*) | Dibujar el grafo de enlaces internos de los servicios y casos, y marcar dónde falta "hub → hija → hub" | Propones 5 enlaces contextuales con su texto y su justificación |
| 8 | **SEO local** | [Cómo mejorar tu ranking local](https://support.google.com/business/answer/7091) · [Negocios de área de servicio](https://support.google.com/business/answer/9157481) | Auditar la ficha de GoGoDevS: categorías, áreas, publicaciones, fotos, coherencia NAP con el sitio y LinkedIn | Lista de cambios en la ficha, cada uno con su motivo; ninguno inventa una dirección |
| 9 | **Análisis competitivo** | `SEO_COMPETITORS.md` | Elegir 2 competidores y comparar su página de servicio contra /servicios/sistemas-a-medida/: estructura, prueba, precio y llamada a la acción | Encuentras 3 diferencias que GoGoDevS puede sostener con evidencia |
| 10 | **Marketing de contenidos e IA** | [AI features](https://developers.google.com/search/docs/appearance/ai-features) · [Guía de optimización para IA](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) | Escribir el primer caso ampliado con la plantilla (`SEO_CONTENT_PLAN.md`, sección 4) y hacer la auditoría de prompts | El caso pasa la revisión: tiene permiso, datos con su fuente, voz de marca y ninguna afirmación sin respaldo |
| 11 | **Analítica y conversiones** | [Eventos clave en GA4](https://support.google.com/analytics/answer/13128484) · [Referencias no deseadas](https://support.google.com/analytics/answer/10327750) | Cierre mensual: cruzar `lead_formulario` contra los correos y el CRM, y atribuir cada lead a su canal | Cuadra la cuenta, o explicas cada diferencia |
| 12 | **Auditoría y estrategia** | Todo lo anterior | Repetir la auditoría completa (`SEO_AUDIT.md`, sección 6) y escribir tú el plan de los siguientes 90 días | El plan prioriza con datos, no promete posiciones y cada acción tiene su métrica |

---

## Lección 1: cómo decide Google qué indexar (tus 23 URLs)

### La idea

Un buscador hace tres cosas, en orden, y cada una puede fallar por separado:

1. **Descubrir y rastrear.** Encuentra URLs por enlaces y sitemaps, las pone en una cola y las descarga cuando decide que vale la pena.
2. **Indexar.** Lee la página, elige la URL canónica, compara contra lo que ya tiene y **decide** si la guarda.
3. **Mostrar (ranking).** Cuando alguien busca, elige entre lo indexado según relevancia, calidad, experiencia y contexto (país, idioma, dispositivo).

**Una página que no pasa la etapa 2 no existe para la etapa 3.** Tampoco para AI Overviews ni AI Mode, que usan el mismo índice. Por eso lo primero no son las palabras clave: es saber qué está indexado.

### Tu caso, con datos del 05-11

Se consultaron las 68 URLs del sitemap con la API de inspección de Search Console:

| Estado | URLs | Qué significa |
|---|---|---|
| Enviada e indexada | 45 | Pasó las etapas 1 y 2 |
| **Descubierta: actualmente sin indexar** | 9 (entre ellas /sobre-gogodevs/ y /contacto/) | Google la conoce **pero todavía no la rastrea**. La ayuda oficial dice que suele pasar cuando Google prevé sobrecargar el servidor y reprograma el rastreo |
| **Google no reconoce esta URL** | 14 (Santiago, rubros, automatización y 10 artículos recientes) | Ni siquiera la tiene en la cola, aunque esté en el sitemap |

Hay un estado que **no** aparece en tu sitio: *"Rastreada: actualmente sin indexar"*. Ese significa que Google la leyó y decidió no guardarla, muchas veces por calidad o por parecerse a otra. Que no aparezca es una buena noticia: Google todavía no rechazó contenido tuyo después de leerlo.

### El razonamiento de un profesional (y la trampa)

- **La trampa:** "es el *crawl budget*". La documentación de Google dice que el presupuesto de rastreo **solo preocupa en sitios muy grandes** (miles de URLs que cambian seguido). Con 68 URLs, no es tu problema.
- **"¿Se sobrecarga el servidor?":** tu tiempo hasta el primer byte es de 44 ms. Muy improbable.
- **Lo más probable** *(hipótesis, no un hecho documentado)*: Google le asigna a tu sitio una **demanda de rastreo baja**. El sitio tiene pocos enlaces externos (unos 15 dominios), y en las últimas semanas apareció una URL nueva por día, casi todas con la misma estructura. Google prioriza: rastrea las páginas que ya le resultaron útiles (la home, Mercado Pago, integraciones; última visita el 05-11) y deja en cola lo nuevo y lo que parece de poco valor.
- **La consecuencia práctica:** cada artículo genérico compite por la atención de Google con tus páginas que venden. /servicios/automatizacion-de-procesos/ está enlazada desde todo el sitio y aun así Google no la reconoce.

### Qué se hace (y qué no)

**Sí:**
1. **Solicitar la indexación** de las 6 páginas comerciales desde Inspección de URLs. Hay una cuota diaria: unas pocas por día.
2. **Enlaces contextuales** hacia esas páginas desde las que Google rastrea seguido. Un enlace dentro del texto de una página fuerte pesa más que uno en el pie.
3. **Darle a cada página una razón para existir:** contenido propio que no esté en otro lado. La página "Sobre" sin nombre ni datos es el ejemplo perfecto de lo contrario.
4. **Menos URLs de poco valor:** bajar el ritmo del blog y fusionar lo que no despegue.

**No:**
- Reenviar el sitemap todos los días: no acelera nada.
- Usar la Indexing API: es solo para ofertas de trabajo y transmisiones en vivo.
- Pagar "indexadores" o comprar enlaces.

### Ejercicio (unos 45 minutos)

1. Abre Search Console > **Indexación > Páginas**. Compara los motivos que muestra con la tabla de arriba. ¿Coinciden los números? El informe se actualiza con atraso, así que anota la diferencia.
2. Entra a **Inspección de URLs** con `https://www.gogodevs.cl/sobre-gogodevs/`. Mira "Descubrimiento": ¿qué sitemap y qué página de referencia ve Google?
3. Solicita la indexación de las 6 páginas: /sobre-gogodevs/, /contacto/, /servicios/automatizacion-de-procesos/, /paginas-web-santiago/, /paginas-web-por-rubro/inmobiliarias/ y /paginas-web-por-rubro/peluquerias-y-salones/. **Anota la fecha** en `SEO_ROADMAP_90_DAYS.md`.
4. Escribe tu hipótesis en una línea: "Si hago X, espero que el día Y pase Z". El 01-12 la contrastamos con datos.

### Evaluación

Respóndelas por escrito, sin mirar:

1. ¿Cuál es la diferencia entre "Descubierta, sin indexar" y "Rastreada, sin indexar", y cuál te preocuparía más?
2. ¿Por qué decir "es el crawl budget" sería un error en gogodevs.cl?
3. Una página no indexada ¿puede aparecer en un AI Overview? ¿Por qué?
4. Si mañana /sobre-gogodevs/ queda indexada, ¿ya está resuelto el problema de entidad? ¿Qué falta?
5. Propón una prueba para saber si bajar el ritmo del blog mejora la indexación de las páginas comerciales. ¿Qué medirías y cuándo?

**Pauta:**
1. La primera no se ha leído; la segunda se leyó y se descartó. Preocupa más la segunda.
2. El sitio es chico, el servidor responde rápido y la documentación lo descarta para sitios de este tamaño.
3. No: las funciones de IA usan el mismo índice.
4. No. Indexarla es la condición; falta que tenga contenido de entidad (persona, datos, perfiles) y que la web externa confirme lo mismo.
5. Hay que fijar una métrica (por ejemplo, días hasta indexar una página comercial nueva, o el número de páginas indexadas), una fecha de corte y la comparación contra el periodo anterior. Ojo con los factores que se mezclan: si al mismo tiempo cambian los enlaces, no se puede separar el efecto.
