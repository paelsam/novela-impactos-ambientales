## Nota de campo, idea clave y cierre (spec §2, §4.13).

define nota = Character(None, screen="nota_campo")
define clave = Character(None, screen="idea_clave")

screen nota_campo(who, what, fuente=""):
    use teclas_voz
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
    use teclas_voz
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
                text cap.numero.upper() style "kicker" min_width 190
                text cap.idea style "ficha_texto" xmaximum 740
        null height 6
        text _("Aciertos del salón: {} de {} preguntas respondidas").format(aciertos, len(respondidas)) style "subtitulo"

screen fin():
    vbox:
        xalign 0.5
        ypos 1016
        yanchor 1.0
        spacing 16
        textbutton _("Créditos") action ShowMenu("creditos") style "boton_sec" xminimum 440
        textbutton _("Volver al menú") action Return() style "boton" xminimum 440
