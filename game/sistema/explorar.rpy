## Exploración del paisaje: puntos observables y sus fichas (spec §2, §7).

init -10 python:
    class Punto(object):
        """Elemento observable: posición relativa (0–1), etiqueta y label con su ficha."""
        def __init__(self, id, x, y, etiqueta, label):
            self.id = id
            self.x = x
            self.y = y
            self.etiqueta = etiqueta
            self.label = label

default vistos = set()
default puntos_escena = []
default punto_activo = None

label explorar(puntos):
    $ puntos_escena = puntos
    while True:
        $ punto_activo = renpy.call_screen("explorar", puntos=puntos)
        if not isinstance(punto_activo, Punto):
            return
        $ vistos.add(punto_activo.id)
        call expression punto_activo.label
