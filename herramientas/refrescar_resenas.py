# -*- coding: utf-8 -*-
"""Trae las resenas de la ficha de Google y dice cuales faltan en el sitio.

    python herramientas/refrescar_resenas.py              # ensayo: solo informa
    python herramientas/refrescar_resenas.py --confirmar  # ademas actualiza el total

POR QUE VARIAS LLAMADAS: la Places API devuelve como MAXIMO 5 resenas por local
y no se puede elegir cuales. Pero NO devuelve siempre las mismas: cambiando
`languageCode` responde con otro subconjunto. Con ~10 llamadas se juntaron 8 de
las 16 el 30-09-2026. No es un truco contra Google: son llamadas legitimas a su
API con la key del proyecto.

POR QUE NO ESCRIBE LAS TARJETAS SOLO: el texto de una resena es lo que un
cliente publico con su nombre. Antes de ponerlo en la portada conviene mirarlo,
y sobre todo decidir a que proyecto se enlaza -- un enlace equivocado lo ve el
cliente. El script deja el HTML listo para pegar y la decision es de quien mira.

La key sale de GOOGLE_MAPS_API_KEY (env) o del .env de GoGoCRM. Nunca se
escribe en este archivo ni se imprime.
"""
import argparse, html as H, io, json, os, re, sys, urllib.request
from pathlib import Path

PLACE_ID = 'ChIJz7iiJJpaC4sREf_2_WIRqYY'          # ficha de GoGoDevS
IDIOMAS = ['', 'es', 'es-CL', 'es-419', 'en', 'pt', 'fr', 'de', 'it']
INDEX = Path(__file__).resolve().parent.parent / 'index.html'
DOTENV = Path.home() / 'Desktop' / 'backup-gogodevs' / 'Proyectos GoGoDevS' / 'GoGoCRM' / '.env'


def leer_key():
    k = os.environ.get('GOOGLE_MAPS_API_KEY')
    if k:
        return k.strip()
    if DOTENV.exists():
        for linea in DOTENV.read_text(encoding='utf-8', errors='ignore').splitlines():
            if linea.startswith('GOOGLE_MAPS_API_KEY='):
                return linea.split('=', 1)[1].strip().strip('"\'')
    sys.exit('falta GOOGLE_MAPS_API_KEY (env o el .env de GoGoCRM)')


def pedir(key, idioma):
    url = 'https://places.googleapis.com/v1/places/%s' % PLACE_ID
    if idioma:
        url += '?languageCode=%s' % idioma
    req = urllib.request.Request(url, headers={
        'X-Goog-Api-Key': key,
        'X-Goog-FieldMask': 'reviews,rating,userRatingCount',
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def texto_de(r):
    """El texto TAL CUAL lo escribio la persona. `text` viene traducido al
    idioma del request; `originalText` es el original."""
    return ((r.get('originalText') or {}).get('text')
            or (r.get('text') or {}).get('text') or '').strip()


def tarjeta(nombre, texto):
    return (
'          <figure class="testi-card testi-card--google">\n'
'            <div class="testi-card__top">\n'
'              <span class="estrellas" role="img" aria-label="5 de 5 estrellas">\u2605\u2605\u2605\u2605\u2605</span>\n'
'              <span class="sello-google">Rese\u00f1a en Google</span>\n'
'            </div>\n'
'            <blockquote class="testi-card__quote">%s</blockquote>\n'
'            <figcaption class="testi-card__author">\n'
'              <span class="testi-card__avatar" aria-hidden="true">%s</span>\n'
'              <span class="testi-card__meta">\n'
'                <strong>%s</strong>\n'
'                <!-- si sabes de que cliente es:\n'
'                <a class="testi-card__proyecto" href="/proyectos/SLUG/">Nombre</a> -->\n'
'              </span>\n'
'            </figcaption>\n'
'          </figure>\n'
    ) % (H.escape(texto), nombre.strip()[0].upper(), H.escape(nombre))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--confirmar', action='store_true',
                    help='actualiza el total de resenas en index.html')
    args = ap.parse_args()

    key = leer_key()
    pool, total, rating = {}, None, None
    for idioma in IDIOMAS:
        try:
            d = pedir(key, idioma)
        except Exception as e:                       # una llamada que falla no corta el resto
            print('  aviso: fallo la llamada %r (%s)' % (idioma or 'sin idioma', e))
            continue
        total = d.get('userRatingCount', total)
        rating = d.get('rating', rating)
        for r in d.get('reviews', []):
            pool.setdefault(r.get('authorAttribution', {}).get('displayName'), r)

    print('Ficha de Google: %s resenas, nota %s' % (total, rating))
    print('Juntadas en %d llamadas: %d (la API da 5 por vez)' % (len(IDIOMAS), len(pool)))

    # Solo los <strong> DEL CARRUSEL: el resto del index tiene otros (precios,
    # titulares) y contarlos daba "publicadas: 17" con 11 tarjetas.
    html_completo = INDEX.read_text(encoding='utf-8')
    ini = html_completo.find('testi-grid--carrusel')
    fin = html_completo.find('</section>', ini)
    if ini == -1 or fin == -1:
        sys.exit('no encontre el carrusel en index.html')
    publicadas = set(re.findall(r'<strong>([^<]+)</strong>', html_completo[ini:fin]))
    nuevas = [(n, texto_de(r)) for n, r in pool.items()
              if n not in publicadas and texto_de(r)]
    sin_texto = [n for n, r in pool.items() if not texto_de(r)]

    print('Publicadas en el carrusel: %d' % len(publicadas))
    if sin_texto:
        print('Solo estrellas (no van como tarjeta, si cuentan en el total): %s'
              % ', '.join(sin_texto))

    if not nuevas:
        print('\nNo hay resenas nuevas con texto.')
    else:
        print('\n%d RESENA(S) NUEVA(S). Pegar dentro de .testi-grid--carrusel:\n' % len(nuevas))
        for n, t in nuevas:
            print(tarjeta(n, t))

    if total:
        html = html_completo
        actual = re.search(r'A base de (\d+) rese\u00f1as', html)
        if actual and int(actual.group(1)) != total:
            print('El total del sitio dice %s y son %s.' % (actual.group(1), total))
            if args.confirmar:
                INDEX.write_text(
                    re.sub(r'A base de \d+ rese\u00f1as',
                           'A base de %d rese\u00f1as' % total, html),
                    encoding='utf-8', newline='')
                print('  -> actualizado a %d.' % total)
            else:
                print('  -> correr con --confirmar para actualizarlo.')
        elif actual:
            print('El total del sitio (%s) esta al dia.' % actual.group(1))


if __name__ == '__main__':
    main()
