## Quiz, decisión y retroalimentación: una sola lámina que se ajusta a su contenido.

define pregunta = Character(None, screen="pregunta")
define dilema = Character(None, screen="pregunta")
define porque = Character(None, screen="retroalimentacion")
define segun = Character(None, screen="segun")

define VELO_SEPIA = "#1B160DB8"

style opcion:
    background Frame("gui/opcion.png", 14, 14)
    hover_background Frame("gui/opcion_hover.png", 14, 14)
    padding (20, 14)
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
    background "gui/letra.png"
    xysize (44, 44)

style letra_bien is letra:
    background "gui/letra_bien.png"

style letra_mal is letra:
    background "gui/letra_mal.png"

style letra_texto:
    font SANS_NEGRITA
    size 22
    color TINTA
    xalign 0.5
    yalign 0.5

style letra_marcada is letra_texto:
    color PAPEL

style pregunta_texto:
    font SERIF_SEMI
    size 38
    line_spacing 8
    color TINTA

style resultado_bien:
    font SERIF_SEMI_SIMBOLOS
    size 38
    color CORRECTA

style resultado_mal is resultado_bien:
    color INCORRECTA

style estado_bien:
    font SANS_NEGRITA
    size 20
    color CORRECTA

style estado_mal is estado_bien:
    color INCORRECTA

style porque_marco:
    background Frame("gui/filete.png", 8, 0, 0, 0)
    left_padding 22

transform opcion_viva:
    on idle:
        easein 0.15 xoffset 0
    on hover:
        easein 0.15 xoffset 8

transform apagada:
    alpha 0.5

## La pregunta suena con su voz; el texto se dibuja dentro de la lámina del quiz.
screen pregunta(who, what):
    use teclas_voz
    text what id "what" color "#00000000" size 18

screen lamina_pregunta(etiqueta, texto):
    text etiqueta style "kicker"
    text texto style "pregunta_texto"
    add Solid("#B7A882") xysize (1104, 2)

screen quiz(items, quiz):
    use teclas_voz
    add Solid(VELO_SEPIA)
    $ opciones = [i.caption for i in items]
    $ correcta = next((n for n, i in enumerate(items) if i.kwargs.get("correcta")), None)
    $ acciones = [[Function(responder_quiz, quiz, opciones, n, correcta), item.action] for n, item in enumerate(items)]
    frame:
        style "lamina"
        xalign 0.5
        yalign 0.5
        xsize 1200
        at entrada(0.0)
        has vbox
        xfill True
        spacing 18
        hbox:
            xfill True
            text _("❦  PREGUNTA") style "kicker"
            text _("ACIERTOS DEL SALÓN: {} DE {}").format(aciertos, len(respondidas)) style "kicker" xalign 1.0
        use lamina_pregunta(kicker(), _last_say_what or "")
        use lista_opciones(items, acciones)

screen decision(items):
    use teclas_voz
    add Solid(VELO_SEPIA)
    $ opciones = [i.caption for i in items]
    $ acciones = [[Function(elegir_decision, opciones, n), item.action] for n, item in enumerate(items)]
    frame:
        style "lamina"
        xalign 0.5
        yalign 0.5
        xsize 1200
        at entrada(0.0)
        has vbox
        xfill True
        spacing 18
        text _("❦  DECISIÓN") style "kicker"
        use lamina_pregunta(kicker(), _last_say_what or "")
        use lista_opciones(items, acciones)

screen choice(items):
    use decision(items)

screen lista_opciones(items, acciones):
    vbox:
        xfill True
        spacing 14
        for n, item in enumerate(items):
            button:
                style "opcion"
                action acciones[n]
                at entrada(0.2 + 0.08 * n), opcion_viva
                hbox:
                    spacing 18
                    frame:
                        style "letra"
                        text "ABC"[n] style "letra_texto"
                    text item.caption style "opcion_texto" yalign 0.5
            key "K_{}".format(n + 1) action acciones[n]

screen tarjeta_explicacion(etiqueta, what):
    frame:
        style "porque_marco"
        at entrada(0.35)
        has vbox
        spacing 6
        text etiqueta style "kicker"
        text what id "what" style "ficha_texto"

## Retroalimentación del quiz: la opción elegida mal se marca en rojo con ✗ y la correcta en verde con ✓.
screen retroalimentacion(who, what):
    $ e = estado_quiz
    add Solid(VELO_SEPIA)
    use teclas_voz
    frame:
        style "lamina"
        xalign 0.5
        yalign 0.5
        xsize 1200
        has vbox
        xfill True
        spacing 16
        hbox:
            xfill True
            text (_("✓  ¡Correcto!") if e.acerto else _("✗  No es así")) style ("resultado_bien" if e.acerto else "resultado_mal") at entrada(0.0, 10)
            text _("ACIERTOS DEL SALÓN: {} DE {}").format(aciertos, len(respondidas)) style "kicker" xalign 1.0 yalign 0.5
        text e.pregunta style "ficha_texto"
        for n, opcion in enumerate(e.opciones):
            if n == e.correcta:
                frame:
                    style "opcion_bien"
                    hbox:
                        spacing 18
                        frame:
                            style "letra_bien"
                            text "✓" style "letra_marcada"
                        text opcion style "opcion_texto" yalign 0.5 xmaximum 800
                        text _("CORRECTA") style "estado_bien" yalign 0.5
            elif n == e.elegida:
                frame:
                    style "opcion_mal"
                    at sacudida
                    hbox:
                        spacing 18
                        frame:
                            style "letra_mal"
                            text "✗" style "letra_marcada"
                        text opcion style "opcion_texto" yalign 0.5 xmaximum 800
                        text _("TU RESPUESTA") style "estado_mal" yalign 0.5
            else:
                frame:
                    style "opcion"
                    at apagada
                    hbox:
                        spacing 18
                        frame:
                            style "letra"
                            text "ABC"[n] style "letra_texto"
                        text opcion style "opcion_texto" yalign 0.5 xmaximum 800
        use tarjeta_explicacion(_("POR QUÉ"), what)

## Explicación de la decisión: no hay opción correcta, se muestra lo que ocurrió.
screen segun(who, what):
    $ e = estado_decision
    add Solid(VELO_SEPIA)
    use teclas_voz
    frame:
        style "lamina"
        xalign 0.5
        yalign 0.5
        xsize 1200
        has vbox
        xfill True
        spacing 16
        text _("❦  DECISIÓN · {}").format(kicker()) style "kicker"
        text e.pregunta style "ficha_texto"
        frame:
            style "opcion_elegida"
            hbox:
                spacing 18
                frame:
                    style "letra"
                    text "ABC"[e.elegida] style "letra_texto"
                text e.opciones[e.elegida] style "opcion_texto" yalign 0.5 xmaximum 820
                text _("TU DECISIÓN") style "estado_bien" yalign 0.5
        use tarjeta_explicacion(_("LO QUE MUESTRA LA HISTORIA"), what)
