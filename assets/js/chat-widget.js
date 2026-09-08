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
    '.gg-chat-panel{position:fixed;right:1.2rem;bottom:16.2rem;z-index:32;width:min(360px,calc(100vw - 2.4rem));',
    'height:min(520px,calc(100vh - 19rem));background:#0d1a30;border:1px solid rgba(37,99,235,.25);',
    'border-radius:16px;box-shadow:0 24px 60px rgba(0,0,0,.5);display:none;flex-direction:column;overflow:hidden;',
    'font-family:"Inter",system-ui,sans-serif;}',
    '.gg-chat-panel.gg-open{display:flex;}',
    '.gg-chat-head{background:linear-gradient(135deg,#0A1428,#0f1f38);padding:.9rem 1.1rem;',
    'display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid rgba(37,99,235,.2);}',
    '.gg-chat-head strong{color:#fff;font-size:.88rem;font-family:"Montserrat",sans-serif;}',
    '.gg-chat-head span{display:block;color:#A8B3CF;font-size:.72rem;margin-top:.15rem;}',
    '.gg-chat-close{background:none;border:none;color:#A8B3CF;font-size:1.3rem;cursor:pointer;line-height:1;padding:.2rem;}',
    '.gg-chat-close:hover{color:#fff;}',
    '.gg-chat-body{flex:1;overflow-y:auto;padding:1rem;display:flex;flex-direction:column;gap:.65rem;}',
    '.gg-msg{max-width:85%;padding:.6rem .85rem;border-radius:12px;font-size:.85rem;line-height:1.45;white-space:pre-wrap;}',
    '.gg-msg-agente{align-self:flex-start;background:rgba(37,99,235,.14);color:#fff;border-bottom-left-radius:4px;}',
    '.gg-msg-usuario{align-self:flex-end;background:#FFB627;color:#0A1428;border-bottom-right-radius:4px;font-weight:500;}',
    '.gg-msg-error{align-self:flex-start;background:rgba(37,99,235,.14);color:#fff;',
    'border-left:3px solid #FFB627;border-bottom-left-radius:4px;}',
    '.gg-chat-foot{padding:.75rem;border-top:1px solid rgba(37,99,235,.2);display:flex;gap:.5rem;}',
    '.gg-chat-input{flex:1;background:#0A1428;border:1px solid rgba(37,99,235,.25);border-radius:999px;',
    'padding:.6rem 1rem;color:#fff;font-size:.85rem;outline:none;}',
    '.gg-chat-input:focus{border-color:#2563eb;}',
    '.gg-chat-send{background:#2563eb;border:none;border-radius:999px;width:2.4rem;height:2.4rem;flex-shrink:0;',
    'display:flex;align-items:center;justify-content:center;cursor:pointer;color:#fff;}',
    '.gg-chat-send:disabled{opacity:.5;cursor:default;}',
    '.gg-typing{align-self:flex-start;color:#A8B3CF;font-size:.78rem;font-style:italic;}',
    '@media(max-width:480px){.gg-chat-fab span{display:none;}.gg-chat-fab{padding:.85rem;min-width:3.2rem;justify-content:center;}}',
    /* 07-09-2026: Diego pidio el boton al centro, pero solo en desktop -- en
       mobile se queda apilado con WhatsApp/Instagram (poco ancho, el centro
       ahi tapa contenido). El panel se centra igual, para que abra justo
       arriba del boton en vez de quedar descuadrado a la derecha. */
    '@media(min-width:769px){',
    '.gg-chat-fab{right:auto;left:50%;transform:translateX(-50%);bottom:1.6rem;}',
    '.gg-chat-fab:hover{transform:translateX(-50%) translateY(-3px);}',
    '.gg-chat-panel{right:auto;left:50%;transform:translateX(-50%);bottom:5.4rem;}',
    '}',
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

  function agregarMensaje(texto, clase) {
    var div = document.createElement('div');
    div.className = 'gg-msg ' + clase;
    div.textContent = texto;
    body.appendChild(div);
    body.scrollTop = body.scrollHeight;
    return div;
  }

  var saludado = false;
  function abrir() {
    panel.classList.add('gg-open');
    if (!saludado) {
      agregarMensaje('¡Hola! Soy el asistente de GoGoDevS. Preguntame por servicios, precios o algún proyecto parecido al tuyo.', 'gg-msg-agente');
      saludado = true;
    }
    input.focus();
  }
  function cerrar() { panel.classList.remove('gg-open'); }

  fab.addEventListener('click', function () {
    if (panel.classList.contains('gg-open')) cerrar(); else abrir();
  });
  cerrarBtn.addEventListener('click', cerrar);

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
    indicador.textContent = 'Escribiendo...';
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
