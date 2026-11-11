#!/usr/bin/env bash
# Pruebas de instalar_lftp.sh con comandos FALSOS (sudo, dpkg, apt-get, lftp): no instala nada.
#   bash .github/scripts/test_instalar_lftp.sh
set -u
AQUI="$(cd "$(dirname "$0")" && pwd)"
SCRIPT="$AQUI/instalar_lftp.sh"
FALLAS=0

escenario() {
  # $1 nombre · $2 deb (ok|malo|ninguno) · $3 dpkg (ok|falla) · $4 fallas de apt antes de funcionar · $5 lftp previo (si|no)
  # $6 exit esperado · $7 texto esperado · $8 llamadas a dpkg · $9 llamadas a apt-get install
  local nombre="$1" deb="$2" dpkg="$3" apt_fallas="$4" previo="$5" exit_esp="$6" texto="$7" dpkg_esp="$8" apt_esp="$9"
  local tmp; tmp="$(mktemp -d)"
  mkdir -p "$tmp/bin" "$tmp/estado"
  local instalar_lftp="printf '#!/usr/bin/env bash\\necho \"LFTP | Version 4.9.3\"\\n' > \"$tmp/bin/lftp\"; chmod +x \"$tmp/bin/lftp\""
  printf '#!/usr/bin/env bash\nexec "$@"\n' > "$tmp/bin/sudo"
  cat > "$tmp/bin/dpkg" <<EOF
#!/usr/bin/env bash
echo dpkg >> "$tmp/estado/llamadas"
if [ "$dpkg" = ok ]; then $instalar_lftp; exit 0; fi
exit 1
EOF
  cat > "$tmp/bin/apt-get" <<EOF
#!/usr/bin/env bash
[ "\$1" = update ] && exit 0
echo apt-install >> "$tmp/estado/llamadas"
n=\$(grep -c apt-install "$tmp/estado/llamadas")
if [ "\$n" -le "$apt_fallas" ]; then exit 100; fi
$instalar_lftp
exit 0
EOF
  chmod +x "$tmp/bin/sudo" "$tmp/bin/dpkg" "$tmp/bin/apt-get"
  [ "$previo" = si ] && eval "$instalar_lftp"
  printf 'contenido-del-deb' > "$tmp/lftp.deb"
  local sha; sha="$(sha256sum "$tmp/lftp.deb" | cut -d' ' -f1)"
  case "$deb" in
    malo) sha="0000000000000000000000000000000000000000000000000000000000000000" ;;
    ninguno) rm -f "$tmp/lftp.deb" ;;
  esac
  local salida codigo
  salida="$(PATH="$tmp/bin:$PATH" LFTP_DEB="$tmp/lftp.deb" LFTP_SHA256="$sha" APT_INTENTOS=3 APT_ESPERA_INICIAL=0 \
            bash "$SCRIPT" 2>&1)"
  codigo=$?
  local n_dpkg n_apt
  n_dpkg=$(grep -c '^dpkg$' "$tmp/estado/llamadas" 2>/dev/null); n_dpkg=${n_dpkg:-0}
  n_apt=$(grep -c '^apt-install$' "$tmp/estado/llamadas" 2>/dev/null); n_apt=${n_apt:-0}
  if [ "$codigo" = "$exit_esp" ] && printf '%s' "$salida" | grep -q -- "$texto" && [ "$n_dpkg" = "$dpkg_esp" ] && [ "$n_apt" = "$apt_esp" ]; then
    echo "ok    $nombre"
  else
    echo "FALLA $nombre (exit $codigo, dpkg $n_dpkg, apt $n_apt)"; printf '%s\n' "$salida" | sed 's/^/      /'
    FALLAS=$((FALLAS + 1))
  fi
  rm -rf "$tmp"
}

#         nombre                                         deb      dpkg   apt  previo exit texto                         dpkg apt
escenario "deb versionado verificado: no usa apt"        ok       ok     0    no     0    "desde el .deb versionado"    1    0
escenario "SHA-256 no coincide: apt con reintentos"      malo     ok     2    no     0    "intento 3"                   0    3
escenario "sin deb: apt al primer intento"               ninguno  ok     0    no     0    "apt-get (intento 1)"         0    1
escenario "dpkg falla y apt nunca: FALLA el deploy"      ok       falla  99   no     1    "::error::"                   1    3
escenario "lftp ya instalado: no toca nada"              ok       ok     0    si     0    "ya estaba instalado"         0    0

if [ "$FALLAS" -gt 0 ]; then echo "$FALLAS escenario(s) en rojo"; exit 1; fi
echo "instalar_lftp.sh: 5 escenarios OK"
