# -*- coding: utf-8 -*-
"""Lo que se repite en TODAS las paginas de gogodevs.cl, escrito una sola vez.

POR QUE EXISTE (auditoria SEO del 14-10-2026, metodo /seo-gogodevs)
El footer estaba copiado a mano en cada pagina y habia 31 versiones distintas
en 40 paginas: el de la home no enlazaba al blog, el de los casos no enlazaba
a los servicios, ninguno enlazaba a los casos uno por uno, y la mitad decia
"(c) 2025". Para Google, el footer es el enlazado interno que esta en todas las
paginas: el lugar donde mas pesa que este completo.

Y los casos tenian como H1 solo la marca ("Medina4x4"), sin decir de que
rubro son. El H1 ahora dice marca + rubro, y el footer enlaza cada caso con
ese mismo H1 como texto (regla de Jorge Urzua: la miga y el enlace = el H1).

    python _blog/sitio_comun.py --aplicar     escribe footer, H1 y titles
    python _blog/sitio_comun.py --revisar     falla si alguna pagina se desvio

verificar.py corre --revisar antes de cada deploy del blog.
"""
import html
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS_VERSION = "20261014-footer"

# slug -> (marca, rubro). El rubro sale de la descripcion de cada caso, no se
# inventa: si un caso no dice su rubro, dice lo que si es ("marca gastronomica").
CASOS = [
    ("medina4x4", "Medina4x4", "tienda online de repuestos 4x4"),
    ("villarreal", "Comercial Villarreal", "ecommerce de repuestos automotrices"),
    ("popi", "Popi Uniformes Clínicos", "ecommerce de uniformes clínicos"),
    ("dulcecita", "Dulcecita", "tienda online de repostería"),
    ("punto-parcelas", "Punto Parcelas", "página web para venta de parcelas"),
    ("salon-amanda", "Salón Amanda", "página web para salón de belleza con reservas"),
    ("puas-tatuajes", "Púas Tatuajes", "página web para estudio de tatuajes"),
    ("saferoom", "SafeRoom Chile", "plataforma web de seguridad residencial"),
    ("voa-chile", "VOA Chile", "página web de transporte y turismo"),
    ("travesia-logistica", "Travesía Logística", "página web para empresa de logística"),
    ("fco-climatizacion", "FCO Climatización", "página web para empresa de climatización"),
    ("sindicato-aza", "Sindicato AZA", "sitio web para sindicato"),
    ("la-dolce-mammina", "La Dolce Mammina", "sitio web para marca gastronómica"),
    ("max-services-spa", "MAX SERVICES SPA", "sitio web corporativo de servicios"),
]

SERVICIOS = [
    ("desarrollo-web", "Desarrollo web"),
    ("ecommerce", "Ecommerce"),
    ("sistemas-a-medida", "Sistemas a medida"),
    ("apps-a-medida", "Apps a medida"),
    ("automatizacion-de-procesos", "Automatización de procesos"),
    ("integraciones", "Integraciones de pago"),
    ("seo-tecnico", "SEO técnico"),
    ("consultoria", "Consultoría / auditoría"),
]

GUIAS = [
    ("/cuanto-cuesta-una-pagina-web-chile/", "¿Cuánto cuesta una página web en Chile?"),
    ("/blog/que-pedirle-a-una-empresa-de-desarrollo-web/", "Qué pedirle a una empresa de desarrollo web"),
    ("/blog/catalogo-o-tienda-online/", "¿Catálogo o tienda online?"),
    ("/blog/mercado-pago-o-webpay-tienda-online/", "Mercado Pago o Webpay"),
    ("/blog/software-a-medida-o-herramienta-generica/", "Software a medida o herramienta ya hecha"),
    ("/blog/", "Todas las guías del blog"),
]

# Paginas que NO llevan el footer comun: el arbol de enlaces y la home vieja,
# y los stubs de redireccion (no tienen footer).
FUERA = {"links/index.html", "index-v2.html"}


def h1_caso(marca, rubro):
    return "%s: %s" % (marca, rubro)


def _a(href, texto):
    return '<a href="%s">%s</a>' % (href, html.escape(texto, quote=False))


def footer_html():
    redes = open(os.path.join(RAIZ, "_blog", "footer_redes.html"), encoding="utf-8").read().strip()
    casos = "".join(_a("/proyectos/%s/" % s, h1_caso(m, r)) for s, m, r in CASOS)
    servicios = "".join(_a("/servicios/%s/" % s, t) for s, t in SERVICIOS)
    guias = "".join(_a(h, t) for h, t in GUIAS)
    explorar = "".join(_a(h, t) for h, t in (
        ("/", "Inicio"), ("/servicios/", "Servicios"), ("/proyectos/", "Proyectos"),
        ("/blog/", "Blog"), ("/cotizar/", "Cotizar"), ("/sobre-gogodevs/", "Nosotros"),
        ("/contacto/", "Contacto")))
    return (
        '<footer class="site-footer"><!-- footer comun: se edita en _blog/sitio_comun.py, no aca -->'
        '<div class="container site-footer__content site-footer__content--comun">'
        '<div class="site-footer__brand">'
        '<p>GoGoDevS &middot; Desarrollo Web Profesional &middot; gogodevs.cl</p>'
        '<p class="site-footer__note">Desarrollo web, ecommerce, sistemas a medida y automatización '
        'para negocios en Chile.</p>'
        '<a href="mailto:contacto@gogodevs.cl">contacto@gogodevs.cl</a>' + redes +
        '<p class="site-footer__copy">&copy; 2026 GoGoDevS.</p>'
        '<p class="site-footer__copy">GoGoDevS es la marca comercial de Diego Alfonso Dinamarca Abarca.</p>'
        '</div>'
        '<nav class="site-footer__nav" aria-label="Explorar"><span class="site-footer__nav-title">Explorar</span>'
        '<div class="site-footer__links">' + explorar + '</div></nav>'
        '<nav class="site-footer__nav" aria-label="Servicios"><span class="site-footer__nav-title">Servicios</span>'
        '<div class="site-footer__links">' + servicios + '</div></nav>'
        '<nav class="site-footer__nav" aria-label="Casos reales"><span class="site-footer__nav-title">Casos reales</span>'
        '<div class="site-footer__links site-footer__links--casos">' + casos + '</div></nav>'
        '<nav class="site-footer__nav" aria-label="Guías"><span class="site-footer__nav-title">Guías</span>'
        '<div class="site-footer__links">' + guias + '</div></nav>'
        '<div class="footer-legal">'
        '<a href="/legal/privacidad/">Privacidad</a><a href="/legal/terminos/">Términos</a>'
        '<a href="/legal/pagos-y-cancelacion/">Pagos y cancelación</a>'
        '<a href="https://maps.google.com/?cid=9703305989011734289" target="_blank" rel="noopener">Nuestra ficha en Google</a>'
        '</div></div></footer>'
    )


FOOTER_RE = re.compile(r'<footer class="site-footer">.*?</footer>', re.S)


def paginas():
    for carpeta, dirs, archivos in os.walk(RAIZ):
        dirs[:] = [d for d in dirs if not d.startswith((".", "_"))]
        for n in archivos:
            if n.endswith(".html"):
                ruta = os.path.join(carpeta, n)
                rel = os.path.relpath(ruta, RAIZ).replace("\\", "/")
                if rel not in FUERA:
                    yield rel, ruta
    for n in ("plantilla_articulo.html", "plantilla_indice.html"):
        yield "_blog/" + n, os.path.join(RAIZ, "_blog", n)


def _leer(ruta):
    return open(ruta, encoding="utf-8", newline="").read()


def _escribir(ruta, texto):
    open(ruta, "w", encoding="utf-8", newline="").write(texto)


def aplicar():
    footer = footer_html()
    cambiadas = []
    for rel, ruta in paginas():
        t = _leer(ruta)
        if not FOOTER_RE.search(t):
            continue  # stub de redireccion
        n = FOOTER_RE.sub(lambda m: footer, t, count=0)
        n = re.sub(r"style\.css\?v=[0-9A-Za-z_-]+", "style.css?v=" + CSS_VERSION, n)
        m = re.match(r"proyectos/([^/]+)/index\.html$", rel)
        if m:
            caso = {s: (ma, ru) for s, ma, ru in CASOS}.get(m.group(1))
            if caso:
                marca, rubro = caso
                # El ": " va oculto a la vista: el texto del H1 queda "Marca: rubro",
                # igual al enlace del footer, y en pantalla el rubro va debajo.
                n = re.sub(r'<h1 id="page-title">.*?</h1>',
                           '<h1 id="page-title">%s<span class="caso-rubro"><span class="visually-hidden">: </span>%s</span></h1>'
                           % (html.escape(marca, quote=False), html.escape(rubro, quote=False)), n, count=1)
                # Los 6 casos con title generico ("Caso de Desarrollo Web") pasan a decir su rubro.
                n = re.sub(r"<title>([^<|]+)\| Caso de Desarrollo Web \| GoGoDevS</title>",
                           lambda mm: "<title>%s| %s | GoGoDevS</title>" % (mm.group(1), rubro[0].upper() + rubro[1:]), n)
        if n != t:
            _escribir(ruta, n)
            cambiadas.append(rel)
    print("Paginas cambiadas: %d" % len(cambiadas))
    return cambiadas


def revisar():
    """Errores si alguna pagina tiene un footer distinto al comun."""
    footer = footer_html()
    errores = []
    for rel, ruta in paginas():
        t = _leer(ruta)
        encontrados = FOOTER_RE.findall(t)
        if not encontrados:
            continue
        if any(f != footer for f in encontrados):
            errores.append("%s: el footer no es el comun (se edita en _blog/sitio_comun.py y se corre --aplicar)" % rel)
    return errores


if __name__ == "__main__":
    if "--aplicar" in sys.argv:
        aplicar()
    elif "--revisar" in sys.argv:
        e = revisar()
        print("\n".join(e) or "footer comun en todas las paginas")
        sys.exit(1 if e else 0)
    else:
        print(__doc__)
