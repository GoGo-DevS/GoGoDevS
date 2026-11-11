#!/usr/bin/env python3
"""Generador del GoGoDevS Tree para negocios SIN web (solo biblioteca estandar).

POR QUE EXISTE (11-11-2026)
  Diego vende el Tree a quien no tiene pagina web: un enlace para la bio de
  Instagram con su logo, sus colores y sus botones (WhatsApp con mensaje
  listo, Instagram, mapa, catalogo...). Vive en gogodevs.cl/t/<negocio>/ o,
  con el plan de dominio propio, en tunegocio.cl (ver docs/tree/).
  Cada Tree sale de UN JSON: nadie edita el HTML a mano, asi un cambio de
  diseno o de medicion se hace una vez aca y se regeneran todos.

QUE HACE
  1. Lee _tree/negocios/<slug>.json (el nombre del archivo ES el slug).
  2. Valida los datos (colores con contraste suficiente, enlaces https,
     WhatsApp con codigo de pais, plan y credito coherentes).
  3. Escribe t/<slug>/index.html con la plantilla y la skin elegida, y copia
     los archivos del negocio (logo, foto de fondo) desde _tree/negocios/<slug>/.
  4. Escribe t/index.html (redirige a la pagina del producto: sin el, el
     servidor podria listar la carpeta con todos los clientes).

  _tree/ NO se sube al servidor (deploy.yml y blog-diario.yml lo excluyen).
  Lo que se sube es lo generado en t/.

Uso:
  python _tree/generar.py              genera o actualiza todos los Tree
  python _tree/generar.py --revisar    no escribe; falla si algo esta desactualizado
                                       o invalido (lo corre _blog/verificar.py)
"""
import html
import json
import os
import re
import shutil
import sys
from urllib.parse import quote

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
CARPETA_NEGOCIOS = os.path.join(AQUI, "negocios")
CARPETA_SALIDA = os.path.join(RAIZ, "t")
SITIO = "https://www.gogodevs.cl"
PRODUCTO = "/servicios/link-en-bio/"
# Misma version que pone _blog/sitio_comun.py en el resto del sitio.
MEDICION = "/assets/js/medicion.js?v=20261111-tree"
POLITICA_GOGODEVS = SITIO + "/legal/privacidad/#cookies"

SKINS = ("base", "oscura", "foto")
PLANES = ("gogodevs", "dominio_propio")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
EXT_IMAGEN = (".webp", ".png", ".jpg", ".jpeg", ".svg")
MAX_BYTES_IMAGEN = 200 * 1024

# Iconos (24x24). "f" = relleno (marcas), "s" = trazo.
ICONOS = {
    "whatsapp": ("f", '<path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.07-.3-.15-1.26-.46-2.39-1.47-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.18.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.61-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48 0 1.46 1.07 2.88 1.21 3.07.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.7.63.71.23 1.36.2 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.18-1.41-.08-.13-.28-.2-.57-.35m-5.42 7.4h-.01a9.87 9.87 0 0 1-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1-1.51-5.26c0-5.45 4.44-9.88 9.89-9.88 2.64 0 5.12 1.03 6.99 2.9a9.82 9.82 0 0 1 2.89 6.99c0 5.45-4.44 9.88-9.88 9.88m8.41-18.3A11.82 11.82 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.89c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.88 11.88 0 0 0 5.68 1.45h.01c6.55 0 11.89-5.34 11.89-11.89 0-3.18-1.24-6.17-3.48-8.41z"/>'),
    "instagram": ("f", '<path d="M12 2.16c3.2 0 3.58.01 4.85.07 3.25.15 4.77 1.69 4.92 4.92.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.15 3.23-1.66 4.77-4.92 4.92-1.27.06-1.64.07-4.85.07s-3.58-.01-4.85-.07c-3.26-.15-4.77-1.7-4.92-4.92C2.17 15.58 2.16 15.2 2.16 12s.01-3.58.07-4.85C2.38 3.92 3.9 2.38 7.15 2.23 8.42 2.17 8.8 2.16 12 2.16zM12 0C8.74 0 8.33.01 7.05.07 2.7.27.27 2.7.07 7.05.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.2 4.36 2.62 6.78 6.98 6.98C8.33 23.99 8.74 24 12 24s3.67-.01 4.95-.07c4.35-.2 6.78-2.62 6.98-6.98.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95c-.2-4.35-2.62-6.78-6.98-6.98C15.67.01 15.26 0 12 0zm0 5.84a6.16 6.16 0 1 0 0 12.32 6.16 6.16 0 0 0 0-12.32zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.4-11.85a1.44 1.44 0 1 0 0 2.88 1.44 1.44 0 0 0 0-2.88z"/>'),
    "facebook": ("f", '<path d="M24 12.07C24 5.45 18.63.07 12 .07S0 5.45 0 12.07c0 5.99 4.39 10.95 10.13 11.85v-8.38H7.08v-3.47h3.05V9.43c0-3 1.79-4.67 4.53-4.67 1.31 0 2.69.24 2.69.24v2.95h-1.51c-1.49 0-1.96.93-1.96 1.88v2.25h3.33l-.53 3.47h-2.8v8.38C19.61 23.03 24 18.06 24 12.07z"/>'),
    "tiktok": ("f", '<path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-2.88 2.5 2.89 2.89 0 0 1-2.89-2.89 2.89 2.89 0 0 1 2.89-2.89c.28 0 .54.04.79.1V9.01a6.33 6.33 0 0 0-.79-.05 6.34 6.34 0 0 0-6.34 6.34 6.34 6.34 0 0 0 6.34 6.34 6.34 6.34 0 0 0 6.33-6.34V8.69a8.18 8.18 0 0 0 4.78 1.52V6.78a4.85 4.85 0 0 1-1.01-.09z"/>'),
    "youtube": ("f", '<path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.6 12 3.6 12 3.6s-7.5 0-9.4.5A3 3 0 0 0 .5 6.2 31 31 0 0 0 0 12a31 31 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.5 9.4.5 9.4.5s7.5 0 9.4-.5a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24 12a31 31 0 0 0-.5-5.8zM9.6 15.6V8.4l6.2 3.6-6.2 3.6z"/>'),
    "mapa": ("s", '<path d="M12 21s-7-6.1-7-11.5a7 7 0 0 1 14 0C19 14.9 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>'),
    "catalogo": ("s", '<rect x="3" y="3" width="7.5" height="7.5" rx="1.6"/><rect x="13.5" y="3" width="7.5" height="7.5" rx="1.6"/><rect x="3" y="13.5" width="7.5" height="7.5" rx="1.6"/><rect x="13.5" y="13.5" width="7.5" height="7.5" rx="1.6"/>'),
    "tienda": ("s", '<path d="M6 2.5 3 6.5v13a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-13l-3-4z"/><path d="M3 6.5h18M16 10.5a4 4 0 0 1-8 0"/>'),
    "carta": ("s", '<path d="M4 2.5v7a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2v-7M7 2.5v19M20 15V2.5a4.5 4.5 0 0 0-4.5 4.5v6a2 2 0 0 0 2 2H20zm0 0v6.5"/>'),
    "calendario": ("s", '<rect x="3" y="4.5" width="18" height="16.5" rx="2"/><path d="M16 2.5v4M8 2.5v4M3 10h18"/>'),
    "estrella": ("s", '<path d="m12 2.8 2.8 5.8 6.4.9-4.6 4.5 1.1 6.3L12 17.3l-5.7 3 1.1-6.3-4.6-4.5 6.4-.9z"/>'),
    "web": ("s", '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>'),
    "telefono": ("s", '<path d="M21.5 16.4v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 1.6 3.7 2 2 0 0 1 3.6 1.5h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L7.5 9.4a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.8 2z"/>'),
    "correo": ("s", '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 7 10-7"/>'),
    "enlace": ("s", '<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>'),
}
RELOJ = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
FLECHA = '<svg class="boton__flecha" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'


class ErrorTree(ValueError):
    pass


# --------------------------------------------------------------------------
# Color y contraste (WCAG 2.1)
# --------------------------------------------------------------------------
def rgb(hexa):
    return tuple(int(hexa[i:i + 2], 16) for i in (1, 3, 5))


def luminancia(hexa):
    def canal(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (canal(c) for c in rgb(hexa))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(a, b):
    la, lb = sorted((luminancia(a), luminancia(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def mezclar(hexa, con, peso):
    """peso = cuanto de `con` (0..1)."""
    a, b = rgb(hexa), rgb(con)
    return "#%02x%02x%02x" % tuple(round(x * (1 - peso) + y * peso) for x, y in zip(a, b))


def rgba(hexa, alfa):
    return "rgba(%d, %d, %d, %s)" % (rgb(hexa) + (alfa,))


# --------------------------------------------------------------------------
# Lectura y validacion
# --------------------------------------------------------------------------
def leer_negocios():
    if not os.path.isdir(CARPETA_NEGOCIOS):
        return []
    salida = []
    for nombre in sorted(os.listdir(CARPETA_NEGOCIOS)):
        if nombre.endswith(".json"):
            salida.append(validar(nombre[:-5], os.path.join(CARPETA_NEGOCIOS, nombre)))
    return salida


def _texto(d, clave, slug, maximo, obligatorio=True):
    v = d.get(clave)
    if v is None or (isinstance(v, str) and not v.strip()):
        if obligatorio:
            raise ErrorTree("%s: falta '%s'" % (slug, clave))
        return ""
    if not isinstance(v, str):
        raise ErrorTree("%s: '%s' tiene que ser texto" % (slug, clave))
    v = v.strip()
    if len(v) > maximo:
        raise ErrorTree("%s: '%s' tiene %d caracteres (maximo %d)" % (slug, clave, len(v), maximo))
    return v


def _archivo_del_negocio(slug, valor, campo):
    """Un archivo dentro de _tree/negocios/<slug>/ (logo, foto de fondo)."""
    if not isinstance(valor, str) or "/" in valor or "\\" in valor or valor.startswith("."):
        raise ErrorTree("%s: '%s' debe ser un nombre de archivo dentro de _tree/negocios/%s/" % (slug, campo, slug))
    if not valor.lower().endswith(EXT_IMAGEN):
        raise ErrorTree("%s: '%s' debe ser %s" % (slug, campo, ", ".join(EXT_IMAGEN)))
    ruta = os.path.join(CARPETA_NEGOCIOS, slug, valor)
    if not os.path.isfile(ruta):
        raise ErrorTree("%s: no existe _tree/negocios/%s/%s" % (slug, slug, valor))
    if os.path.getsize(ruta) > MAX_BYTES_IMAGEN:
        raise ErrorTree("%s: %s pesa %d KB (maximo %d KB: achicarla y pasarla a WebP)"
                        % (slug, valor, os.path.getsize(ruta) // 1024, MAX_BYTES_IMAGEN // 1024))
    return ruta


def _enlace_del_boton(slug, i, b):
    claves = [k for k in ("url", "whatsapp", "telefono", "correo") if k in b]
    if len(claves) != 1:
        raise ErrorTree("%s: el boton %d necesita UNO de url / whatsapp / telefono / correo" % (slug, i))
    k = claves[0]
    v = b[k]
    if k == "url":
        if not isinstance(v, str) or not v.startswith("https://"):
            raise ErrorTree("%s: boton %d: la url tiene que empezar con https://" % (slug, i))
        return v, True
    if k == "whatsapp":
        if not isinstance(v, dict):
            raise ErrorTree("%s: boton %d: whatsapp es {\"numero\": \"569...\", \"mensaje\": \"...\"}" % (slug, i))
        numero = re.sub(r"\D", "", str(v.get("numero", "")))
        if not 10 <= len(numero) <= 15:
            raise ErrorTree("%s: boton %d: el numero de WhatsApp va con codigo de pais y sin +, ej. 56912345678" % (slug, i))
        url = "https://wa.me/" + numero
        mensaje = (v.get("mensaje") or "").strip()
        if mensaje:
            url += "?text=" + quote(mensaje, safe="")
        return url, True
    if k == "telefono":
        numero = re.sub(r"[^\d+]", "", str(v))
        if not re.match(r"^\+\d{9,15}$", numero):
            raise ErrorTree("%s: boton %d: telefono con + y codigo de pais, ej. +56912345678" % (slug, i))
        return "tel:" + numero, False
    if not re.match(r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$", str(v), re.I):
        raise ErrorTree("%s: boton %d: correo invalido" % (slug, i))
    return "mailto:" + v, False


def validar(slug, ruta):
    if not SLUG_RE.match(slug):
        raise ErrorTree("%s.json: el nombre del archivo es el slug (minusculas, numeros y guiones)" % slug)
    try:
        d = json.load(open(ruta, encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ErrorTree("%s.json no es JSON valido: %s" % (slug, e))
    if not isinstance(d, dict):
        raise ErrorTree("%s.json tiene que ser un objeto {...}" % slug)
    conocidas = {"plan", "dominio", "nombre", "descripcion", "logo", "colores", "skin", "fondo",
                 "horario", "botones", "credito_gogodevs", "aviso", "politica_url", "nota"}
    sobran = sorted(set(d) - conocidas)
    if sobran:
        raise ErrorTree("%s: clave(s) desconocida(s): %s" % (slug, ", ".join(sobran)))

    n = {"slug": slug}
    n["plan"] = d.get("plan", "gogodevs")
    if n["plan"] not in PLANES:
        raise ErrorTree("%s: plan debe ser %s" % (slug, " o ".join(PLANES)))
    n["dominio"] = (d.get("dominio") or "").strip().lower()
    if n["plan"] == "dominio_propio" and not re.match(r"^[a-z0-9-]+(\.[a-z0-9-]+)+$", n["dominio"]):
        raise ErrorTree("%s: el plan dominio_propio necesita 'dominio' (ej. tunegocio.cl)" % slug)
    # El credito "Hecho por GoGoDevS" va en el plan de gogodevs.cl (es parte de
    # ese precio). En el de dominio propio se apaga: es lo que el cliente paga.
    n["credito"] = d.get("credito_gogodevs", n["plan"] == "gogodevs")
    if not isinstance(n["credito"], bool):
        raise ErrorTree("%s: credito_gogodevs es true o false" % slug)
    if n["plan"] == "gogodevs" and not n["credito"]:
        raise ErrorTree("%s: el plan gogodevs lleva el credito (credito_gogodevs: true)" % slug)

    n["nombre"] = _texto(d, "nombre", slug, 40)
    n["descripcion"] = _texto(d, "descripcion", slug, 140)
    n["horario"] = _texto(d, "horario", slug, 50, obligatorio=False)

    colores = d.get("colores") or {}
    principal = colores.get("principal", "")
    if not HEX_RE.match(principal):
        raise ErrorTree("%s: colores.principal debe ser #RRGGBB" % slug)
    n["principal"] = principal.lower()
    # El texto sobre el color principal: blanco o casi negro, el que contraste mas.
    blanco, negro = contraste(principal, "#ffffff"), contraste(principal, "#111111")
    n["sobre_principal"] = "#ffffff" if blanco >= negro else "#111111"
    mejor = max(blanco, negro)
    if mejor < 4.5:
        raise ErrorTree("%s: colores.principal %s no deja leer el texto encima (contraste %.2f, minimo 4,5). "
                        "Usar un tono mas oscuro o mas claro del color de la marca." % (slug, principal, mejor))
    fondo = colores.get("fondo")
    if fondo is not None and not HEX_RE.match(fondo):
        raise ErrorTree("%s: colores.fondo debe ser #RRGGBB" % slug)
    n["fondo"] = (fondo or mezclar(principal, "#ffffff", 0.92)).lower()

    n["skin"] = d.get("skin", "base")
    if n["skin"] not in SKINS:
        raise ErrorTree("%s: skin debe ser %s" % (slug, ", ".join(SKINS)))
    if n["skin"] == "base" and contraste(n["fondo"], "#16181d") < 7:
        raise ErrorTree("%s: colores.fondo %s es muy oscuro para la skin base (usar la skin oscura)" % (slug, n["fondo"]))

    n["foto"] = None
    if n["skin"] == "foto":
        if not d.get("fondo"):
            raise ErrorTree("%s: la skin foto necesita 'fondo' (foto del negocio)" % slug)
        valor = d["fondo"]
        if isinstance(valor, str) and valor.startswith("/assets/"):
            # Solo para los ejemplos: una foto que ya existe en gogodevs.cl. En el
            # dominio propio no sirve (la ruta seria la del dominio del cliente).
            if n["plan"] != "gogodevs" or not os.path.isfile(os.path.join(RAIZ, valor.lstrip("/"))):
                raise ErrorTree("%s: 'fondo' %s no existe o no se puede usar con dominio propio" % (slug, valor))
            n["foto"] = ("sitio", valor)
        else:
            n["foto"] = ("archivo", _archivo_del_negocio(slug, valor, "fondo"))

    n["logo"] = _archivo_del_negocio(slug, d["logo"], "logo") if d.get("logo") else None

    botones = d.get("botones")
    if not isinstance(botones, list) or not 1 <= len(botones) <= 8:
        raise ErrorTree("%s: 'botones' es una lista de 1 a 8 botones" % slug)
    n["botones"] = []
    destacados = 0
    for i, b in enumerate(botones, 1):
        if not isinstance(b, dict):
            raise ErrorTree("%s: el boton %d tiene que ser un objeto" % (slug, i))
        icono = b.get("icono", "enlace")
        if icono not in ICONOS:
            raise ErrorTree("%s: boton %d: icono '%s' no existe (%s)" % (slug, i, icono, ", ".join(sorted(ICONOS))))
        url, externo = _enlace_del_boton(slug, i, b)
        destacado = bool(b.get("destacado"))
        destacados += destacado
        n["botones"].append({
            "texto": _texto(b, "texto", "%s boton %d" % (slug, i), 48),
            "detalle": _texto(b, "detalle", "%s boton %d" % (slug, i), 70, obligatorio=False),
            "icono": icono, "url": url, "externo": externo, "destacado": destacado,
        })
    if destacados > 1:
        raise ErrorTree("%s: solo un boton puede ser destacado (el que mas importa, casi siempre WhatsApp)" % slug)

    aviso = d.get("aviso")
    n["aviso"] = None
    if aviso:
        if not isinstance(aviso, dict) or not aviso.get("texto"):
            raise ErrorTree("%s: aviso es {\"texto\": ..., \"enlace\": ..., \"enlace_texto\": ...}" % slug)
        enlace = aviso.get("enlace", "")
        if enlace and not (enlace.startswith("/") or enlace.startswith("https://")):
            raise ErrorTree("%s: aviso.enlace debe ser una ruta del sitio o https://" % slug)
        n["aviso"] = {"texto": _texto(aviso, "texto", slug, 160), "enlace": enlace,
                      "enlace_texto": _texto(aviso, "enlace_texto", slug, 40, obligatorio=bool(enlace))}

    politica = d.get("politica_url")
    if politica and not str(politica).startswith("https://"):
        raise ErrorTree("%s: politica_url tiene que empezar con https://" % slug)
    n["politica"] = politica or (POLITICA_GOGODEVS if n["plan"] == "dominio_propio" else "")
    return n


# --------------------------------------------------------------------------
# Render
# --------------------------------------------------------------------------
def esc(s):
    return html.escape(s, quote=True)


def iniciales(nombre):
    palabras = [p for p in re.split(r"\s+", nombre) if p.lower() not in {"de", "del", "la", "el", "los", "las", "y"}]
    return "".join(p[0] for p in palabras[:2]).upper() or nombre[:1].upper()


def favicon_iniciales(n):
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle cx="32" cy="32" r="32" fill="%s"/>'
           '<text x="32" y="41" font-family="Arial,sans-serif" font-size="26" font-weight="700" text-anchor="middle" fill="%s">%s</text></svg>'
           % (n["principal"], n["sobre_principal"], esc(iniciales(n["nombre"]))))
    return "data:image/svg+xml," + quote(svg, safe="")


def nombre_publicado(ruta_origen, base):
    return base + os.path.splitext(ruta_origen)[1].lower().replace(".jpeg", ".jpg")


def icono_svg(nombre):
    tipo, cuerpo = ICONOS[nombre]
    if tipo == "f":
        return '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">%s</svg>' % cuerpo
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true">%s</svg>' % cuerpo)


def boton_html(b):
    clase = "boton boton--destacado" if b["destacado"] else "boton"
    destino = ' target="_blank" rel="noopener"' if b["externo"] else ""
    detalle = '<span class="boton__detalle">%s</span>' % esc(b["detalle"]) if b["detalle"] else ""
    return ('      <a class="%s" href="%s"%s data-texto="%s">\n'
            '        <span class="boton__icono">%s</span>\n'
            '        <span class="boton__texto"><span class="boton__titulo">%s</span>%s</span>\n'
            '        %s\n'
            '      </a>\n' % (clase, esc(b["url"]), destino, esc(b["texto"]), icono_svg(b["icono"]),
                              esc(b["texto"]), detalle, FLECHA))


def css_negocio(n):
    reglas = ["--principal: %s" % n["principal"],
              "--sobre-principal: %s" % n["sobre_principal"],
              "--sobre-principal-suave: %s" % (rgba("#ffffff", ".2") if n["sobre_principal"] == "#ffffff" else rgba("#000000", ".12")),
              "--sombra-principal: %s" % rgba(n["principal"], ".32")]
    if n["skin"] == "base":
        reglas.append("--fondo: %s" % n["fondo"])
    if n["skin"] == "oscura":
        reglas += ["--brillo: %s" % rgba(n["principal"], ".34"), "--brillo-suave: %s" % rgba(n["principal"], ".12")]
    if n["skin"] == "foto":
        archivo = n["foto"][1] if n["foto"][0] == "sitio" else nombre_publicado(n["foto"][1], "fondo")
        reglas.append("--foto: url('%s')" % archivo)
    return "body {\n  " + ";\n  ".join(reglas) + ";\n}"


def render(n, plantilla):
    leer = lambda nombre: open(os.path.join(AQUI, "skins", nombre), encoding="utf-8").read().strip()
    css = "\n".join((leer("_comun.css"), leer(n["skin"] + ".css"), css_negocio(n)))
    # Los comentarios son para quien edita las skins, no para el visitante.
    css = re.sub(r"/\*.*?\*/\s*", "", css, flags=re.S).strip()
    css = "\n".join("    " + linea if linea else "" for linea in css.split("\n"))

    if n["logo"]:
        logo_pub = nombre_publicado(n["logo"], "logo")
        logo = ('<div class="logo"><img src="%s" alt="Logo de %s" width="92" height="92" fetchpriority="high"></div>'
                % (logo_pub, esc(n["nombre"])))
        favicon = logo_pub
    else:
        logo = '<div class="logo logo--iniciales" aria-hidden="true">%s</div>' % esc(iniciales(n["nombre"]))
        favicon = favicon_iniciales(n)

    aviso = ""
    if n["aviso"]:
        enlace = ' <a href="%s">%s</a>' % (esc(n["aviso"]["enlace"]), esc(n["aviso"]["enlace_texto"])) if n["aviso"]["enlace"] else ""
        aviso = '  <p class="aviso">%s%s</p>\n' % (esc(n["aviso"]["texto"]), enlace)

    horario = ('      <p class="horario">%s<span>%s</span></p>\n' % (RELOJ, esc(n["horario"]))) if n["horario"] else ""

    pie = ""
    if n["credito"]:
        pie = ('\n    <footer class="pie"><a href="%s">Hecho por <strong>GoGoDevS</strong></a></footer>\n'
               % (PRODUCTO if n["plan"] == "gogodevs" else SITIO + PRODUCTO))

    # Dominio propio: el visitante esta en tunegocio.cl, asi que lo compartido
    # con gogodevs.cl va con URL absoluta (una ruta /assets/... seria del dominio
    # del cliente). Lo del negocio (logo, foto) va relativo y viaja con el Tree.
    medicion = MEDICION if n["plan"] == "gogodevs" else SITIO + MEDICION
    reemplazos = {
        "SLUG": n["slug"],
        "ATRIBUTO_POLITICA": ' data-politica="%s"' % esc(n["politica"]) if n["politica"] else "",
        "TITULO": esc(n["nombre"]),
        "DESCRIPCION": esc(n["descripcion"]),
        "NOMBRE": esc(n["nombre"]),
        "COLOR_TEMA": n["fondo"] if n["skin"] == "base" else ("#0d0f13" if n["skin"] == "oscura" else "#111111"),
        "FAVICON": esc(favicon),
        "OG_IMAGEN": "",
        "CSS": css,
        "AVISO": aviso,
        "LOGO": logo,
        "HORARIO": horario,
        "BOTONES": "".join(boton_html(b) for b in n["botones"]),
        "PIE": pie,
        "MEDICION": esc(medicion),
    }
    salida = plantilla
    for k, v in reemplazos.items():
        salida = salida.replace("{{%s}}" % k, v)
    if "{{" in salida:
        raise ErrorTree("%s: quedo un marcador sin reemplazar" % n["slug"])
    return salida


INDICE_T = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!-- ARCHIVO GENERADO por _tree/generar.py. Existe para que /t/ no liste la
       carpeta con todos los Tree: manda a la pagina del producto. -->
  <title>GoGoDevS Tree</title>
  <meta name="robots" content="noindex, follow">
  <meta http-equiv="refresh" content="0; url=%(p)s">
  <link rel="canonical" href="%(s)s%(p)s">
</head>
<body>
  <p><a href="%(p)s">GoGoDevS Tree: link en bio para tu negocio</a></p>
</body>
</html>
""" % {"p": PRODUCTO, "s": SITIO}


# --------------------------------------------------------------------------
# Escritura / revision
# --------------------------------------------------------------------------
def archivos_esperados(negocios, plantilla):
    """{ruta relativa a la raiz: bytes} de todo lo que tiene que haber en t/."""
    esperado = {"t/index.html": INDICE_T.encode("utf-8")}
    for n in negocios:
        base = "t/%s/" % n["slug"]
        esperado[base + "index.html"] = render(n, plantilla).encode("utf-8")
        if n["logo"]:
            esperado[base + nombre_publicado(n["logo"], "logo")] = open(n["logo"], "rb").read()
        if n["foto"] and n["foto"][0] == "archivo":
            esperado[base + nombre_publicado(n["foto"][1], "fondo")] = open(n["foto"][1], "rb").read()
    return esperado


def _leer_bytes(ruta):
    """Bytes del archivo; los .html con CRLF (checkout en Windows) cuentan como LF."""
    b = open(ruta, "rb").read()
    return b.replace(b"\r\n", b"\n") if ruta.endswith(".html") else b


def revisar():
    """Lista de errores (vacia = todo al dia). No escribe nada."""
    try:
        negocios = leer_negocios()
        plantilla = open(os.path.join(AQUI, "plantilla.html"), encoding="utf-8").read()
        esperado = archivos_esperados(negocios, plantilla)
    except ErrorTree as e:
        return ["Tree: %s" % e]
    errores = []
    for rel, contenido in sorted(esperado.items()):
        ruta = os.path.join(RAIZ, rel)
        if not os.path.isfile(ruta):
            errores.append("Tree: falta %s (correr python _tree/generar.py)" % rel)
        elif _leer_bytes(ruta) != contenido:
            errores.append("Tree: %s no coincide con su JSON (se edita _tree/negocios/, no t/; correr python _tree/generar.py)" % rel)
    if os.path.isdir(CARPETA_SALIDA):
        for carpeta, _, archivos in os.walk(CARPETA_SALIDA):
            for a in archivos:
                rel = os.path.relpath(os.path.join(carpeta, a), RAIZ).replace("\\", "/")
                if rel not in esperado:
                    errores.append("Tree: %s no sale de ningun JSON de _tree/negocios/ (si el negocio se dio de baja, borrar su carpeta)" % rel)
    sitemap = os.path.join(RAIZ, "sitemap.xml")
    if os.path.isfile(sitemap) and "/t/" in open(sitemap, encoding="utf-8").read():
        errores.append("Tree: sitemap.xml no puede listar paginas de /t/ (van con noindex)")
    return errores


def generar():
    negocios = leer_negocios()
    plantilla = open(os.path.join(AQUI, "plantilla.html"), encoding="utf-8").read()
    cambios = []
    for rel, contenido in sorted(archivos_esperados(negocios, plantilla).items()):
        ruta = os.path.join(RAIZ, rel)
        if os.path.isfile(ruta) and _leer_bytes(ruta) == contenido:
            continue
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "wb") as f:
            f.write(contenido)
        cambios.append(rel)
    print("Tree: %d negocio(s) | archivos escritos: %d" % (len(negocios), len(cambios)))
    for c in cambios:
        print("  - " + c)
    for n in negocios:
        print("  %-22s plan %-15s skin %-7s %s" % (n["slug"], n["plan"], n["skin"],
              ("https://" + n["dominio"]) if n["plan"] == "dominio_propio" else SITIO + "/t/%s/" % n["slug"]))
    sobrantes = [e for e in revisar() if "no sale de ningun JSON" in e]
    for e in sobrantes:
        print("  ! " + e)
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if "--revisar" in sys.argv:
        errores = revisar()
        print("\n".join(errores) or "Tree: todo al dia")
        sys.exit(1 if errores else 0)
    try:
        sys.exit(generar())
    except ErrorTree as e:
        print("ERROR: %s" % e)
        sys.exit(1)
