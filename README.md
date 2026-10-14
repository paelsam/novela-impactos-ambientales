# Los orígenes: del ecosistema a la cultura

Novela visual interactiva (Ren'Py 8.5) para el curso **Impactos Ambientales** (Universidad del Valle, docente Diana Marcela Mendoza). Presenta la Introducción y los Caps. 1–3 de *La fragilidad ambiental de la cultura* (Augusto Ángel Maya, pp. 6–27) con paisajes de grabado entintados, voz narrada, observaciones, quices y decisiones.

| Parte | Integrante | Archivo |
| --- | --- | --- |
| Introducción · pp. 6–9 | Elkin Samir Angulo Panameño | `game/capitulos/intro.rpy` |
| Cap. 1 · El lejano Paleolítico · pp. 10–12 | Sebastián Bolaños Morales | `game/capitulos/cap1.rpy` |
| Cap. 2 · Del Homo sapiens al Neolítico · pp. 13–17 | María Fernanda Cano Cobo | `game/capitulos/cap2.rpy` |
| Cap. 3 · El cercano Neolítico · pp. 18–27 | Javier Felipe Contreras Díaz | `game/capitulos/cap3.rpy` |
| Reflexión final (Buenaventura, la semilla y el árbol) | Todo el equipo | `game/capitulos/final.rpy` |

Los textos narrados son los del guion del equipo (`references/`). El cierre sobre Buenaventura es una conexión preparada por el equipo, no un dato del libro.

## Presentar en Google Meet

1. Abre la versión publicada en Vercel (ver «Publicar en Vercel») o, sin internet, genérala y sírvela: `./desplegar.sh --solo-compilar && python3 -m http.server 8000 --directory .cache/web`.
2. Ábrela en **Chrome** (`http://localhost:8000` en local).
3. En Meet: **Presentar → Una pestaña →** la del juego, y marca **«Compartir también el audio de la pestaña»**.
4. Respaldo sin internet ni navegador: el paquete de escritorio (`.cache/dist/LosOrigenes-2.0-pc.zip`).

Cada parte dura unos 3 minutos de voz, más las observaciones, el quiz y la decisión.

## Controles

| Acción | Teclas |
| --- | --- |
| Avanzar | clic · Espacio · → · AvPág |
| Retroceder | ← · RePág |
| Repetir la voz | R |
| Modo automático (avanza al terminar la voz) | A |
| Elegir opción en quiz o decisión | 1 · 2 · 3 |
| Pausa y ajustes (reducir movimiento, voz, volumen) | Esc o clic derecho |

## Requisitos y ejecución

- Ren'Py 8.5.3 SDK en `~/renpy-8.5.3-sdk` (o `RENPY_SDK=/ruta`), descargable en [renpy.org](https://www.renpy.org/latest.html).
- [uv](https://docs.astral.sh/uv/) para los scripts de Python.

```bash
~/renpy-8.5.3-sdk/renpy.sh .         # jugar
~/renpy-8.5.3-sdk/renpy.sh . lint    # revisar el script
```

## Estructura

```text
.
├── game/
│   ├── capitulos/        # contenido: una parte por integrante
│   ├── sistema/          # capítulos, voz, exploración, respuestas
│   ├── pantallas/        # menú, narración, observación, quiz, notas, pausa
│   ├── images/           # fondos/ y laminas/ (generados por ilustraciones.py)
│   ├── gui/              # piezas de interfaz (generadas)
│   ├── fonts/            # Literata y Atkinson Hyperlegible
│   ├── audio/            # ambiente/, sfx/, voz/ (generadas), voz/grabadas/ (propias)
│   └── tests/            # recorridos automáticos (no viajan en los paquetes)
├── fuentes.toml          # registro de imágenes: URL, recorte, tinta, licencia
├── ilustraciones.py      # fuentes.toml → imágenes entintadas, mapas, interfaz, créditos
├── generar_voz.py        # guion → voces OGG con Kokoro
├── probar_juego.sh       # lint + recorridos automáticos
├── desplegar.sh          # compila la versión web y la publica en Vercel (vercel.json)
└── tests/                # pytest de los scripts y de las reglas del guion
```

## Editar un capítulo

- Cada línea hablada es **una sola línea** con `id` único y sin `[...]`: `n "Texto." id cap2_03` (`nl` la muestra en el panel lateral). La voz se busca por ese `id`.
- Observación: `call explorar(lista_de_puntos)` con `Punto("id", x, y, "Etiqueta", "label_de_la_ficha")`; `x` e `y` son fracciones de la imagen.
- Quiz: `menu (screen="quiz", quiz="capN_quiz", pagina="p. 15")` con exactamente una opción `(correcta=True)`. Decisión: `menu (screen="decision", pagina=…)`; cada opción termina en un `segun "…" id …`.
- Nota de campo (`nota`) e idea clave (`clave`) cierran cada parte. El índice y las ideas clave están en `game/sistema/capitulos.rpy`.

## Imágenes y voces

```bash
uv run ilustraciones.py                    # descarga (caché en .cache/) y procesa todo
uv run ilustraciones.py --rejilla <id>     # rejilla del 5 % para colocar marcadores
uv run --group voz generar_voz.py          # genera solo las líneas nuevas o cambiadas
uv run --group voz generar_voz.py --revisar    # lista líneas sin voz o huérfanas
uv run --group voz generar_voz.py --duracion   # minutos de voz por parte
```

- Toda imagen entra por `fuentes.toml` con licencia y atribución; `game/creditos_generados.rpy` se genera solo.
- Para usar una grabación propia, guarda `game/audio/voz/grabadas/<id>.ogg`: tiene prioridad sobre la voz sintética y el script nunca la toca.
- La voz es Kokoro-82M (`em_alex`). El motor de pronunciación (espeak-ng) necesita que la ruta del proyecto tenga menos de 160 caracteres.

## Pruebas

```bash
uv run pytest -q          # scripts y reglas del guion (sin red)
./probar_juego.sh         # lint (0 avisos) + recorridos sin pantalla (mutter headless)
./probar_juego.sh cap2    # un solo recorrido
```

`probar_juego.sh` falla si algún caso queda sin ejecutar, aunque Ren'Py imprima `Status: PASSED`.

## Compilar

```bash
~/renpy-8.5.3-sdk/renpy.sh ~/renpy-8.5.3-sdk/launcher web_build "$PWD" --destination "$PWD/.cache/web"
~/renpy-8.5.3-sdk/renpy.sh ~/renpy-8.5.3-sdk/launcher distribute --package pc --destination "$PWD/.cache/dist" "$PWD"
```

La versión web necesita el módulo `renpy-8.5.3-web.zip` descomprimido dentro del SDK.

## Publicar en Vercel

Vercel solo aloja la versión web ya compilada (no puede ejecutar Ren'Py), así que se compila en local y se sube la carpeta resultante:

```bash
./desplegar.sh          # vista previa con URL temporal
./desplegar.sh --prod   # producción
```

- Requiere Node (`npx`). La primera vez pide iniciar sesión en Vercel y elegir cuenta y nombre de proyecto; el enlace queda en `.cache/vercel`.
- `vercel.json` (cabeceras y tipos de contenido) se copia solo a la carpeta publicada. La versión web pesa unos 65 MB, por debajo del límite de los despliegues estáticos.
- Tras cambiar texto, imágenes o voces, vuelve a ejecutar `./desplegar.sh --prod`.

## Créditos y licencias

- Libro: Augusto Ángel Maya, *La fragilidad ambiental de la cultura* (2015).
- Imágenes: grabados y fotografías de dominio público o con licencia abierta (CC BY, CC BY-SA); autor, obra, licencia y enlace de cada una en `fuentes.toml` y en la pantalla **Créditos** del juego.
- Voz: Kokoro-82M. Tipografías: Literata y Atkinson Hyperlegible (SIL OFL). Motor: Ren'Py (MIT/LGPL).
