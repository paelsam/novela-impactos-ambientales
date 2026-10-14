## Marcadores sobre el paisaje y ficha de observación (spec §2, §4.6–7).

screen explorar(puntos):
    default foco = None
    for i, p in enumerate(puntos):
        button:
            style "marca"
            pos (p.x, p.y)
            anchor (0.5, 0.5)
            selected p.id in vistos
            alt p.etiqueta
            action Return(p)
            hovered SetScreenVariable("foco", i)
            unhovered SetScreenVariable("foco", None)
            text str(i + 1) style "marca_num"
        if p.id in vistos:
            add "gui/insignia_vista.png" pos (p.x, p.y) xoffset 14 yoffset -42
            text "✓" font "DejaVuSans-Bold.ttf" size 18 color "#FFFFFF" pos (p.x, p.y) xoffset 21 yoffset -40
        key "K_{}".format(i + 1) action Return(p)
    if foco is not None:
        frame:
            style "marca_etiqueta"
            pos (puntos[foco].x, puntos[foco].y)
            xoffset 40
            yanchor 0.5
            text puntos[foco].etiqueta.upper() style "kicker"
    frame:
        style "bloque"
        xpos 64
        ypos 1016
        yanchor 1.0
        xsize 800
        hbox:
            xfill True
            text _("Explora el paisaje: elige un punto (1–{})").format(len(puntos)) style "pie" yalign 0.5
            textbutton _("Continuar →") action Return(None) style "boton" xalign 1.0
    key "K_PAGEDOWN" action Return(None)

define ficha = Character(None, screen="ficha")

screen ficha(who, what, lamina=None, titulo="", leyenda="", pagina=""):
    $ p = punto_activo
    $ px = int(p.x * 1920)
    $ py = int(p.y * 1080)
    $ derecha = px < 960                       # la ficha va en la mitad opuesta al punto
    $ fx = 1236 if derecha else 64
    $ borde = fx if derecha else fx + 620
    $ numero = next((i + 1 for i, q in enumerate(puntos_escena) if q.id == p.id), 1)
    use teclas_voz
    key "dismiss" action Return()
    for i, q in enumerate(puntos_escena):
        add ("gui/marca_hover.png" if q.id == p.id else ("gui/marca_vista.png" if q.id in vistos else "gui/marca.png")):
            pos (q.x, q.y)
            anchor (0.5, 0.5)
        text str(i + 1) style "marca_num" pos (q.x, q.y) anchor (0.5, 0.5)
    # Línea guía en ángulo: sale de la ficha a la altura del título y baja hasta el punto.
    add Solid(PAPEL) xpos min(borde, px) ypos 150 xsize abs(px - borde) ysize 3
    add Solid(PAPEL) xpos px - 1 ypos 150 xsize 3 ysize max(0, py - 150 - 32)
    frame:
        style "bloque"
        xpos fx
        ypos 48
        xsize 620
        has vbox
        xfill True
        spacing 10
        hbox:
            xfill True
            text _("OBSERVACIÓN {} DE {}").format(numero, len(puntos_escena)) style "kicker"
        if lamina:
            add lamina xysize (552, 220) fit "contain" xalign 0.5
            text leyenda style "leyenda"
        text titulo style "titulo"
        text what id "what" style "ficha_texto"
        hbox:
            xfill True
            text _("R · repetir voz") style "pie" yalign 0.5
            textbutton _("← Volver al paisaje") action Return() style "boton_sec" xalign 1.0
