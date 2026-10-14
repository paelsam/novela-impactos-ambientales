## Voz automática y progreso de cada línea (spec §6, §7).

default seccion = ""

init -10 python:
    import re

    _BLOQUE = re.compile(r"^(?P<parte>[a-z]+[0-9]?)_(?P<n>[0-9]{2})$")

    def voz_de(tlid):
        """Voz de una línea: la grabación propia si existe; si no, la voz sintética."""
        grabada = "audio/voz/grabadas/{}.ogg".format(tlid)
        if renpy.loadable(grabada):
            return grabada
        return "audio/voz/{}.ogg".format(tlid)

    def progreso(tlid):
        """("cap2", 3, 10) para la línea cap2_03, o None si no es un bloque narrativo."""
        m = _BLOQUE.match(tlid or "")
        if not m:
            return None
        return m.group("parte"), int(m.group("n")), TOTAL_BLOQUES.get(m.group("parte"), 0)

    def kicker():
        cap = CAPITULO.get(store.capitulo_actual)
        if not cap:
            return ""
        texto = cap.etiqueta + (" · " + store.seccion if store.seccion else "")
        return texto.upper()

    def linea_actual():
        return renpy.game.context().translate_identifier

init 999 python:
    # Bloques narrativos de cada parte, contados a partir de los id del guion.
    TOTAL_BLOQUES = {}
    for _tlid in renpy.game.script.translator.default_translates:
        _m = _BLOQUE.match(_tlid)
        if _m:
            TOTAL_BLOQUES[_m.group("parte")] = TOTAL_BLOQUES.get(_m.group("parte"), 0) + 1

define config.auto_voice = voz_de
define config.default_afm_time = 1
define config.afm_voice_delay = 0.6
