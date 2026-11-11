#!/usr/bin/env bash
# Despliega gogodevs.cl por FTPS: TLS OBLIGATORIO y servidor VERIFICADO. Nunca cae a FTP en claro.
# Lo usan deploy.yml y blog-diario.yml (un solo lugar para la configuracion de transporte).
#
#   - ftp:ssl-force yes: si el servidor no acepta AUTH TLS, lftp aborta ANTES de mandar el usuario.
#   - ftp:ssl-protect-data/list yes: los archivos y los listados tambien van cifrados (PROT P).
#   - ssl:verify-certificate + ssl:check-hostname + ssl:ca-file: el certificado tiene que encadenar a
#     ISRG Root X1 por los intermedios de Let's Encrypt versionados y ser del nombre FTP_SERVIDOR.
#
# Por que vsur2.vtosur.cl y no ftp.gogodevs.cl: el certificado del servidor (VtoSur, DirectAdmin) es
# de vsur2.vtosur.cl; con ftp.gogodevs.cl la verificacion de nombre falla. Es el mismo servidor
# (138.186.10.116 / 2803:8240:310:1c::2f, comprobado el 11-11-2026).
# Por que un ca-file propio: el servidor manda SOLO su certificado final, sin intermedio.
# La clave viaja en LFTP_PASSWORD (--env-password): no queda en la linea de comandos.
set -euo pipefail

AQUI="$(cd "$(dirname "$0")" && pwd)"
SERVIDOR="${FTP_SERVIDOR:-vsur2.vtosur.cl}"
PUERTO="${FTP_PUERTO:-21}"
CA="${FTP_CA:-$AQUI/../certs/ftp-vtosur-ca.pem}"
ORIGEN="${DEPLOY_ORIGEN:-.}"
DESTINO="${DEPLOY_DESTINO:-/domains/gogodevs.cl/public_html/}"

if [ -z "${FTP_USERNAME:-}" ] || [ -z "${LFTP_PASSWORD:-}" ]; then
  echo "::error::faltan FTP_USERNAME o LFTP_PASSWORD"; exit 1
fi
if [ ! -f "$CA" ]; then
  echo "::error::no esta el archivo de CA $CA"; exit 1
fi
echo "FTPS explicito a $SERVIDOR:$PUERTO · TLS obligatorio · certificado verificado contra $(basename "$CA")"

lftp --env-password -u "$FTP_USERNAME" -p "$PUERTO" "ftp://$SERVIDOR" <<EOF
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
mirror -R --delete --only-newer --exclude-glob .git* --exclude-glob .vscode/ --exclude ^_blog/ --exclude ^_programados/ --exclude ^docs/ --exclude ^README.md --exclude ^CAMBIOS_GOGODEVS.txt --exclude ^index-v2.html --exclude ^assets/css/style-v2.css --verbose "$ORIGEN" "$DESTINO"
bye
EOF
