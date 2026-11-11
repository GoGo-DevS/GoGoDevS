#!/usr/bin/env bash
# Prueba desplegar_ftp.sh contra servidores FTP LOCALES (127.0.0.1): nunca toca el servidor real ni usa
# credenciales reales (usuario "prueba" y una clave aleatoria generada aqui).
# Requiere lftp y python con pyftpdlib + pyopenssl + cryptography (los instala el workflow de prueba).
#
#  Transporte
#   1. TLS valido: despliega; el log del servidor muestra AUTH TLS (control cifrado) y PROT P (datos
#      cifrados; el servidor ademas RECHAZA datos sin PROT P, asi que si subio, subio cifrado).
#   2-4. Nombre equivocado, CA equivocada, certificado vencido: falla POR EL CERTIFICADO, sin tocar nada.
#   5. Servidor SIN TLS: falla, el AUTH queda rechazado y el servidor NO recibe el USER.
#  Raiz (mirror --delete solo con la raiz comprobada)
#   6. Despues del deploy real: lo viejo se borra, lo nuevo esta, _blog/ no se sube y el CENTINELA SIGUE.
#   7. Destino sin centinela: falla y no toca nada.
#   8. Destino que parece el home de la cuenta (domains/): falla y no toca nada.
#   9. Simulacion (DEPLOY_SIMULAR=1): sale 0 y no escribe nada.
#  Credenciales
#  10. La clave no aparece en la salida del deploy ni en los logs de los servidores.
set -u
AQUI="$(cd "$(dirname "$0")" && pwd)"
PY="${PYTHON:-python3}"
tmp="$(mktemp -d)"
FALLAS=0
CLAVE="clave-de-prueba-$RANDOM$RANDOM-no-real"
CENT=".gogodevs-publicacion"
pids=()
limpiar() { for p in "${pids[@]}"; do kill "$p" 2>/dev/null; done; rm -rf "${tmp:?}"; }
trap limpiar EXIT
cd "$tmp" || exit 1

"$PY" "$AQUI/certs_prueba.py" . || { echo "FALLA no se pudieron generar los certificados de prueba"; exit 1; }

# Sitio de muestra: un archivo que se sube y uno excluido (_blog/ no se publica)
mkdir -p sitio/_blog; echo hola > sitio/index.html; echo borrador > sitio/_blog/no-subir.txt

# Destinos en el servidor TLS de prueba
preparar() {  # $1 carpeta · $2 con centinela (si|no) · $3 con domains/ (si|no)
  mkdir -p "raiz-tls/$1"; echo viejo > "raiz-tls/$1/viejo.html"
  [ "$2" = si ] && echo "raiz publica" > "raiz-tls/$1/$CENT"
  [ "$3" = si ] && mkdir -p "raiz-tls/$1/domains"
  return 0
}
preparar ok si no; preparar sim si no; preparar sinc no no; preparar home si si
mkdir -p raiz-plana raiz-vencido

"$PY" "$AQUI/servidor_ftp_prueba.py" tls 2121 raiz-tls prueba "$CLAVE" log-tls.txt srv.pem srv.key & pids+=($!)
"$PY" "$AQUI/servidor_ftp_prueba.py" plano 2122 raiz-plana prueba "$CLAVE" log-plano.txt & pids+=($!)
"$PY" "$AQUI/servidor_ftp_prueba.py" tls 2123 raiz-vencido prueba "$CLAVE" log-vencido.txt vencido.pem vencido.key & pids+=($!)
sleep 3

desplegar() {  # $1 servidor · $2 puerto · $3 CA · $4 destino · $5 nombre de la salida · [$6 simular]
  FTP_SERVIDOR="$1" FTP_PUERTO="$2" FTP_CA="$3" DEPLOY_ORIGEN=sitio DEPLOY_DESTINO="$4" DEPLOY_SIMULAR="${6:-0}" \
  FTP_USERNAME=prueba LFTP_PASSWORD="$CLAVE" timeout 120 bash "$AQUI/desplegar_ftp.sh" > "salida-$5.txt" 2>&1
}
resultado() {  # $1 nombre · $2 condicion (0 = ok) · $3 salida a mostrar si falla
  if [ "$2" = 0 ]; then echo "ok    $1"; else echo "FALLA $1"; FALLAS=$((FALLAS + 1)); [ -n "${3:-}" ] && sed 's/^/      /' "$3"; fi
}
intacto() {  # $1 carpeta: sigue el viejo, no llego nada nuevo
  [ -f "raiz-tls/$1/viejo.html" ] && [ ! -e "raiz-tls/$1/index.html" ]
}
# El motivo tiene que venir de lftp ("Certificate ..."), no de nuestro propio mensaje ni de un timeout.
motivo_cert() { grep -qi "certificate" "$1" && ! grep -qiE "timed out|timeout" "$1"; }

# 1 + 6. Deploy real con TLS valido y raiz comprobada
desplegar localhost 2121 ca.pem /ok ok; c=$?
[ "$c" = 0 ] && grep -q "<- AUTH TLS" log-tls.txt && grep -q "<- PROT P" log-tls.txt
resultado "TLS verificado: control (AUTH TLS) y datos (PROT P) cifrados (exit $c)" $? salida-ok.txt
[ -f raiz-tls/ok/index.html ] && [ ! -e raiz-tls/ok/viejo.html ] && [ ! -e raiz-tls/ok/_blog ] && [ -f "raiz-tls/ok/$CENT" ]
resultado "despues del deploy: nuevo arriba, viejo borrado, _blog/ excluido y el CENTINELA sigue" $? salida-ok.txt

# 2-4. Certificados invalidos: falla por el certificado y no toca nada
preparar nombre si no; preparar ca si no
desplegar 127.0.0.1 2121 ca.pem /nombre nombre; c=$?
[ "$c" != 0 ] && intacto nombre && motivo_cert salida-nombre.txt
resultado "nombre que no es del certificado: falla por el certificado, sin tocar nada (exit $c)" $? salida-nombre.txt
desplegar localhost 2121 otra-ca.pem /ca ca; c=$?
[ "$c" != 0 ] && intacto ca && motivo_cert salida-ca.txt
resultado "CA equivocada: falla por el certificado, sin tocar nada (exit $c)" $? salida-ca.txt
desplegar localhost 2123 ca.pem /vencido vencido; c=$?
[ "$c" != 0 ] && [ -z "$(ls -A raiz-vencido)" ] && motivo_cert salida-vencido.txt
resultado "certificado vencido: falla por el certificado, sin tocar nada (exit $c)" $? salida-vencido.txt

# 5. Sin TLS: el log TIENE que mostrar el AUTH (si no, "no hay USER" pasaria aunque el log no registre nada)
desplegar localhost 2122 ca.pem /plano plano; c=$?
[ "$c" != 0 ] && [ -z "$(ls -A raiz-plana)" ] && grep -q "<- AUTH TLS" log-plano.txt && ! grep -q "<- USER" log-plano.txt \
  && grep -qi "ssl" salida-plano.txt
resultado "servidor sin TLS: falla, el AUTH queda rechazado y no recibe el USER (exit $c)" $? salida-plano.txt

# 7-8. Raiz equivocada: no se borra nada
desplegar localhost 2121 ca.pem /sinc sinc; c=$?
[ "$c" != 0 ] && intacto sinc && grep -q "centinela" salida-sinc.txt
resultado "destino sin centinela: falla y no toca nada (exit $c)" $? salida-sinc.txt
desplegar localhost 2121 ca.pem /home home; c=$?
[ "$c" != 0 ] && intacto home && [ -d raiz-tls/home/domains ] && grep -q "HOME" salida-home.txt
resultado "destino que parece el home (domains/): falla y no toca nada (exit $c)" $? salida-home.txt

# 9. Simulacion: sale 0 y no escribe nada
desplegar localhost 2121 ca.pem /sim sim 1; c=$?
[ "$c" = 0 ] && intacto sim && [ -f "raiz-tls/sim/$CENT" ] && grep -q "SIMULACION" salida-sim.txt
resultado "simulacion (mirror --dry-run): sale 0 y no escribe nada (exit $c)" $? salida-sim.txt

# 10. Credenciales
! grep -rq -- "$CLAVE" salida-*.txt log-tls.txt log-plano.txt log-vencido.txt
resultado "la clave no aparece en salidas ni logs" $?

if [ "$FALLAS" -gt 0 ]; then echo "$FALLAS escenario(s) en rojo"; exit 1; fi
echo "desplegar_ftp.sh: 10 escenarios OK"
