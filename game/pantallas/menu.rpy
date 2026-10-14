## Inicio, índice de capítulos, créditos y portada de cada parte (spec §2, §4).

screen teclas_voz():
    key "r" action VoiceReplay()
    key "a" action Preference("auto-forward", "toggle")

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
    use teclas_voz
    vbox:
        xalign 0.5
        yalign 0.45
        spacing 20
        text cap.numero.upper() style "kicker" xalign 0.5
        text cap.titulo style "titulo_portada" xalign 0.5 text_align 0.5
        text _("Presenta: {}").format(cap.presenta) style "subtitulo" xalign 0.5
        text cap.paginas style "pie" xalign 0.5
    text what id "what" color "#00000000"
