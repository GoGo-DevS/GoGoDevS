/* Cotizador en 4 pasos — gogodevs.cl/cotizar/  (11-09-2026)
 *
 * Por que existe: el sitio mandaba todo a WhatsApp y el prospecto llegaba sin
 * decir que quiere ni con cuanto cuenta. Cada conversacion empezaba de cero.
 * Con los pasos, la consulta llega calificada y con presupuesto declarado.
 *
 * Por que TODO vive en el cliente: gogodevs.cl es estatico (se sube por lftp a
 * DirectAdmin, no hay servidor propio). El envio lo hace FormSubmit, igual que
 * el formulario de /contacto/, y main.js ya sabe mandarlo por AJAX y avisar a
 * medicion.js. Aca solo se controla el avance entre pasos.
 *
 * REGLA: si el JS no carga, la pagina NO puede quedar inservible. Por eso los
 * cuatro paneles se muestran de corrido cuando este script no corre (ver la
 * clase `js-cot` que se pone recien al arrancar) y el formulario se envia igual.
 */
(function () {
  "use strict";

  var form = document.getElementById("form-cotizar");
  if (!form) return;

  var paneles = Array.prototype.slice.call(form.querySelectorAll(".cot-panel"));
  var pasos = Array.prototype.slice.call(document.querySelectorAll(".cot-paso"));
  var btnAtras = document.getElementById("cot-atras");
  var btnSiguiente = document.getElementById("cot-siguiente");
  var btnEnviar = document.getElementById("cot-enviar");
  var error = document.getElementById("cot-error");
  if (!paneles.length || !btnSiguiente) return;

  var actual = 0;

  function pintar() {
    paneles.forEach(function (p, i) { p.classList.toggle("is-activo", i === actual); });
    pasos.forEach(function (p, i) {
      p.classList.toggle("is-activo", i === actual);
      p.classList.toggle("is-hecho", i < actual);
    });
    btnAtras.hidden = actual === 0;
    var ultimo = actual === paneles.length - 1;
    btnSiguiente.hidden = ultimo;
    btnEnviar.hidden = !ultimo;
    error.hidden = true;
  }

  /* Valida SOLO el panel visible. `form.reportValidity()` revisaria tambien los
   * campos de los pasos que todavia no se ven, y el navegador intenta enfocar un
   * campo oculto: no muestra ningun mensaje y el boton parece que no hace nada. */
  function panelValido() {
    var campos = paneles[actual].querySelectorAll("input, select, textarea");
    for (var i = 0; i < campos.length; i++) {
      if (!campos[i].checkValidity()) {
        error.textContent = campos[i].type === "radio"
          ? "Elige una opcion para continuar."
          : "Revisa este paso antes de seguir.";
        error.hidden = false;
        if (campos[i].type !== "radio" && campos[i].type !== "checkbox") campos[i].focus();
        return false;
      }
    }
    return true;
  }

  btnSiguiente.addEventListener("click", function () {
    if (!panelValido()) return;
    if (actual < paneles.length - 1) {
      actual++;
      pintar();
      // Volver arriba del formulario: en celular el paso nuevo nace fuera de
      // pantalla y parece que no paso nada.
      var caja = document.querySelector(".cot-caja");
      if (caja) caja.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });

  btnAtras.addEventListener("click", function () {
    if (actual > 0) {
      actual--;
      pintar();
      var caja = document.querySelector(".cot-caja");
      if (caja) caja.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });

  // Elegir una opcion en un paso de una sola respuesta avanza solo: son 4 pasos,
  // y obligar a un clic extra en "Siguiente" por cada uno es friccion regalada.
  form.addEventListener("change", function (e) {
    if (e.target.type !== "radio") return;
    if (!paneles[actual].contains(e.target)) return;
    if (actual === paneles.length - 1) return;
    setTimeout(function () { btnSiguiente.click(); }, 220);
  });

  // Enter no debe enviar el formulario en los pasos intermedios.
  form.addEventListener("keydown", function (e) {
    if (e.key !== "Enter") return;
    if (e.target.tagName === "TEXTAREA") return;
    if (actual < paneles.length - 1) { e.preventDefault(); btnSiguiente.click(); }
  });

  document.documentElement.classList.add("js-cot");
  pintar();
})();
