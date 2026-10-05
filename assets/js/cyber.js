/* ===========================================================================
   Cyber GoGoDevS — campana con fecha, que se apaga SOLA
   ===========================================================================

   POR QUE ASI (05-10-2026)
   gogodevs.cl es HTML estatico y se publica por FTP desde GitHub Actions. Si el
   fin de la campana dependiera de que alguien haga otro deploy, el "Cyber" se
   queda publicado en diciembre: ya paso con los testimonios de ejemplo de Ruta
   Motors y con el horario [EJEMPLO], que vivieron semanas en produccion.

   Entonces la regla es al reves de lo habitual: el bloque nace OCULTO en el
   HTML y este script lo MUESTRA solo si hoy cae dentro de la ventana.

       sin JS            -> no se ve nada          (estado seguro)
       antes de la fecha -> no se ve nada
       dentro            -> se ve, con el contador
       despues           -> no se ve nada          sin tocar un archivo

   Lo unico que hay que cambiar para cerrar antes es FIN. Y lo unico que hay que
   editar para la proxima campana es este archivo, no las nueve paginas.

   LOS PRECIOS DE LISTA NO SE REEMPLAZAN, SE TACHAN. Es a proposito: protege el
   piso. Cuando alguien pida el precio Cyber en noviembre, el sitio ya dijo cual
   era el precio normal y hasta cuando valia el otro. Ver la regla de Diego de
   que la flexibilidad va en las cuotas y no bajando el precio de lista.
   =========================================================================== */
(function () {
  "use strict";

  // Ventana de la campana. Hora de Chile (UTC-3 en octubre).
  var INICIO = new Date("2026-10-05T00:00:00-03:00");
  var FIN    = new Date("2026-10-12T23:59:59-03:00");

  var ahora = new Date();
  if (ahora < INICIO || ahora > FIN) return;   // fuera de ventana: no se toca nada

  // --- 1. Mostrar lo que el HTML dejo oculto -------------------------------
  // Y esconder el precio de lista, que es el que se ve cuando NO hay campana.
  // Los dos existen en el HTML a proposito: asi la pagina es correcta sin JS
  // (muestra el precio normal) y correcta con JS dentro de la ventana.
  var bloques = document.querySelectorAll("[data-cyber]");
  if (!bloques.length) return;
  for (var i = 0; i < bloques.length; i++) {
    bloques[i].hidden = false;
  }
  var normales = document.querySelectorAll("[data-cyber-normal]");
  for (var n = 0; n < normales.length; n++) {
    normales[n].hidden = true;
  }

  // --- 2. Contador ---------------------------------------------------------
  // Se actualiza cada minuto, no cada segundo: un reloj al segundo en una
  // franja fija es ruido y obliga a repintar sin que nadie lo mire.
  var salidas = document.querySelectorAll("[data-cyber-cuenta]");

  function plural(n, uno, varios) {
    return n + " " + (n === 1 ? uno : varios);
  }

  function texto() {
    var ms = FIN - new Date();
    if (ms <= 0) return null;
    var min = Math.floor(ms / 60000);
    var dias = Math.floor(min / 1440);
    var horas = Math.floor((min % 1440) / 60);
    if (dias >= 1) return "Quedan " + plural(dias, "día", "días") + " y " + plural(horas, "hora", "horas");
    if (horas >= 1) return "Quedan " + plural(horas, "hora", "horas");
    return "Últimos " + plural(Math.max(min, 1), "minuto", "minutos");
  }

  function pintar() {
    var t = texto();
    if (t === null) {
      // La campana vencio con la pestana abierta: se esconde en el momento y
      // vuelve el precio de lista, sin esperar a que alguien recargue.
      for (var j = 0; j < bloques.length; j++) bloques[j].hidden = true;
      for (var q = 0; q < normales.length; q++) normales[q].hidden = false;
      return false;
    }
    for (var k = 0; k < salidas.length; k++) salidas[k].textContent = t;
    return true;
  }

  if (pintar()) {
    var reloj = setInterval(function () {
      if (!pintar()) clearInterval(reloj);
    }, 60000);
  }

  // --- 3. Medicion ---------------------------------------------------------
  // Diego quiere saber si la campana genera flujo, no suponerlo. Un evento
  // propio, separado de los contactos normales, para poder comparar la semana
  // del Cyber contra la anterior en GA4.
  function medir(nombre, extra) {
    if (typeof window.gtag !== "function") return;
    var datos = { campana: "cyber_2026_10" };
    if (extra) for (var p in extra) if (Object.prototype.hasOwnProperty.call(extra, p)) datos[p] = extra[p];
    window.gtag("event", nombre, datos);
  }

  medir("cyber_visto");

  document.addEventListener("click", function (ev) {
    var el = ev.target && ev.target.closest ? ev.target.closest("[data-cyber-cta]") : null;
    if (!el) return;
    medir("cyber_clic", { plan: el.getAttribute("data-cyber-cta") || "sin_plan" });
  });
})();
