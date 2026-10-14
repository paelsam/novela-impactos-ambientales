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

screen lista_opciones(items, acciones):
    vbox:
        xalign 0.5
        ypos 340
        xsize 1052
        spacing 14
        for n, item in enumerate(items):
            $ accion = acciones[n]
            button:
                style "opcion"
                action accion
                hbox:
                    spacing 18
                    frame:
                        style "letra"
                        text "ABC"[n] style "letra_texto"
                    text item.caption style "opcion_texto" yalign 0.5
            key "K_{}".format(n + 1) action accion

screen quiz(items, quiz, pagina=""):
    use teclas_voz
    $ opciones = [i.caption for i in items]
    $ correcta = next((n for n, i in enumerate(items) if i.kwargs.get("correcta")), None)
    $ acciones = [[Function(responder_quiz, quiz, opciones, n, correcta, pagina), item.action] for n, item in enumerate(items)]
    use lista_opciones(items, acciones)

screen decision(items, pagina=""):
    use teclas_voz
    $ opciones = [i.caption for i in items]
    $ acciones = [[Function(elegir_decision, opciones, n, pagina), item.action] for n, item in enumerate(items)]
    use lista_opciones(items, acciones)

screen choice(items):
    use decision(items)

screen tarjeta_explicacion(etiqueta, what, pagina):
    frame:
        style "porque_marco"
        has vbox
        spacing 6
        text etiqueta style "kicker"
        text what id "what" style "ficha_texto"

screen retroalimentacion(who, what):
    $ e = estado_quiz
    add Solid(VELO)
    use teclas_voz
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
        use tarjeta_explicacion(_("POR QUÉ"), what, e.pagina)

screen segun(who, what):
    $ e = estado_decision
    add Solid(VELO)
    use teclas_voz
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
        use tarjeta_explicacion(_("SEGÚN EL LIBRO"), what, e.pagina)
