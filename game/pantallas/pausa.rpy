## Menú de pausa (Esc o clic derecho) y confirmaciones (spec §2).

define _game_menu_screen = "pausa"

style control_barra:
    ysize 28
    left_bar Solid(BOSQUE)
    right_bar Solid("#CFC3A6")
    thumb "gui/insignia_vista.png"
    thumb_offset 14

screen pausa():
    tag menu
    add Solid(VELO)
    frame:
        style "lamina"
        xalign 0.5
        yalign 0.5
        xsize 820
        at entrada(0.0)
        has vbox
        xfill True
        spacing 14
        text _("❦  PAUSA") style "kicker" xalign 0.5
        textbutton _("Continuar") action Return() style "boton" xfill True
        textbutton _("Momentos") action ShowMenu("momentos") style "boton_sec" xfill True
        use controles_sonido
        textbutton _("Menú principal") action MainMenu() style "boton_sec" xfill True
        textbutton _("Salir del juego") action Quit() style "boton_sec" xfill True

## Opciones desde el menú principal: los mismos controles que la pausa.
screen opciones():
    tag menu
    add "menu_fondo" at paneo
    add Solid("#F3ECDCC7")
    frame:
        style "lamina"
        xalign 0.5
        yalign 0.5
        xsize 820
        at entrada(0.0)
        has vbox
        xfill True
        spacing 14
        text _("❦  OPCIONES") style "kicker" xalign 0.5
        use controles_sonido
        textbutton _("← Volver") action Return() style "boton" xfill True

## Volumen de voz, música y ambiente, y preferencias de la presentación.
screen controles_sonido():
    grid 2 3:
        xfill True
        spacing 14
        text _("Voz") style "pie" yalign 0.5
        bar value Preference("voice volume") style "control_barra" xsize 520 xalign 1.0
        text _("Música") style "pie" yalign 0.5
        bar value Preference("music volume") style "control_barra" xsize 520 xalign 1.0
        text _("Ambiente y efectos") style "pie" yalign 0.5
        bar value Preference("sound volume") style "control_barra" xsize 520 xalign 1.0
    textbutton (_("Voz: no") if preferences.get_mute("voice") else _("Voz: sí")) action Preference("voice mute", "toggle") style "boton_sec" xfill True
    textbutton (_("Modo automático: sí") if preferences.afm_enable else _("Modo automático: no")) action Preference("auto-forward", "toggle") style "boton_sec" xfill True
    textbutton (_("Reducir movimiento: sí") if persistent.reducir_movimiento else _("Reducir movimiento: no")) action ToggleField(persistent, "reducir_movimiento") style "boton_sec" xfill True

screen confirm(message, yes_action, no_action):
    modal True
    zorder 200
    add Solid(VELO)
    frame:
        style "bloque"
        xalign 0.5
        yalign 0.5
        xsize 760
        has vbox
        xfill True
        spacing 22
        text _(message) style "titulo" text_align 0.5 xalign 0.5
        hbox:
            xalign 0.5
            spacing 20
            textbutton _("Sí") action yes_action style "boton" xminimum 220
            textbutton _("No") action no_action style "boton_sec" xminimum 220
    key "game_menu" action no_action
