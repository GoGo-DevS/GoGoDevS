/* ===========================================================================
   Campanas de GoGoDevS con fecha, que se apagan SOLAS
   ===========================================================================

   Hoy: NAVIDAD 2026. Antes fue el Cyber (05 al 12-10-2026), con este mismo
   mecanismo; por eso el archivo se llamaba cyber.js.

   POR QUE ASI (05-10-2026)
   gogodevs.cl es HTML estatico y se publica por FTP desde GitHub Actions. Si el
   fin de la campana dependiera de que alguien haga otro deploy, la campana se
   queda publicada: ya paso con los testimonios de ejemplo de Ruta Motors y con
   el horario [EJEMPLO], que vivieron semanas en produccion.

   Entonces la regla es al reves de lo habitual: todo lo de la campana nace
   OCULTO en el HTML y este script lo MUESTRA solo si hoy cae dentro de la
   ventana.

       sin JS            -> no se ve nada          (estado seguro)
       antes de la fecha -> no se ve nada
       dentro            -> se ve, con el contador
       despues           -> no se ve nada          sin tocar un archivo

   DOS VENTANAS (Navidad)
   - DECORACION: luces en el menu, gorro en el logo y nieve en la llegada. No
     dice ningun precio, asi que puede empezar antes.
   - OFERTA: franja, precios de Navidad tachando la lista, la seccion de la
     portada y el contador. Empieza el 23-11 a proposito: Enoturismo Chile
     decide su propuesta (15% de descuento) hasta el 20-11 y Jorge GP decide su
     sitio esta semana. Si vieran un precio publico mejor que el que se les
     ofrecio por escrito mientras deciden, su "precio especial" queda peor que
     el de un desconocido. El piso lo fija el CRM.

   LOS PRECIOS DE LISTA NO SE REEMPLAZAN, SE TACHAN. Protege el piso: cuando
   alguien pida el precio de Navidad en marzo, el sitio ya dijo cual era el
   normal y hasta cuando valia el otro. La flexibilidad va en las cuotas.

   PARA LA PROXIMA CAMPANA: cambiar CAMPANA (fechas, id, tema) aca y los textos
   y precios en las paginas (buscar data-campana). Para sacarla: borrar las
   fechas o el <script>.
   =========================================================================== */
(function () {
  "use strict";

  // Hora de Chile: UTC-3 de septiembre a abril.
  var CAMPANA = {
    id: "navidad_2026",
    tema: "tema-navidad",
    decoracion: { inicio: "2026-11-16T00:00:00-03:00", fin: "2026-12-26T23:59:59-03:00" },
    oferta:     { inicio: "2026-11-23T00:00:00-03:00", fin: "2026-12-24T23:59:59-03:00" }
  };

  function dentro(ventana, cuando) {
    return cuando >= new Date(ventana.inicio) && cuando <= new Date(ventana.fin);
  }

  var ahora = new Date();
  if (dentro(CAMPANA.decoracion, ahora)) decorar();
  if (dentro(CAMPANA.oferta, ahora)) ofertar();

  /* -------------------------------------------------------------------------
     DECORACION
     ------------------------------------------------------------------------- */
  function decorar() {
    document.documentElement.classList.add(CAMPANA.tema);
    // Quien pidio menos movimiento al sistema no ve nieve: las luces quedan
    // quietas por CSS y la pagina se lee igual. Nunca quitar este respeto para
    // "que se vea": a algunas personas el movimiento les da mareo o migrana.
    var quieto = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!quieto) nevar();
  }

  function nevar() {
    var lienzo = document.createElement("canvas");
    lienzo.className = "campana-nieve";
    lienzo.setAttribute("aria-hidden", "true");
    // Estilo propio: /links/ y /t/ (el Tree) no cargan style.css, y sin esto
    // el lienzo quedaba en el flujo de la pagina y la desbordaba 16 px.
    lienzo.style.cssText = "position:fixed;left:0;top:0;z-index:15;pointer-events:none;";
    document.body.appendChild(lienzo);
    var ctx = lienzo.getContext("2d");
    if (!ctx) return;

    var copos = [];
    var ancho = 0, alto = 0, escala = 1, corriendo = false, ultimo = 0;

    function medir() {
      escala = Math.min(window.devicePixelRatio || 1, 2);
      // clientWidth y no innerWidth: innerWidth incluye la barra de scroll.
      ancho = document.documentElement.clientWidth || window.innerWidth;
      alto = window.innerHeight;
      lienzo.width = Math.round(ancho * escala);
      lienzo.height = Math.round(alto * escala);
      lienzo.style.width = ancho + "px";
      lienzo.style.height = alto + "px";
      ctx.setTransform(escala, 0, 0, escala, 0, 0);
      // Pocos copos: es un adorno, no una tormenta que tape el texto.
      var cuantos = Math.round(Math.min(70, Math.max(24, ancho / 20)));
      while (copos.length < cuantos) copos.push(nuevo(true));
      copos.length = cuantos;
    }

    function nuevo(enCualquierAltura) {
      var r = 0.8 + Math.random() * 2.4;
      return {
        x: Math.random() * ancho,
        y: enCualquierAltura ? Math.random() * alto : -6,
        r: r,
        v: 18 + r * 14 + Math.random() * 12,     // px por segundo
        fase: Math.random() * Math.PI * 2,
        vaiven: 8 + Math.random() * 18,
        a: 0.35 + Math.random() * 0.5
      };
    }

    // La nieve es para la llegada: se desvanece al bajar y se detiene del
    // todo cuando ya no se ve, para no gastar bateria mientras alguien lee.
    function opacidad() {
      return Math.max(0, 1 - window.scrollY / (alto * 0.9 || 1));
    }

    function cuadro(t) {
      if (!corriendo) return;
      var dt = Math.min(0.05, ((t - ultimo) / 1000) || 0);
      ultimo = t;
      var op = opacidad();
      lienzo.style.opacity = op.toFixed(3);
      if (op <= 0) { corriendo = false; return; }
      ctx.clearRect(0, 0, ancho, alto);
      for (var i = 0; i < copos.length; i++) {
        var c = copos[i];
        c.y += c.v * dt;
        c.fase += dt * 0.9;
        var x = c.x + Math.sin(c.fase) * c.vaiven;
        if (c.y > alto + 6) { copos[i] = nuevo(false); continue; }
        ctx.beginPath();
        ctx.arc(x, c.y, c.r, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(255,255,255," + c.a + ")";
        ctx.fill();
      }
      window.requestAnimationFrame(cuadro);
    }

    function arrancar() {
      if (corriendo || document.hidden || opacidad() <= 0) return;
      corriendo = true;
      ultimo = performance.now();
      window.requestAnimationFrame(cuadro);
    }

    medir();
    arrancar();
    window.addEventListener("resize", medir, { passive: true });
    window.addEventListener("scroll", arrancar, { passive: true });
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) corriendo = false; else arrancar();
    });
  }

  /* -------------------------------------------------------------------------
     OFERTA
     ------------------------------------------------------------------------- */
  function ofertar() {
    var FIN = new Date(CAMPANA.oferta.fin);

    // --- 1. Mostrar lo que el HTML dejo oculto -----------------------------
    // Y esconder el precio de lista "normal". Los dos existen en el HTML a
    // proposito: la pagina es correcta sin JS (precio normal) y correcta con
    // JS dentro de la ventana.
    var bloques = document.querySelectorAll("[data-campana]");
    if (!bloques.length) return;
    for (var i = 0; i < bloques.length; i++) bloques[i].hidden = false;
    var normales = document.querySelectorAll("[data-campana-normal]");
    for (var n = 0; n < normales.length; n++) normales[n].hidden = true;
    document.documentElement.classList.add("campana-activa");

    // --- 2. Contador ---------------------------------------------------------
    // Cada minuto, no cada segundo: un reloj al segundo en una franja fija es
    // ruido y obliga a repintar sin que nadie lo mire.
    var salidas = document.querySelectorAll("[data-campana-cuenta]");

    function plural(n, uno, varios) {
      return n + " " + (n === 1 ? uno : varios);
    }

    function texto() {
      var ms = FIN - new Date();
      if (ms <= 0) return null;
      var min = Math.floor(ms / 60000);
      var dias = Math.floor(min / 1440);
      var horas = Math.floor((min % 1440) / 60);
      if (dias >= 2) return "Quedan " + plural(dias, "día", "días");
      if (dias === 1) return "Queda 1 día y " + plural(horas, "hora", "horas");
      if (horas >= 1) return "Quedan " + plural(horas, "hora", "horas");
      return "Últimos " + plural(Math.max(min, 1), "minuto", "minutos");
    }

    function pintar() {
      var t = texto();
      if (t === null) {
        // Vencio con la pestana abierta: se esconde en el momento y vuelve el
        // precio de lista, sin esperar a que alguien recargue.
        for (var j = 0; j < bloques.length; j++) bloques[j].hidden = true;
        for (var q = 0; q < normales.length; q++) normales[q].hidden = false;
        document.documentElement.classList.remove("campana-activa");
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
    // Diego quiere saber si la campana genera flujo, no suponerlo. Eventos
    // propios, separados de los contactos normales. window.gtag solo existe si
    // la persona acepto la analitica (ver medicion.js).
    function medir(nombre, extra) {
      if (typeof window.gtag !== "function") return;
      var datos = { campana: CAMPANA.id };
      if (extra) for (var p in extra) if (Object.prototype.hasOwnProperty.call(extra, p)) datos[p] = extra[p];
      window.gtag("event", nombre, datos);
    }

    medir("campana_vista");

    document.addEventListener("click", function (ev) {
      var el = ev.target && ev.target.closest ? ev.target.closest("[data-campana-cta]") : null;
      if (!el) return;
      medir("campana_clic", { plan: el.getAttribute("data-campana-cta") || "sin_plan" });
    });
  }
})();
