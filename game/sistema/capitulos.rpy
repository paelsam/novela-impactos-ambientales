## Los seis momentos de la presentación: quién presenta, título e idea central.

init -10 python:
    class Capitulo(object):
        """Un momento de la presentación (el nombre se conserva por compatibilidad con el resto del sistema)."""
        def __init__(self, id, numero, titulo, presenta):
            self.id = id
            self.numero = numero        # "Momento 1"…
            self.titulo = titulo
            self.presenta = presenta

        @property
        def etiqueta(self):
            """Indicador de los bloques: "Momento 3 · Cuando sobrevivir también transforma el entorno"."""
            return "{} · {}".format(self.numero, self.titulo)

        @property
        def idea(self):
            return IDEAS.get(self.id, "")

    # Las ideas con línea `clave` en su momento deben coincidir letra por letra (lo vigila tests/test_guion.py).
    IDEAS = {
        "m1": "La historia humana no ocurre en un escenario vacío: sociedad, técnica y ecosistemas se transforman juntos.",
        "m2": "Sin garras ni colmillos, los seres humanos persistieron gracias a sus instrumentos y a la cooperación, y empezaron a cambiar su relación con el ecosistema.",
        "m3": "Al perfeccionar la caza, los grupos humanos presionaron a otras especies: la intervención sobre la naturaleza tiene raíces en las primeras sociedades.",
        "m4": "Al asentarse junto al agua, las comunidades empezaron a intervenir de forma continua en su entorno.",
        "m5": "Con la agricultura, las sociedades pusieron partes del ecosistema al servicio de la producción: ganaron autonomía, pero alteraron las cadenas tróficas.",
        "m6": "Del primer cultivo al último manglar, lo que hoy decidimos sobre un territorio continúa esta historia.",
    }

    CAPITULOS = [
        Capitulo("m1", "Momento 1", "Una humanidad dentro del ecosistema", "Elkin Samir Angulo Panameño"),
        Capitulo("m2", "Momento 2", "Persistir y adaptarse", "Sebastián Bolaños Morales"),
        Capitulo("m3", "Momento 3", "Cuando sobrevivir también transforma el entorno", "María Fernanda Cano Cobo"),
        Capitulo("m4", "Momento 4", "Un cambio en la cultura", "Javier Felipe Contreras Díaz"),
        Capitulo("m5", "Momento 5", "La transformación de un paisaje", "Javier Felipe Contreras Díaz"),
        Capitulo("m6", "Momento 6", "Del pasado al presente", "Todo el equipo"),
    ]
    CAPITULO = {c.id: c for c in CAPITULOS}

    def abrir_capitulo(cap_id):
        """Marca el momento actual: lo usan la portada y el indicador de los bloques."""
        store.capitulo_actual = cap_id
        store.seccion = ""

default capitulo_actual = "m1"

label start:
    jump momento1
