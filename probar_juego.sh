#!/usr/bin/env bash
# Prueba el juego sin pantalla: lint de Ren'Py (0 avisos) y recorridos automáticos (game/tests/).
# Uso: ./probar_juego.sh [testcase]     sin argumento corre todos (suite "global").
# Requiere el SDK en $RENPY_SDK (por defecto ~/renpy-8.5.3-sdk) y mutter (GNOME).
set -euo pipefail
SDK="${RENPY_SDK:-$HOME/renpy-8.5.3-sdk}"
JUEGO="$(cd "$(dirname "$0")" && pwd)"
PRUEBA="${1:-global}"
[[ "$PRUEBA" == global* ]] || PRUEBA="global::$PRUEBA"
REGISTRO="$JUEGO/.cache/pruebas"
mkdir -p "$REGISTRO" "$JUEGO/.cache/capturas"

echo "== Lint"
if ! "$SDK/renpy.sh" "$JUEGO" lint --error-code > "$REGISTRO/lint.txt" 2>&1; then
    cat "$REGISTRO/lint.txt"
    echo "Lint falló con código de error (detalle en $REGISTRO/lint.txt)"
    exit 1
fi
if grep -E "^game/.+:[0-9]+ " "$REGISTRO/lint.txt"; then
    echo "Lint con avisos (detalle en $REGISTRO/lint.txt)"
    exit 1
fi
echo "Lint sin avisos."

echo "== Recorrido: $PRUEBA"
PANTALLA="renpy-pruebas-$$"
mutter --headless --wayland --no-x11 --virtual-monitor 1920x1080 --wayland-display="$PANTALLA" \
    > "$REGISTRO/mutter.log" 2>&1 &
COMPOSITOR=$!
trap 'kill -9 $COMPOSITOR 2>/dev/null || true' EXIT
for _ in $(seq 50); do [ -S "$XDG_RUNTIME_DIR/$PANTALLA" ] && break; sleep 0.2; done

WAYLAND_DISPLAY="$PANTALLA" SDL_VIDEODRIVER=wayland SDL_AUDIODRIVER=disk SDL_DISKAUDIOFILE=/dev/null \
    timeout --kill-after=10 900 "$SDK/renpy.sh" "$JUEGO" test "$PRUEBA" --report-detailed \
    > "$REGISTRO/recorrido.txt" 2>&1 || true
kill -9 $COMPOSITOR 2>/dev/null || true
grep -E "^\[rpytest\] (Status|Test cases|Assertions)" "$REGISTRO/recorrido.txt" | sort -u || true
if ! grep -q "Status: PASSED" "$REGISTRO/recorrido.txt"; then
    grep -E "Error|assert|failed" "$REGISTRO/recorrido.txt" | head -20 || true
    echo "Recorrido con fallos (detalle en $REGISTRO/recorrido.txt)"
    exit 1
fi
