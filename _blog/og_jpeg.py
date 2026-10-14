# -*- coding: utf-8 -*-
"""La miniatura al compartir (og:image) en JPEG, porque WhatsApp no muestra WebP.

Probado en iPhone y Android el 13-10-2026 con puntoparcelas.cl: con og:image en
WebP el link llega sin foto. Todo gogodevs.cl tenia og:image en WebP (40 de 40
paginas, auditoria del 14-10), asi que los links que se comparten del sitio
llegaban sin imagen.

La foto de la pagina se queda en WebP (pesa menos). Esto arma APARTE una copia
1200x630 recortada al centro, en JPEG bajo 300 KB, con el sufijo `-og.jpg`.

    python _blog/og_jpeg.py --todo     convierte todas las og:image del sitio y
                                       corrige las etiquetas de cada pagina

publicar.py la usa para cada articulo nuevo del blog.
"""
import io
import os
import re
import sys

ANCHO, ALTO = 1200, 630
LIMITE = 300 * 1024
DOMINIO = "https://www.gogodevs.cl"


def hacer_og(origen, destino):
    """Escribe en `destino` el JPEG 1200x630 de `origen`. Devuelve los bytes escritos."""
    from PIL import Image, ImageOps  # aca y no arriba: publicar.py sin og no lo necesita

    img = ImageOps.exif_transpose(Image.open(origen)).convert("RGB")
    img = ImageOps.fit(img, (ANCHO, ALTO), Image.LANCZOS, centering=(0.5, 0.5))
    datos = b""
    for calidad in (85, 78, 70, 62):
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=calidad, optimize=True, progressive=True)
        datos = buf.getvalue()
        if len(datos) <= LIMITE:
            break
    with open(destino, "wb") as f:
        f.write(datos)
    return len(datos)


def nombre_og(ruta_webp):
    """'assets/img/x.webp' -> 'assets/img/x-og.jpg'"""
    return re.sub(r"\.webp$", "-og.jpg", ruta_webp, flags=re.I)


def _corregir_etiquetas(texto, url_jpg):
    """og:image y twitter:image al JPEG, y su tipo y medidas reales."""
    texto = re.sub(r'(<meta\s+property="og:image"\s+content=")[^"]+\.webp(")', r"\g<1>%s\2" % url_jpg, texto)
    texto = re.sub(r'(<meta\s+name="twitter:image"\s+content=")[^"]+\.webp(")', r"\g<1>%s\2" % url_jpg, texto)
    texto = re.sub(r'(<meta\s+property="og:image:width"\s+content=")\d+(")', r"\g<1>%d\2" % ANCHO, texto)
    texto = re.sub(r'(<meta\s+property="og:image:height"\s+content=")\d+(")', r"\g<1>%d\2" % ALTO, texto)
    texto = re.sub(r'(<meta\s+property="og:image:type"\s+content=")image/webp(")', r"\1image/jpeg\2", texto)
    return texto


def todo(raiz):
    hechos, paginas = {}, 0
    for carpeta, dirs, archivos in os.walk(raiz):
        dirs[:] = [d for d in dirs if not d.startswith((".", "_"))]
        for nombre in archivos:
            if not nombre.endswith(".html"):
                continue
            ruta = os.path.join(carpeta, nombre)
            texto = open(ruta, encoding="utf-8", newline="").read()
            m = re.search(r'<meta\s+property="og:image"\s+content="%s(/[^"]+\.webp)"' % re.escape(DOMINIO), texto)
            if not m:
                continue
            rel = m.group(1).lstrip("/")
            jpg_rel = nombre_og(rel)
            if rel not in hechos:
                origen = os.path.join(raiz, *rel.split("/"))
                if not os.path.isfile(origen):
                    print("FALTA la imagen de origen %s (en %s)" % (rel, ruta))
                    continue
                hechos[rel] = hacer_og(origen, os.path.join(raiz, *jpg_rel.split("/")))
            nuevo = _corregir_etiquetas(texto, DOMINIO + "/" + jpg_rel)
            if nuevo != texto:
                open(ruta, "w", encoding="utf-8", newline="").write(nuevo)
                paginas += 1
    for rel, peso in sorted(hechos.items()):
        print("%6d KB  %s" % (peso // 1024, nombre_og(rel)))
    print("Imagenes: %d · paginas corregidas: %d" % (len(hechos), paginas))


if __name__ == "__main__":
    if "--todo" in sys.argv:
        todo(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    else:
        print(__doc__)
