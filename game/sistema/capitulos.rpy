## Partes de la presentación: quién presenta, páginas e ideas clave (spec §1–§3).

init -10 python:
    class Capitulo(object):
        def __init__(self, id, numero, titulo, presenta, paginas):
            self.id = id
            self.numero = numero        # "Introducción", "Capítulo 1"…
            self.titulo = titulo
            self.presenta = presenta
            self.paginas = paginas

        @property
        def etiqueta(self):
            """Indicador de los bloques: "Cap. 2 · Del Homo sapiens al Neolítico"."""
            if not self.numero.startswith("Capítulo"):
                return self.numero
            return "{} · {}".format(self.numero.replace("Capítulo", "Cap."), self.titulo)

        @property
        def idea(self):
            return IDEAS.get(self.id, "")

    # Deben coincidir letra por letra con las líneas `clave` de cada capítulo (lo vigila tests/test_guion.py).
    IDEAS = {
        "intro": "La historia humana no ocurre en un escenario vacío: sociedad, técnica y ecosistemas se transforman juntos.",
        "cap1": "Sin garras ni colmillos, los seres humanos se adaptaron mediante instrumentos y cooperación; al especializarse en la caza, empezaron a ejercer una presión importante sobre algunos ecosistemas.",
        "cap2": "Cada avance técnico transformó el medio, y cada cambio del medio obligó a reorganizar la sociedad.",
        "cap3": "Con la agricultura, las sociedades pusieron partes del ecosistema al servicio de la producción: ganaron autonomía, pero también alteraron las cadenas tróficas.",
    }

    CAPITULOS = [
        Capitulo("intro", "Introducción", "Historia y medio ambiente", "Elkin Samir Angulo Panameño", "pp. 6–9"),
        Capitulo("cap1", "Capítulo 1", "El lejano Paleolítico", "Sebastián Bolaños Morales", "pp. 10–12"),
        Capitulo("cap2", "Capítulo 2", "Del Homo sapiens al Neolítico", "María Fernanda Cano Cobo", "pp. 13–17"),
        Capitulo("cap3", "Capítulo 3", "El cercano Neolítico", "Javier Felipe Contreras Díaz", "pp. 18–27"),
    ]
    FINAL = Capitulo("final", "Reflexión final", "Del pasado al presente", "Todo el equipo", "p. 9")
    CAPITULO = {c.id: c for c in CAPITULOS + [FINAL]}

    REFERENCIAS_NOTAS = [
        "Neandertales erguidos: Smithsonian National Museum of Natural History, Human Origins Program, «Homo neanderthalensis».",
        "Homo sapiens de Jebel Irhoud: Hublin, J.-J. et al. (2017). Nature, 546, 289–292.",
        "Domesticación del maíz: Matsuoka, Y. et al. (2002). PNAS, 99(9), 6080–6084.",
    ]

    def abrir_capitulo(cap_id):
        """Marca la parte actual: la usan la portada y el indicador de los bloques."""
        store.capitulo_actual = cap_id
        store.pagina = CAPITULO[cap_id].paginas

default capitulo_actual = "intro"
default pagina = ""

label start:
    jump intro
