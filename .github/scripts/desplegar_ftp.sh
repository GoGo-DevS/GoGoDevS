#!/usr/bin/env bash
# Despliega gogodevs.cl por FTPS: TLS OBLIGATORIO, servidor VERIFICADO y RAIZ COMPROBADA antes de borrar.
# Lo usan deploy.yml y blog-diario.yml (un solo lugar para la configuracion de transporte).
#
# Transporte:
#   - ftp:ssl-force yes: si el servidor no acepta AUTH TLS, lftp aborta ANTES de mandar el usuario.
#   - ftp:ssl-protect-data/list yes: los archivos y los listados tambien van cifrados (PROT P).
#   - ssl:verify-certificate + ssl:check-hostname + ssl:ca-file: el certificado tiene que encadenar a
#     ISRG Root X1 por los intermedios de Let's Encrypt versionados y ser del nombre FTP_SERVIDOR.
# Raiz (antes de cualquier operacion destructiva; mirror --delete borra lo que no esta en el repo):
#   1. listado de SOLO LECTURA del destino: tiene que estar el centinela .gogodevs-publicacion (lo crea
#      Diego una vez, a mano, en public_html) y el destino NO puede parecer el home de la cuenta.
#   2. el centinela esta excluido del mirror: nunca se sube, se pisa ni se borra.
#   3. DEPLOY_SIMULAR=1 hace mirror --dry-run: muestra que subiria y que borraria, sin escribir.
#   4. despues del mirror real se comprueba que el centinela sigue ahi.
#
# Por que vsur2.vtosur.cl y no ftp.gogodevs.cl: el certificado del servidor (VtoSur, DirectAdmin) es
# de vsur2.vtosur.cl; con ftp.gogodevs.cl la verificacion de nombre falla. Es el mismo servidor
# (138.186.10.116 / 2803:8240:310:1c::2f, comprobado el 11-11-2026).
# La clave viaja en LFTP_PASSWORD (--env-password): no queda en la linea de comandos.
set -euo pipefail

AQUI="$(cd "$(dirname "$0")" && pwd)"
SERVIDOR="${FTP_SERVIDOR:-vsur2.vtosur.cl}"
PUERTO="${FTP_PUERTO:-21}"
CA="${FTP_CA:-$AQUI/../certs/ftp-vtosur-ca.pem}"
ORIGEN="${DEPLOY_ORIGEN:-.}"
DESTINO="${DEPLOY_DESTINO:-/domains/gogodevs.cl/public_html/}"
SIMULAR="${DEPLOY_SIMULAR:-0}"
CENTINELA=".gogodevs-publicacion"   # fijo a proposito: no se puede cambiar por variable de entorno

if [ -z "${FTP_USERNAME:-}" ] || [ -z "${LFTP_PASSWORD:-}" ]; then
  echo "::error::faltan FTP_USERNAME o LFTP_PASSWORD"; exit 1
fi
if [ ! -f "$CA" ]; then
  echo "::error::no esta el archivo de CA $CA"; exit 1
fi
case "$DESTINO" in */) ;; *) DESTINO="$DESTINO/" ;; esac
tmp="$(mktemp -d)"
trap 'rm -rf "${tmp:?}"' EXIT

lftp_seguro() {  # lee comandos lftp por stdin y los corre con el transporte seguro
  { cat <<EOF
set cmd:fail-exit yes
set ftp:ssl-force yes
set ftp:ssl-protect-data yes
set ftp:ssl-protect-list yes
set ftp:ssl-use-ccc no
set ssl:verify-certificate yes
set ssl:check-hostname yes
set ssl:ca-file "$CA"
set ftp:passive-mode on
set net:max-retries 3
set net:timeout 30
EOF
    cat; echo "bye"; } | lftp --env-password -u "$FTP_USERNAME" -p "$PUERTO" "ftp://$SERVIDOR"
}

listar_destino() {  # listado de SOLO LECTURA: un nombre por linea, directorios con "/" al final
  printf 'cls -1aF "%s"\n' "$DESTINO" | lftp_seguro > "$tmp/listado.txt"
  awk '{ l = $0; sub(/\r$/, "", l); dir = (l ~ /\/$/); sub(/\/$/, "", l); n = split(l, p, "/"); nom = p[n];
         if (!dir) sub(/[*@=|]$/, "", nom); if (nom == "" || nom == "." || nom == "..") next;
         print (dir ? nom "/" : nom) }' "$tmp/listado.txt" > "$tmp/nombres.txt"
}

echo "FTPS explicito a $SERVIDOR:$PUERTO · TLS obligatorio · certificado verificado contra $(basename "$CA")"

# 1. Raiz real ANTES de tocar nada
if ! listar_destino; then
  echo "::error::no se pudo listar $DESTINO por FTPS (TLS, certificado, credenciales o ruta): no se toca nada"; exit 1
fi
echo "destino $DESTINO: $(wc -l < "$tmp/nombres.txt") entradas"
if ! grep -qx "$CENTINELA" "$tmp/nombres.txt"; then
  echo "::error::$DESTINO no tiene el centinela $CENTINELA: raiz equivocada o falta crearlo. NO se despliega"; exit 1
fi
if grep -qxE 'domains/|public_html/|\.bash_profile|\.bashrc|Maildir/|imap/' "$tmp/nombres.txt"; then
  echo "::error::$DESTINO parece el HOME de la cuenta (domains/, public_html/...), no la raiz publica. NO se despliega"; exit 1
fi

# 2. Mirror (el centinela nunca se toca)
# lftp prueba los directorios con "/" al final y su glob no cruza "/": --exclude-glob .git* NO excluia
# la carpeta .git/ (el deploy del 16-11-2026 subio .git/ y .github/ enteros). Van como regex con ^ y /.
SIM=""
if [ "$SIMULAR" = "1" ]; then SIM="--dry-run"; echo "SIMULACION: mirror --dry-run, no se escribe nada"; fi
lftp_seguro <<EOF
mirror -R --delete --only-newer $SIM --exclude ^\\.gogodevs-publicacion\$ --exclude ^\\.git/ --exclude ^\\.github/ --exclude ^\\.vscode/ --exclude-glob .git* --exclude-glob .vscode/ --exclude ^_blog/ --exclude ^_programados/ --exclude ^_tree/ --exclude ^docs/ --exclude ^README.md --exclude ^CAMBIOS_GOGODEVS.txt --exclude ^index-v2.html --exclude ^assets/css/style-v2.css --verbose "$ORIGEN" "$DESTINO"
EOF

# 3. Despues del mirror real, el centinela tiene que seguir
if [ "$SIMULAR" != "1" ]; then
  listar_destino
  if ! grep -qx "$CENTINELA" "$tmp/nombres.txt"; then
    echo "::error::el centinela desaparecio de $DESTINO despues del mirror: revisar el sitio YA"; exit 1
  fi
  echo "centinela presente despues del mirror"
fi
