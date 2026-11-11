// Worker de Cloudflare: sirve un GoGoDevS Tree en el dominio propio del cliente
// (tunegocio.cl) sin que se vea gogodevs.cl. Se pega tal cual en la cuenta de
// Cloudflare del cliente y se cambia SOLO la constante ORIGEN.
// Guia completa: docs/tree/dominio-propio.md
//
// Que hace:
//   tunegocio.cl/            -> https://www.gogodevs.cl/t/<slug>/
//   tunegocio.cl/logo.webp   -> https://www.gogodevs.cl/t/<slug>/logo.webp
//   www.tunegocio.cl/...     -> 301 a tunegocio.cl/... (una sola direccion)
// Nunca sale de la carpeta del Tree, nunca reenvia una redireccion del origen
// (llevaria a gogodevs.cl) y un 404 del origen se responde aca, sin la pagina
// de error de GoGoDevS.

const ORIGEN = "https://www.gogodevs.cl/t/SLUG/"; // <- cambiar SLUG

export default {
  async fetch(request) {
    if (request.method !== "GET" && request.method !== "HEAD") {
      return new Response("Método no permitido", { status: 405, headers: { Allow: "GET, HEAD" } });
    }
    const url = new URL(request.url);
    if (url.hostname.startsWith("www.")) {
      url.hostname = url.hostname.slice(4);
      return Response.redirect(url.toString(), 301);
    }
    const ruta = url.pathname.replace(/^\/+/, "");
    if (ruta.includes("..") || ruta.includes("//") || ruta.includes("\\")) {
      return noEncontrado();
    }
    const destino = new URL(ruta, ORIGEN);
    if (!destino.href.startsWith(ORIGEN)) return noEncontrado();
    destino.search = url.search;

    const respuesta = await fetch(destino.href, {
      method: request.method,
      headers: { "User-Agent": request.headers.get("User-Agent") || "", Accept: request.headers.get("Accept") || "*/*" },
      redirect: "manual",
      cf: { cacheEverything: true, cacheTtl: 300 },
    });
    if (respuesta.status >= 300 && respuesta.status < 400) return noEncontrado();
    if (respuesta.status === 404) return noEncontrado();

    const salida = new Response(respuesta.body, respuesta);
    salida.headers.delete("Set-Cookie");
    return salida;
  },
};

function noEncontrado() {
  return new Response(
    '<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' +
      '<meta name="robots" content="noindex"><title>No encontrado</title>' +
      '<p style="font-family:system-ui,sans-serif;text-align:center;margin-top:20vh">Esta página no existe. <a href="/">Volver al inicio</a></p></html>',
    { status: 404, headers: { "Content-Type": "text/html; charset=utf-8" } }
  );
}
