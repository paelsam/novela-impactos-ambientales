# La fragilidad ambiental de la cultura

Juego educativo (novela visual) hecho con [Ren'Py](https://www.renpy.org/), basado en la Introducción y los tres primeros capítulos de *La fragilidad ambiental de la cultura*, de Augusto Ángel Maya. Recorre el Paleolítico, el Homo sapiens y el Neolítico para mostrar que la cultura y la naturaleza se transforman mutuamente.

## Requisitos

- [Ren'Py 8.5](https://www.renpy.org/latest.html) para ejecutar el juego.
- [uv](https://docs.astral.sh/uv/) solo para regenerar las voces de la narración.

## Ejecutar el juego

Instala el SDK de Ren'Py una sola vez (Linux):

```bash
cd ~
curl -LO https://www.renpy.org/dl/8.5.3/renpy-8.5.3-sdk.tar.bz2
tar xjf renpy-8.5.3-sdk.tar.bz2 && rm renpy-8.5.3-sdk.tar.bz2
```

Desde la carpeta del proyecto:

```bash
~/renpy-8.5.3-sdk/renpy.sh .        # jugar
~/renpy-8.5.3-sdk/renpy.sh . lint   # revisar errores del script
```

Con el Ren'Py Launcher (`~/renpy-8.5.3-sdk/renpy.sh` sin argumentos): en **Preferences → Projects Directory** elige la carpeta que *contiene* este proyecto. El proyecto aparece en la lista; selecciónalo y pulsa **Launch Project**.

Ren'Py exige que el contenido del juego esté en la carpeta `game/`.

## Estructura

```text
.
├── game/
│   ├── script.rpy           # historia: diálogos, tarjetas narradas y preguntas
│   ├── screens.rpy          # interfaz: menú, diálogo, tarjetas, HUD, preguntas y final
│   ├── options.rpy          # configuración: nombre, versión, resolución 960×540
│   ├── tl/None/common.rpym  # textos internos de Ren'Py traducidos al español
│   ├── images/              # fondos (bg_*.png) y escenas de las tarjetas (scenes/)
│   └── audio/               # ambientes (amb_*), efectos (sfx_*) y narraciones (voice/)
├── generar_voz.py           # genera game/audio/voice/*.wav con Kokoro TTS
├── pyproject.toml           # dependencias de generar_voz.py
└── uv.lock
```

## Cómo funciona

Orden del recorrido: Prólogo → Introducción → Paleolítico → Homo sapiens → Neolítico → Reflexión final.

- **Tarjetas narradas** (`screen mini_story`): cada etapa tiene 4, con ilustración, texto y voz. La voz arranca sola y la tarjeta avanza cuando termina el audio. **SALTAR** avanza antes y **REPETIR VOZ** la reproduce otra vez. Si falta el WAV, la tarjeta espera a que se pulse SALTAR.
- **Preguntas** (`label quiz`): al final de cada etapa. Cada acierto suma 100 puntos (máximo 400). Cada error muestra una pista, suma una en «Pistas utilizadas» y repite la pregunta.
- **Pantalla final**: muestra la puntuación y las pistas usadas. **VOLVER A JUGAR** regresa al menú principal.

Para añadir una tarjeta o una pregunta, copia una llamada existente en `game/script.rpy`:

```renpy
call screen mini_story("TÍTULO", "images/scenes/archivo.png", "Texto en pantalla.", "audio/voice/archivo.wav")

call quiz(
    "¿Pregunta?",
    ["A. ...", "B. ...", "C. ..."],
    correct=1,  # posición de la respuesta correcta, empezando en 0
    praise="Mensaje al acertar.",
    hint="Pista al fallar.",
)
```

## Regenerar las voces

Los 16 WAV ya están en `game/audio/voice/`. Solo hay que regenerar uno si cambia su texto.

1. Actualiza el texto en `NARRATIONS`, dentro de `generar_voz.py`. Debe coincidir con la tarjeta de `script.rpy`.
2. Borra el WAV correspondiente. El script conserva los que ya existen.
3. Ejecuta:

   ```bash
   uv run generar_voz.py
   ```

La primera vez, uv crea el entorno `.venv` con Python 3.12 y las dependencias (~1,3 GB, con PyTorch solo para CPU), y Kokoro descarga el modelo Kokoro-82M desde Hugging Face (~330 MB). Cada narración tarda unos segundos en CPU.

Si aparece `Error processing file '.../espeak-ng-data/phontab'`, la ruta del proyecto es demasiado larga: espeak-ng no admite rutas de datos de más de 160 caracteres. Mueve el proyecto a una carpeta con una ruta más corta.

**Voz y licencia:** Kokoro-82M se publica bajo licencia Apache-2.0. La voz `em_alex` es masculina, sintética y en español, pero no tiene acento colombiano. Escucha las narraciones nuevas antes de distribuir el juego para revisar pausas y pronunciación.

## Historial

- **Reestructuración (oct. 2026):** proyecto uv con un único README, archivos sin uso eliminados y una sola definición por pantalla. El HUD, las preguntas y la pantalla final ahora usan el diseño neo-moderno de la 1.4, que antes quedaba tapado por las versiones antiguas de `script.rpy`. Arreglado el avance automático de las tarjetas, que no pasaba a la siguiente al terminar la voz.
- **1.6:** narración automática en la introducción y en las 12 tarjetas, botones SALTAR y REPETIR VOZ, y panel de texto más compacto.
- **1.5:** generador de voz local con Kokoro.
- **1.4:** fondos renovados e interfaz neo-moderna (azul profundo, paneles translúcidos y acentos turquesa).
- **1.3:** una ilustración propia para cada una de las 12 tarjetas.
