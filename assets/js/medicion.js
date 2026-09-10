/* Medición de gogodevs.cl — 10-09-2026.

   Contexto: el sitio no medía NADA (ni GA4, ni Tag Manager, ni Pixel de Meta).
   Diego quiere pagar campañas en Meta y Google Ads, y sin esto no hay forma de
   saber qué campaña trae clientes: se paga a ciegas y no se puede optimizar.

   Todo vive en UN archivo a propósito. El sitio son 30 HTML sueltos sin
   plantillas: si el código de medición se pega en cada uno, la próxima vez que
   haya que cambiar un evento hay que tocar 30 archivos y uno se queda atrás.

   IDs vacíos = esa plataforma NO carga. Así este archivo se puede subir hoy y
   activarse cuando existan las cuentas, sin tocar nada más que estas líneas.

   Consentimiento de cookies: no se agrega banner. El público es Chile, que no
   exige el opt-in previo del RGPD. Si algún día se pauta a Europa, hay que
   revisarlo. */
(function () {
  'use strict';

  var CONFIG = {
    GA4_ID: '',       // G-XXXXXXXXXX  (Google Analytics 4)
    META_PIXEL_ID: '' // 15 dígitos    (Meta / Facebook Pixel)
  };

  var WHATSAPP = /(?:wa\.me|api\.whatsapp\.com|web\.whatsapp\.com)/i;

  /* ---------- Carga de plataformas ---------- */

  function cargarScript(src) {
    var s = document.createElement('script');
    s.async = true;
    s.src = src;
    document.head.appendChild(s);
  }

  var ga4Listo = false;
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }

  if (CONFIG.GA4_ID) {
    cargarScript('https://www.googletagmanager.com/gtag/js?id=' + CONFIG.GA4_ID);
    gtag('js', new Date());
    // send_page_view por defecto: GA4 ya cuenta la visita y el scroll solo.
    gtag('config', CONFIG.GA4_ID);
    ga4Listo = true;
  }

  var pixelListo = false;
  if (CONFIG.META_PIXEL_ID) {
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

  /* Formulario de contacto: se envía a formsubmit.co (fuera del sitio) y vuelve
     a /contacto/?enviado=1. Se marcan las dos cosas y NO significan lo mismo:
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

  if (/[?&]enviado=1/.test(window.location.search)) {
    evento('lead_formulario', { metodo: 'formulario' }, 'Lead');
  }

})();
