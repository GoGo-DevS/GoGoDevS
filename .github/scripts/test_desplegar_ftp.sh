#!/usr/bin/env bash
# Prueba desplegar_ftp.sh contra servidores FTP LOCALES (127.0.0.1): nunca toca el servidor real.
# Requiere lftp, openssl y python con pyftpdlib + pyopenssl (los instala el workflow de prueba).
#   1. TLS con certificado de una CA de prueba y nombre correcto: despliega, y respeta las exclusiones.
#   2. Nombre que no es el del certificado (127.0.0.1): FALLA y no sube nada.
#   3. CA equivocada: FALLA y no sube nada.
#   4. Servidor SIN TLS: FALLA, y el servidor no llega a recibir el USER (no hay caida a FTP en claro).
#   5. La clave no aparece en la salida del deploy ni en los logs de los servidores.
set -u
AQUI="$(cd "$(dirname "$0")" && pwd)"
PY="${PYTHON:-python3}"
tmp="$(mktemp -d)"
FALLAS=0
CLAVE="clave-de-prueba-$RANDOM-no-real"
pids=()
limpiar() { for p in "${pids[@]}"; do kill "$p" 2>/dev/null; done; rm -rf "$tmp"; }
trap limpiar EXIT
cd "$tmp"

# CA de prueba y certificado del servidor para "localhost"
openssl req -x509 -newkey rsa:2048 -nodes -keyout ca.key -out ca.pem -days 2 -subj "/CN=CA de prueba" 2>/dev/null
openssl req -newkey rsa:2048 -nodes -keyout srv.key -out srv.csr -subj "/CN=localhost" 2>/dev/null
printf 'subjectAltName=DNS:localhost\n' > ext.cnf
openssl x509 -req -in srv.csr -CA ca.pem -CAkey ca.key -CAcreateserial -out srv.pem -days 2 -extfile ext.cnf 2>/dev/null
openssl req -x509 -newkey rsa:2048 -nodes -keyout otra.key -out otra-ca.pem -days 2 -subj "/CN=Otra CA" 2>/dev/null

# Sitio de muestra: un archivo que se sube y uno excluido (_blog/ no se publica)
mkdir -p sitio/_blog; echo hola > sitio/index.html; echo borrador > sitio/_blog/no-subir.txt

mkdir -p raiz-tls raiz-plana
"$PY" "$AQUI/servidor_ftp_prueba.py" tls 2121 raiz-tls prueba "$CLAVE" log-tls.txt srv.pem srv.key & pids+=($!)
"$PY" "$AQUI/servidor_ftp_prueba.py" plano 2122 raiz-plana prueba "$CLAVE" log-plano.txt & pids+=($!)
sleep 3

desplegar() {  # $1 servidor · $2 puerto · $3 CA · $4 carpeta destino en el servidor de prueba
  FTP_SERVIDOR="$1" FTP_PUERTO="$2" FTP_CA="$3" DEPLOY_ORIGEN=sitio DEPLOY_DESTINO="$4" \
  FTP_USERNAME=prueba LFTP_PASSWORD="$CLAVE" timeout 60 bash "$AQUI/desplegar_ftp.sh" > "salida-$5.txt" 2>&1
}
resultado() {  # $1 nombre · $2 condicion (0 = ok)
  if [ "$2" = 0 ]; then echo "ok    $1"; else echo "FALLA $1"; FALLAS=$((FALLAS + 1)); fi
}

desplegar localhost 2121 ca.pem /ok ok; c=$?
[ "$c" = 0 ] && [ -f raiz-tls/ok/index.html ] && [ ! -e raiz-tls/ok/_blog ]; resultado "TLS verificado: despliega y respeta exclusiones (exit $c)" $?
[ "$c" = 0 ] || sed 's/^/      /' salida-ok.txt

desplegar 127.0.0.1 2121 ca.pem /nombre nombre; c=$?
[ "$c" != 0 ] && [ ! -e raiz-tls/nombre ]; resultado "nombre que no es del certificado: falla sin subir (exit $c)" $?

desplegar localhost 2121 otra-ca.pem /ca ca; c=$?
[ "$c" != 0 ] && [ ! -e raiz-tls/ca ]; resultado "CA equivocada: falla sin subir (exit $c)" $?

desplegar localhost 2122 ca.pem /plano plano; c=$?
# El log TIENE que mostrar el AUTH (si no, "no hay USER" pasaria aunque el log no registre nada).
[ "$c" != 0 ] && [ -z "$(ls -A raiz-plana)" ] && grep -q "AUTH" log-plano.txt && ! grep -q "USER prueba" log-plano.txt
resultado "servidor sin TLS: falla, el log muestra el AUTH y no recibe el USER (exit $c)" $?
[ "$c" != 0 ] || sed 's/^/      /' salida-plano.txt

! grep -rq -- "$CLAVE" salida-*.txt log-tls.txt log-plano.txt; resultado "la clave no aparece en salidas ni logs" $?

if [ "$FALLAS" -gt 0 ]; then echo "$FALLAS escenario(s) en rojo"; exit 1; fi
echo "desplegar_ftp.sh: 5 escenarios OK"
