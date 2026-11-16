#!/usr/bin/env bash
# Instala lftp para el deploy SIN depender de los mirrors de Ubuntu en cada corrida.
#
# Por que: el 11-11-2026 el deploy fallo 4 veces seguidas porque el runner de GitHub no resolvia
# archive.ubuntu.com ni security.ubuntu.com (github.com si resolvia): `apt-get install lftp` no
# podia bajar el paquete y el FTP ni se intentaba.
#
# Orden:
#   1. lftp ya instalado -> nada que hacer.
#   2. El .deb OFICIAL versionado en .github/vendor/, verificado por SHA-256 (sacado del indice de
#      Ubuntu resolute/main/binary-amd64, misma version que instalaba apt).
#   3. Si no sirve (otra version de Ubuntu, dependencias), apt-get con reintentos acotados y backoff.
#   4. Si nada funciona, FALLA (exit 1): el workflow no sigue ni informa exito sin publicar.
set -euo pipefail

DEB="${LFTP_DEB:-.github/vendor/lftp_4.9.3-1.1ubuntu2_amd64.deb}"
SHA256="${LFTP_SHA256:-994f0e52e7c223e21b7f8513cc16243bd6b6c0e36bba49dc003340b0c75a0593}"
INTENTOS="${APT_INTENTOS:-4}"
ESPERA="${APT_ESPERA_INICIAL:-15}"

if command -v lftp >/dev/null 2>&1; then
  echo "lftp ya estaba instalado: $(lftp --version | head -n 1)"
  exit 0
fi

if [ -f "$DEB" ] && echo "$SHA256  $DEB" | sha256sum -c --status; then
  if sudo dpkg -i "$DEB"; then
    echo "lftp instalado desde el .deb versionado: $(lftp --version | head -n 1)"
    exit 0
  fi
  echo "::warning::dpkg no pudo instalar el .deb versionado (dependencias o version de Ubuntu); se intenta con apt-get"
else
  echo "::warning::el .deb versionado no esta o su SHA-256 no coincide; se intenta con apt-get"
fi

for intento in $(seq 1 "$INTENTOS"); do
  if sudo apt-get update -o Acquire::Retries=2 && sudo apt-get install -y -o Acquire::Retries=2 lftp; then
    echo "lftp instalado con apt-get (intento $intento): $(lftp --version | head -n 1)"
    exit 0
  fi
  if [ "$intento" -lt "$INTENTOS" ]; then
    echo "::warning::apt-get fallo (intento $intento de $INTENTOS); reintento en ${ESPERA}s"
    sleep "$ESPERA"
    ESPERA=$((ESPERA * 2))
  fi
done

echo "::error::no se pudo instalar lftp (ni el .deb versionado ni apt-get tras $INTENTOS intentos): NO se despliega"
exit 1
