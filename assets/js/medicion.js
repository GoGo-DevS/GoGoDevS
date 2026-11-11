/* Medición de gogodevs.cl — 10-09-2026.

   Contexto: el sitio no medía NADA (ni GA4, ni Tag Manager, ni Pixel de Meta).
   Diego quiere pagar campañas en Meta y Google Ads, y sin esto no hay forma de
   saber qué campaña trae clientes: se paga a ciegas y no se puede optimizar.

   Todo vive en UN archivo a propósito. El sitio son 30 HTML sueltos sin
   plantillas: si el código de medición se pega en cada uno, la próxima vez que
   haya que cambiar un evento hay que tocar 30 archivos y uno se queda atrás.

   IDs vacíos = esa plataforma NO carga. Así este archivo se puede subir hoy y
   activarse cuando existan las cuentas, sin tocar nada más que estas líneas.

   Consentimiento (01-11-2026): la decisión del 10-09 de no poner banner ("Chile
   no exige opt-in") quedó obsoleta. La Ley 21.719 rige desde el 01-12-2026 y
   GA4 y el Pixel tratan datos personales (identificadores, IP). Ahora NADA de
   medición carga hasta que el visitante acepta. Si rechaza, o no decide, el
   sitio funciona igual y no se mide. La decisión dura un año; la señal Global
   Privacy Control del navegador cuenta como rechazo. Cualquier elemento con
   data-gg-consentimiento (la política de privacidad tiene uno) reabre el aviso. */
(function () {
  'use strict';

  var CONFIG = {
    GA4_ID: 'G-L5V8KTG6N2', // G-XXXXXXXXXX  (Google Analytics 4)
    META_PIXEL_ID: '' // 15 dígitos    (Meta / Facebook Pixel)
  };

  var WHATSAPP = /(?:wa\.me|api\.whatsapp\.com|web\.whatsapp\.com)/i;

  /* Tree de un cliente (/t/<negocio>/, 11-11-2026): la pagina marca
     <html data-tree-cliente>. Ahi se carga GA4 (con el mismo consentimiento)
     solo para la visita y el evento tree_click del propio Tree; los
     disparadores de conversion de GoGoDevS (contacto_whatsapp, etc.) NO
     corren, porque el WhatsApp de ese boton es el del cliente y contarlo como
     contacto de GoGoDevS inflaria las conversiones de las campanas.
     data-politica cambia el enlace a la politica de privacidad del aviso (el
     Tree con dominio propio no puede enlazar a una ruta relativa de gogodevs.cl). */
  var RAIZ_HTML = document.documentElement;
  var TREE_CLIENTE = RAIZ_HTML.hasAttribute('data-tree-cliente');
  var POLITICA = RAIZ_HTML.getAttribute('data-politica') || '/legal/privacidad/#cookies';

  /* ---------- Consentimiento ---------- */

  var CLAVE_DECISION = 'gg_consentimiento_v1';
  var VIGENCIA_MS = 365 * 24 * 60 * 60 * 1000;

  function leerDecision() {
    try {
      var d = JSON.parse(window.localStorage.getItem(CLAVE_DECISION));
      if (d && typeof d.analitica === 'boolean' && Date.now() - d.fecha < VIGENCIA_MS) return d;
    } catch (e) {}
    return null;
  }

  function guardarDecision(acepta) {
    try {
      window.localStorage.setItem(CLAVE_DECISION, JSON.stringify({ analitica: acepta, fecha: Date.now() }));
    } catch (e) {}
  }

  /* Quien acepta y después rechaza no puede quedar medido: se corta GA4 en esta
     página y se borran las cookies que ya había dejado. */
  function revocar() {
    if (CONFIG.GA4_ID) window['ga-disable-' + CONFIG.GA4_ID] = true;
    ga4Listo = pixelListo = false;
    if (window.gtag === gtag) window.gtag = undefined;
    document.cookie.split(';').forEach(function (c) {
      var nombre = c.split('=')[0].trim();
      if (/^(_ga|_gid|_gat|_fbp|_fbc)/.test(nombre)) {
        var base = nombre + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/';
        document.cookie = base;
        document.cookie = base + '; domain=.' + window.location.hostname.replace(/^www\./, '');
      }
    });
  }

  var aviso = null;
  function cerrarAviso() {
    if (aviso) { aviso.remove(); aviso = null; }
  }

  function decidir(acepta) {
    guardarDecision(acepta);
    cerrarAviso();
    if (acepta) cargarPlataformas(); else revocar();
  }

  function mostrarAviso() {
    if (aviso) return;
    var estilos = document.getElementById('gg-consent-css');
    if (!estilos) {
      estilos = document.createElement('style');
      estilos.id = 'gg-consent-css';
      estilos.textContent = [
        '.gg-consent{position:fixed;left:1rem;right:1rem;bottom:1rem;z-index:40;max-width:46rem;margin:0 auto;',
        'background:#0D1A30;border:1px solid #2A3B5E;border-radius:16px;padding:1rem 1.2rem;',
        'box-shadow:0 24px 60px rgba(0,0,0,.55);color:#FFFFFF;font-family:"Montserrat",system-ui,sans-serif;',
        'display:flex;flex-wrap:wrap;align-items:center;gap:.9rem 1.2rem;}',
        '.gg-consent p{margin:0;flex:1 1 20rem;font-size:.85rem;line-height:1.5;color:#FFFFFF;}',
        '.gg-consent a{color:#FFB627;}',
        '.gg-consent-botones{display:flex;gap:.6rem;flex:0 0 auto;}',
        '.gg-consent button{font:inherit;font-size:.82rem;font-weight:700;border-radius:999px;',
        'padding:.65rem 1.3rem;cursor:pointer;min-width:7.5rem;}',
        '.gg-consent .gg-si{background:#FFB627;color:#0A1428;border:1px solid #FFB627;}',
        '.gg-consent .gg-no{background:transparent;color:#FFFFFF;border:1px solid #A8B3CF;}',
        '.gg-consent button:focus-visible{outline:2px solid #FFB627;outline-offset:2px;}',
        // Fuera del celular va abajo a la IZQUIERDA: la derecha es de WhatsApp,
        // Instagram y el chat. Y mientras el chat esta abierto se esconde.
        '@media(min-width:641px){.gg-consent{left:1.2rem;right:5.6rem;margin:0;max-width:34rem;}}',
        'html.gg-chat-abierto .gg-consent{display:none;}'
      ].join('');
      document.head.appendChild(estilos);
    }
    aviso = document.createElement('div');
    aviso.className = 'gg-consent';
    aviso.setAttribute('role', 'region');
    aviso.setAttribute('aria-label', 'Aviso de cookies');
    aviso.innerHTML =
      '<p>Usamos Google Analytics para saber qué páginas sirven y mejorar el sitio. ' +
      'Solo se activa si aceptas; si no, el sitio funciona igual. ' +
      '<a href="' + POLITICA.replace(/"/g, '&quot;') + '">Política de privacidad</a></p>' +
      '<div class="gg-consent-botones">' +
        '<button type="button" class="gg-no">Rechazar</button>' +
        '<button type="button" class="gg-si">Aceptar</button>' +
      '</div>';
    aviso.querySelector('.gg-si').addEventListener('click', function () { decidir(true); });
    aviso.querySelector('.gg-no').addEventListener('click', function () { decidir(false); });
    document.body.appendChild(aviso);
  }

  window.ggConsentimiento = { abrir: mostrarAviso, decision: leerDecision };

  document.addEventListener('click', function (e) {
    var el = e.target && e.target.closest ? e.target.closest('[data-gg-consentimiento]') : null;
    if (!el) return;
    e.preventDefault();
    mostrarAviso();
  });

  /* ---------- Carga de plataformas (solo con consentimiento) ---------- */

  function cargarScript(src) {
    var s = document.createElement('script');
    s.async = true;
    s.src = src;
    document.head.appendChild(s);
  }

  var ga4Listo = false;
  var pixelListo = false;
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }

  function cargarPlataformas() {
    if (CONFIG.GA4_ID) {
      window['ga-disable-' + CONFIG.GA4_ID] = false;
      if (!document.querySelector('script[src*="googletagmanager.com/gtag/js"]')) {
        cargarScript('https://www.googletagmanager.com/gtag/js?id=' + CONFIG.GA4_ID);
      }
      gtag('js', new Date());
      // send_page_view por defecto: GA4 ya cuenta la visita y el scroll solo.
      gtag('config', CONFIG.GA4_ID);
      ga4Listo = true;
      /* 11-11-2026: el Tree (/links/ y /t/) y cyber.js mandan sus eventos con
         window.gtag, pero gtag era una funcion local de este archivo y el
         gtag.js de Google no la define: esos eventos nunca salian. Se expone
         SOLO con consentimiento; revocar() la retira. */
      if (typeof window.gtag !== 'function') window.gtag = gtag;
    }
    if (CONFIG.META_PIXEL_ID) cargarPixel();
  }

  function cargarPixel() {
    /* Snippet oficial de Meta, con el mismo nombre de cola (fbq) que espera
       su plataforma. No se reescribe "más lindo": Meta valida que exista. */
    !function (f, b, e, v, n, t, s) {
      if (f.fbq) return; n = f.fbq = function () {
        n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
      };
      if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0';
      n.queue = []; t = b.createElement(e); t.async = !0; t.src = v;
      s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
    }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    window.fbq('init', CONFIG.META_PIXEL_ID);
    window.fbq('track', 'PageView');
    pixelListo = true;
  }

  /* ---------- Arranque ---------- */

  var decision = leerDecision();
  if (decision) {
    if (decision.analitica) cargarPlataformas();
  } else if (navigator.globalPrivacyControl !== true) {
    // Con Global Privacy Control el navegador ya dijo que no: no se pregunta.
    if (document.body) mostrarAviso();
    else document.addEventListener('DOMContentLoaded', mostrarAviso);
  }

  /* ---------- Envío de eventos ---------- */

  /* Un solo lugar por donde salen los eventos: si mañana se agrega otra
     plataforma (Clarity, TikTok), se toca solo esta función. */
  function evento(nombre, datos, eventoMeta) {
    datos = datos || {};
    if (ga4Listo) gtag('event', nombre, datos);
    if (pixelListo && eventoMeta) window.fbq('track', eventoMeta, datos);
    if (!ga4Listo && !pixelListo && window.console && window.localStorage.getItem('ggDebugMedicion')) {
      // Sin IDs cargados no se pierde el trabajo: se puede comprobar que los
      // disparadores funcionan poniendo ggDebugMedicion=1 en localStorage.
      console.log('[medicion]', nombre, eventoMeta || '', datos);
    }
  }

  /* ---------- Disparadores ---------- */

  /* Delegación en document: los botones flotantes y el widget de chat se
     inyectan por JS DESPUÉS de que carga la página, así que escuchar cada
     elemento uno por uno se perdería justamente los más importantes. */
  document.addEventListener('click', function (e) {
    if (TREE_CLIENTE) return;
    var el = e.target && e.target.closest ? e.target.closest('a, button') : null;
    if (!el) return;

    var href = el.getAttribute('href') || '';

    if (WHATSAPP.test(href)) {
      // La conversión real del negocio: 3 de los últimos clientes llegaron por
      // conversación, no por formulario.
      evento('contacto_whatsapp', { metodo: 'whatsapp', origen: ubicacion(el) }, 'Contact');
      return;
    }
    if (href.indexOf('mailto:') === 0) {
      evento('contacto_email', { metodo: 'email', origen: ubicacion(el) }, 'Contact');
      return;
    }
    if (/instagram\.com/i.test(href)) {
      evento('click_instagram', { origen: ubicacion(el) });
      return;
    }
    if (el.classList && el.classList.contains('gg-chat-fab')) {
      evento('chat_abierto', { origen: 'widget' });
      return;
    }
    if (el.id === 'ggChatSend') {
      // Preguntar por el chat es intención real, no una visita más.
      evento('chat_mensaje', { origen: 'widget' }, 'Contact');
    }
  }, true);

  /* De dónde salió el click: sirve para saber si convierte el botón flotante,
     el hero o el pie, que es lo que después se optimiza en las campañas. */
  function ubicacion(el) {
    if (el.closest('.floating-whatsapp, .floating-instagram, .gg-chat-fab')) return 'boton_flotante';
    if (el.closest('header, .site-header, .navbar')) return 'navbar';
    if (el.closest('.hero')) return 'hero';
    if (el.closest('footer, .site-footer')) return 'pie';
    return 'contenido';
  }

  /* Formulario de contacto: main.js lo envía por AJAX a formsubmit.co y avisa
     con "gg:lead-formulario" cuando formsubmit confirma (antes volvía a
     /contacto/?enviado=1; se deja por si algún formulario aún lo usa).
     Se marcan las dos cosas y NO significan lo mismo:
       submit  = apretó enviar (puede fallar o abandonar)
       enviado = formsubmit confirmó y lo devolvió  <- este es el lead de verdad
     El Lead de Meta y la conversión de Ads van SOLO en el segundo, si no se
     infla el número y las campañas optimizan hacia un dato falso. */
  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (form && form.classList && form.classList.contains('contact-form')) {
      evento('formulario_enviado_intento', {
        tipo_servicio: (form.querySelector('[name="tipo_servicio"]') || {}).value || ''
      });
    }
  }, true);

  document.addEventListener('gg:lead-formulario', function (e) {
    evento('lead_formulario', {
      metodo: 'formulario',
      tipo_servicio: (e.detail || {}).tipo_servicio || ''
    }, 'Lead');
  });

  if (/[?&]enviado=1/.test(window.location.search)) {
    evento('lead_formulario', { metodo: 'formulario' }, 'Lead');
  }

})();
