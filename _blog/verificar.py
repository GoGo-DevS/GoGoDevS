#!/usr/bin/env python3
"""Chequeo antes de publicar (solo biblioteca estandar). Sale con codigo 1 si
algo esta mal, asi el workflow NO despliega un sitio roto.

Revisa:
  - todos los JSON-LD de las paginas que se suben parsean con json.loads
  - 0 enlaces internos rotos (href/src que empiezan con "/")
  - articulos del blog: title <= 60, description <= 155, un solo <h1>,
    canonical correcto, foto de portada presente
  - borradores: slugs unicos, 900-1500 palabras, sin voseo, sin "Cyber",
    sin *.onrender.com, y sin enlaces a articulos que se publican despues
  - NADA futuro en lo que se sube: ni HTML, ni foto, ni sitemap, ni indice
  - los workflows de deploy excluyen _blog/ y _programados/

Uso: python _blog/verificar.py [--hoy AAAA-MM-DD] [--raiz RUTA]
"""
import argparse
import datetime as dt
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import publicar  # noqa: E402

EXCLUIR = {".git", ".github", "_blog", "_programados", "whatsapp-agentkit", "node_modules", ".vscode"}
VOSEO = re.compile(r"\b(vos|fijate|acordate|mirá|andá|vení|dale|che)\b", re.I)
VOSEO_TILDE = re.compile(r"\b\w+(?:ás|és|ís)\b")
VOSEO_OK = {"más", "después", "además", "jamás", "atrás", "detrás", "demás", "través", "inglés", "interés",
            "francés", "portugués", "japonés", "país", "maíz", "anís", "mes", "vez", "ves", "das", "das",
            "estás", "están", "está", "tendrás", "podrás", "verás", "sabrás", "harás", "dirás", "querrás",
            "vendrás", "estés", "des", "veces", "cortés", "revés", "ciprés", "marqués", "parís", "estrés",
            "ciempiés", "quizás", "compás", "jamás", "mamás", "papás", "sofás", "ajís", "rubís", "esquís",
            "cafés", "bebés", "tés", "pies", "cuchuflís"}


def archivos_publicables(raiz):
    for dirpath, dirnames, filenames in os.walk(raiz):
        dirnames[:] = [d for d in dirnames if d not in EXCLUIR]
        for f in filenames:
            if f.endswith(".html"):
                yield os.path.join(dirpath, f)


def existe_interno(raiz, href):
    ruta = re.split(r"[?#]", href)[0]
    if not ruta or ruta == "/":
        return True
    p = os.path.join(raiz, ruta.lstrip("/").replace("/", os.sep))
    if ruta.endswith("/"):
        return os.path.isfile(os.path.join(p, "index.html"))
    return os.path.isfile(p) or os.path.isfile(os.path.join(p, "index.html"))


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--hoy")
    ap.add_argument("--raiz", default=publicar.RAIZ_DEF)
    args = ap.parse_args()
    raiz = os.path.abspath(args.raiz)
    hoy = dt.date.fromisoformat(args.hoy) if args.hoy else publicar.hoy_en_chile()
    errores = []
    avisos = []

    # 1-2. JSON-LD y enlaces internos en todo lo que se sube
    n_html = n_ld = n_links = 0
    for ruta in archivos_publicables(raiz):
        n_html += 1
        rel = os.path.relpath(ruta, raiz)
        t = open(ruta, encoding="utf-8", errors="replace").read()
        for bloque in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
            n_ld += 1
            try:
                json.loads(bloque)
            except Exception as e:
                errores.append("JSON-LD invalido en %s: %s" % (rel, e))
        for href in re.findall(r'(?:href|src)="(/[^"/][^"]*|/)"', t):
            n_links += 1
            if not existe_interno(raiz, href):
                errores.append("Enlace interno roto en %s -> %s" % (rel, href))

    # 3. Borradores
    borradores = publicar.cargar_borradores(raiz)  # ya falla si hay slugs repetidos
    fechas = {b["slug"]: b["fecha"] for b in borradores}
    for b in borradores:
        nombre = b["archivo"]
        palabras = publicar.contar_palabras(b)
        if not 900 <= palabras <= 1500:
            errores.append("%s: %d palabras (debe ser 900-1500)" % (nombre, palabras))
        if len(b["titulo"]) > 60:
            errores.append("%s: title de %d caracteres" % (nombre, len(b["titulo"])))
        if len(b["descripcion"]) > 155:
            errores.append("%s: description de %d caracteres" % (nombre, len(b["descripcion"])))
        texto = publicar.texto_plano(b["cuerpo"]) + " " + " ".join(q + " " + a for q, a in b["faq"])
        texto += " " + b["titulo"] + " " + b["h1"] + " " + b["descripcion"]
        for m in VOSEO.finditer(texto):
            errores.append("%s: posible voseo '%s'" % (nombre, m.group(0)))
        for m in VOSEO_TILDE.finditer(texto):
            if m.group(0).lower() not in VOSEO_OK:
                errores.append("%s: revisar palabra '%s' (voseo?)" % (nombre, m.group(0)))
        if re.search(r"cyber", texto + b["cuerpo"], re.I):
            errores.append("%s: menciona Cyber" % nombre)
        if "onrender.com" in b["cuerpo"]:
            errores.append("%s: enlaza a onrender.com" % nombre)
        if "<h1" in b["cuerpo"]:
            errores.append("%s: el cuerpo trae un <h1> propio" % nombre)
        for href in re.findall(r'href="([^"]+)"', b["cuerpo"]):
            if href.startswith("http"):
                errores.append("%s: enlace externo en el cuerpo (%s), revisar" % (nombre, href))
                continue
            m = re.match(r"^/blog/([^/]+)/", href)
            if m and m.group(1) in fechas and fechas[m.group(1)] > b["fecha"]:
                errores.append("%s: enlaza a un articulo que se publica despues (%s)" % (nombre, href))
            elif not (m and m.group(1) in fechas) and not existe_interno(raiz, href):
                errores.append("%s: enlace interno roto %s" % (nombre, href))
        if not os.path.isfile(publicar.ruta_foto_fuente(raiz, b["slug"])):
            # Aviso, no error: el publicador ya se salta ese articulo y el resto
            # del dia tiene que poder desplegarse igual.
            avisos.append("%s: falta la foto %s.webp (no se publica hasta que exista)" % (nombre, b["slug"]))

    # 4. Nada futuro en lo que se sube
    sitemap = open(os.path.join(raiz, "sitemap.xml"), encoding="utf-8").read()
    indice = open(os.path.join(raiz, "blog", "index.html"), encoding="utf-8").read()
    publicados = 0
    for b in borradores:
        html_pub = os.path.join(raiz, "blog", b["slug"], "index.html")
        foto_pub = publicar.ruta_foto_publicada(raiz, b["slug"])
        if b["fecha"] > hoy:
            for cosa, presente in (("HTML", os.path.exists(html_pub)), ("foto", os.path.exists(foto_pub)),
                                   ("sitemap", "/blog/%s/" % b["slug"] in sitemap),
                                   ("indice", "/blog/%s/" % b["slug"] in indice)):
                if presente:
                    errores.append("FUTURO %s (%s) presente en %s" % (b["slug"], b["fecha"], cosa))
        elif os.path.exists(html_pub):
            publicados += 1
            if not os.path.exists(foto_pub):
                errores.append("%s publicado SIN su foto" % b["slug"])

    # 5. Articulos publicados
    for slug in sorted(os.listdir(os.path.join(raiz, "blog"))):
        ruta = os.path.join(raiz, "blog", slug, "index.html")
        if not os.path.isfile(ruta):
            continue
        t = open(ruta, encoding="utf-8").read()
        title = re.search(r"<title>(.*?)</title>", t, re.S).group(1)
        desc = re.search(r'<meta name="description" content="([^"]*)"', t).group(1)
        import html as _h
        if len(_h.unescape(title)) > 60:
            errores.append("/blog/%s/: title de %d caracteres" % (slug, len(_h.unescape(title))))
        if len(_h.unescape(desc)) > 155:
            errores.append("/blog/%s/: description de %d caracteres" % (slug, len(_h.unescape(desc))))
        if len(re.findall(r"<h1[\s>]", t)) != 1:
            errores.append("/blog/%s/: no tiene exactamente un <h1>" % slug)
        if '<link rel="canonical" href="https://www.gogodevs.cl/blog/%s/">' % slug not in t:
            errores.append("/blog/%s/: canonical incorrecto" % slug)
        if "onrender.com" in t:
            errores.append("/blog/%s/: contiene onrender.com" % slug)

    # 6. Los deploys excluyen las carpetas privadas
    for wf in ("deploy.yml", "blog-diario.yml"):
        ruta = os.path.join(raiz, ".github", "workflows", wf)
        if os.path.exists(ruta):
            t = open(ruta, encoding="utf-8").read()
            for carpeta in ("_blog", "_programados"):
                if "--exclude ^%s/" % carpeta not in t:
                    errores.append("%s no excluye %s/ del FTP" % (wf, carpeta))
        else:
            errores.append("falta .github/workflows/%s" % wf)

    print("Hoy: %s | HTML revisados: %d | JSON-LD: %d | enlaces internos: %d | borradores: %d | publicados: %d"
          % (hoy, n_html, n_ld, n_links, len(borradores), publicados))
    for a in avisos:
        print("  ! " + a)
    if errores:
        print("ERRORES (%d):" % len(errores))
        for e in errores:
            print("  x " + e)
        return 1
    print("OK: sin errores")
    return 0


if __name__ == "__main__":
    sys.exit(main())
