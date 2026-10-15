## Menú de pausa (Esc o clic derecho) y confirmaciones (spec §2).

define _game_menu_screen = "pausa"

style control_barra:
    ysize 22
    left_bar Solid(BOSQUE)
    right_bar Solid(PAPEL_2)
    thumb None

screen pausa():
    tag menu
    add Solid(VELO)
    frame:
        style "bloque"
        xalign 0.5
        yalign 0.5
        xsize 720
        has vbox
        xfill True
        spacing 14
        text _("PAUSA") style "kicker" xalign 0.5
        textbutton _("Continuar") action Return() style "boton" xfill True
        textbutton _("Momentos") action ShowMenu("momentos") style "boton_sec" xfill True
        textbutton (_("Voz: no") if preferences.get_mute("voice") else _("Voz: sí")) action Preference("voice mute", "toggle") style "boton_sec" xfill True
        hbox:
            spacing 20
            text _("Volumen de la voz") style "pie" yalign 0.5
            bar value Preference("voice volume") style "control_barra" xsize 380
        textbutton (_("Modo automático: sí") if preferences.afm_enable else _("Modo automático: no")) action Preference("auto-forward", "toggle") style "boton_sec" xfill True
        textbutton (_("Reducir movimiento: sí") if persistent.reducir_movimiento else _("Reducir movimiento: no")) action ToggleField(persistent, "reducir_movimiento") style "boton_sec" xfill True
        textbutton _("Menú principal") action MainMenu() style "boton_sec" xfill True
        textbutton _("Salir del juego") action Quit() style "boton_sec" xfill True

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
