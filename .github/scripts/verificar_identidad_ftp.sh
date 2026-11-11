#!/usr/bin/env bash
# Verifica la IDENTIDAD del servidor FTP de gogodevs.cl SIN iniciar sesion (solo STARTTLS + certificado):
#   1. el servidor acepta AUTH TLS;
#   2. su certificado encadena a ISRG Root X1 usando SOLO .github/certs/ftp-vtosur-ca.pem;
#   3. el certificado es del nombre esperado (vsur2.vtosur.cl).
# Y al reves: con el nombre ftp.gogodevs.cl la verificacion TIENE que fallar (si no falla, la
# comprobacion no esta probando el nombre).
#   bash .github/scripts/verificar_identidad_ftp.sh
set -euo pipefail

AQUI="$(cd "$(dirname "$0")" && pwd)"
SERVIDOR="${FTP_SERVIDOR:-vsur2.vtosur.cl}"
CA="${FTP_CA:-$AQUI/../certs/ftp-vtosur-ca.pem}"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

openssl s_client -connect "$SERVIDOR:21" -starttls ftp -servername "$SERVIDOR" </dev/null >"$tmp/sc.txt" 2>"$tmp/err" || true
if ! openssl x509 -in "$tmp/sc.txt" -out "$tmp/final.pem" 2>/dev/null; then
  cat "$tmp/err"; echo "::error::el servidor no entrego certificado por AUTH TLS (red, DNS o sin TLS)"; exit 1
fi
echo "certificado: $(openssl x509 -in "$tmp/final.pem" -noout -subject -enddate | tr '\n' ' ')"

if ! openssl verify -x509_strict -CAfile "$CA" -verify_hostname "$SERVIDOR" "$tmp/final.pem"; then
  echo "::error::el certificado de $SERVIDOR NO verifica contra $(basename "$CA")"; exit 1
fi
if openssl verify -CAfile "$CA" -verify_hostname ftp.gogodevs.cl "$tmp/final.pem" >/dev/null 2>&1; then
  echo "::error::la verificacion acepto un nombre que no es del certificado: no esta probando el nombre"; exit 1
fi
echo "IDENTIDAD VERIFICADA: $SERVIDOR, cadena hasta ISRG Root X1; el nombre equivocado se rechaza"
