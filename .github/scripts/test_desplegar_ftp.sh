#!/usr/bin/env bash
# Prueba desplegar_ftp.sh contra servidores FTP LOCALES (127.0.0.1): nunca toca el servidor real ni usa
# credenciales reales (usuario "prueba" y una clave aleatoria generada aqui).
# Requiere lftp y python con pyftpdlib + pyopenssl (los instala el workflow de prueba).
#   1. TLS con certificado de una CA de prueba y nombre correcto: despliega y respeta las exclusiones;
#      el log del servidor muestra AUTH TLS (control cifrado) y PROT P (datos cifrados; el servidor
#      ademas RECHAZA datos sin PROT P, asi que si subio, subio cifrado).
#   2. Nombre que no es el del certificado (127.0.0.1): FALLA y no sube nada.
#   3. CA equivocada: FALLA y no sube nada.
#   4. Certificado vencido: FALLA y no sube nada.
#   5. Servidor SIN TLS: FALLA, el log muestra el AUTH rechazado y el servidor NO recibe el USER.
#   6. La clave no aparece en la salida del deploy ni en los logs de los servidores.
set -u
AQUI="$(cd "$(dirname "$0")" && pwd)"
PY="${PYTHON:-python3}"
tmp="$(mktemp -d)"
FALLAS=0
CLAVE="clave-de-prueba-$RANDOM$RANDOM-no-real"
pids=()
limpiar() { for p in "${pids[@]}"; do kill "$p" 2>/dev/null; done; rm -rf "${tmp:?}"; }
trap limpiar EXIT
cd "$tmp" || exit 1

"$PY" "$AQUI/certs_prueba.py" . || { echo "FALLA no se pudieron generar los certificados de prueba"; exit 1; }

# Sitio de muestra: un archivo que se sube y uno excluido (_blog/ no se publica)
mkdir -p sitio/_blog; echo hola > sitio/index.html; echo borrador > sitio/_blog/no-subir.txt
mkdir -p raiz-tls raiz-plana raiz-vencido
"$PY" "$AQUI/servidor_ftp_prueba.py" tls 2121 raiz-tls prueba "$CLAVE" log-tls.txt srv.pem srv.key & pids+=($!)
"$PY" "$AQUI/servidor_ftp_prueba.py" plano 2122 raiz-plana prueba "$CLAVE" log-plano.txt & pids+=($!)
"$PY" "$AQUI/servidor_ftp_prueba.py" tls 2123 raiz-vencido prueba "$CLAVE" log-vencido.txt vencido.pem vencido.key & pids+=($!)
sleep 3

desplegar() {  # $1 servidor · $2 puerto · $3 CA · $4 destino en el servidor de prueba · $5 nombre de la salida
  FTP_SERVIDOR="$1" FTP_PUERTO="$2" FTP_CA="$3" DEPLOY_ORIGEN=sitio DEPLOY_DESTINO="$4" \
  FTP_USERNAME=prueba LFTP_PASSWORD="$CLAVE" timeout 90 bash "$AQUI/desplegar_ftp.sh" > "salida-$5.txt" 2>&1
}
resultado() {  # $1 nombre · $2 condicion (0 = ok) · $3 salida a mostrar si falla
  if [ "$2" = 0 ]; then echo "ok    $1"; else echo "FALLA $1"; FALLAS=$((FALLAS + 1)); [ -n "${3:-}" ] && sed 's/^/      /' "$3"; fi
}

desplegar localhost 2121 ca.pem /ok ok; c=$?
[ "$c" = 0 ] && [ -f raiz-tls/ok/index.html ] && [ ! -e raiz-tls/ok/_blog ] \
  && grep -q "<- AUTH TLS" log-tls.txt && grep -q "<- PROT P" log-tls.txt
resultado "TLS verificado: despliega, respeta exclusiones, control (AUTH TLS) y datos (PROT P) cifrados (exit $c)" $? salida-ok.txt

# Un fallo por timeout u otra cosa NO cuenta como "fallo seguro": el motivo tiene que ser el certificado.
motivo_cert() { grep -qiE "certificate|certificado|verif" "$1" && ! grep -qiE "timed out|timeout" "$1"; }

desplegar 127.0.0.1 2121 ca.pem /nombre nombre; c=$?
[ "$c" != 0 ] && [ ! -e raiz-tls/nombre ] && motivo_cert salida-nombre.txt
resultado "nombre que no es del certificado: falla por el certificado, sin subir (exit $c)" $? salida-nombre.txt

desplegar localhost 2121 otra-ca.pem /ca ca; c=$?
[ "$c" != 0 ] && [ ! -e raiz-tls/ca ] && motivo_cert salida-ca.txt
resultado "CA equivocada: falla por el certificado, sin subir (exit $c)" $? salida-ca.txt

desplegar localhost 2123 ca.pem /vencido vencido; c=$?
[ "$c" != 0 ] && [ -z "$(ls -A raiz-vencido)" ] && motivo_cert salida-vencido.txt
resultado "certificado vencido: falla por el certificado, sin subir (exit $c)" $? salida-vencido.txt

# El log TIENE que mostrar el AUTH (si no, "no hay USER" pasaria aunque el log no registre nada).
desplegar localhost 2122 ca.pem /plano plano; c=$?
[ "$c" != 0 ] && [ -z "$(ls -A raiz-plana)" ] && grep -q "<- AUTH TLS" log-plano.txt && ! grep -q "<- USER" log-plano.txt \
  && grep -qiE "ssl" salida-plano.txt
resultado "servidor sin TLS: falla, el AUTH queda rechazado y no recibe el USER (exit $c)" $? salida-plano.txt

! grep -rq -- "$CLAVE" salida-*.txt log-tls.txt log-plano.txt log-vencido.txt
resultado "la clave no aparece en salidas ni logs" $?

if [ "$FALLAS" -gt 0 ]; then echo "$FALLAS escenario(s) en rojo"; exit 1; fi
echo "desplegar_ftp.sh: 6 escenarios OK"
