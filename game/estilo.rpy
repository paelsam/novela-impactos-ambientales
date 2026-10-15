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
define SERIF_SEMI_SIMBOLOS = FontGroup().add("DejaVuSans-Bold.ttf", 0x2190, 0x22FF).add("DejaVuSans-Bold.ttf", 0x25A0, 0x27BF).add("fonts/Literata-SemiBold.ttf", 0x0000, 0xFFFF)
define SERIF_CURSIVA = "fonts/Literata-Italic.ttf"
define SANS = FontGroup().add("DejaVuSans.ttf", 0x2190, 0x22FF).add("DejaVuSans.ttf", 0x25A0, 0x27BF).add("fonts/AtkinsonHyperlegible-Regular.ttf", 0x0000, 0xFFFF)
define SANS_NEGRITA = FontGroup().add("DejaVuSans-Bold.ttf", 0x2190, 0x22FF).add("DejaVuSans-Bold.ttf", 0x25A0, 0x27BF).add("fonts/AtkinsonHyperlegible-Bold.ttf", 0x0000, 0xFFFF)

style default:
    font SERIF
    size 34
    color TINTA
    language "unicode"
    activate_sound "audio/sfx/clic.wav"

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

style titulo_menu is titulo:
    size 64

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
    background Frame("gui/marco_grabado.png", 22, 22)
    hover_background Frame("gui/marco_grabado_hover.png", 22, 22)
    padding (34, 30)

style tarjeta_titulo:
    font SERIF_SEMI
    size 32
    line_spacing 4
    color TINTA

style tarjeta_idea:
    font SERIF_CURSIVA
    size 22
    line_spacing 6
    color TINTA_2

## Marco de lámina antigua (doble filete) para portadas, quiz, idea clave y cierre.
style lamina:
    background Frame("gui/marco_grabado.png", 22, 22)
    padding (48, 40)

style cita:
    font SERIF_CURSIVA
    size 30
    line_spacing 8
    color TINTA_2

style cita_final is cita:
    size 40
    line_spacing 12
    color TINTA

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

style marca:
    background "gui/marca.png"
    hover_background "gui/marca_hover.png"
    selected_background "gui/marca_vista.png"
    selected_hover_background "gui/marca_hover.png"
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


style vscrollbar:
    xsize 12
    base_bar Solid(PAPEL_2)
    thumb Solid(BOSQUE)
    unscrollable "hide"

## Animación: entradas suaves de tarjetas y láminas (se apagan con "Reducir movimiento").
transform entrada(retraso=0.0, desde=18):
    on show, replace:
        alpha (1.0 if persistent.reducir_movimiento else 0.0)
        yoffset (0 if persistent.reducir_movimiento else desde)
        pause (0.0 if persistent.reducir_movimiento else retraso)
        easein (0.01 if persistent.reducir_movimiento else 0.5) alpha 1.0 yoffset 0

transform tarjeta_viva:
    on idle:
        easein 0.18 yoffset 0
    on hover:
        easein 0.18 yoffset -8

transform sacudida:
    on show:
        xoffset 0
        linear 0.06 xoffset (0 if persistent.reducir_movimiento else -10)
        linear 0.06 xoffset (0 if persistent.reducir_movimiento else 10)
        linear 0.06 xoffset (0 if persistent.reducir_movimiento else -6)
        linear 0.06 xoffset 0

## Lámina montada sobre cartón, para las composiciones de varias láminas (collages).
init python:
    def montada(imagen, ancho, alto, leyenda="", borde=14):
        """Lámina sobre cartón con filete, y su leyenda debajo."""
        interior = Fixed(Solid("#FBF7EE"), Transform(imagen, xysize=(ancho, alto), xpos=borde - 2, ypos=borde - 2),
                         xpos=2, ypos=2, xysize=(ancho + 2 * borde - 4, alto + 2 * borde - 4))
        carton = Fixed(Solid("#B7A882"), interior, xysize=(ancho + 2 * borde, alto + 2 * borde))
        if not leyenda:
            return carton
        return VBox(carton, Text(leyenda, style="leyenda", xmaximum=ancho + 2 * borde), spacing=8)

transform pieza_collage(x, y, angulo=0.0, retraso=0.0):
    pos (x, y)
    rotate angulo
    rotate_pad False
    alpha (1.0 if persistent.reducir_movimiento else 0.0)
    yoffset (0 if persistent.reducir_movimiento else 40)
    pause (0.0 if persistent.reducir_movimiento else retraso)
    easein (0.01 if persistent.reducir_movimiento else 0.9) alpha 1.0 yoffset 0
