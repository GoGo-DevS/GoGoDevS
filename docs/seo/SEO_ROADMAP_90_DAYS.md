# Plan SEO de 90 días — 05-11-2026 al 02-02-2027

**No hay promesas de posiciones.** Los criterios miden si se hizo el trabajo y
si los indicadores se mueven respecto de la línea base de `SEO_AUDIT.md`. Una
posición no es un entregable.

Responsables: **D** = Diego · **E** = agente de ingeniería (`ENGINEERING_BACKLOG.md`) · **S** = estrategia (este agente).

## Línea base que se compara

| Indicador | Valor al 05-11 | Fuente |
|---|---|---|
| Clics e impresiones en 28 días | 4 / 1.192 | Search Console (06-10 a 02-11) |
| Impresiones propias sin marca en 90 días | 324, con 0 clics | Search Console, consulta × página |
| URLs del sitemap indexadas | 45 de 68 (blog: 12 de 29) | API de inspección |
| Eventos clave desde orgánico en 90 días | 0 | GA4 |
| `lead_formulario` en 90 días | 0 (4 intentos) | GA4 |
| Sesiones desde asistentes de IA en 90 días | 0 | GA4 |
| Casos con datos y permiso | 0 de 15 | Sitio |
| Reseñas de Google | 16, con 5,0 | Ficha |

## Días 1-30 (05-11 al 04-12): diagnóstico, P0 y medición

| Entregable | Responsable | Criterio medible |
|---|---|---|
| Auditoría, estrategia, mapa, competencia, plan y backlog (estos documentos) | S | Hecho el 05-11 |
| Decidir el texto de mantención e infraestructura (ENG-01) | D | Texto aprobado |
| ENG-01 implementado | E | 0 frases prohibidas en el HTML público y la guarda comprobada al revés |
| ENG-02: prueba simulada y prueba real autorizada | E + D | 1 envío = 1 lead en DebugView = 1 correo. Eventos clave marcados y `formsubmit.co` excluido |
| Decidir el ritmo del blog (ENG-05) | D | Calendario de 2 por semana como máximo |
| Solicitar la indexación de las 6 páginas comerciales | D | Solicitudes hechas (la fecha queda anotada abajo) |
| Revisar los paneles que no se ven por API: el informe de IA generativa de Search Console (si aparece), Bing Webmaster Tools (verificar el sitio si no lo está) y el informe de Páginas | D | Captura o nota con lo que muestra cada uno |
| Ficha de Google: sitio con UTM, revisión de categorías y una publicación de noviembre | D | Hecho en el panel |
| **Medición del 16-11** (tandas del 30-10 y del 02-11) | S | Informe comparado con la línea base |
| Primera auditoría de prompts (10 preguntas en 5 asistentes) | S + D | Planilla con quién aparece y qué URL se cita |
| ENG-07 (LCP de la home) y ENG-06 (fuentes) | E | LCP ≤ 2,5 s y CLS ≤ 0,1 en laboratorio (mediana de 3 corridas) |
| Guía Ley 21.719 publicada antes del 01-12 | S + D | Publicada y revisada contra el texto de la ley |
| **Medición del 01-12** (tandas del 03-11 y del 04-11) | S | Informe con indexación, consultas propias y leads |

## Días 31-60 (05-12 al 03-01): páginas comerciales, casos y conversión

| Entregable | Responsable | Criterio medible |
|---|---|---|
| ENG-03: página "Sobre" con Diego y schema unificado | D (contenido) + E | Validador con 0 errores, autor enlazado en los 29 o más artículos |
| ENG-04: plantilla de caso y guarda de permiso | E | La guarda falla sin `data-permiso` (comprobada al revés) |
| 2 casos ampliados con permiso (Medina4x4, Punto Parcelas) | D + S | Publicados con un resultado medido y su fuente |
| ENG-14: el servicio de mantención se queda con la palabra | E | Title y H1 según la especificación y los enlaces cruzados |
| Sistemas a medida: precio de entrada y caso | D + S | Página actualizada con el precio que confirme Diego |
| Comparativa de tienda propia o SaaS con costos reales | S | Publicada con sus fuentes fechadas |
| Campo "¿Cómo nos encontraste?" en los formularios | E | Llega en el correo y como parámetro sin datos personales |
| Primer cierre mensual de leads: GA4 contra correos y CRM | S + D | Diferencia explicada; si no calza, no se informa |
| ENG-08, ENG-10 y ENG-11 | E | Cada uno con sus criterios del backlog |
| **Medición del 15-12 y del 01-01** | S | Informe y decisión de qué artículos fusionar |

## Días 61-90 (04-01 al 02-02): resultados, optimización e hipótesis

| Entregable | Responsable | Criterio medible |
|---|---|---|
| Análisis de 90 días contra la línea base | S | Informe con lo que se movió, lo que no y la hipótesis de por qué |
| Fusionar o mejorar los artículos sin indexar y sin impresiones | S + E | Decisión por artículo, con un 301 a su hermano cuando corresponda |
| Optimizar las páginas con impresiones en posición 5-15 | S + E | Lista con title, description y bloque de respuesta por página |
| 2 casos más ampliados | D + S | Publicados con permiso |
| **Prueba de hipótesis** (elegir 1 o 2, con un control) | S | Diseño, fecha de inicio, métrica y fecha de lectura definidos antes de empezar |
| Segunda y tercera auditoría de prompts | S + D | Comparadas contra la primera |
| Revisión de competencia | S | `SEO_COMPETITORS.md` actualizado |
| Plan de los siguientes 90 días | S | Documento nuevo |

**Hipótesis candidatas para el día 61** (se elige con datos, no ahora):

- **H1:** un caso con datos sube las impresiones de su rubro más que un artículo genérico de ese mismo rubro.
- **H2:** sumar datos propios con fecha a un artículo que ya recibe preguntas de IA aumenta las citas en la auditoría de prompts o en Bing AI Performance.
- **H3:** el campo "¿Cómo nos encontraste?" explica más leads que GA4, que depende del consentimiento.

## Calendario de medición

| Fecha | Qué se mide |
|---|---|
| 16-11 | Tandas del 30-10 y del 02-11, e indexación de las 6 páginas comerciales |
| 01-12 | Tandas del 03-11 y del 04-11, consultas "desarrollo web para empresas" y "seo técnico chile", y leads |
| 15-12 | Indexación, primeros datos de los casos y auditoría de prompts |
| 01-01 | Revisión del blog (fusionar o mejorar) y cierre mensual de leads |
| 01-02 | Cierre de los 90 días |

## Registro de cambios en URLs bajo medición

| Fecha | URL | Cambio | Motivo |
|---|---|---|---|
| — | — | — | — |
