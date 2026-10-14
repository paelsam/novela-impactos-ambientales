#!/usr/bin/env bash
# Compila la versión web de Ren'Py y la publica en Vercel.
# Uso: ./desplegar.sh                vista previa (URL temporal)
#      ./desplegar.sh --prod         producción
#      ./desplegar.sh --solo-compilar   solo genera .cache/web (para probar con http.server)
# La primera vez, Vercel pregunta por la cuenta y el nombre del proyecto (se guarda en .cache/vercel).
set -euo pipefail
SDK="${RENPY_SDK:-$HOME/renpy-8.5.3-sdk}"
JUEGO="$(cd "$(dirname "$0")" && pwd)"
SALIDA="$JUEGO/.cache/web"
ENLACE="$JUEGO/.cache/vercel"

[ -d "$SDK/web" ] || { echo "Falta el módulo web del SDK: descomprime renpy-8.5.3-web.zip dentro de $SDK"; exit 1; }

echo "== Compilar versión web"
"$SDK/renpy.sh" "$SDK/launcher" web_build "$JUEGO" --destination "$SALIDA" > /dev/null
[ -f "$SALIDA/index.html" ] || { echo "La compilación no generó index.html"; exit 1; }
cp "$JUEGO/vercel.json" "$SALIDA/vercel.json"
echo "Listo: $SALIDA ($(du -sh "$SALIDA" | cut -f1))"
[ "${1:-}" = "--solo-compilar" ] && exit 0

echo "== Publicar en Vercel"
[ -d "$ENLACE" ] && cp -r "$ENLACE" "$SALIDA/.vercel"
(cd "$SALIDA" && npx --yes vercel@latest deploy "$@")
[ -d "$SALIDA/.vercel" ] && { mkdir -p "$ENLACE"; cp -r "$SALIDA/.vercel/." "$ENLACE/"; }
