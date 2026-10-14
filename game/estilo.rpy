## Sistema visual: paleta, tipografías, estilos y movimiento (spec §4).

define PAPEL = "#F3ECDC"
define PAPEL_2 = "#E9DFC8"
define TINTA = "#2A2722"
define TINTA_2 = "#5E574B"
define BOSQUE = "#2E4A3A"
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
