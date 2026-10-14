# Interfaz neo-moderna: paneles oscuros translúcidos con acentos turquesa.

screen say(who, what):
    window:
        background Solid("#071522eF")
        xalign 0.5
        yalign 1.0
        xsize 900
        ysize 160
        padding (28, 18)
        vbox:
            spacing 8
            if who is not None:
                text who size 21 color "#a9d8d2"
            text what id "what" size 22 color "#f4f7fb" line_spacing 3

screen main_menu():
    tag menu
    add "images/bg_title.png"
    add Solid("#06111a44")
    frame:
        xalign 0.5
        yalign 0.23
        xsize 720
        background Solid("#071522d9")
        padding (34, 25)
        vbox:
            spacing 9
            text "LA FRAGILIDAD AMBIENTAL DE LA CULTURA" size 35 bold True color "#ffffff" xalign 0.5 text_align 0.5
            text "Historia, cultura y medio ambiente" size 19 color "#b9d9df" xalign 0.5
            text "Una experiencia narrativa interactiva" size 15 color "#8eb8c4" xalign 0.5
    vbox:
        xalign 0.5
        yalign 0.78
        spacing 12
        textbutton "COMENZAR  →" action Start():
            text_size 24
            text_color "#ffffff"
            text_hover_color "#ffffff"
            background Solid("#187f82")
            hover_background Solid("#24a4a1")
            xminimum 310
            xalign 0.5
            padding (26, 14)
        textbutton "SALIR" action Quit(confirm=True):
            text_size 18
            text_color "#e2edf2"
            text_hover_color "#ffffff"
            xalign 0.5

transform story_pan:
    xalign 0.5
    yalign 0.5
    zoom 1.0
    linear 10.0 zoom 1.045
    linear 10.0 zoom 1.0
    repeat

init python:
    def narration_finished():
        # Un valor distinto de None cierra la pantalla llamada.
        if not renpy.music.is_playing(channel="voice"):
            return True

# Tarjeta narrada: si existe el WAV, la voz arranca sola y la tarjeta
# avanza cuando termina. Sin WAV, se avanza con SALTAR.
screen mini_story(title, background, narration, voice_file):
    modal True
    default has_voice = renpy.loadable(voice_file)
    default voice_started = False
    add background at story_pan
    add Solid("#06111a22")

    if has_voice:
        on "show" action Play("voice", voice_file)
        # Espera inicial para no avanzar antes de que el canal de voz arranque.
        timer 0.45 action SetScreenVariable("voice_started", True)
        if voice_started:
            # La condición se evalúa en cada tick; un If() quedaría fijo al dibujar la pantalla.
            timer 0.2 repeat True action Function(narration_finished)

    frame:
        xalign 0.5
        yalign 0.965
        xsize 820
        background Solid("#071522F0")
        padding (18, 10)
        vbox:
            spacing 5
            text title size 20 color "#7fe0d4" bold True
            text narration size 17 color "#f4f7fb" line_spacing 1
            hbox:
                xfill True
                text "RELATO INTERACTIVO  ·  NARRACIÓN AUTOMÁTICA" size 11 color "#9bbbc7" yalign 0.5
                if has_voice:
                    textbutton "↻ REPETIR VOZ" action Play("voice", voice_file):
                        text_size 13
                        text_color "#ffffff"
                        background Solid("#285b68")
                        hover_background Solid("#187f82")
                        padding (9, 6)
                textbutton "SALTAR  →" action [Stop("voice"), Play("sound", "audio/sfx_ui.wav"), Return()] xalign 1.0:
                    text_size 16
                    text_color "#ffffff"
                    background Solid("#187f82")
                    hover_background Solid("#24a4a1")
                    padding (13, 7)

screen hud(level_name):
    frame:
        xalign 0.98
        yalign 0.03
        background Solid("#071522d9")
        padding (17, 10)
        hbox:
            spacing 22
            text "MISIÓN  ·  [level_name]" size 17 color "#ffffff"
            text "PUNTOS  [score]" size 17 color "#7fe0d4"

screen quiz_card(question, answers):
    modal True
    add "images/bg_village.png"
    add Solid("#06111acc")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 850
        background Solid("#0b2030f2")
        padding (32, 28)
        vbox:
            spacing 18
            text "DESAFÍO DE CONOCIMIENTO" size 22 color "#7fe0d4" xalign 0.5
            text question size 26 color "#ffffff" xalign 0.5 text_align 0.5
            for i, answer in enumerate(answers):
                textbutton answer action Return(i) xfill True:
                    text_size 21
                    text_color "#edf5f8"
                    text_hover_color "#ffffff"
                    background Solid("#18394a")
                    hover_background Solid("#187f82")
                    padding (18, 12)

screen end_card():
    modal True
    add "images/bg_victory.png"
    add Solid("#06111a55")
    frame:
        xalign 0.5
        yalign 0.22
        background Solid("#071522e8")
        padding (28, 22)
        vbox:
            spacing 12
            text "RECORRIDO COMPLETADO" size 35 color "#ffffff" xalign 0.5
            text "Has recorrido la Introducción y los tres primeros capítulos." size 20 color "#e0edf2" xalign 0.5
            text "Puntuación: [score] / 400" size 28 color "#7fe0d4" xalign 0.5
            text "Pistas utilizadas: [hints_used]" size 19 color "#c2d7df" xalign 0.5
            text "La historia humana también es una historia de relaciones con el ambiente." size 18 color "#f4f7fb" xalign 0.5 text_align 0.5
    textbutton "VOLVER A JUGAR" action Return() xalign 0.5 yalign 0.82:
        text_size 22
        text_color "#ffffff"
        text_hover_color "#ffffff"
        background Solid("#187f82")
        hover_background Solid("#24a4a1")
        padding (24, 14)
