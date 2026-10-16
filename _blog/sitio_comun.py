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
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS_VERSION = "20261016-rubros"

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

# RUBROS (tandas 3 y 4 del piloto, 16-10-2026): cada rubro con sus casos reales y
# la guia del blog que le corresponde. La guia se enlaza SOLO si ya esta
# publicada (existe blog/<slug>/index.html): el blog diario publica una por dia
# y el workflow corre --aplicar despues de publicar, asi que el enlace aparece
# solo el dia que la guia sale. Un rubro sin caso real no entra (regla 2 del
# metodo: no se publica una pagina vacia). Sin "abogados" ni "restaurantes"
# hasta tener uno.
RUBROS = [
    ("salon-de-belleza", "Página web para salón de belleza", ["salon-amanda"], "pagina-web-salon-de-belleza"),
    ("venta-de-parcelas", "Página web para venta de parcelas", ["punto-parcelas"], "sitio-web-venta-de-parcelas"),
    ("repuestos-automotrices", "Tienda online de repuestos automotrices", ["medina4x4", "villarreal"], "ecommerce-repuestos-automotrices"),
    ("ropa-y-uniformes", "Tienda online de ropa y uniformes", ["popi"], "tienda-online-ropa-tallas-colores"),
    ("pasteleria-y-reposteria", "Tienda online de pastelería y repostería", ["dulcecita", "la-dolce-mammina"], "tienda-online-pasteleria-reposteria"),
    ("climatizacion", "Página web para empresa de climatización", ["fco-climatizacion"], "pagina-web-empresa-climatizacion"),
    ("transporte-y-logistica", "Página web para transporte, turismo y logística", ["voa-chile", "travesia-logistica"], "pagina-web-empresa-de-transporte-y-turismo"),
    ("sindicatos", "Sitio web para sindicatos", ["sindicato-aza"], "sitio-web-para-sindicatos"),
    ("estudio-de-tatuajes", "Página web para estudio de tatuajes", ["puas-tatuajes"], None),
    ("seguridad", "Plataforma web para empresa de seguridad", ["saferoom"], None),
]
HUB = "paginas-web-por-rubro"
HUB_H1 = "Páginas web por rubro"


def guia_publicada(slug):
    """(href, H1 de la guia) si esta publicada; None si todavia no sale."""
    if not slug:
        return None
    ruta = os.path.join(RAIZ, "blog", slug, "index.html")
    if not os.path.isfile(ruta):
        return None
    m = re.search(r"<h1[^>]*>(.*?)</h1>", _leer(ruta), re.S)
    h1 = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else slug
    return "/blog/%s/" % slug, h1


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
        ("/blog/", "Blog"), ("/%s/" % HUB, HUB_H1), ("/cotizar/", "Cotizar"), ("/sobre-gogodevs/", "Nosotros"),
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
            if m:
                n = _con_bloque_rubro(n, m.group(1))
        if n != t:
            _escribir(ruta, n)
            cambiadas.append(rel)
    if escribir_hub():
        cambiadas.append(HUB + "/index.html")
    print("Paginas cambiadas: %d" % len(cambiadas))
    return cambiadas


BLOQUE_RE = re.compile(r"<!-- rubro:inicio -->.*?<!-- rubro:fin -->\n?", re.S)


def _con_bloque_rubro(texto, slug_caso):
    """Al final del caso: la guia de su rubro (si ya salio) y la pagina de rubros.

    Tanda 3: los casos recibian entre 3 y 14 enlaces internos y no enlazaban a
    ninguna guia; las guias si enlazaban a los casos. Ahora es ida y vuelta.
    """
    rubro = next((r for r in RUBROS if slug_caso in r[2]), None)
    texto = BLOQUE_RE.sub("", texto)
    if not rubro or "</main>" not in texto:
        return texto
    nombre, articulo = rubro[1], rubro[3]
    enlaces = []
    guia = guia_publicada(articulo)
    if guia:
        enlaces.append("Guía: " + _a(guia[0], guia[1]))
    # El texto es el H1 del hub (regla de Jorge: el enlace dice el H1 de su destino).
    enlaces.append(_a("/%s/#%s" % (HUB, rubro[0]), HUB_H1))
    bloque = (
        '<!-- rubro:inicio -->'
        '<section class="section section--surface" aria-labelledby="rubro-title">'
        '<div class="container"><h2 id="rubro-title">%s</h2>'
        '<p>%s</p></div></section>'
        '<!-- rubro:fin -->\n' % (html.escape(nombre, quote=False), " · ".join(enlaces))
    )
    i = texto.rfind("</main>")
    return texto[:i] + bloque + texto[i:]


def escribir_hub():
    """Escribe /paginas-web-por-rubro/ con el esqueleto de /servicios/. True si cambio."""
    casos = {s: (m, r) for s, m, r in CASOS}
    shell = _leer(os.path.join(RAIZ, "servicios", "index.html"))
    titulo = "Páginas web por rubro: casos reales en Chile | GoGoDevS"
    desc = ("Páginas web y tiendas online para salones de belleza, inmobiliarias, repuestos, "
            "pastelerías, transporte, sindicatos y más: casos reales hechos por GoGoDevS en Chile.")
    url = "https://www.gogodevs.cl/%s/" % HUB

    bloques, items = [], []
    for slug, nombre, slugs_casos, articulo in RUBROS:
        presentes = [c for c in slugs_casos if c in casos]
        if not presentes:
            continue
        lis = "".join("<li>%s</li>" % _a("/proyectos/%s/" % c, h1_caso(*casos[c])) for c in presentes)
        guia = guia_publicada(articulo)
        extra = "<p>Guía: %s</p>" % _a(guia[0], guia[1]) if guia else ""
        bloques.append('<article class="service-card" id="%s"><h2>%s</h2><ul>%s</ul>%s</article>'
                       % (slug, html.escape(nombre, quote=False), lis, extra))
        items.append(nombre)
    main = (
        '<main id="contenido" tabindex="-1">'
        '<section class="hero section" aria-labelledby="rubro-hub-title"><div class="container">'
        '<h1 id="rubro-hub-title">%s</h1>'
        '<p>Cada rubro necesita cosas distintas: un salón necesita que le reserven, una tienda de '
        'repuestos que el cliente encuentre la pieza exacta, una inmobiliaria mostrar cada proyecto '
        'con su ubicación. Acá están los sitios que ya hicimos, ordenados por rubro, y la guía de '
        'cada uno.</p></div></section>'
        '<section class="section rubro-hub"><div class="container"><div class="services-grid">%s</div>'
        '<p>¿Tu rubro no está? %s o revisa %s.</p></div></section></main>'
        % (html.escape(HUB_H1, quote=False), "".join(bloques),
           _a("/cotizar/", "Cuéntanos tu proyecto"), _a("/servicios/", "todos los servicios"))
    )
    ld = json.dumps([
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://www.gogodevs.cl/"},
            {"@type": "ListItem", "position": 2, "name": HUB_H1, "item": url}]},
        {"@context": "https://schema.org", "@type": "CollectionPage", "name": HUB_H1, "url": url,
         "description": desc, "about": items},
    ], ensure_ascii=False, indent=2)

    t = shell
    t = re.sub(r"<title>.*?</title>", lambda m: "<title>%s</title>" % html.escape(titulo, quote=False), t, count=1, flags=re.S)
    for patron in (r'(<meta name="description" content=")[^"]*(")',
                   r'(<meta property="og:description" content=")[^"]*(")',
                   r'(<meta name="twitter:description" content=")[^"]*(")'):
        t = re.sub(patron, lambda m: m.group(1) + html.escape(desc) + m.group(2), t, count=1)
    for patron in (r'(<meta property="og:title" content=")[^"]*(")',
                   r'(<meta name="twitter:title" content=")[^"]*(")'):
        t = re.sub(patron, lambda m: m.group(1) + html.escape(titulo) + m.group(2), t, count=1)
    t = re.sub(r'(<link rel="canonical" href=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), t, count=1)
    t = re.sub(r'(<meta property="og:url" content=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), t, count=1)
    # El segundo JSON-LD del esqueleto es el BreadcrumbList de /servicios/: se reemplaza.
    bloques_ld = list(re.finditer(r'<script type="application/ld\+json">.*?</script>', t, re.S))
    if len(bloques_ld) >= 2:
        b = bloques_ld[1]
        t = t[:b.start()] + '<script type="application/ld+json">\n%s\n</script>' % ld + t[b.end():]
    t = re.sub(r"<main\b.*?</main>", lambda m: main, t, count=1, flags=re.S)
    # Sin la marca de "pagina activa" del menu que trae el esqueleto de Servicios.
    t = t.replace(' aria-current="page"', "")

    ruta = os.path.join(RAIZ, HUB, "index.html")
    if os.path.isfile(ruta) and _leer(ruta) == t:
        return False
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    _escribir(ruta, t)
    _sitemap_con_hub()
    return True


def _sitemap_con_hub():
    ruta = os.path.join(RAIZ, "sitemap.xml")
    sm = _leer(ruta)
    loc = "https://www.gogodevs.cl/%s/" % HUB
    if loc in sm:
        return
    entrada = "  <url>\n    <loc>%s</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n" % loc
    _escribir(ruta, sm.replace("</urlset>", entrada + "</urlset>", 1))


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
