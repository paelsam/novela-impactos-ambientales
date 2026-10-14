## Bloque narrativo (spec §2, §4): tarjeta de papel abajo a la izquierda o panel lateral derecho.

define n = Character(None, screen="bloque", show_posicion="abajo")
define nl = Character(None, screen="bloque", show_posicion="lado")
define narrator = n

screen bloque(who, what, posicion="abajo"):
    $ prog = progreso(linea_actual())
    $ lateral = posicion == "lado"
    use teclas_voz
    frame:
        style "bloque"
        xpos (1136 if lateral else 64)
        ypos (64 if lateral else 1016)
        yanchor (0.0 if lateral else 1.0)
        xsize (720 if lateral else 800)
        has vbox
        spacing 12
        hbox:
            xfill True
            text kicker() style "kicker"
            if prog:
                text "{} / {}".format(prog[1], prog[2]) style "kicker" xalign 1.0
        text what id "what" style "narracion"
        if prog:
            bar value StaticValue(prog[1], prog[2]) style "progreso"
        hbox:
            xfill True
            text _("R · repetir voz    A · automático") style "pie"

screen say(who, what):
    use bloque(who, what)
