<?php
/**
 * API de "Equipos Futbolitos" (https://www.gogodevs.cl/pichanga/).
 *
 * Cada jugador abre el link, pone su nombre y manda su versión de los equipos
 * (Negro y Blanco). La página cuenta cuál versión se repite más.
 *
 * Los datos viven FUERA de public_html (domains/gogodevs.cl/pichanga-data/):
 * el deploy hace `mirror --delete` sobre public_html y borraría cualquier
 * archivo que no esté en el repo.
 *
 * GET               -> partido actual + versiones enviadas (sin tokens).
 * POST {accion}     -> votar | nuevoPartido | borrarVoto | esAdmin
 *
 * El organizador se identifica con una clave. La primera clave que abre un
 * partido queda como clave del organizador (se guarda solo su hash).
 */
declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store, max-age=0');
header('X-Robots-Tag: noindex, nofollow');
header('X-Content-Type-Options: nosniff');

const MAX_JUGADORES = 40;
const MAX_VOTOS = 80;
const MAX_NOMBRE = 30;
const MAX_TITULO = 80;
const MAX_CUERPO = 65536;
const PARTIDOS_GUARDADOS = 10;

function responder(array $data, int $codigo = 200): void
{
    http_response_code($codigo);
    echo json_encode($data, JSON_UNESCAPED_UNICODE);
    exit;
}

function fallar(string $mensaje, int $codigo = 400): void
{
    responder(['ok' => false, 'error' => $mensaje], $codigo);
}

/** Igual que norm() del navegador: sin tildes, sin mayúsculas, sin el guante. */
function norm(string $s): string
{
    $s = preg_replace('/\(.*?\)/u', '', $s) ?? '';
    $s = str_replace('🧤', '', $s);
    $s = mb_strtolower($s, 'UTF-8');
    $s = strtr($s, [
        'á' => 'a', 'à' => 'a', 'ä' => 'a', 'â' => 'a',
        'é' => 'e', 'è' => 'e', 'ë' => 'e', 'ê' => 'e',
        'í' => 'i', 'ì' => 'i', 'ï' => 'i', 'î' => 'i',
        'ó' => 'o', 'ò' => 'o', 'ö' => 'o', 'ô' => 'o',
        'ú' => 'u', 'ù' => 'u', 'ü' => 'u', 'û' => 'u',
        'ñ' => 'n', 'ç' => 'c',
    ]);
    $s = preg_replace('/[*_~]/u', '', $s) ?? '';
    $s = preg_replace('/\s+/u', ' ', $s) ?? '';
    return trim($s);
}

function limpiarTexto($s, int $max): string
{
    if (!is_string($s)) {
        return '';
    }
    $s = preg_replace('/[\x00-\x1F\x7F<>]/u', ' ', $s) ?? '';
    $s = trim(preg_replace('/\s+/u', ' ', $s) ?? '');
    return mb_substr($s, 0, $max, 'UTF-8');
}

function limpiarNombre($s): string
{
    if (!is_string($s)) {
        return '';
    }
    $s = str_replace('🧤', '', $s);
    $s = preg_replace('/[,;]/u', ' ', $s) ?? '';
    return limpiarTexto($s, MAX_NOMBRE);
}

function dirDatos(): string
{
    $dir = dirname(__DIR__, 2) . '/pichanga-data';
    if (!is_dir($dir)) {
        @mkdir($dir, 0700, true);
    }
    if (!is_dir($dir) || !is_writable($dir)) {
        fallar('El servidor no tiene dónde guardar las versiones.', 500);
    }
    return $dir;
}

function estadoVacio(): array
{
    return ['partido' => null, 'votos' => [], 'admin' => null, 'anteriores' => []];
}

/**
 * Abre el estado con candado, se lo pasa a $fn y, si $escribir y $fn no
 * devolvió error, guarda lo que $fn cambió.
 */
function conEstado(callable $fn, bool $escribir): array
{
    $ruta = dirDatos() . '/estado.json';
    $fh = @fopen($ruta, 'c+');
    if ($fh === false) {
        fallar('No se pudieron abrir los datos.', 500);
    }
    flock($fh, $escribir ? LOCK_EX : LOCK_SH);
    $crudo = stream_get_contents($fh);
    $estado = $crudo ? json_decode($crudo, true) : null;
    if (!is_array($estado)) {
        $estado = estadoVacio();
    }
    $estado += estadoVacio();
    if (!is_array($estado['votos'])) {
        $estado['votos'] = [];
    }

    $r = $fn($estado);

    if ($escribir && !isset($r['err'])) {
        $json = json_encode($estado, JSON_UNESCAPED_UNICODE);
        if ($json === false) {
            flock($fh, LOCK_UN);
            fclose($fh);
            fallar('No se pudieron guardar los datos.', 500);
        }
        ftruncate($fh, 0);
        rewind($fh);
        fwrite($fh, $json);
        fflush($fh);
    }
    flock($fh, LOCK_UN);
    fclose($fh);
    return $r;
}

function vistaPublica(array $e): array
{
    $votos = [];
    foreach ($e['votos'] as $v) {
        $votos[] = [
            'nombre' => $v['nombre'],
            'negro' => $v['negro'],
            'blanco' => $v['blanco'],
            'ts' => $v['ts'],
        ];
    }
    usort($votos, function ($a, $b) {
        return $a['ts'] <=> $b['ts'];
    });
    return [
        'ok' => true,
        'partido' => $e['partido'],
        'votos' => $votos,
        'hayAdmin' => !empty($e['admin']),
    ];
}

function claveValida($clave): bool
{
    return is_string($clave) && strlen($clave) >= 12 && strlen($clave) <= 128;
}

function esOrganizador(array $e, $clave): bool
{
    return claveValida($clave) && !empty($e['admin']) && hash_equals($e['admin'], hash('sha256', $clave));
}

function rechazo(int $codigo, string $mensaje): array
{
    return ['err' => [$codigo, $mensaje]];
}

// ---------------------------------------------------------------------------

$metodo = $_SERVER['REQUEST_METHOD'] ?? 'GET';

if ($metodo === 'GET') {
    responder(conEstado(function (array &$e) {
        return vistaPublica($e);
    }, false));
}
if ($metodo !== 'POST') {
    fallar('Método no permitido.', 405);
}

$crudo = file_get_contents('php://input', false, null, 0, MAX_CUERPO + 1);
if ($crudo === false || strlen($crudo) > MAX_CUERPO) {
    fallar('El mensaje es demasiado grande.', 413);
}
$in = json_decode($crudo, true);
if (!is_array($in)) {
    fallar('Mensaje inválido.');
}
$accion = is_string($in['accion'] ?? null) ? $in['accion'] : '';

switch ($accion) {
    case 'votar':
        $r = conEstado(function (array &$e) use ($in) {
            $p = $e['partido'];
            if (!$p) {
                return rechazo(409, 'Todavía no hay partido abierto.');
            }
            if (($in['partidoId'] ?? '') !== $p['id']) {
                return rechazo(409, 'El partido cambió. Recarga la página.');
            }
            $nombre = limpiarNombre($in['nombre'] ?? '');
            if (norm($nombre) === '') {
                return rechazo(400, 'Falta tu nombre.');
            }
            $token = $in['token'] ?? '';
            if (!is_string($token) || !preg_match('/^[A-Za-z0-9]{16,64}$/', $token)) {
                return rechazo(400, 'Recarga la página e inténtalo de nuevo.');
            }

            $roster = [];
            foreach ($p['jugadores'] as $j) {
                $roster[norm($j['nombre'])] = $j;
            }
            $lados = ['negro' => [], 'blanco' => []];
            $vistos = [];
            foreach (['negro', 'blanco'] as $lado) {
                $lista = $in[$lado] ?? null;
                if (!is_array($lista)) {
                    return rechazo(400, 'Faltan los equipos.');
                }
                foreach ($lista as $n) {
                    if (!is_string($n)) {
                        return rechazo(400, 'Hay un nombre inválido.');
                    }
                    $k = norm($n);
                    $corto = mb_substr(limpiarNombre($n), 0, MAX_NOMBRE, 'UTF-8');
                    if (!isset($roster[$k])) {
                        return rechazo(400, $corto . ' no está en la lista de este partido. Recarga la página.');
                    }
                    if (isset($vistos[$k])) {
                        return rechazo(400, $corto . ' aparece dos veces.');
                    }
                    $vistos[$k] = true;
                    $lados[$lado][] = $roster[$k]['nombre'];
                }
            }
            if (count($vistos) !== count($roster)) {
                return rechazo(400, 'Faltan jugadores por ubicar.');
            }
            if (abs(count($lados['negro']) - count($lados['blanco'])) > 1) {
                return rechazo(400, 'Los equipos tienen que quedar parejos.');
            }
            $arqueros = function (array $nombres) use ($roster) {
                $c = 0;
                foreach ($nombres as $n) {
                    if (!empty($roster[norm($n)]['arquero'])) {
                        $c++;
                    }
                }
                return $c;
            };
            if (abs($arqueros($lados['negro']) - $arqueros($lados['blanco'])) > 1) {
                return rechazo(400, 'Los arqueros tienen que quedar uno en cada equipo.');
            }

            $clave = norm($nombre);
            $hash = hash('sha256', $token);
            $previo = $e['votos'][$clave] ?? null;
            if ($previo) {
                if (!hash_equals($previo['tok'], $hash)) {
                    return rechazo(409, 'Ya hay una versión a nombre de ' . $previo['nombre']
                        . ' enviada desde otro teléfono. Si eras tú, pídele al organizador que la borre.');
                }
            } elseif (count($e['votos']) >= MAX_VOTOS) {
                return rechazo(409, 'Se llegó al máximo de versiones para este partido.');
            }
            $e['votos'][$clave] = [
                'nombre' => $nombre,
                'negro' => $lados['negro'],
                'blanco' => $lados['blanco'],
                'ts' => $previo ? $previo['ts'] : time(),
                'editado' => time(),
                'tok' => $hash,
            ];
            return vistaPublica($e);
        }, true);
        break;

    case 'nuevoPartido':
        $r = conEstado(function (array &$e) use ($in) {
            $clave = $in['clave'] ?? '';
            if (!claveValida($clave)) {
                return rechazo(403, 'Clave inválida.');
            }
            $primeraVez = empty($e['admin']);
            if (!$primeraVez && !esOrganizador($e, $clave)) {
                return rechazo(403, 'Clave incorrecta.');
            }
            $jugadores = [];
            $vistos = [];
            foreach ((is_array($in['jugadores'] ?? null) ? $in['jugadores'] : []) as $j) {
                if (!is_array($j)) {
                    continue;
                }
                $n = limpiarNombre($j['nombre'] ?? '');
                $k = norm($n);
                if ($k === '' || isset($vistos[$k])) {
                    continue;
                }
                $vistos[$k] = true;
                $jugadores[] = ['nombre' => $n, 'arquero' => !empty($j['arquero'])];
            }
            if (count($jugadores) < 2) {
                return rechazo(400, 'La lista necesita al menos 2 jugadores.');
            }
            if (count($jugadores) > MAX_JUGADORES) {
                return rechazo(400, 'La lista tiene demasiados jugadores.');
            }
            $total = $in['total'] ?? null;
            $total = (is_int($total) && $total > 0 && $total < 100000000) ? $total : null;

            if ($primeraVez) {
                $e['admin'] = hash('sha256', $clave);
            }
            if ($e['partido']) {
                array_unshift($e['anteriores'], ['partido' => $e['partido'], 'votos' => $e['votos']]);
                $e['anteriores'] = array_slice($e['anteriores'], 0, PARTIDOS_GUARDADOS);
            }
            $e['partido'] = [
                'id' => bin2hex(random_bytes(6)),
                'titulo' => limpiarTexto($in['titulo'] ?? '', MAX_TITULO),
                'total' => $total,
                'jugadores' => $jugadores,
                'creado' => time(),
            ];
            $e['votos'] = [];
            return vistaPublica($e);
        }, true);
        break;

    case 'borrarVoto':
        $r = conEstado(function (array &$e) use ($in) {
            if (!esOrganizador($e, $in['clave'] ?? '')) {
                return rechazo(403, 'Solo el organizador puede borrar versiones.');
            }
            $k = norm(is_string($in['nombre'] ?? null) ? $in['nombre'] : '');
            if ($k === '' || !isset($e['votos'][$k])) {
                return rechazo(404, 'Esa versión ya no está.');
            }
            unset($e['votos'][$k]);
            return vistaPublica($e);
        }, true);
        break;

    case 'esAdmin':
        $r = conEstado(function (array &$e) use ($in) {
            $v = vistaPublica($e);
            $v['admin'] = esOrganizador($e, $in['clave'] ?? '');
            $v['libre'] = empty($e['admin']);
            return $v;
        }, false);
        break;

    default:
        fallar('Acción desconocida.');
}

if (isset($r['err'])) {
    fallar($r['err'][1], $r['err'][0]);
}
responder($r);
