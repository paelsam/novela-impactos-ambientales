## Aciertos del salón y estado de la última respuesta (spec §2, §7).

init -10 python:
    class EstadoRespuesta(object):
        def __init__(self, opciones, elegida, correcta):
            self.pregunta = store._last_say_what or ""   # la pregunta o el dilema que acaba de sonar
            self.opciones = opciones
            self.elegida = elegida
            self.correcta = correcta

        @property
        def acerto(self):
            return self.elegida == self.correcta

    def responder_quiz(quiz, opciones, elegida, correcta):
        """Guarda la respuesta; solo el primer intento de cada quiz cuenta para los aciertos."""
        if correcta is None:
            raise Exception("El quiz «{}» no marca ninguna opción con (correcta=True).".format(quiz))
        store.estado_quiz = EstadoRespuesta(opciones, elegida, correcta)
        if quiz not in store.respondidas:
            store.respondidas[quiz] = elegida == correcta
            if elegida == correcta:
                store.aciertos += 1
        renpy.sound.play("audio/sfx/acierto.wav" if elegida == correcta else "audio/sfx/error.wav")

    def elegir_decision(opciones, elegida):
        store.estado_decision = EstadoRespuesta(opciones, elegida, None)

default aciertos = 0
default respondidas = {}
default estado_quiz = None
default estado_decision = None
