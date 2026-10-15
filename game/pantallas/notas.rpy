## Idea central de cada momento y cierre de la presentación.

define clave = Character(None, screen="idea_clave")

screen idea_clave(who, what):
    add Solid("#F3ECDCB3")
    use teclas_voz
    frame:
        style "lamina"
        xalign 0.5
        yalign 0.5
        xsize 1240
        at entrada(0.0, 24)
        has vbox
        xfill True
        spacing 20
        text _("❦  IDEA CENTRAL · {}").format(kicker()) style "kicker" xalign 0.5
        text what id "what" style "titulo" text_align 0.5 xalign 0.5

## Cierre: la frase central de todo el recorrido sobre el manglar, y la salida.
screen fin():
    add Solid("#1B160D80")
    frame:
        style "lamina"
        xalign 0.5
        yalign 0.42
        xsize 1300
        at entrada(0.2, 30)
        has vbox
        xfill True
        spacing 22
        text _("DEL PRIMER CULTIVO AL ÚLTIMO MANGLAR") style "kicker" xalign 0.5
        text CITA_CENTRAL style "cita_final" xalign 0.5 text_align 0.5
        text _("Aciertos del salón: {} de {} preguntas").format(aciertos, len(respondidas)) style "pie" xalign 0.5
    hbox:
        xalign 0.5
        ypos 1016
        yanchor 1.0
        spacing 24
        at entrada(0.8)
        textbutton _("Créditos") action ShowMenu("creditos") style "boton_sec" xminimum 360
        textbutton _("Volver al menú") action Return() style "boton" xminimum 360
