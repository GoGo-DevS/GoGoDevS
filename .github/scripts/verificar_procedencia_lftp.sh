#!/usr/bin/env bash
# Verifica la PROCEDENCIA del .deb de lftp versionado en .github/vendor/ por la cadena de confianza de
# Ubuntu, no solo por un SHA-256 copiado de un indice (un indice sin firma no prueba nada):
#   1. InRelease de resolute, firmado por la clave del archivo de Ubuntu. Se verifica con gpgv contra
#      un llavero de confianza: el que trae la imagen del runner o, en local, el que se pase en KEYRING.
#   2. Del Release firmado sale el SHA-256 de main/binary-amd64/Packages.gz.
#   3. De Packages.gz sale el SHA-256 de lftp 4.9.3-1.1ubuntu2 (amd64).
#   4. Ese SHA-256 tiene que ser el del .deb versionado Y el que fija instalar_lftp.sh.
# Si cualquier eslabon falla (red, firma, hash), sale distinto de 0.
#   bash .github/scripts/verificar_procedencia_lftp.sh
#   KEYRING=/ruta/llavero.gpg bash .github/scripts/verificar_procedencia_lftp.sh
set -euo pipefail

AQUI="$(cd "$(dirname "$0")" && pwd)"
DEB="${LFTP_DEB:-$AQUI/../vendor/lftp_4.9.3-1.1ubuntu2_amd64.deb}"
VERSION="4.9.3-1.1ubuntu2"
BASE="${UBUNTU_ARCHIVO:-https://archive.ubuntu.com/ubuntu}"
SUITE="resolute"
# Ubuntu Archive Automatic Signing Key (2018) <ftpmaster@ubuntu.com>: la que firma resolute/InRelease
HUELLA="${HUELLA:-F6ECB3762474EDA9D21B7022871920D1991BC93C}"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

KEYRING="${KEYRING:-}"
if [ -z "$KEYRING" ]; then
  for k in /usr/share/keyrings/ubuntu-archive-keyring.gpg /usr/share/keyrings/ubuntu-archive-keyring.pgp; do
    if [ -f "$k" ]; then KEYRING="$k"; break; fi
  done
fi
if [ -z "$KEYRING" ] || [ ! -f "$KEYRING" ]; then
  echo "::error::no hay llavero de confianza de Ubuntu (KEYRING)"; exit 1
fi
echo "llavero de confianza: $KEYRING"
gpg --show-keys --with-colons "$KEYRING" 2>/dev/null | awk -F: '$1=="fpr"{print "  huella en el llavero: " $10}' || true

descargar() {
  if ! curl -fsS --retry 3 --retry-delay 5 -o "$2" "$1"; then
    echo "::error::no se pudo descargar $1 (red o DNS)"; exit 1
  fi
}

# 1. Firma de InRelease, con SOLO ese llavero; ademas se exige la huella exacta que firmo.
descargar "$BASE/dists/$SUITE/InRelease" "$tmp/InRelease"
if ! gpgv --status-fd 3 --keyring "$KEYRING" --output "$tmp/Release" "$tmp/InRelease" 3>"$tmp/estado" 2>"$tmp/gpgv.txt"; then
  cat "$tmp/gpgv.txt"
  echo "::error::la firma de InRelease NO verifica con el llavero de Ubuntu"; exit 1
fi
if ! grep -q "^\[GNUPG:\] VALIDSIG .*$HUELLA" "$tmp/estado"; then
  cat "$tmp/estado"
  echo "::error::InRelease no esta firmado por la clave esperada $HUELLA"; exit 1
fi
echo "1. InRelease de $SUITE firmado por $HUELLA: OK"

# 2. Packages.gz, por el hash que trae el Release firmado.
idx="main/binary-amd64/Packages.gz"
esperado_idx="$(awk -v f="$idx" '/^SHA256:/{s=1;next} /^[^ ]/{s=0} s && $3==f {print $1; exit}' "$tmp/Release")"
if [ -z "$esperado_idx" ]; then
  echo "::error::el Release firmado no lista $idx"; exit 1
fi
descargar "$BASE/dists/$SUITE/$idx" "$tmp/Packages.gz"
if [ "$(sha256sum "$tmp/Packages.gz" | cut -d' ' -f1)" != "$esperado_idx" ]; then
  echo "::error::$idx no coincide con el Release firmado"; exit 1
fi
echo "2. $idx coincide con el Release firmado: OK ($esperado_idx)"

# 3. La entrada de lftp en ese indice.
# Primero a archivo: con un pipe, el awk que termina antes mata a gunzip (SIGPIPE) y pipefail aborta.
gunzip -c "$tmp/Packages.gz" > "$tmp/Packages"
awk 'BEGIN{RS="";FS="\n"} $1=="Package: lftp"{print; exit}' "$tmp/Packages" > "$tmp/lftp.txt"
campo() { awk -v c="$1" 'index($0, c ": ")==1 {print substr($0, length(c) + 3); exit}' "$tmp/lftp.txt"; }
if [ "$(campo Version)" != "$VERSION" ] || [ "$(campo Architecture)" != "amd64" ]; then
  echo "::error::el indice firmado trae lftp '$(campo Version)' '$(campo Architecture)', no $VERSION amd64"; exit 1
fi
sha_idx="$(campo SHA256)"
echo "3. lftp $VERSION amd64 en el indice firmado: SHA-256 $sha_idx ($(campo Filename))"

# 4. El .deb versionado y el SHA-256 que fija el instalador son esos.
sha_deb="$(sha256sum "$DEB" | cut -d' ' -f1)"
sha_fijado="$(grep -oE 'LFTP_SHA256:-[0-9a-f]{64}' "$AQUI/instalar_lftp.sh" | cut -d- -f2)"
if [ "$sha_deb" != "$sha_idx" ]; then
  echo "::error::el .deb versionado NO es el del indice firmado (su SHA-256 es $sha_deb)"; exit 1
fi
if [ "$sha_fijado" != "$sha_idx" ]; then
  echo "::error::instalar_lftp.sh fija otro SHA-256 ($sha_fijado)"; exit 1
fi
echo "4. el .deb versionado y el SHA-256 de instalar_lftp.sh son los del indice firmado: OK"
echo "PROCEDENCIA VERIFICADA: lftp $VERSION amd64 viene del archivo de Ubuntu (firma $HUELLA)"
