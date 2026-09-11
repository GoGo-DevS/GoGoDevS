/* Agente IA de gogodevs.cl (07-09-2026).
   Widget autocontenido: inyecta su propio CSS y HTML, así que agregarlo a
   una página nueva es solo un <script src="/assets/js/chat-widget.js">.
   Le pega al endpoint en GoGoCRM (ya desplegado) — la API key de Gemini
   nunca toca el navegador, vive solo del lado del servidor. */
(function () {
  'use strict';

  var ENDPOINT = 'https://gogocrm-h050.onrender.com/agente-web/chat/';
  var historial = []; // [{rol:'usuario'|'agente', texto:'...'}]

  var estilos = document.createElement('style');
  estilos.textContent = [
    '.gg-chat-fab{position:fixed;right:1.2rem;bottom:12.4rem;z-index:31;',
    'display:inline-flex;align-items:center;gap:.7rem;min-height:3.2rem;',
    'padding:.85rem 1.1rem;border-radius:999px;border:none;cursor:pointer;',
    'background:linear-gradient(135deg,#2563eb,#FFB627);color:#0A1428;',
    'box-shadow:0 18px 42px rgba(37,99,235,.32);font-family:"Montserrat",sans-serif;',
    'font-size:.78rem;font-weight:700;letter-spacing:.04em;transition:transform .2s,box-shadow .2s;}',
    '.gg-chat-fab:hover{transform:translateY(-3px);box-shadow:0 24px 52px rgba(37,99,235,.42);}',
    '.gg-chat-fab svg{width:1.3rem;height:1.3rem;flex-shrink:0;}',
    '.gg-chat-panel{position:fixed;right:1.2rem;bottom:16.2rem;z-index:32;width:min(400px,calc(100vw - 2rem));',
    'height:min(600px,calc(100vh - 18rem));background:#0d1a30;border:1px solid rgba(37,99,235,.25);',
    'border-radius:22px;box-shadow:0 24px 60px rgba(0,0,0,.5);display:flex;flex-direction:column;overflow:hidden;',
    'font-family:"Montserrat",system-ui,sans-serif;',
    /* 11-09: el panel se abria de golpe porque se alternaba `display`, que NO es
       animable -- no hay estado intermedio entre none y flex. Ahora vive siempre
       en flex y lo que cambia son opacidad, escala y visibilidad, que si se
       pueden transicionar.
       `visibility` va con retraso SOLO al cerrar: sin eso el panel desaparece en
       el primer fotograma y la animacion de salida no se ve. Al abrir el retraso
       es 0, porque tiene que ser visible desde el principio para animarse. */
    'opacity:0;visibility:hidden;pointer-events:none;',
    'transform:translateY(14px) scale(.96);transform-origin:100% 100%;',
    'transition:opacity .28s cubic-bezier(.16,1,.3,1),transform .34s cubic-bezier(.16,1,.3,1),visibility 0s linear .34s;}',
    '.gg-chat-panel.gg-open{opacity:1;visibility:visible;pointer-events:auto;',
    'transform:translateY(0) scale(1);transition-delay:0s,0s,0s;}',
    '@media (prefers-reduced-motion: reduce){.gg-chat-panel{transition:none;transform:none;}',
    '.gg-chat-panel.gg-open{transform:none;}}',
    '.gg-chat-head{background:linear-gradient(135deg,#0A1428,#0f1f38);padding:.9rem 1.1rem;',
    'display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid rgba(37,99,235,.2);}',
    '.gg-chat-head strong{color:#fff;font-size:.88rem;font-family:"Montserrat",sans-serif;}',
    '.gg-chat-head span{display:block;color:#A8B3CF;font-size:.72rem;margin-top:.15rem;}',
    '.gg-chat-close{background:none;border:none;color:#A8B3CF;font-size:1.3rem;cursor:pointer;line-height:1;padding:.2rem;}',
    '.gg-chat-close:hover{color:#fff;}',
    /* overscroll-behavior: al llegar al tope de la lista, la rueda dejaba de
   mover el chat y empezaba a mover la pagina de atras. `contain` corta esa
   herencia sin bloquear el scroll del propio panel. */
    '.gg-chat-body{flex:1;overflow-y:auto;overscroll-behavior:contain;padding:1rem;display:flex;flex-direction:column;gap:.65rem;}',
    '.gg-msg{max-width:85%;padding:.65rem .95rem;border-radius:18px;font-size:.85rem;line-height:1.5;}',
    '.gg-msg-agente{align-self:flex-start;background:rgba(37,99,235,.14);color:#fff;border-bottom-left-radius:6px;}',
    '.gg-msg-usuario{align-self:flex-end;background:#FFB627;color:#0A1428;border-bottom-right-radius:6px;font-weight:500;white-space:pre-wrap;}',
    '.gg-msg-error{align-self:flex-start;background:rgba(37,99,235,.14);color:#fff;',
    'border-left:3px solid #FFB627;border-bottom-left-radius:6px;}',
    '.gg-msg p{margin:0 0 .55rem;}',
    '.gg-msg p:last-child{margin-bottom:0;}',
    '.gg-msg ul{list-style:disc;margin:.2rem 0 .55rem;padding-left:1.15rem;}',
    '.gg-msg ul:last-child{margin-bottom:0;}',
    '.gg-msg li{margin-bottom:.3rem;}',
    '.gg-msg li::marker{color:#FFB627;}',
    '.gg-msg strong{font-weight:700;}',
    '.gg-chat-foot{padding:.75rem;border-top:1px solid rgba(37,99,235,.2);display:flex;gap:.5rem;}',
    '.gg-chat-input{flex:1;background:#0A1428;border:1px solid rgba(37,99,235,.25);border-radius:999px;',
    'padding:.6rem 1rem;color:#fff;font-size:.85rem;outline:none;}',
    '.gg-chat-input:focus{border-color:#2563eb;}',
    '.gg-chat-send{background:#2563eb;border:none;border-radius:999px;width:2.4rem;height:2.4rem;flex-shrink:0;',
    'display:flex;align-items:center;justify-content:center;cursor:pointer;color:#fff;}',
    '.gg-chat-send:disabled{opacity:.5;cursor:default;}',
    '.gg-typing{align-self:flex-start;background:rgba(37,99,235,.14);border-radius:18px;',
    'border-bottom-left-radius:6px;padding:.75rem 1rem;display:flex;gap:.3rem;}',
    '.gg-typing i{width:.4rem;height:.4rem;border-radius:50%;background:#A8B3CF;',
    'animation:ggBounce 1.2s infinite;}',
    '.gg-typing i:nth-child(2){animation-delay:.15s;}',
    '.gg-typing i:nth-child(3){animation-delay:.3s;}',
    '@keyframes ggBounce{0%,60%,100%{transform:translateY(0);opacity:.5;}30%{transform:translateY(-4px);opacity:1;}}',
    '@media(max-width:480px){.gg-chat-fab span{display:none;}.gg-chat-fab{padding:.85rem;min-width:3.2rem;justify-content:center;}}',
    /* 07-09-2026: Diego pidio el boton al centro, pero solo en desktop -- en
       mobile se queda apilado con WhatsApp/Instagram (poco ancho, el centro
       ahi tapa contenido). El panel se centra igual, para que abra justo
       arriba del boton en vez de quedar descuadrado a la derecha. */
    '@media(min-width:769px){',
    '.gg-chat-fab{right:auto;left:50%;transform:translateX(-50%);bottom:1.6rem;}',
    '.gg-chat-fab:hover{transform:translateX(-50%) translateY(-3px);}',
    /* OJO: en escritorio el panel se CENTRA con translateX(-50%), y eso pisaba
       entera la transformacion de entrada -- quedaba solo el fade, sin el
       deslizamiento ni la escala. Las transformaciones no se heredan: la de
       abajo reemplaza a la de arriba completa. Por eso aca se COMPONEN las dos
       en la misma declaracion. */
    '.gg-chat-panel{right:auto;left:50%;bottom:5.4rem;',
    'width:440px;height:min(680px,calc(100vh - 9rem));',
    'transform-origin:50% 100%;transform:translateX(-50%) translateY(14px) scale(.96);}',
    '.gg-chat-panel.gg-open{transform:translateX(-50%) translateY(0) scale(1);}',
    '@media(prefers-reduced-motion:reduce){',
    '.gg-chat-panel,.gg-chat-panel.gg-open{transform:translateX(-50%);}}',
    '}',
    '@media(prefers-reduced-motion:reduce){.gg-typing i{animation:none;opacity:.8;}}',
  ].join('');
  document.head.appendChild(estilos);

  var fab = document.createElement('button');
  fab.className = 'gg-chat-fab';
  fab.setAttribute('aria-label', 'Habla con nuestro asistente');
  fab.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg><span>Pregúntanos</span>';

  var panel = document.createElement('div');
  panel.className = 'gg-chat-panel';
  panel.innerHTML =
    '<div class="gg-chat-head">' +
      '<div><strong>Asistente GoGoDevS</strong><span>Responde con info real de la agencia</span></div>' +
      '<button class="gg-chat-close" aria-label="Cerrar">&times;</button>' +
    '</div>' +
    '<div class="gg-chat-body" id="ggChatBody"></div>' +
    '<div class="gg-chat-foot">' +
      '<input class="gg-chat-input" id="ggChatInput" type="text" placeholder="Escribe tu pregunta..." maxlength="500">' +
      '<button class="gg-chat-send" id="ggChatSend" aria-label="Enviar">' +
        '<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M2 21l21-9L2 3v7l15 2-15 2z"/></svg>' +
      '</button>' +
    '</div>';

  document.body.appendChild(fab);
  document.body.appendChild(panel);

  var body = panel.querySelector('#ggChatBody');
  var input = panel.querySelector('#ggChatInput');
  var enviarBtn = panel.querySelector('#ggChatSend');
  var cerrarBtn = panel.querySelector('.gg-chat-close');

  function escaparHtml(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  // Gemini/Groq contestan en markdown liviano (**negrita**, listas con "- ").
  // Sin esto salian los asteriscos literales en pantalla. Escapa TODO primero
  // y solo despues abre las etiquetas propias -- nunca inyecta HTML ajeno.
  function formatearMarkdown(texto) {
    var html = escaparHtml(texto).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    var lineas = html.split('\n');
    var salida = '';
    var enLista = false;
    lineas.forEach(function (linea) {
      var t = linea.trim();
      if (/^[-*]\s+/.test(t)) {
        if (!enLista) { salida += '<ul>'; enLista = true; }
        salida += '<li>' + t.replace(/^[-*]\s+/, '') + '</li>';
      } else {
        if (enLista) { salida += '</ul>'; enLista = false; }
        if (t) salida += '<p>' + t + '</p>';
      }
    });
    if (enLista) salida += '</ul>';
    return salida;
  }

  function agregarMensaje(texto, clase) {
    var div = document.createElement('div');
    div.className = 'gg-msg ' + clase;
    if (clase === 'gg-msg-usuario') {
      div.textContent = texto;
    } else {
      div.innerHTML = formatearMarkdown(texto);
    }
    body.appendChild(div);
    body.scrollTop = body.scrollHeight;
    return div;
  }

  var saludado = false;
  function abrir(porElUsuario) {
    panel.classList.add('gg-open');
    if (!saludado) {
      agregarMensaje('¡Hola! 👋 Soy el asistente de GoGoDevS. Cuéntame qué necesitas: un sitio, una tienda online o un sistema a medida.', 'gg-msg-agente');
      saludado = true;
    }
    // El foco solo se toma cuando el visitante abrio el chat el mismo. En la
    // apertura automatica robarle el cursor mientras lee es agresivo.
    if (porElUsuario !== false) input.focus();
  }
  function cerrar() { panel.classList.remove('gg-open'); }

  fab.addEventListener('click', function () {
    if (panel.classList.contains('gg-open')) cerrar(); else abrir();
  });
  cerrarBtn.addEventListener('click', function () {
    cerrar();
    // Si lo cerro a mano, NO se vuelve a abrir solo en toda la sesion. Un chat
    // que reaparece despues de que lo cerraste es el motivo por el que la gente
    // termina odiando estos widgets.
    try { sessionStorage.setItem('gg_chat_cerrado', '1'); } catch (e) {}
  });

  /* APERTURA AUTOMATICA — solo escritorio.
   *
   * En celular NO se abre nunca: el panel tapa la pantalla completa y lo
   * primero que hace el visitante es buscar la X. En escritorio convive con el
   * contenido, que es el caso que Diego vio y le gusto.
   *
   * Tres frenos, y cada uno evita una forma distinta de molestar:
   *   1. una sola vez por sesion -- no en cada pagina que abra;
   *   2. nunca si ya lo cerro a mano;
   *   3. nunca si el visitante pidio menos movimiento.
   */
  (function autoApertura() {
    var esEscritorio = window.matchMedia('(min-width: 1024px) and (hover: hover) and (pointer: fine)').matches;
    if (!esEscritorio) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    try {
      if (sessionStorage.getItem('gg_chat_cerrado')) return;
      if (sessionStorage.getItem('gg_chat_autoabierto')) return;
    } catch (e) { return; }   // sin sessionStorage no hay memoria: mejor no abrir

    setTimeout(function () {
      if (panel.classList.contains('gg-open')) return;
      try { sessionStorage.setItem('gg_chat_autoabierto', '1'); } catch (e) {}
      abrir(false);
      // El foco NO se roba al abrir solo: si el visitante esta leyendo o
      // escribiendo en otro campo, saltarle el cursor al chat es agresivo.
      // Al abrirlo con el boton si se enfoca, porque ahi lo pidio el.
      if (document.activeElement === document.body) { /* nada */ }
      else { input.blur(); }
    }, 4000);
  })();

  var enviando = false;
  function enviar() {
    var texto = input.value.trim();
    if (!texto || enviando) return;
    agregarMensaje(texto, 'gg-msg-usuario');
    historial.push({ rol: 'usuario', texto: texto });
    input.value = '';
    enviando = true;
    enviarBtn.disabled = true;

    var indicador = document.createElement('div');
    indicador.className = 'gg-typing';
    indicador.setAttribute('aria-label', 'Escribiendo...');
    indicador.innerHTML = '<i></i><i></i><i></i>';
    body.appendChild(indicador);
    body.scrollTop = body.scrollHeight;

    fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mensaje: texto, historial: historial }),
    })
      .then(function (r) { return r.json().then(function (data) { return { ok: r.ok, data: data }; }); })
      .then(function (res) {
        indicador.remove();
        if (res.ok && res.data.respuesta) {
          agregarMensaje(res.data.respuesta, 'gg-msg-agente');
          historial.push({ rol: 'agente', texto: res.data.respuesta });
        } else {
          agregarMensaje(res.data.error || 'Algo salió mal. Escríbenos por WhatsApp: +56 9 5639 2509', 'gg-msg-error');
        }
      })
      .catch(function () {
        indicador.remove();
        agregarMensaje('No pude conectarme. Escríbenos directo por WhatsApp: +56 9 5639 2509', 'gg-msg-error');
      })
      .finally(function () {
        enviando = false;
        enviarBtn.disabled = false;
      });
  }

  enviarBtn.addEventListener('click', enviar);
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') enviar();
  });
})();
