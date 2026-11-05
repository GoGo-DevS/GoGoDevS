# Plan de contenido y autoridad — gogodevs.cl — 05-11-2026

Por qué: `SEO_STRATEGY_CHILE.md`. Qué URL atiende cada búsqueda: `KEYWORD_MAP.md`.

## 1. El cambio de rumbo: menos piezas, más información propia

**Dato:** de 29 artículos publicados en unos 29 días, Google indexó 12. Siete están "descubiertos, sin indexar" y diez ni siquiera los conoce (`SEO_AUDIT.md`, A-04). Casi todos tienen unas 1.000 palabras, la misma estructura y su FAQ. La guía de Google de mayo de 2026 trata el contenido hecho a escala como spam. Esto **no prueba una penalización**, pero sí que publicar más del mismo tipo no está sumando.

**Propuesta (decide Diego):**
1. **Ritmo: de 1 artículo al día a 1 o 2 por semana**, desde ya. Quedan 15 programados entre el 05 y el 20-11. Los del 07 al 10-11 ya tienen foto y salen solos si no se cambia nada.
2. **Filtro de publicación.** Un artículo sale solo si trae **al menos un dato propio de GoGoDevS**:
   - un caso con permiso,
   - un precio de la lista publicada,
   - un número medido (Search Console, GA4, plazo real, comisión verificada con su fecha y fuente),
   - o un error real con su solución.
   Si no lo trae, se queda en `_blog/en-pausa/`.
3. **Reasignar las fechas** de los programados que pasen el filtro: dos por semana hasta enero (ENG-05).
4. **Revisión el 01-01-2027:** el artículo que siga sin indexar y sin impresiones se fusiona con su artículo hermano más fuerte, con un 301. Se decide caso por caso, nunca en masa.

## 2. Qué contenido, en orden de valor

| Prioridad | Tipo | Qué es | Por qué gana | Necesita de Diego |
|---|---|---|---|---|
| 1 | **Casos con datos** | Ficha completa por cliente: problema, alcance, plazo, tramo en UF, stack, resultado medido y enlace al sitio en vivo | Es la brecha número 1 de la competencia y la información propia que buscan Google y las IA | Permiso escrito y datos de cada cliente |
| 2 | **Páginas de servicio** | Mantención (después de ENG-01), sistemas a medida (precio de entrada y proceso), ecommerce (prueba de Medina), integraciones (datos) | Es donde convierte la intención comercial | Precio de entrada de sistemas, texto de mantención |
| 3 | **Comparativas con datos propios** | Mercado Pago, Webpay o Flow; tienda propia, Jumpseller o Shopify; Wix, WordPress o a medida | Es donde ya llegan las preguntas de IA, y la SERP de tiendas está llena de guías escritas por las mismas plataformas | Costos reales y verificados, con su fecha |
| 4 | **Guías para pymes chilenas** | Problemas locales con respuesta concreta: Ley 21.719 en la web, boleta y cobro online, dominio .cl | Demanda local con poca competencia buena *(supuesto)* | Revisión de exactitud |
| 5 | **Ingeniería demostrable** | Cómo se hizo algo real y qué se midió | Muestra experiencia (E-E-A-T) y genera enlaces de otros desarrolladores *(supuesto)* | Datos y permiso del caso |
| 6 | **Preguntas comerciales** | Dentro de las páginas de servicio y de precios, no como artículos sueltos | Responde la duda de compra justo donde se decide | — |

**Prohibido:**
- Testimonios inventados o resultados de clientes sin su permiso escrito.
- Páginas casi iguales para variantes de una misma palabra.
- Páginas por comuna que solo cambian el nombre.
- Fechas de "actualizado" sin un cambio real.
- Imágenes de IA presentadas como si fueran personas o proyectos reales.

**Revisión obligatoria** antes de publicar cualquier pieza:
- Voz de marca: tú, sin voseo, "mantención".
- Regla de infraestructura del 03-11: nunca "hosting incluido".
- Precios: solo 9/14/18/25 UF.
- Cruzar cada afirmación sobre un cliente con su nota en la memoria (lección `casos-publicados-con-datos-falsos`).

## 3. Calendario de 90 días

| Semana | Pieza | Tipo | URL (nueva o existente) | Dato propio que la sostiene |
|---|---|---|---|---|
| 09-11 | Texto nuevo de mantención e infraestructura (con ENG-01) | Servicio | /servicios/mantencion-web/ | Modelo SINAIL (regla del 03-11) |
| 16-11 | **Qué tiene que cambiar tu página web con la Ley 21.719** (rige el 01-12-2026) | Guía con fecha | /blog/ley-21719-pagina-web/ (nueva) | GoGoDevS implementó en su sitio, el 01-11, el consentimiento y la política. No es asesoría legal: se cita la ley |
| 16-11 | Caso Medina4x4 ampliado | Caso | /proyectos/medina4x4/ | De Mercado Libre a tienda propia con cobro con tarjeta. Cifras solo con OK de Vanessa |
| 23-11 | Caso Punto Parcelas ampliado: migración desde JumpSeller | Caso e ingeniería | /proyectos/punto-parcelas/ | La migración. **El SEO es de Jorge Urzúa y se dice.** OK de Leonardo |
| 30-11 | Tienda propia, Jumpseller o Shopify: costo real a 12 meses en Chile | Comparativa | /blog/jumpseller-shopify-o-tienda-propia/ (programado para el 12-11; reprogramar y enriquecer) | Costos de los e-commerce entregados y planes vigentes con fecha |
| 07-12 | Sistemas a medida: precio de entrada, etapas y caso | Servicio | /servicios/sistemas-a-medida/ | Precio de entrada que confirme Diego y un caso con permiso |
| 14-12 | Mercado Pago, Webpay o Flow: actualización con comisiones verificadas | Actualización | /blog/mercado-pago-o-webpay-tienda-online/ | Tarifas públicas con fecha y fuente, más la experiencia de integración |
| 21-12 | Caso FCO Climatización o Max Services ampliado | Caso | /proyectos/fco-climatizacion/ o /proyectos/max-services-spa/ | Datos con permiso. "max service" es otra empresa: no confundir |
| 04-01 | Qué medimos en cada sitio que entregamos, y por qué tu formulario puede estar perdiendo leads | Ingeniería | /blog/medir-leads-pagina-web/ (nueva) | El bug real de lead_formulario y la solución con AJAX y respaldo a WhatsApp |
| 11-01 | Wix, WordPress o página a medida (programado para el 13-11; reprogramar y enriquecer) | Comparativa | /blog/wix-wordpress-o-pagina-a-medida/ | Casos de rescate y migración reales |
| 18-01 | Revisión del 01-01: fusionar o mejorar los artículos sin indexar | Mantención de contenido | varias | Datos de Search Console |
| 25-01 | Página de servicio de ecommerce: prueba arriba | Servicio | /servicios/ecommerce/ | Casos Medina, Popi y Dulcecita (los que tengan permiso) |

Los programados restantes (restaurante, Instagram, página barata, tatuajes, reservas, rediseño, WooCommerce, servicios, sitio hackeado, freelance, correo corporativo) entran en los huecos **solo si pasan el filtro de la sección 1**. Uno por semana como máximo, además de lo de la tabla.

## 4. Plantilla de caso (contenido)

La estructura técnica está en ENG-04.

1. **Cliente y rubro.** Nombre, comuna si es pública y enlace al sitio en vivo.
2. **El problema**, en palabras del negocio. Una cita textual solo si el cliente la dio por escrito.
3. **Qué se hizo:** alcance, decisiones técnicas y por qué.
4. **Plazo real y tramo.** El precio exacto nunca sin permiso; el tramo de la lista sí.
5. **Stack.**
6. **Resultado medido**, con la fuente y el periodo (por ejemplo, "Search Console, 28 días al 01-12"). Sin dato: "en medición desde <fecha>".
7. **Lo que no salió bien y cómo se resolvió.** Esto es lo que hace creíble un caso.
8. **Llamada a la acción** al servicio que corresponde.

## 5. Autoridad fuera del sitio

- **Créditos en los sitios de clientes:** unos 15, con "Desarrollo web por GoGoDevS" (02/03-11). Medir en Search Console > Enlaces a fines de noviembre.
- **Casos publicados en conjunto:** pedir al cliente que comparta o enlace su caso, cuando quiera.
- **LinkedIn de Diego y de la empresa:** publicar cada caso y cada comparativa con un aprendizaje propio. Es la plataforma que la industria señala como muy citada por las IA *(hipótesis)*.
- **YouTube @gogodevs:** recorridos de 2-3 minutos de cada caso, embebidos en su ficha. Google recomienda imágenes y video que apoyen el contenido. Va después de los casos escritos.
- **Directorios B2B con reseñas verificables:** evaluar uno por uno, sin registros masivos.
