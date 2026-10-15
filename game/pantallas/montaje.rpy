## Transiciones con imágenes: cada diapositiva entra con fundido, se ve unos segundos con su rótulo
## y pasa sola (un clic o → la adelanta). No llevan voz.

default diapositiva_texto = ""

label montaje(encabezado, diapositivas, duracion=3.0):
    $ i = 0
    while i < len(diapositivas):
        $ imagen, diapositiva_texto = diapositivas[i]
        scene expression imagen at paneo with fundido
        show screen rotulo(encabezado, diapositiva_texto)
        $ renpy.pause(duracion)
        $ i += 1
    hide screen rotulo
    return

screen rotulo(encabezado, texto):
    frame:
        style "lamina"
        xpos 64
        ypos 1016
        yanchor 1.0
        xmaximum 900
        padding (36, 26)
        at entrada(0.1)
        has vbox
        spacing 6
        text encabezado style "kicker"
        text texto style "rotulo_texto"
