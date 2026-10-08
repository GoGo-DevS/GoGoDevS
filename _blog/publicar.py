#!/usr/bin/env python3
"""Publicador diario del blog de gogodevs.cl (solo biblioteca estandar).

POR QUE EXISTE (07-10-2026)
  Los articulos se escriben todos de una vez, pero en el servidor solo puede
  existir lo que ya tiene fecha cumplida. Esconder un articulo futuro con JS no
  sirve: el HTML igual estaria subido, en el sitemap y al alcance de Google.
  Por eso los borradores viven en _blog/programados/ (carpeta que el deploy por
  FTP EXCLUYE) y este script copia a /blog/<slug>/ solo lo que corresponde.

QUE HACE, en este orden
  1. Lee _blog/programados/AAAA-MM-DD-slug.html (cabecera "clave: valor",
     una linea "---" y despues el cuerpo en HTML).
  2. Publica todo lo que tenga fecha <= hoy en hora de Chile
     (America/Santiago). Si un dia el cron no corrio, el siguiente publica lo
     atrasado: no hay "dia de hoy", hay "todo lo vencido".
  3. Si encuentra publicado un articulo cuya fecha todavia no llega, lo BORRA.
     Asi una simulacion con --hoy o un error de mano no deja nada adelantado.
  2b. Cada articulo necesita su foto de portada en _programados/_fotos/<slug>.webp
     (1200x675). Al publicar se copia a /assets/img/blog/<slug>.webp. Si la
     foto no existe, el articulo NO se publica ese dia y queda en el log:
     mejor un dia de atraso que un post sin portada.
  4. Regenera /blog/index.html mirando lo que hay en /blog/*/ (incluye los
     articulos escritos a mano, no solo los programados).
  5. Actualiza sitemap.xml: agrega los articulos publicados con su lastmod y
     saca los que no existen.

IDEMPOTENTE: la salida depende solo de los borradores y de la fecha, nunca de
la hora en que corre. Correrlo dos veces el mismo dia no cambia ni un byte.

Uso:
  python _blog/publicar.py                 # hoy en Chile
  python _blog/publicar.py --hoy 2026-10-15  # simular otra fecha
  python _blog/publicar.py --listar        # ver el calendario y salir
"""
import argparse
import datetime as dt
import html
import json
import os
import re
import shutil
import struct
import sys

RAIZ_DEF = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITIO = "https://www.gogodevs.cl"
ORG_ID = SITIO + "/#organization"
LOGO = SITIO + "/assets/img/logo-gogodevs.png"
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
PALABRAS_POR_MINUTO = 200
CARPETA_FOTOS = os.path.join("_programados", "_fotos")   # fuera del FTP
DESTINO_FOTOS = os.path.join("assets", "img", "blog")


def medidas_webp(ruta):
    """Ancho y alto de un WebP sin Pillow (VP8, VP8L y VP8X)."""
    with open(ruta, "rb") as f:
        cab = f.read(40)
    if cab[:4] != b"RIFF" or cab[8:12] != b"WEBP":
        raise ValueError("No es un WebP valido: " + ruta)
    tipo = cab[12:16]
    if tipo == b"VP8X":
        w = 1 + int.from_bytes(cab[24:27], "little")
        h = 1 + int.from_bytes(cab[27:30], "little")
    elif tipo == b"VP8 ":
        w, h = struct.unpack("<HH", cab[26:30])
        w, h = w & 0x3FFF, h & 0x3FFF
    elif tipo == b"VP8L":
        b = cab[21:25]
        w = 1 + (((b[1] & 0x3F) << 8) | b[0])
        h = 1 + (((b[3] & 0x0F) << 10) | (b[2] << 2) | ((b[1] & 0xC0) >> 6))
    else:
        raise ValueError("WebP desconocido (%r): %s" % (tipo, ruta))
    return w, h


def ruta_foto_fuente(raiz, slug):
    return os.path.join(raiz, CARPETA_FOTOS, slug + ".webp")


def ruta_foto_publicada(raiz, slug):
    return os.path.join(raiz, DESTINO_FOTOS, slug + ".webp")


# --------------------------------------------------------------------------
# Fecha de hoy en Chile
# --------------------------------------------------------------------------
def hoy_en_chile():
    ahora = dt.datetime.now(dt.timezone.utc)
    try:
        from zoneinfo import ZoneInfo
        return ahora.astimezone(ZoneInfo("America/Santiago")).date()
    except Exception:
        # Windows sin el paquete tzdata. Regla aproximada del horario de Chile
        # continental: verano (UTC-3) de septiembre a marzo, invierno (UTC-4)
        # de abril a agosto. En GitHub Actions (Ubuntu) siempre hay zoneinfo.
        offset = -3 if ahora.month >= 9 or ahora.month <= 3 else -4
        return (ahora + dt.timedelta(hours=offset)).date()


def fecha_texto(f):
    return "%d de %s de %d" % (f.day, MESES[f.month - 1], f.year)


# --------------------------------------------------------------------------
# Borradores
# --------------------------------------------------------------------------
NOMBRE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)\.html$")
CLAVES_UNICAS = {"titulo", "h1", "descripcion", "categoria", "foto_alt", "cta", "cta2_href", "cta2_texto", "modificado"}
CLAVES_LISTA = {"faq"}


def leer_borrador(ruta):
    nombre = os.path.basename(ruta)
    m = NOMBRE_RE.match(nombre)
    if not m:
        raise ValueError("Nombre invalido (debe ser AAAA-MM-DD-slug.html): " + nombre)
    texto = open(ruta, encoding="utf-8").read().replace("\r\n", "\n")
    if "\n---\n" not in texto:
        raise ValueError(nombre + ": falta la linea '---' que separa cabecera y cuerpo")
    cab, cuerpo = texto.split("\n---\n", 1)
    datos = {"faq": []}
    for n, linea in enumerate(cab.split("\n"), 1):
        if not linea.strip() or linea.lstrip().startswith("#"):
            continue
        if ":" not in linea:
            raise ValueError("%s linea %d sin 'clave:'" % (nombre, n))
        k, v = linea.split(":", 1)
        k, v = k.strip(), v.strip()
        if k in CLAVES_LISTA:
            if "||" not in v:
                raise ValueError("%s: faq necesita 'pregunta || respuesta'" % nombre)
            q, a = v.split("||", 1)
            datos["faq"].append((q.strip(), a.strip()))
        elif k in CLAVES_UNICAS:
            datos[k] = v
        else:
            raise ValueError("%s: clave desconocida '%s'" % (nombre, k))
    for k in ("titulo", "h1", "descripcion", "categoria", "foto_alt"):
        if not datos.get(k):
            raise ValueError("%s: falta '%s'" % (nombre, k))
    datos["fecha"] = dt.date.fromisoformat(m.group(1))
    datos["slug"] = m.group(2)
    datos["modificado"] = dt.date.fromisoformat(datos["modificado"]) if datos.get("modificado") else datos["fecha"]
    datos["cuerpo"] = cuerpo.strip("\n")
    datos["archivo"] = nombre
    return datos


def cargar_borradores(raiz):
    carpeta = os.path.join(raiz, "_blog", "programados")
    borradores = []
    for nombre in sorted(os.listdir(carpeta)):
        if nombre.endswith(".html"):
            borradores.append(leer_borrador(os.path.join(carpeta, nombre)))
    slugs = [b["slug"] for b in borradores]
    repetidos = sorted({s for s in slugs if slugs.count(s) > 1})
    if repetidos:
        raise ValueError("Slugs repetidos: " + ", ".join(repetidos))
    return borradores


# --------------------------------------------------------------------------
# Render de un articulo
# --------------------------------------------------------------------------
def texto_plano(fragmento):
    sin_tags = re.sub(r"<[^>]+>", " ", fragmento)
    return re.sub(r"\s+", " ", html.unescape(sin_tags)).strip()


def contar_palabras(datos):
    texto = texto_plano(datos["cuerpo"]) + " " + " ".join(q + " " + a for q, a in datos["faq"])
    return len(re.findall(r"\w+", texto))


def abs_url(ruta):
    return ruta if ruta.startswith("http") else SITIO + ruta


def url_articulo(slug):
    return "%s/blog/%s/" % (SITIO, slug)


def url_foto(slug):
    return "/assets/img/blog/%s.webp" % slug


def jsonld_articulo(d):
    url = url_articulo(d["slug"])
    imagen = {"@type": "ImageObject", "url": abs_url(url_foto(d["slug"])),
              "width": d["foto_w"], "height": d["foto_h"]}
    grafo = [
        {
            "@type": "BlogPosting",
            "@id": url + "#articulo",
            "headline": d["h1"],
            "description": d["descripcion"],
            "image": imagen,
            "datePublished": d["fecha"].isoformat(),
            "dateModified": d["modificado"].isoformat(),
            "inLanguage": "es-CL",
            "wordCount": contar_palabras(d),
            "articleSection": d["categoria"],
            "author": {
                "@type": "Person",
                "name": "Diego Dinamarca",
                "url": "https://www.linkedin.com/in/diegodinamarca/",
            },
            "publisher": {"@id": ORG_ID},
            "mainEntityOfPage": {"@type": "WebPage", "@id": url},
            "isPartOf": {"@id": SITIO + "/blog/#blog"},
        },
        {
            "@type": "Organization",
            "@id": ORG_ID,
            "name": "GoGoDevS",
            "url": SITIO + "/",
            "logo": LOGO,
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITIO + "/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITIO + "/blog/"},
                {"@type": "ListItem", "position": 3, "name": d["h1"], "item": url},
            ],
        },
    ]
    if d["faq"]:
        grafo.append({
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": texto_plano(a)}}
                for q, a in d["faq"]
            ],
        })
    return json.dumps({"@context": "https://schema.org", "@graph": grafo},
                      ensure_ascii=False, indent=2)


def bloque_faq(d):
    if not d["faq"]:
        return ""
    items = []
    for q, a in d["faq"]:
        items.append(
            '            <details class="faq-item">\n'
            '              <summary>%s</summary>\n'
            '              <p>%s</p>\n'
            '            </details>' % (html.escape(q, quote=False), html.escape(a, quote=False)))
    return ('          <h2>Preguntas frecuentes</h2>\n'
            '          <div class="faq-list">\n%s\n          </div>' % "\n".join(items))


def bloque_relacionados(d, publicados):
    """Hasta 2 articulos ANTERIORES. Nunca enlaza hacia adelante: un enlace a
    un articulo futuro seria un 404 hasta el dia en que se publique."""
    previos = [p for p in publicados if p["slug"] != d["slug"]
               and (p["fecha"], p["slug"]) < (d["fecha"], d["slug"])]
    previos.sort(key=lambda p: (p["fecha"], p["slug"]), reverse=True)
    misma = [p for p in previos if p["categoria"] == d["categoria"]]
    elegidos = (misma + [p for p in previos if p not in misma])[:2]
    if not elegidos:
        return ""
    tarjetas = []
    for p in elegidos:
        tarjetas.append(
            '          <a class="blog-card" href="/blog/%s/" style="text-decoration:none;color:inherit">\n'
            '            <img src="%s" alt="%s" width="%d" height="%d" loading="lazy" decoding="async" style="width:100%%;height:auto;aspect-ratio:16/9;object-fit:cover;border-radius:10px">\n'
            '            <span class="blog-card__tag">%s</span>\n'
            '            <h3>%s</h3>\n'
            '            <span class="blog-card__link">Leer &rarr;</span>\n'
            '          </a>' % (p["slug"], url_foto(p["slug"]), html.escape(p["foto_alt"]), p["foto_w"], p["foto_h"],
                              html.escape(p["categoria"]), html.escape(p["h1"])))
    return ('\n        <section aria-labelledby="relacionados-title" style="margin-top:3rem">\n'
            '          <h2 id="relacionados-title" style="font-size:1.2rem;text-align:center">Sigue leyendo</h2>\n'
            '          <div class="blog-grid">\n%s\n          </div>\n'
            '        </section>' % "\n".join(tarjetas))


def render_articulo(d, plantilla, publicados):
    palabras = contar_palabras(d)
    reemplazos = {
        "TITLE": html.escape(d["titulo"]),
        "DESCRIPTION": html.escape(d["descripcion"]),
        "CANONICAL": url_articulo(d["slug"]),
        "OG_TITLE": html.escape(d["h1"]),
        "OG_IMAGE": abs_url(url_foto(d["slug"])),
        "OG_IMAGE_ALT": html.escape(d["foto_alt"]),
        "FOTO_SRC": url_foto(d["slug"]),
        "FOTO_W": str(d["foto_w"]),
        "FOTO_H": str(d["foto_h"]),
        "FECHA_ISO": d["fecha"].isoformat(),
        "MODIFICADO_ISO": d["modificado"].isoformat(),
        "JSONLD": jsonld_articulo(d),
        "CATEGORIA": html.escape(d["categoria"]),
        "H1": html.escape(d["h1"], quote=False),
        "FECHA_TEXTO": fecha_texto(d["fecha"]),
        "MINUTOS": str(max(1, round(palabras / PALABRAS_POR_MINUTO))),
        "CUERPO": d["cuerpo"],
        "FAQ": bloque_faq(d),
        "CTA_TEXTO": html.escape(d.get("cta") or "Cotizar en 4 pasos"),
        "CTA2_HREF": d.get("cta2_href") or "/servicios/",
        "CTA2_TEXTO": html.escape(d.get("cta2_texto") or "Ver servicios"),
        "RELACIONADOS": bloque_relacionados(d, publicados),
    }
    salida = plantilla
    for k, v in reemplazos.items():
        salida = salida.replace("{{%s}}" % k, v)
    if "{{" in salida:
        raise ValueError("Quedo un marcador sin reemplazar en " + d["slug"])
    return salida


# --------------------------------------------------------------------------
# Indice del blog (lee lo que esta publicado en /blog/*/)
# --------------------------------------------------------------------------
def meta_de_publicado(ruta_html, slug):
    t = open(ruta_html, encoding="utf-8").read()
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S)
    desc = re.search(r'<meta name="description" content="([^"]*)"', t)
    fecha = re.search(r'"datePublished":\s*"(\d{4}-\d{2}-\d{2})"', t)
    cat = re.search(r'<a href="/blog/">Blog</a>\s*/\s*(?:<span[^>]*>)?([^<]+)', t)
    alt = re.search(r'<meta property="og:image:alt" content="([^"]*)"', t)
    raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(ruta_html))))
    tiene_foto = os.path.isfile(os.path.join(raiz, DESTINO_FOTOS, slug + ".webp"))
    if not (h1 and desc and fecha):
        raise ValueError("No pude leer titulo/descripcion/fecha de /blog/%s/" % slug)
    return {
        "slug": slug,
        "h1": html.unescape(texto_plano(h1.group(1))),
        "descripcion": html.unescape(desc.group(1)),
        "fecha": dt.date.fromisoformat(fecha.group(1)),
        "categoria": html.unescape(cat.group(1).strip()) if cat else "Artículo",
        "foto": url_foto(slug) if tiene_foto else None,
        "foto_alt": html.unescape(alt.group(1)) if alt else "",
    }


def publicados_en_disco(raiz):
    base = os.path.join(raiz, "blog")
    salida = []
    for slug in sorted(os.listdir(base)):
        ruta = os.path.join(base, slug, "index.html")
        if os.path.isdir(os.path.join(base, slug)) and os.path.isfile(ruta):
            salida.append(meta_de_publicado(ruta, slug))
    salida.sort(key=lambda p: (p["fecha"], p["slug"]), reverse=True)
    return salida


def miniatura(p, destacada=False):
    if not p.get("foto"):
        return ""
    if destacada:
        estilo = "position:absolute;inset:0;width:100%;height:100%;object-fit:cover"
        carga = 'loading="eager" fetchpriority="high"'
    else:
        estilo = "width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;border-radius:10px"
        carga = 'loading="lazy"'
    return ('            <img src="%s" alt="%s" width="1200" height="675" %s decoding="async" style="%s">\n'
            % (p["foto"], html.escape(p["foto_alt"]), carga, estilo))


def render_indice(publicados, plantilla):
    if not publicados:
        raise ValueError("No hay articulos publicados para el indice")
    p0 = publicados[0]
    destacado = (
        '    <section class="section section--surface" aria-labelledby="destacado-title">\n'
        '      <div class="container">\n'
        '        <div class="section-heading">\n'
        '          <span class="eyebrow">Último artículo</span>\n'
        '          <h2 id="destacado-title" class="visually-hidden" style="position:absolute;width:1px;height:1px;overflow:hidden">Último artículo</h2>\n'
        '        </div>\n'
        '        <a class="blog-featured" href="/blog/%s/" style="text-decoration:none;color:inherit">\n'
        '          <div class="blog-featured__media">\n'
        '%s'
        '            <span class="blog-featured__tag" style="position:relative;z-index:1;background:rgba(8,16,32,0.85)">%s</span>\n'
        '          </div>\n'
        '          <div class="blog-featured__content">\n'
        '            <h3>%s</h3>\n'
        '            <p style="color:var(--color-text-muted)">%s</p>\n'
        '            <p class="article-meta" style="justify-content:flex-start"><span>%s</span><span>·</span><span style="color:var(--color-gold);font-weight:700">Leer →</span></p>\n'
        '          </div>\n'
        '        </a>\n'
    ) % (p0["slug"], miniatura(p0, destacada=True), html.escape(p0["categoria"]), html.escape(p0["h1"]),
         html.escape(p0["descripcion"]), fecha_texto(p0["fecha"]))
    resto = publicados[1:]
    if resto:
        tarjetas = []
        for p in resto:
            tarjetas.append(
                '          <a class="blog-card" href="/blog/%s/" style="text-decoration:none;color:inherit">\n'
                '%s'
                '            <span class="blog-card__tag">%s</span>\n'
                '            <h3>%s</h3>\n'
                '            <p>%s</p>\n'
                '            <span class="blog-card__link">%s · Leer &rarr;</span>\n'
                '          </a>' % (p["slug"], miniatura(p), html.escape(p["categoria"]), html.escape(p["h1"]),
                                    html.escape(p["descripcion"]), fecha_texto(p["fecha"])))
        destacado += (
            '\n        <h2 style="margin-top:3rem;font-size:1.3rem">Todos los artículos</h2>\n'
            '        <div class="blog-grid">\n%s\n        </div>\n' % "\n".join(tarjetas))
    destacado += '      </div>\n    </section>\n'

    grafo = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Organization", "@id": ORG_ID, "name": "GoGoDevS",
             "url": SITIO + "/", "logo": LOGO},
            {"@type": "Blog", "@id": SITIO + "/blog/#blog", "url": SITIO + "/blog/",
             "name": "Blog de GoGoDevS", "inLanguage": "es-CL",
             "publisher": {"@id": ORG_ID},
             "blogPost": [{"@type": "BlogPosting", "headline": p["h1"],
                           "url": url_articulo(p["slug"]),
                           "datePublished": p["fecha"].isoformat()} for p in publicados]},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITIO + "/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITIO + "/blog/"}]},
        ],
    }
    salida = plantilla.replace("{{LISTADO}}", destacado)
    salida = salida.replace("{{JSONLD}}", json.dumps(grafo, ensure_ascii=False, indent=2))
    if "{{" in salida:
        raise ValueError("Quedo un marcador sin reemplazar en el indice")
    return salida


# --------------------------------------------------------------------------
# Sitemap
# --------------------------------------------------------------------------
URL_RE = re.compile(r"  <url>\n    <loc>([^<]+)</loc>.*?</url>\n", re.S)


def actualizar_sitemap(texto, publicados, lastmod_por_slug):
    """Deja en el sitemap exactamente los articulos que estan en disco."""
    validos = {url_articulo(p["slug"]) for p in publicados}

    def filtrar(m):
        loc = m.group(1)
        if loc.startswith(SITIO + "/blog/") and loc != SITIO + "/blog/" and loc not in validos:
            return ""
        return m.group(0)

    texto = URL_RE.sub(filtrar, texto)
    ultimo = max(p["fecha"] for p in publicados).isoformat()
    # lastmod del indice = fecha del articulo mas reciente
    texto = re.sub(r"(<loc>%s/blog/</loc>\n    <lastmod>)[^<]+" % re.escape(SITIO),
                   lambda m: m.group(1) + ultimo, texto)
    nuevos = []
    for p in sorted(publicados, key=lambda p: (p["fecha"], p["slug"])):
        loc = url_articulo(p["slug"])
        lastmod = lastmod_por_slug.get(p["slug"], p["fecha"]).isoformat()
        if "<loc>%s</loc>" % loc in texto:
            texto = re.sub(r"(<loc>%s</loc>\n    <lastmod>)[^<]+" % re.escape(loc),
                           lambda m: m.group(1) + lastmod, texto)
        else:
            nuevos.append(
                "  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n"
                "    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>\n"
                % (loc, lastmod))
    if nuevos:
        texto = texto.replace("</urlset>", "".join(nuevos) + "</urlset>")
    return texto


# --------------------------------------------------------------------------
def escribir_si_cambia(ruta, contenido):
    actual = open(ruta, encoding="utf-8").read() if os.path.exists(ruta) else None
    if actual == contenido:
        return False
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write(contenido)
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--hoy", help="Fecha a simular, AAAA-MM-DD (por defecto: hoy en Chile)")
    ap.add_argument("--raiz", default=RAIZ_DEF, help="Raiz del sitio")
    ap.add_argument("--listar", action="store_true", help="Mostrar el calendario y salir")
    args = ap.parse_args()

    hoy = dt.date.fromisoformat(args.hoy) if args.hoy else hoy_en_chile()
    raiz = os.path.abspath(args.raiz)
    borradores = cargar_borradores(raiz)

    if args.listar:
        for b in borradores:
            foto = "foto ok" if os.path.isfile(ruta_foto_fuente(raiz, b["slug"])) else "SIN FOTO"
            estado = ("publica" if b["fecha"] <= hoy else "espera") + " " + foto
            print("%s  %-17s %s  (%d palabras)" % (b["fecha"], estado, b["slug"], contar_palabras(b)))
        return 0

    plantilla_art = open(os.path.join(raiz, "_blog", "plantilla_articulo.html"), encoding="utf-8").read()
    plantilla_idx = open(os.path.join(raiz, "_blog", "plantilla_indice.html"), encoding="utf-8").read()

    cambios = []
    sin_foto = []
    vencidos = []
    for b in borradores:
        if b["fecha"] > hoy:
            continue
        fuente = ruta_foto_fuente(raiz, b["slug"])
        if not os.path.isfile(fuente):
            sin_foto.append(b)
            continue
        b["foto_w"], b["foto_h"] = medidas_webp(fuente)
        vencidos.append(b)
    # Lo que no se puede publicar (futuro o sin foto) no puede quedar en el servidor.
    futuros = [b for b in borradores if b["fecha"] > hoy] + sin_foto

    # 3. Nada adelantado: un articulo con fecha futura no puede estar en /blog/.
    for b in futuros:
        carpeta = os.path.join(raiz, "blog", b["slug"])
        ruta = os.path.join(carpeta, "index.html")
        if os.path.exists(ruta):
            os.remove(ruta)
            try:
                os.rmdir(carpeta)
            except OSError:
                pass
            cambios.append("retirado (%s) %s" % ("sin foto" if b in sin_foto else "fecha futura", b["slug"]))

    for b in futuros:
        foto = ruta_foto_publicada(raiz, b["slug"])
        if os.path.exists(foto):
            os.remove(foto)
            cambios.append("retirada foto " + b["slug"])

    # 2. Publicar todo lo vencido. Los relacionados solo miran lo vencido.
    for b in vencidos:
        destino = ruta_foto_publicada(raiz, b["slug"])
        fuente = ruta_foto_fuente(raiz, b["slug"])
        if not os.path.exists(destino) or open(destino, "rb").read() != open(fuente, "rb").read():
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            shutil.copyfile(fuente, destino)
            cambios.append("foto " + b["slug"])
        ruta = os.path.join(raiz, "blog", b["slug"], "index.html")
        if escribir_si_cambia(ruta, render_articulo(b, plantilla_art, vencidos)):
            cambios.append("publicado %s %s" % (b["fecha"], b["slug"]))

    # 4. Indice desde lo que hay en disco.
    publicados = publicados_en_disco(raiz)
    if escribir_si_cambia(os.path.join(raiz, "blog", "index.html"), render_indice(publicados, plantilla_idx)):
        cambios.append("indice del blog")

    # 5. Sitemap.
    lastmod = {b["slug"]: b["modificado"] for b in vencidos}
    ruta_sm = os.path.join(raiz, "sitemap.xml")
    sm = open(ruta_sm, encoding="utf-8").read()
    if escribir_si_cambia(ruta_sm, actualizar_sitemap(sm, publicados, lastmod)):
        cambios.append("sitemap.xml")

    print("Hoy (Chile): %s | programados: %d | vencidos: %d | en espera: %d | en /blog/: %d"
          % (hoy, len(borradores), len(vencidos), len(futuros), len(publicados)))
    for c in cambios:
        print("  - " + c)
    for b in sin_foto:
        print("  ! NO PUBLICADO (falta la foto %s): %s %s"
              % (os.path.join(CARPETA_FOTOS, b["slug"] + ".webp"), b["fecha"], b["slug"]))
    if not cambios:
        print("  Sin cambios: todo lo vencido ya estaba publicado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
