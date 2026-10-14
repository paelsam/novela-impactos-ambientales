## Aciertos del salón y estado de la última respuesta (spec §2, §7).

init -10 python:
    class EstadoRespuesta(object):
        def __init__(self, opciones, elegida, correcta, pagina):
            self.opciones = opciones
            self.elegida = elegida
            self.correcta = correcta
            self.pagina = pagina

        @property
        def acerto(self):
            return self.elegida == self.correcta

    def responder_quiz(quiz, opciones, elegida, correcta, pagina):
        """Guarda la respuesta; solo el primer intento de cada quiz cuenta para los aciertos."""
        if correcta is None:
            raise Exception("El quiz «{}» no marca ninguna opción con (correcta=True).".format(quiz))
        store.estado_quiz = EstadoRespuesta(opciones, elegida, correcta, pagina)
        if quiz not in store.respondidas:
            store.respondidas[quiz] = elegida == correcta
            if elegida == correcta:
                store.aciertos += 1
        renpy.sound.play("audio/sfx/acierto.wav" if elegida == correcta else "audio/sfx/error.wav")

    def elegir_decision(opciones, elegida, pagina):
        store.estado_decision = EstadoRespuesta(opciones, elegida, None, pagina)

default aciertos = 0
default respondidas = {}
default estado_quiz = None
default estado_decision = None
