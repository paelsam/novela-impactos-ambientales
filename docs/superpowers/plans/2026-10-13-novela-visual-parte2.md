# Plan de implementación · parte 2 de 3: sistema del juego (Tareas 8–12)

> Continúa `2026-10-13-novela-visual.md`, con las mismas restricciones globales y Review Focus. Los recorridos automáticos usan `./probar_juego.sh <testcase>`, que se crea en la Tarea 8.

**Cómo funcionan las pruebas de Ren'Py**
- `probar_juego.sh` ejecuta el lint (exige 0 avisos), levanta un compositor Wayland sin pantalla (`mutter --headless`) y corre `renpy.sh . test <nombre>`.
- Imprime el resumen `[rpytest]` y falla si el estado no es `PASSED`.
- Los testcases viven dentro de `testsuite global:` en `game/tests/pruebas.rpy`. Cada tarea **añade** el suyo al final de ese bloque, con 4 espacios de sangría.

### Task 8: Base del juego, menús, portada y pruebas

**Files:**
- Delete: `game/script.rpy`, `game/screens.rpy`, `game/images/` (todo), `game/audio/voice/` (todo), `game/audio/sfx_fire.wav`, `sfx_steps.wav`, `sfx_tool.wav`, `sfx_transition.wav` (si aún existen)
- Move: `game/audio/amb_forest.wav` → `game/audio/ambiente/bosque.wav`, `amb_cave.wav` → `ambiente/cueva.wav`, `amb_river.wav` → `ambiente/rio.wav`, `sfx_correct.wav` → `sfx/acierto.wav`, `sfx_error.wav` → `sfx/error.wav`, `sfx_ui.wav` → `sfx/clic.wav`
- Create: `game/fonts/*.ttf` + licencias, `fuentes.toml`, `game/options.rpy` (reescritura), `game/estilo.rpy`, `game/sistema/capitulos.rpy`, `game/pantallas/menu.rpy`, `game/capitulos/{intro,cap1,cap2,cap3,final}.rpy` (esqueleto), `probar_juego.sh`, `tests/test_guion.py`, `game/tests/pruebas.rpy`
- Generated: `game/images/fondos/menu_fondo.jpg`, `game/gui/*.png`, `game/creditos_generados.rpy`

**Interfaces:**
- Produces:
  - Constantes de color `PAPEL, PAPEL_2, BORDE, TINTA, TINTA_2, BOSQUE, MUSGO, CORRECTA, INCORRECTA, VELO`.
  - Fuentes `SERIF, SERIF_SEMI, SERIF_CURSIVA, SANS, SANS_NEGRITA`.
  - Estilos `bloque, kicker, titulo, titulo_portada, subtitulo, narracion, ficha_texto, leyenda, pie, progreso, boton(_text), boton_sec(_text), credito, tarjeta`.
  - Transform `paneo`; transiciones `fundido`, `transformacion`; `persistent.reducir_movimiento`.
  - Clase `Capitulo(id, numero, titulo, presenta, paginas)` con las propiedades `etiqueta` e `idea`.
  - `IDEAS` (dict), `CAPITULOS` (lista de 4), `FINAL`, `CAPITULO` (dict por id), `REFERENCIAS_NOTAS`, `abrir_capitulo(cap_id)`.
  - Variables `capitulo_actual` y `pagina`.
  - Personaje `portada`; pantallas `main_menu`, `indice`, `creditos`, `portada`; label `start`.

- [ ] **Step 1: Limpiar lo viejo y ordenar el audio**

```bash
cd "/home/fangulo/Escritorio/Impactos Ambientales/Proyecto"
ls ~/renpy-8.5.3-sdk/renpy.sh                       # el SDK debe existir
git rm -q -r game/script.rpy game/screens.rpy game/images game/audio/voice
mkdir -p game/audio/ambiente game/audio/sfx game/audio/voz/grabadas game/fonts
git mv game/audio/amb_forest.wav game/audio/ambiente/bosque.wav
git mv game/audio/amb_cave.wav game/audio/ambiente/cueva.wav
git mv game/audio/amb_river.wav game/audio/ambiente/rio.wav
git mv game/audio/sfx_correct.wav game/audio/sfx/acierto.wav
git mv game/audio/sfx_error.wav game/audio/sfx/error.wav
git mv game/audio/sfx_ui.wav game/audio/sfx/clic.wav
touch game/audio/voz/grabadas/.gitkeep
```

- [ ] **Step 2: Descargar las tipografías (OFL)**

```bash
cd game/fonts
curl -sSL -o Literata-Regular.ttf "https://fonts.gstatic.com/s/literata/v40/or3PQ6P12-iJxAIgLa78DkrbXsDgk0oVDaDPYLanFLHpPf2TbBG_F_Y.ttf"
curl -sSL -o Literata-SemiBold.ttf "https://fonts.gstatic.com/s/literata/v40/or3PQ6P12-iJxAIgLa78DkrbXsDgk0oVDaDPYLanFLHpPf2TbM-4F_Y.ttf"
curl -sSL -o Literata-Italic.ttf "https://fonts.gstatic.com/s/literata/v40/or3NQ6P12-iJxAIgLYT1PLs1Zd0nfUwAbeGVKoRYzNiCp1OUedn8_7XWSQ.ttf"
curl -sSL -o AtkinsonHyperlegible-Regular.ttf "https://fonts.gstatic.com/s/atkinsonhyperlegible/v12/9Bt23C1KxNDXMspQ1lPyU89-1h6ONRlW45GE5Q.ttf"
curl -sSL -o AtkinsonHyperlegible-Bold.ttf "https://fonts.gstatic.com/s/atkinsonhyperlegible/v12/9Bt73C1KxNDXMspQ1lPyU89-1h6ONRlW45G8WbcNcw.ttf"
curl -sSL -o OFL-Literata.txt "https://raw.githubusercontent.com/google/fonts/main/ofl/literata/OFL.txt"
curl -sSL -o OFL-AtkinsonHyperlegible.txt "https://raw.githubusercontent.com/google/fonts/main/ofl/atkinsonhyperlegible/OFL.txt"
file *.ttf | grep -c "TrueType"     # Expected: 5
cd ../..
```
Si una URL de `fonts.gstatic.com` devuelve 404, se obtiene la vigente con:
`curl -s -A "Mozilla/4.0" "https://fonts.googleapis.com/css2?family=Literata:ital,wght@0,400;0,600;1,400&family=Atkinson+Hyperlegible:wght@400;700" | grep -o "url([^)]*)"`.

- [ ] **Step 3: Crear el registro inicial y generar fondo, interfaz y créditos**

`fuentes.toml`:
```toml
# Registro de imágenes del juego (spec §5). Una entrada por imagen; es la única fuente de los créditos.
# Campos obligatorios: id, uso, tinta, url, pagina_fuente, autor, obra, anio, licencia, atribucion.
# Opcionales: recorte ([x, y, ancho, alto] o "auto"), rotar (grados, sentido horario),
# encaje ("cubrir" | "editorial"), centrado ([x, y] de 0 a 1), mapa ([lon_min, lat_min, lon_max, lat_max]).

[[imagen]]
id = "menu_fondo"
uso = "fondo"
tinta = "archivo"
url = "https://upload.wikimedia.org/wikipedia/commons/7/74/An_ideal_landscape_in_the_Quaternary_epoch_with_bears%2C_elks_Wellcome_V0023204.jpg"
pagina_fuente = "https://commons.wikimedia.org/wiki/File:An_ideal_landscape_in_the_Quaternary_epoch_with_bears,_elks_Wellcome_V0023204.jpg"
autor = "Édouard Riou (grabado, a partir de E. Meunier)"
obra = "La Terre avant le déluge (L. Figuier), lámina 10: paisaje ideal del Cuaternario"
anio = 1863
licencia = "CC BY 4.0"
atribucion = "É. Riou, La Terre avant le déluge (1863), lámina 10. Wellcome Collection, CC BY 4.0."
recorte = [63, 180, 2960, 1665]
notas = "Sin el pie impreso. También es el fondo del cierre."
```
Run: `uv run ilustraciones.py`
Expected: `✓ game/images/fondos/menu_fondo.jpg` y `Listo: 1 imágenes, piezas de interfaz y créditos.`; existen `game/gui/marco.png` y `game/creditos_generados.rpy`.

- [ ] **Step 4: Escribir las reglas del guion (pytest)**

`tests/test_guion.py`:
```python
"""Reglas del guion y de las pantallas que no cubre el lint de Ren'Py."""
import re
from pathlib import Path

JUEGO = Path(__file__).parent.parent / "game"


def archivos_rpy():
    return [p for p in JUEGO.rglob("*.rpy") if "tests" not in p.relative_to(JUEGO).parts]


def test_ningun_texto_menor_de_18px():
    for archivo in archivos_rpy():
        for n, linea in enumerate(archivo.read_text(encoding="utf-8").splitlines(), start=1):
            for tamano in re.findall(r"(?:^|[\s_])size (\d+)\b", linea):
                assert int(tamano) >= 18, f"{archivo.name}:{n} usa size {tamano} (mínimo 18 px)"


def test_ideas_clave_coinciden_con_los_capitulos():
    datos = (JUEGO / "sistema" / "capitulos.rpy").read_text(encoding="utf-8")
    ideas = dict(re.findall(r'^\s*"(\w+)": "(.+)",$', datos, re.M))
    for archivo in (JUEGO / "capitulos").glob("*.rpy"):
        for texto, parte in re.findall(r'^\s*clave "(.+)" id (\w+)_clave$', archivo.read_text(encoding="utf-8"), re.M):
            assert ideas[parte] == texto, f"La idea clave de {parte} no coincide con IDEAS en sistema/capitulos.rpy"
```
Run: `uv run pytest tests/test_guion.py -q`
Expected: `2 passed`.

- [ ] **Step 5: Crear el script de pruebas del juego**

`probar_juego.sh` (y luego `chmod +x probar_juego.sh`):
```bash
#!/usr/bin/env bash
# Prueba el juego sin pantalla: lint de Ren'Py (0 avisos) y recorridos automáticos (game/tests/).
# Uso: ./probar_juego.sh [testcase]     sin argumento corre todos (suite "global").
# Requiere el SDK en $RENPY_SDK (por defecto ~/renpy-8.5.3-sdk) y mutter (GNOME).
set -euo pipefail
SDK="${RENPY_SDK:-$HOME/renpy-8.5.3-sdk}"
JUEGO="$(cd "$(dirname "$0")" && pwd)"
PRUEBA="${1:-global}"
REGISTRO="$JUEGO/.cache/pruebas"
mkdir -p "$REGISTRO" "$JUEGO/.cache/capturas"

echo "== Lint"
"$SDK/renpy.sh" "$JUEGO" lint > "$REGISTRO/lint.txt" 2>&1 || true
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
trap 'kill $COMPOSITOR 2>/dev/null || true' EXIT
for _ in $(seq 50); do [ -S "$XDG_RUNTIME_DIR/$PANTALLA" ] && break; sleep 0.2; done

WAYLAND_DISPLAY="$PANTALLA" SDL_VIDEODRIVER=wayland SDL_AUDIODRIVER=disk SDL_DISKAUDIOFILE=/dev/null \
    timeout --kill-after=10 900 "$SDK/renpy.sh" "$JUEGO" test "$PRUEBA" --report-detailed \
    > "$REGISTRO/recorrido.txt" 2>&1 || true
grep -E "^\[rpytest\] (Status|Test cases|Assertions)" "$REGISTRO/recorrido.txt" | sort -u || true
if ! grep -q "Status: PASSED" "$REGISTRO/recorrido.txt"; then
    grep -E "Error|assert|failed" "$REGISTRO/recorrido.txt" | head -20 || true
    echo "Recorrido con fallos (detalle en $REGISTRO/recorrido.txt)"
    exit 1
fi
```
(`SDL_AUDIODRIVER=disk` hace que el audio avance en tiempo real sin sonar; con `dummy`, la voz nunca termina.)

- [ ] **Step 6: Escribir los recorridos que deben fallar**

`game/tests/pruebas.rpy`:
```renpy
## Recorridos automáticos (./probar_juego.sh). No viajan en los paquetes del juego.

testsuite global:
    before testcase:
        run MainMenu(confirm=False)
        pause 1.0

    testcase navegacion:
        assert screen "main_menu" timeout 10
        click "Capítulos"
        assert screen "indice" timeout 5
        click "Del Homo sapiens al Neolítico"
        assert screen "portada" timeout 10
        assert eval (capitulo_actual == "cap2")
        advance
        assert eval (capitulo_actual == "cap3") timeout 10

    testcase creditos:
        assert screen "main_menu" timeout 10
        click "Créditos"
        assert screen "creditos" timeout 5
        assert eval (any("Riou" in c[0] for c in CREDITOS_IMAGENES))
        click "Volver"
        assert screen "main_menu" timeout 5
```
Run: `./probar_juego.sh navegacion`
Expected: FAIL (el lint marca `game/options.rpy` o pantallas inexistentes, o el recorrido falla).

- [ ] **Step 7: Escribir la configuración**

`game/options.rpy` (reemplaza el anterior):
```renpy
## Configuración general del juego (spec §7).

define config.name = _("Los orígenes: del ecosistema a la cultura")
define config.version = "2.0"
define config.window_title = "Los orígenes: del ecosistema a la cultura"
define config.save_directory = "LosOrigenes-educativo"
define build.name = "LosOrigenes"

define config.window = "hide"
define config.check_conflicting_properties = True
define config.default_music_volume = 0.35

## La voz lee cada bloque: el texto aparece completo de inmediato.
define config.default_text_cps = 0

init python:
    gui.init(1920, 1080)

    # Puntero de presentación y flechas: AvPág y → avanzan; RePág y ← retroceden.
    config.keymap["rollforward"].remove("anyrepeat_K_PAGEDOWN")
    config.keymap["dismiss"].extend(["K_PAGEDOWN", "K_RIGHT"])
    config.keymap["rollback"].append("K_LEFT")

    # Nada de la parte de desarrollo viaja en los paquetes del juego.
    for _patron in ("*.py", "*.toml", "*.lock", "*.md", "*.sh", "*.txt", ".python-version", "tests/**",
                    "docs/**", "references/**", "prompt.md", "game/tests/**", "game/audio/voz/manifest.json"):
        build.classify(_patron, None)
```
Nota: `*.txt` solo afecta a la raíz del proyecto. Las licencias de `game/fonts/*.txt` viajan porque los patrones sin `**` no entran en subcarpetas.

`game/estilo.rpy`:
```renpy
## Sistema visual: paleta, tipografías, estilos y movimiento (spec §4).

define PAPEL = "#F3ECDC"
define PAPEL_2 = "#E9DFC8"
define BORDE = "#CBBE9F"
define TINTA = "#2A2722"
define TINTA_2 = "#5E574B"
define BOSQUE = "#2E4A3A"
define MUSGO = "#6B7A4B"
define CORRECTA = "#2E6B47"
define INCORRECTA = "#9E3B2B"
define VELO = "#101612B8"

## Literata para leer; Atkinson Hyperlegible para la interfaz. DejaVu (incluida en Ren'Py)
## aporta los símbolos que Atkinson no tiene: flechas, ✓, ✗, ≈ y ◉.
define SERIF = "fonts/Literata-Regular.ttf"
define SERIF_SEMI = "fonts/Literata-SemiBold.ttf"
define SERIF_CURSIVA = "fonts/Literata-Italic.ttf"
define SANS = FontGroup().add("DejaVuSans.ttf", 0x2190, 0x22FF).add("DejaVuSans.ttf", 0x25A0, 0x27BF).add("fonts/AtkinsonHyperlegible-Regular.ttf", 0x0000, 0xFFFF)
define SANS_NEGRITA = FontGroup().add("DejaVuSans-Bold.ttf", 0x2190, 0x22FF).add("DejaVuSans-Bold.ttf", 0x25A0, 0x27BF).add("fonts/AtkinsonHyperlegible-Bold.ttf", 0x0000, 0xFFFF)

style default:
    font SERIF
    size 34
    color TINTA
    language "unicode"

style bloque:
    background Frame("gui/marco.png", 16, 16)
    padding (34, 26)

style kicker:
    font SANS_NEGRITA
    size 18
    color TINTA_2
    kerning 1.6

style titulo:
    font SERIF_SEMI
    size 42
    line_spacing 8
    color TINTA

style titulo_portada is titulo:
    size 72

style subtitulo:
    font SANS
    size 26
    color TINTA_2

style narracion:
    font SERIF
    size 34
    line_spacing 15
    color TINTA

style ficha_texto is narracion:
    size 27
    line_spacing 12

style leyenda:
    font SERIF_CURSIVA
    size 18
    color TINTA_2

style pie:
    font SANS
    size 18
    color TINTA_2

style progreso:
    ysize 4
    left_bar Solid(BOSQUE)
    right_bar Solid(PAPEL_2)

style boton:
    background Frame("gui/boton.png", 10, 10)
    hover_background Frame("gui/boton_hover.png", 10, 10)
    padding (24, 14)

style boton_text:
    font SANS_NEGRITA
    size 22
    color PAPEL
    xalign 0.5

style boton_sec is boton:
    background Frame("gui/boton_sec.png", 10, 10)
    hover_background Frame("gui/boton_sec_hover.png", 10, 10)

style boton_sec_text is boton_text:
    color TINTA

style credito:
    font SANS
    size 22
    color TINTA

style tarjeta:
    background Frame("gui/opcion.png", 14, 14)
    hover_background Frame("gui/opcion_hover.png", 14, 14)
    padding (28, 28)

## Movimiento: paneo lento del fondo; "Reducir movimiento" lo apaga y acorta las transiciones.
default persistent.reducir_movimiento = False

define fundido = Dissolve(0.8)
define transformacion = Dissolve(2.5)

init python:
    def _paneo(trans, st, at):
        if persistent.reducir_movimiento:
            trans.zoom = 1.0
            return 0.5
        fase = (st % 40.0) / 20.0
        fase = fase if fase <= 1.0 else 2.0 - fase
        trans.zoom = 1.0 + 0.04 * fase * fase * (3 - 2 * fase)
        return 0

    def _transicion_accesible(trans, paired=None):
        if persistent.reducir_movimiento and trans is not None:
            return Dissolve(0.3)
        return trans

    config.with_callback = _transicion_accesible

transform paneo:
    xalign 0.5
    yalign 0.5
    function _paneo
```

- [ ] **Step 8: Escribir los datos de las partes**

`game/sistema/capitulos.rpy`:
```renpy
## Partes de la presentación: quién presenta, páginas e ideas clave (spec §1–§3).

init -10 python:
    class Capitulo(object):
        def __init__(self, id, numero, titulo, presenta, paginas):
            self.id = id
            self.numero = numero        # "Introducción", "Capítulo 1"…
            self.titulo = titulo
            self.presenta = presenta
            self.paginas = paginas

        @property
        def etiqueta(self):
            """Indicador de los bloques: "Cap. 2 · Del Homo sapiens al Neolítico"."""
            if not self.numero.startswith("Capítulo"):
                return self.numero
            return "{} · {}".format(self.numero.replace("Capítulo", "Cap."), self.titulo)

        @property
        def idea(self):
            return IDEAS.get(self.id, "")

    # Deben coincidir letra por letra con las líneas `clave` de cada capítulo (lo vigila tests/test_guion.py).
    IDEAS = {
        "intro": "La historia humana no ocurre en un escenario vacío: sociedad, técnica y ecosistemas se transforman juntos.",
        "cap1": "Sin garras ni colmillos, los seres humanos se adaptaron mediante instrumentos y cooperación; al especializarse en la caza, empezaron a ejercer una presión importante sobre algunos ecosistemas.",
        "cap2": "Cada avance técnico transformó el medio, y cada cambio del medio obligó a reorganizar la sociedad.",
        "cap3": "Con la agricultura, las sociedades pusieron partes del ecosistema al servicio de la producción: ganaron autonomía, pero también alteraron las cadenas tróficas.",
    }

    CAPITULOS = [
        Capitulo("intro", "Introducción", "Historia y medio ambiente", "Elkin Samir Angulo Panameño", "pp. 6–9"),
        Capitulo("cap1", "Capítulo 1", "El lejano Paleolítico", "Sebastián Bolaños Morales", "pp. 10–12"),
        Capitulo("cap2", "Capítulo 2", "Del Homo sapiens al Neolítico", "María Fernanda Cano Cobo", "pp. 13–17"),
        Capitulo("cap3", "Capítulo 3", "El cercano Neolítico", "Javier Felipe Contreras Díaz", "pp. 18–27"),
    ]
    FINAL = Capitulo("final", "Reflexión final", "Del pasado al presente", "Todo el equipo", "p. 9")
    CAPITULO = {c.id: c for c in CAPITULOS + [FINAL]}

    REFERENCIAS_NOTAS = [
        "Neandertales erguidos: Smithsonian National Museum of Natural History, Human Origins Program, «Homo neanderthalensis».",
        "Homo sapiens de Jebel Irhoud: Hublin, J.-J. et al. (2017). Nature, 546, 289–292.",
        "Domesticación del maíz: Matsuoka, Y. et al. (2002). PNAS, 99(9), 6080–6084.",
    ]

    def abrir_capitulo(cap_id):
        """Marca la parte actual: la usan la portada y el indicador de los bloques."""
        store.capitulo_actual = cap_id
        store.pagina = CAPITULO[cap_id].paginas

default capitulo_actual = "intro"
default pagina = ""

label start:
    jump intro
```

- [ ] **Step 9: Escribir menú, índice, créditos y portada**

`game/pantallas/menu.rpy`:
```renpy
## Inicio, índice de capítulos, créditos y portada de cada parte (spec §2, §4).

screen main_menu():
    tag menu
    add "menu_fondo"
    frame:
        style "bloque"
        xalign 0.5
        ypos 110
        xsize 1180
        has vbox
        spacing 14
        text _("LOS ORÍGENES") style "kicker" xalign 0.5
        text _("Del ecosistema a la cultura") style "titulo_portada" xalign 0.5 text_align 0.5
        text _("Basado en «La fragilidad ambiental de la cultura», de Augusto Ángel Maya") style "subtitulo" xalign 0.5 text_align 0.5
        text _("Introducción y capítulos 1, 2 y 3 · Universidad del Valle · Impactos Ambientales") style "pie" xalign 0.5
    vbox:
        xalign 0.5
        ypos 600
        spacing 16
        textbutton _("Comenzar") action Start() style "boton" xminimum 440
        textbutton _("Capítulos") action ShowMenu("indice") style "boton_sec" xminimum 440
        textbutton _("Créditos") action ShowMenu("creditos") style "boton_sec" xminimum 440
        textbutton _("Salir") action Quit(confirm=True) style "boton_sec" xminimum 440

screen indice():
    tag menu
    add "menu_fondo"
    add Solid("#F3ECDCB3")
    text _("Capítulos") style "titulo_portada" xpos 96 ypos 64
    hbox:
        xpos 96
        ypos 210
        spacing 32
        for cap in CAPITULOS:
            button:
                style "tarjeta"
                xsize 408
                ysize 600
                alt cap.titulo
                action Start(cap.id)
                has vbox
                spacing 12
                text cap.numero.upper() style "kicker"
                text cap.titulo style "titulo"
                null height 20
                text _("Presenta") style "pie"
                text cap.presenta style "subtitulo"
                text "{} · ≈ 5 min".format(cap.paginas) style "pie"
    textbutton _("← Volver") action Return() style "boton_sec" xpos 96 ypos 940

screen creditos():
    tag menu
    add "menu_fondo"
    add Solid("#F3ECDCE6")
    text _("Créditos") style "titulo_portada" xpos 96 ypos 48
    viewport:
        xpos 96
        ypos 170
        xsize 1728
        ysize 740
        mousewheel True
        draggable True
        scrollbars "vertical"
        vbox:
            spacing 10
            text _("Equipo") style "titulo"
            for cap in CAPITULOS:
                text "{} · {}".format(cap.presenta, cap.etiqueta) style "credito"
            null height 16
            text _("Libro") style "titulo"
            text _("Ángel Maya, A. (2015). La fragilidad ambiental de la cultura. Historia y medio ambiente (2.ª ed.). www.augustoangelmaya.com. Uso educativo sin ánimo de lucro, citando la fuente.") style "credito"
            null height 16
            text _("Ilustraciones") style "titulo"
            for atribucion, obra, fuente in CREDITOS_IMAGENES:
                text "{} — {}".format(atribucion, obra) style "credito"
            null height 16
            text _("Ciencia actual (notas de campo)") style "titulo"
            for referencia in REFERENCIAS_NOTAS:
                text referencia style "credito"
            null height 16
            text _("Voz, tipografía y motor") style "titulo"
            text _("Narración sintética: Kokoro-82M (Apache-2.0), voz em_alex.") style "credito"
            text _("Tipografías: Literata y Atkinson Hyperlegible (SIL Open Font License 1.1); símbolos de DejaVu Sans.") style "credito"
            text _("Hecho con Ren'Py 8.5 (licencia MIT).") style "credito"
    textbutton _("← Volver") action Return() style "boton_sec" xpos 96 ypos 950

## Portada narrada: la voz lee el texto del guion; en pantalla se ve la composición.
define portada = Character(None, screen="portada")

screen portada(who, what):
    $ cap = CAPITULO[capitulo_actual]
    add Solid("#F3ECDCD9")
    key "r" action VoiceReplay()
    vbox:
        xalign 0.5
        yalign 0.45
        spacing 20
        text cap.numero.upper() style "kicker" xalign 0.5
        text cap.titulo style "titulo_portada" xalign 0.5 text_align 0.5
        text _("Presenta: {}").format(cap.presenta) style "subtitulo" xalign 0.5
        text cap.paginas style "pie" xalign 0.5
    text what id "what" alpha 0.0
```

- [ ] **Step 10: Escribir los esqueletos de las partes**

`game/capitulos/intro.rpy`:
```renpy
## Introducción · pp. 6–9 · Presenta Elkin Samir Angulo Panameño. (Contenido completo: Tarea 14.)

label intro:
    $ abrir_capitulo("intro")
    scene menu_fondo at paneo with fundido
    portada "Introducción: Los orígenes, del ecosistema a la cultura." id intro_portada
    jump cap1
```
`game/capitulos/cap1.rpy`, `cap2.rpy` y `cap3.rpy`: el mismo patrón. Cada uno con su `label capN`, `abrir_capitulo("capN")`, una línea `portada "Capítulo N." id capN_portada` y `jump` a la siguiente parte (cap1→cap2, cap2→cap3, cap3→final).
`game/capitulos/final.rpy`:
```renpy
## Reflexión final · Todo el equipo. (Contenido completo: Tarea 17.)

label final:
    $ abrir_capitulo("final")
    scene menu_fondo at paneo with fundido
    return
```

- [ ] **Step 11: Ejecutar y ver que pasan**

Run: `./probar_juego.sh navegacion && ./probar_juego.sh creditos && uv run pytest -q`
Expected: `Lint sin avisos.`, `[rpytest] Status: PASSED` dos veces y `37 passed`.
Si el lint da avisos, se corrige lo que indique la línea (`game/archivo.rpy:N`).

- [ ] **Step 12: Commit**

```bash
git add -A
git commit -q -m "feat: base del juego con nueva identidad, menús, índice, créditos y portada" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 9: Bloque narrativo y voz automática

**Files:**
- Create: `game/sistema/voz.rpy`, `game/pantallas/narracion.rpy`, `game/tests/escenas_prueba.rpy`
- Modify: `game/tests/pruebas.rpy` (añadir testcase)

**Interfaces:**
- Consumes: `CAPITULO`, `capitulo_actual`, `pagina` y los estilos (Tarea 8).
- Produces:
  - `voz_de(tlid) -> str`: ruta de `audio/voz/grabadas/<id>.ogg` si existe; si no, `audio/voz/<id>.ogg`.
  - `progreso(tlid) -> (parte, n, total) | None`, `kicker() -> str` en mayúsculas, `linea_actual() -> str`, `TOTAL_BLOQUES`.
  - Personajes `n` (abajo) y `nl` (lateral); pantallas `bloque(who, what, posicion)` y `say`.

- [ ] **Step 1: Escribir la escena de prueba y el recorrido**

`game/tests/escenas_prueba.rpy`:
```renpy
## Escenas mínimas para los recorridos automáticos. No viajan en los paquetes.

label prueba_narracion:
    $ abrir_capitulo("cap2")
    scene expression Solid(PAPEL)
    n "Primera línea de prueba." id prueba_01
    nl "Segunda línea, en el panel lateral." id prueba_02
    n "Tercera línea." id prueba_03
    return
```
Añadir a `game/tests/pruebas.rpy`, dentro de `testsuite global:`:
```renpy
    testcase narracion:
        run Start("prueba_narracion")
        assert screen "bloque" timeout 5
        assert eval (progreso("prueba_01") == ("prueba", 1, 3))
        assert eval (kicker() == "CAP. 2 · DEL HOMO SAPIENS AL NEOLÍTICO")
        assert eval (voz_de("no_existe") == "audio/voz/no_existe.ogg")
        advance
        assert eval (renpy.get_screen("bloque").scope["posicion"] == "lado") timeout 5
        keysym "K_PAGEDOWN"
        assert eval (renpy.get_screen("bloque").scope["posicion"] == "abajo") timeout 5
        keysym "K_LEFT"
        assert eval (renpy.get_screen("bloque").scope["posicion"] == "lado") timeout 5
```
Run: `./probar_juego.sh narracion`
Expected: FAIL (`n` no está definido o la pantalla `bloque` no existe).

- [ ] **Step 2: Implementar la voz y el progreso**

`game/sistema/voz.rpy`:
```renpy
## Voz automática y progreso de cada línea (spec §6, §7).

init -10 python:
    import re

    _BLOQUE = re.compile(r"^(?P<parte>[a-z]+[0-9]?)_(?P<n>[0-9]{2})$")

    def voz_de(tlid):
        """Voz de una línea: la grabación propia si existe; si no, la voz sintética."""
        grabada = "audio/voz/grabadas/{}.ogg".format(tlid)
        if renpy.loadable(grabada):
            return grabada
        return "audio/voz/{}.ogg".format(tlid)

    def progreso(tlid):
        """("cap2", 3, 10) para la línea cap2_03, o None si no es un bloque narrativo."""
        m = _BLOQUE.match(tlid or "")
        if not m:
            return None
        return m.group("parte"), int(m.group("n")), TOTAL_BLOQUES.get(m.group("parte"), 0)

    def kicker():
        cap = CAPITULO.get(store.capitulo_actual)
        return cap.etiqueta.upper() if cap else ""

    def linea_actual():
        return renpy.game.context().translate_identifier

init 999 python:
    # Bloques narrativos de cada parte, contados a partir de los id del guion.
    TOTAL_BLOQUES = {}
    for _tlid in renpy.game.script.translator.default_translates:
        _m = _BLOQUE.match(_tlid)
        if _m:
            TOTAL_BLOQUES[_m.group("parte")] = TOTAL_BLOQUES.get(_m.group("parte"), 0) + 1

define config.auto_voice = voz_de
define config.default_afm_time = 1
define config.afm_voice_delay = 0.6
```

- [ ] **Step 3: Implementar el bloque narrativo**

`game/pantallas/narracion.rpy`:
```renpy
## Bloque narrativo (spec §2, §4): tarjeta de papel abajo a la izquierda o panel lateral derecho.

define n = Character(None, screen="bloque", show_posicion="abajo")
define nl = Character(None, screen="bloque", show_posicion="lado")
define narrator = n

screen bloque(who, what, posicion="abajo"):
    $ prog = progreso(linea_actual())
    $ lateral = posicion == "lado"
    key "r" action VoiceReplay()
    key "a" action Preference("auto-forward", "toggle")
    frame:
        style "bloque"
        xpos (1136 if lateral else 64)
        ypos (64 if lateral else 1028)
        yanchor (0.0 if lateral else 1.0)
        xsize (720 if lateral else 800)
        has vbox
        spacing 12
        hbox:
            xfill True
            text kicker() style "kicker"
            if prog:
                text "{} / {}".format(prog[1], prog[2]) style "kicker" xalign 1.0
        text what id "what" style "narracion"
        if prog:
            bar value StaticValue(prog[1], prog[2]) style "progreso"
        hbox:
            xfill True
            text _("R · repetir voz    A · automático") style "pie"
            text pagina style "pie" xalign 1.0

screen say(who, what):
    use bloque(who, what)
```

- [ ] **Step 4: Ejecutar y ver que pasa**

Run: `./probar_juego.sh narracion && ./probar_juego.sh navegacion`
Expected: `Status: PASSED` en ambos.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -q -m "feat: bloque narrativo con voz automática, progreso por id y teclas de presentación" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 10: Observación del paisaje

**Files:**
- Create: `game/sistema/explorar.rpy`, `game/pantallas/observacion.rpy`
- Modify: `game/tests/escenas_prueba.rpy`, `game/tests/pruebas.rpy`, `game/estilo.rpy` (estilos de marcador)

**Interfaces:**
- Produces:
  - Clase `Punto(id, x, y, etiqueta, label)`, con `x` e `y` entre 0 y 1.
  - `call explorar(puntos)`: devuelve el control al pulsar "Continuar".
  - Variables `vistos` (set de ids), `puntos_escena` y `punto_activo`.
  - Personaje `ficha`, con argumentos `show_lamina`, `show_titulo`, `show_leyenda`, `show_pagina`.
  - Pantallas `explorar(puntos)` y `ficha(who, what, lamina, titulo, leyenda, pagina)`.

- [ ] **Step 1: Escribir la escena de prueba y el recorrido**

Añadir a `game/tests/escenas_prueba.rpy`:
```renpy
define prueba_puntos = [
    Punto("uno", 0.70, 0.40, "Punto uno", "prueba_obs_uno"),
    Punto("dos", 0.30, 0.60, "Punto dos", "prueba_obs_dos"),
]

label prueba_observacion:
    $ abrir_capitulo("cap2")
    scene menu_fondo
    call explorar(prueba_puntos)
    n "Después de explorar." id prueba_04
    return

label prueba_obs_uno:
    ficha "Texto de la ficha uno." (show_lamina="menu_fondo", show_titulo="Uno", show_leyenda="Leyenda de prueba.", show_pagina="p. 1") id prueba_obs_uno
    return

label prueba_obs_dos:
    ficha "Texto de la ficha dos, sin lámina." (show_titulo="Dos", show_pagina="p. 2") id prueba_obs_dos
    return
```
Añadir a `pruebas.rpy`:
```renpy
    testcase observacion:
        run Start("prueba_observacion")
        assert screen "explorar" timeout 5
        click "Punto uno"
        assert screen "ficha" timeout 5
        assert eval ("uno" in vistos)
        click "Volver al paisaje"
        assert screen "explorar" timeout 5
        keysym "K_2"
        assert eval (punto_activo is not None and punto_activo.id == "dos") timeout 5
        advance
        assert screen "explorar" timeout 5
        click "Continuar"
        assert screen "bloque" timeout 5
```
Run: `./probar_juego.sh observacion`
Expected: FAIL (`Punto` no definido).

- [ ] **Step 2: Implementar la lógica**

`game/sistema/explorar.rpy`:
```renpy
## Exploración del paisaje: puntos observables y sus fichas (spec §2, §7).

init -10 python:
    class Punto(object):
        """Elemento observable: posición relativa (0–1), etiqueta y label con su ficha."""
        def __init__(self, id, x, y, etiqueta, label):
            self.id = id
            self.x = x
            self.y = y
            self.etiqueta = etiqueta
            self.label = label

default vistos = set()
default puntos_escena = []
default punto_activo = None

label explorar(puntos):
    $ puntos_escena = puntos
    while True:
        $ punto_activo = renpy.call_screen("explorar", puntos=puntos)
        if punto_activo is None:
            return
        $ vistos.add(punto_activo.id)
        call expression punto_activo.label
```

- [ ] **Step 3: Implementar las pantallas**

Añadir a `game/estilo.rpy`:
```renpy
style marca:
    background "gui/marca.png"
    hover_background "gui/marca_hover.png"
    selected_background "gui/marca_vista.png"
    xysize (56, 56)

style marca_num:
    font SANS_NEGRITA
    size 26
    color TINTA
    xalign 0.5
    yalign 0.5

style marca_etiqueta:
    background Frame("gui/marco.png", 16, 16)
    padding (12, 8)
```
`game/pantallas/observacion.rpy`:
```renpy
## Marcadores sobre el paisaje y ficha de observación (spec §2, §4.6–7).

screen explorar(puntos):
    default foco = None
    for i, p in enumerate(puntos):
        button:
            style "marca"
            pos (p.x, p.y)
            anchor (0.5, 0.5)
            selected p.id in vistos
            alt p.etiqueta
            action Return(p)
            hovered SetScreenVariable("foco", i)
            unhovered SetScreenVariable("foco", None)
            text str(i + 1) style "marca_num"
        if p.id in vistos:
            add "gui/insignia_vista.png" pos (p.x, p.y) xoffset 14 yoffset -42
            text "✓" font "DejaVuSans-Bold.ttf" size 18 color "#FFFFFF" pos (p.x, p.y) xoffset 21 yoffset -40
        key "K_{}".format(i + 1) action Return(p)
    if foco is not None:
        frame:
            style "marca_etiqueta"
            pos (puntos[foco].x, puntos[foco].y)
            xoffset 40
            yanchor 0.5
            text puntos[foco].etiqueta style "kicker"
    frame:
        style "bloque"
        xpos 64
        ypos 1028
        yanchor 1.0
        xsize 800
        hbox:
            xfill True
            text _("Explora el paisaje: elige un punto (1–{})").format(len(puntos)) style "pie" yalign 0.5
            textbutton _("Continuar →") action Return(None) style "boton" xalign 1.0
    key "K_PAGEDOWN" action Return(None)

define ficha = Character(None, screen="ficha")

screen ficha(who, what, lamina=None, titulo="", leyenda="", pagina=""):
    $ p = punto_activo
    $ px = int(p.x * 1920)
    $ py = int(p.y * 1080)
    $ derecha = px < 960                       # la ficha va en la mitad opuesta al punto
    $ fx = 1236 if derecha else 64
    $ borde = fx if derecha else fx + 620
    $ numero = next((i + 1 for i, q in enumerate(puntos_escena) if q.id == p.id), 1)
    key "r" action VoiceReplay()
    for i, q in enumerate(puntos_escena):
        add ("gui/marca_hover.png" if q.id == p.id else ("gui/marca_vista.png" if q.id in vistos else "gui/marca.png")):
            pos (q.x, q.y)
            anchor (0.5, 0.5)
        text str(i + 1) style "marca_num" pos (q.x, q.y) anchor (0.5, 0.5)
    # Línea guía en ángulo: sale de la ficha a la altura del título y baja hasta el punto.
    add Solid(PAPEL) xpos min(borde, px) ypos 150 xsize abs(px - borde) ysize 3
    add Solid(PAPEL) xpos px - 1 ypos 150 xsize 3 ysize max(0, py - 150 - 32)
    frame:
        style "bloque"
        xpos fx
        ypos 48
        xsize 620
        has vbox
        spacing 10
        hbox:
            xfill True
            text _("OBSERVACIÓN {} DE {}").format(numero, len(puntos_escena)) style "kicker"
            text pagina style "kicker" xalign 1.0
        if lamina:
            add lamina xysize (552, 300) fit "cover"
            text leyenda style "leyenda"
        text titulo style "titulo"
        text what id "what" style "ficha_texto"
        hbox:
            xfill True
            text _("R · repetir voz") style "pie" yalign 0.5
            textbutton _("← Volver al paisaje") action Return() style "boton_sec" xalign 1.0
```

- [ ] **Step 4: Ejecutar y ver que pasa**

Run: `./probar_juego.sh observacion && ./probar_juego.sh narracion`
Expected: `Status: PASSED` en ambos.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -q -m "feat: exploración del paisaje con marcadores, fichas y línea guía" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 11: Quiz y decisión

**Files:**
- Create: `game/sistema/respuestas.rpy`, `game/pantallas/quiz.rpy`
- Modify: `tests/test_guion.py`, `game/tests/escenas_prueba.rpy`, `game/tests/pruebas.rpy`

**Interfaces:**
- Produces:
  - Clase `EstadoRespuesta(opciones, elegida, correcta, pagina)` con la propiedad `acerto`.
  - `responder_quiz(quiz, opciones, elegida, correcta, pagina)`: lanza una excepción si `correcta` es `None`. `elegir_decision(opciones, elegida, pagina)`.
  - Variables `aciertos`, `respondidas` (dict quiz → bool del primer intento), `estado_quiz` y `estado_decision`.
  - Personajes `pregunta`, `dilema`, `porque` y `segun`.
  - Pantallas `pregunta(who, what, tipo)`, `quiz(items, quiz, pagina)`, `decision(items, pagina)`, `choice(items)`, `retroalimentacion` y `segun`.
  - **Uso en un capítulo:** `menu (screen="quiz", quiz="cap2_quiz", pagina="p. 15"):` con `(correcta=True)` en una opción, y luego `porque "…" id cap2_quiz_porque`.

- [ ] **Step 1: Escribir la regla del guion (debe pasar ya, y fallar cuando falte la correcta)**

Añadir a `tests/test_guion.py`:
```python
def test_cada_quiz_tiene_una_correcta():
    for archivo in (JUEGO / "capitulos").glob("*.rpy"):
        lineas = archivo.read_text(encoding="utf-8").splitlines()
        for n, linea in enumerate(lineas):
            if 'screen="quiz"' not in linea:
                continue
            sangria = len(linea) - len(linea.lstrip())
            bloque = []
            for siguiente in lineas[n + 1:]:
                if siguiente.strip() and len(siguiente) - len(siguiente.lstrip()) <= sangria:
                    break
                bloque.append(siguiente)
            correctas = sum("(correcta=True)" in b for b in bloque)
            assert correctas == 1, f"{archivo.name}:{n + 1}: el quiz tiene {correctas} opciones correctas (debe ser 1)"
```

- [ ] **Step 2: Escribir la escena de prueba y el recorrido**

Añadir a `game/tests/escenas_prueba.rpy`:
```renpy
label prueba_quiz:
    $ abrir_capitulo("cap2")
    scene menu_fondo
    call prueba_quiz_bloque
    call prueba_quiz_bloque
    menu (screen="decision", pagina="p. 14"):
        dilema "¿Decisión de prueba?" id prueba_dec
        "Camino A":
            segun "Según el libro, A." id prueba_dec_a
        "Camino B":
            segun "Según el libro, B." id prueba_dec_b
    n "Fin de la prueba." id prueba_05
    return

label prueba_quiz_bloque:
    menu (screen="quiz", quiz="prueba_quiz", pagina="p. 15"):
        pregunta "¿Pregunta de prueba?" id prueba_quiz
        "Opción incorrecta":
            pass
        "Opción correcta" (correcta=True):
            pass
        "Otra incorrecta":
            pass
    porque "Explicación de prueba." id prueba_quiz_porque
    return
```
Añadir a `pruebas.rpy`:
```renpy
    testcase quiz:
        run Start("prueba_quiz")
        assert screen "quiz" timeout 5
        click "Opción incorrecta"
        assert screen "retroalimentacion" timeout 5
        assert eval (aciertos == 0 and respondidas == {"prueba_quiz": False})
        assert eval (estado_quiz.correcta == 1 and estado_quiz.elegida == 0)
        advance
        assert screen "quiz" timeout 5
        keysym "K_2"
        assert screen "retroalimentacion" timeout 5
        assert eval (aciertos == 0)
        advance
        assert screen "decision" timeout 5
        click "Camino B"
        assert screen "segun" timeout 5
        assert eval (estado_decision.elegida == 1)
```
Run: `./probar_juego.sh quiz`
Expected: FAIL (la pantalla `quiz` no existe).

- [ ] **Step 3: Implementar el estado de las respuestas**

`game/sistema/respuestas.rpy`:
```renpy
## Aciertos del salón y estado de la última respuesta (spec §2, §7).

init -10 python:
    class EstadoRespuesta(object):
        def __init__(self, opciones, elegida, correcta, pagina):
            self.opciones = opciones
            self.elegida = elegida
            self.correcta = correcta
            self.pagina = pagina

        @property
        def acerto(self):
            return self.elegida == self.correcta

    def responder_quiz(quiz, opciones, elegida, correcta, pagina):
        """Guarda la respuesta; solo el primer intento de cada quiz cuenta para los aciertos."""
        if correcta is None:
            raise Exception("El quiz «{}» no marca ninguna opción con (correcta=True).".format(quiz))
        store.estado_quiz = EstadoRespuesta(opciones, elegida, correcta, pagina)
        if quiz not in store.respondidas:
            store.respondidas[quiz] = elegida == correcta
            if elegida == correcta:
                store.aciertos += 1
        renpy.sound.play("audio/sfx/acierto.wav" if elegida == correcta else "audio/sfx/error.wav")

    def elegir_decision(opciones, elegida, pagina):
        store.estado_decision = EstadoRespuesta(opciones, elegida, None, pagina)

default aciertos = 0
default respondidas = {}
default estado_quiz = None
default estado_decision = None
```

- [ ] **Step 4: Implementar las pantallas**

`game/pantallas/quiz.rpy`:
```renpy
## Quiz, decisión y retroalimentación (spec §2, §4.8–10).

define pregunta = Character(None, screen="pregunta", show_tipo="quiz")
define dilema = Character(None, screen="pregunta", show_tipo="decision")
define porque = Character(None, screen="retroalimentacion")
define segun = Character(None, screen="segun")

style opcion:
    background Frame("gui/opcion.png", 14, 14)
    hover_background Frame("gui/opcion_hover.png", 14, 14)
    padding (20, 16)
    xfill True

style opcion_bien is opcion:
    background Frame("gui/opcion_bien.png", 14, 14)

style opcion_mal is opcion:
    background Frame("gui/opcion_mal.png", 14, 14)

style opcion_elegida is opcion:
    background Frame("gui/opcion_hover.png", 14, 14)

style opcion_texto:
    font SANS
    size 28
    color TINTA

style letra:
    background Frame("gui/letra.png", 10, 10)
    xysize (44, 44)

style letra_texto:
    font SANS_NEGRITA
    size 22
    color TINTA
    xalign 0.5
    yalign 0.5

style resultado_bien:
    font SANS_NEGRITA
    size 30
    color CORRECTA

style resultado_mal is resultado_bien:
    color INCORRECTA

style estado_bien:
    font SANS_NEGRITA
    size 22
    color CORRECTA

style estado_mal is estado_bien:
    color INCORRECTA

style porque_marco:
    background Frame("gui/filete.png", 8, 0, 0, 0)
    left_padding 22

screen pregunta(who, what, tipo="quiz"):
    add Solid(VELO)
    frame:
        style "bloque"
        xalign 0.5
        ypos 110
        xsize 1120
        ysize 860
        has vbox
        spacing 16
        hbox:
            xfill True
            text (_("PREGUNTA · {}") if tipo == "quiz" else _("DECISIÓN · {}")).format(kicker()) style "kicker"
            if tipo == "quiz":
                text _("ACIERTOS DEL SALÓN: {} DE {}").format(aciertos, len(respondidas)) style "kicker" xalign 1.0
        text what id "what" style "titulo"

screen quiz(items, quiz, pagina=""):
    $ opciones = [i.caption for i in items]
    $ correcta = next((n for n, i in enumerate(items) if i.kwargs.get("correcta")), None)
    vbox:
        xalign 0.5
        ypos 340
        xsize 1052
        spacing 14
        for n, item in enumerate(items):
            $ elegir = [Function(responder_quiz, quiz, opciones, n, correcta, pagina), item.action]
            button:
                style "opcion"
                action elegir
                hbox:
                    spacing 18
                    frame:
                        style "letra"
                        text "ABC"[n] style "letra_texto"
                    text item.caption style "opcion_texto" yalign 0.5
            key "K_{}".format(n + 1) action elegir

screen decision(items, pagina=""):
    $ opciones = [i.caption for i in items]
    vbox:
        xalign 0.5
        ypos 340
        xsize 1052
        spacing 14
        for n, item in enumerate(items):
            $ elegir = [Function(elegir_decision, opciones, n, pagina), item.action]
            button:
                style "opcion"
                action elegir
                hbox:
                    spacing 18
                    frame:
                        style "letra"
                        text "ABC"[n] style "letra_texto"
                    text item.caption style "opcion_texto" yalign 0.5
            key "K_{}".format(n + 1) action elegir

screen choice(items):
    use decision(items)

screen retroalimentacion(who, what):
    $ e = estado_quiz
    add Solid(VELO)
    key "r" action VoiceReplay()
    frame:
        style "bloque"
        xalign 0.5
        ypos 90
        xsize 1120
        has vbox
        spacing 14
        hbox:
            xfill True
            text (_("✓ ¡Correcto!") if e.acerto else _("✗ No es así")) style ("resultado_bien" if e.acerto else "resultado_mal")
            text _("ACIERTOS DEL SALÓN: {} DE {}").format(aciertos, len(respondidas)) style "kicker" xalign 1.0 yalign 0.5
        for n, opcion in enumerate(e.opciones):
            frame:
                style ("opcion_bien" if n == e.correcta else ("opcion_mal" if n == e.elegida else "opcion"))
                hbox:
                    spacing 18
                    frame:
                        style "letra"
                        text "ABC"[n] style "letra_texto"
                    text opcion style "opcion_texto" yalign 0.5 xmaximum 760
                    if n == e.correcta:
                        text _("✓ Correcta") style "estado_bien" yalign 0.5
                    elif n == e.elegida:
                        text _("✗ No es así") style "estado_mal" yalign 0.5
        frame:
            style "porque_marco"
            has vbox
            spacing 6
            text _("POR QUÉ") style "kicker"
            text what id "what" style "ficha_texto"
        text e.pagina style "pie"

screen segun(who, what):
    $ e = estado_decision
    add Solid(VELO)
    key "r" action VoiceReplay()
    frame:
        style "bloque"
        xalign 0.5
        ypos 110
        xsize 1120
        has vbox
        spacing 14
        text _("DECISIÓN · {}").format(kicker()) style "kicker"
        frame:
            style "opcion_elegida"
            hbox:
                spacing 18
                frame:
                    style "letra"
                    text "ABC"[e.elegida] style "letra_texto"
                text e.opciones[e.elegida] style "opcion_texto" yalign 0.5
        frame:
            style "porque_marco"
            has vbox
            spacing 6
            text _("SEGÚN EL LIBRO") style "kicker"
            text what id "what" style "ficha_texto"
        text e.pagina style "pie"
```

- [ ] **Step 5: Ejecutar y ver que pasa**

Run: `./probar_juego.sh quiz && uv run pytest -q`
Expected: `Status: PASSED` y `38 passed`.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -q -m "feat: quiz con retroalimentación y aciertos del salón, decisiones según el libro" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 12: Nota de campo, idea clave, resumen, pausa y confirmación

**Files:**
- Create: `game/pantallas/notas.rpy`, `game/pantallas/pausa.rpy`
- Modify: `game/tests/escenas_prueba.rpy`, `game/tests/pruebas.rpy`

**Interfaces:**
- Produces:
  - Personajes `nota` (argumento `show_fuente`) y `clave`.
  - Pantallas `nota_campo`, `idea_clave`, `resumen()`, `fin()`, `pausa()` y `confirm(message, yes_action, no_action)`.
  - `_game_menu_screen = "pausa"`.

- [ ] **Step 1: Escribir la escena de prueba y los recorridos**

Añadir a `game/tests/escenas_prueba.rpy`:
```renpy
label prueba_cierre:
    $ abrir_capitulo("cap2")
    scene menu_fondo
    nota "Texto de una nota de campo de prueba." (show_fuente="Fuente de prueba") id prueba_nota
    clave "Idea clave de prueba." id prueba_clave
    return

label prueba_resumen:
    $ abrir_capitulo("final")
    scene menu_fondo
    show screen resumen
    n "Línea final de prueba." id prueba_06
    call screen fin
    hide screen resumen
    return
```
Añadir a `pruebas.rpy`:
```renpy
    testcase pausa:
        run Start("prueba_narracion")
        assert screen "bloque" timeout 5
        keysym "K_ESCAPE"
        assert screen "pausa" timeout 5
        click "Reducir movimiento"
        assert eval (persistent.reducir_movimiento)
        click "Reducir movimiento"
        assert eval (not persistent.reducir_movimiento)
        click "Continuar"
        assert screen "bloque" timeout 5

    testcase cierre:
        run Start("prueba_cierre")
        assert screen "nota_campo" timeout 5
        advance
        assert screen "idea_clave" timeout 5
        run Start("prueba_resumen")
        assert screen "resumen" timeout 10
        assert eval (aciertos == 0 and len(respondidas) == 0)
        advance until screen "fin" timeout 30
        click "Volver al menú"
        assert screen "main_menu" timeout 10
```
Run: `./probar_juego.sh pausa`
Expected: FAIL (no existe la pantalla `pausa`).

- [ ] **Step 2: Implementar notas, idea clave, resumen y fin**

`game/pantallas/notas.rpy`:
```renpy
## Nota de campo, idea clave y cierre (spec §2, §4.13).

define nota = Character(None, screen="nota_campo")
define clave = Character(None, screen="idea_clave")

screen nota_campo(who, what, fuente=""):
    key "r" action VoiceReplay()
    frame:
        style "bloque"
        xpos 1176
        ypos 64
        xsize 680
        has vbox
        spacing 12
        text _("NOTA DE CAMPO · CIENCIA ACTUAL") style "kicker"
        text what id "what" style "ficha_texto"
        if fuente:
            text _("Fuente: {}").format(fuente) style "leyenda"

screen idea_clave(who, what):
    add Solid("#F3ECDCB3")
    key "r" action VoiceReplay()
    frame:
        style "bloque"
        xalign 0.5
        yalign 0.5
        xsize 1240
        has vbox
        spacing 18
        text _("IDEA CLAVE · {}").format(kicker()) style "kicker" xalign 0.5
        text what id "what" style "titulo" text_align 0.5 xalign 0.5

screen resumen():
    frame:
        style "bloque"
        xpos 64
        ypos 64
        xsize 1000
        has vbox
        spacing 14
        text _("LO QUE APRENDIMOS") style "kicker"
        for cap in CAPITULOS:
            hbox:
                spacing 16
                text cap.numero style "kicker" min_width 190
                text cap.idea style "ficha_texto" xmaximum 740
        null height 6
        text _("Aciertos del salón: {} de {} preguntas respondidas").format(aciertos, len(respondidas)) style "subtitulo"

screen fin():
    vbox:
        xalign 0.5
        ypos 900
        spacing 16
        textbutton _("Créditos") action ShowMenu("creditos") style "boton_sec" xminimum 440
        textbutton _("Volver al menú") action Return() style "boton" xminimum 440
```

- [ ] **Step 3: Implementar pausa y confirmación**

`game/pantallas/pausa.rpy`:
```renpy
## Menú de pausa (Esc o clic derecho) y confirmaciones (spec §2).

define _game_menu_screen = "pausa"

style control_barra:
    ysize 22
    left_bar Solid(BOSQUE)
    right_bar Solid(PAPEL_2)
    thumb None

screen pausa():
    tag menu
    add Solid(VELO)
    frame:
        style "bloque"
        xalign 0.5
        yalign 0.5
        xsize 720
        has vbox
        spacing 14
        text _("PAUSA") style "kicker" xalign 0.5
        textbutton _("Continuar") action Return() style "boton" xfill True
        textbutton _("Capítulos") action ShowMenu("indice") style "boton_sec" xfill True
        textbutton (_("Voz: no") if preferences.get_mute("voice") else _("Voz: sí")) action Preference("voice mute", "toggle") style "boton_sec" xfill True
        hbox:
            spacing 20
            text _("Volumen de la voz") style "pie" yalign 0.5
            bar value Preference("voice volume") style "control_barra" xsize 380
        textbutton (_("Modo automático: sí") if preferences.afm_enable else _("Modo automático: no")) action Preference("auto-forward", "toggle") style "boton_sec" xfill True
        textbutton (_("Reducir movimiento: sí") if persistent.reducir_movimiento else _("Reducir movimiento: no")) action ToggleField(persistent, "reducir_movimiento") style "boton_sec" xfill True
        textbutton _("Menú principal") action MainMenu() style "boton_sec" xfill True
        textbutton _("Salir del juego") action Quit() style "boton_sec" xfill True

screen confirm(message, yes_action, no_action):
    modal True
    zorder 200
    add Solid(VELO)
    frame:
        style "bloque"
        xalign 0.5
        yalign 0.5
        xsize 760
        has vbox
        spacing 22
        text _(message) style "titulo" text_align 0.5 xalign 0.5
        hbox:
            xalign 0.5
            spacing 20
            textbutton _("Sí") action yes_action style "boton" xminimum 220
            textbutton _("No") action no_action style "boton_sec" xminimum 220
    key "game_menu" action no_action
```

- [ ] **Step 4: Ejecutar todos los recorridos**

Run: `./probar_juego.sh && uv run pytest -q`
Expected: `Status: PASSED` con `Test cases: 7 | 7 passed` y `38 passed`.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -q -m "feat: notas de campo, idea clave, resumen final, pausa y confirmación" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

**Sigue en** `docs/superpowers/plans/2026-10-13-novela-visual-parte3.md` (Tarea 13).
