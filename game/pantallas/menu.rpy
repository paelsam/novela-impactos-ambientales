## Inicio, menú de momentos, créditos y portada de cada momento.

define CITA_CENTRAL = "“La cultura no solo vive dentro de la naturaleza: la transforma, y de nosotros depende que esa transformación no destruya lo que nos sostiene”"

screen teclas_voz():
    key "r" action VoiceReplay()
    key "a" action Preference("auto-forward", "toggle")

screen main_menu():
    tag menu
    add "menu_fondo" at paneo
    frame:
        style "lamina"
        xalign 0.5
        ypos 90
        xsize 1240
        at entrada(0.1)
        has vbox
        xfill True
        spacing 18
        text _("IMPACTOS AMBIENTALES · UNIVERSIDAD DEL VALLE") style "kicker" xalign 0.5
        text _("Del primer cultivo al último manglar") style "titulo_menu" xalign 0.5 text_align 0.5
        text CITA_CENTRAL style "cita" xalign 0.5 text_align 0.5
    vbox:
        xalign 0.5
        ypos 610
        spacing 16
        textbutton _("Comenzar") action Start() style "boton" xminimum 440 at entrada(0.3)
        textbutton _("Momentos") action ShowMenu("momentos") style "boton_sec" xminimum 440 at entrada(0.38)
        textbutton _("Créditos") action ShowMenu("creditos") style "boton_sec" xminimum 440 at entrada(0.46)
        textbutton _("Salir") action Quit(confirm=True) style "boton_sec" xminimum 440 at entrada(0.54)

## Los seis momentos: título arriba y, debajo, la idea central de cada uno.
screen momentos():
    tag menu
    add "menu_fondo" at paneo
    add Solid("#F3ECDCC7")
    text _("Momentos") style "titulo_portada" xpos 96 ypos 56 at entrada(0.0)
    text _("Del primer cultivo al último manglar") style "subtitulo" xpos 100 ypos 156 at entrada(0.05)
    grid 3 2:
        xpos 96
        ypos 206
        spacing 26
        for i, cap in enumerate(CAPITULOS):
            button:
                style "tarjeta"
                xsize 557
                ysize 360
                alt cap.titulo
                action Start("momento{}".format(i + 1))
                at entrada(0.12 + 0.07 * i), tarjeta_viva
                has vbox
                spacing 10
                text cap.numero.upper() style "kicker"
                text cap.titulo style "tarjeta_titulo"
                text cap.idea style "tarjeta_idea"
    textbutton _("← Volver") action Return() style "boton_sec" xpos 1824 xanchor 1.0 ypos 80

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
                text "{} · {}".format(cap.etiqueta, cap.presenta) style "credito"
            null height 16
            text _("Fuente") style "titulo"
            text _("Ángel Maya, A. (2015). La fragilidad ambiental de la cultura. Historia y medio ambiente (2.ª ed.). www.augustoangelmaya.com. Uso educativo sin ánimo de lucro, citando la fuente.") style "credito"
            null height 16
            text _("Ilustraciones") style "titulo"
            for atribucion, obra, fuente in CREDITOS_IMAGENES:
                text "{} — {}".format(atribucion, obra) style "credito"
            null height 16
            text _("Voz, tipografía y motor") style "titulo"
            text _("Narración sintética: Kokoro-82M (Apache-2.0), voz em_alex.") style "credito"
            text _("Tipografías: Literata y Atkinson Hyperlegible (SIL Open Font License 1.1); símbolos de DejaVu Sans.") style "credito"
            text _("Hecho con Ren'Py 8.5 (licencia MIT).") style "credito"
    textbutton _("← Volver") action Return() style "boton_sec" xpos 96 ypos 950

## Portada narrada: la voz lee el título; en pantalla se ve la composición.
define portada = Character(None, screen="portada")

screen portada(who, what):
    $ cap = CAPITULO[capitulo_actual]
    add Solid("#F3ECDCD9")
    use teclas_voz
    vbox:
        xalign 0.5
        yalign 0.45
        spacing 20
        text cap.numero.upper() style "kicker" xalign 0.5 at entrada(0.0)
        text cap.titulo style "titulo_portada" xalign 0.5 text_align 0.5 xmaximum 1500 at entrada(0.15, 30)
        add Solid(TINTA_2) xysize (180, 2) xalign 0.5 at entrada(0.3)
        text _("Presenta: {}").format(cap.presenta) style "subtitulo" xalign 0.5 at entrada(0.4)
    text what id "what" color "#00000000"
