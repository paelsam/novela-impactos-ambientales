## Capítulo 1 · El lejano Paleolítico · pp. 10–12 · Presenta Sebastián Bolaños Morales.
## Texto: guion del equipo. Fichas del mapa: redactadas a partir de la p. 12.
## Posiciones del mapa: ilustraciones.posicion_en_mapa(lon, lat, (-15, 20, 135, 75)).

define cap1_puntos_mapa = [
    Punto("china", 0.811, 0.638, "China: ciervos", "cap1_obs_china"),
    Punto("espana", 0.102, 0.583, "España: toros y caballos", "cap1_obs_espana"),
    Punto("rusia", 0.313, 0.450, "Rusia y Europa Central: mamuts", "cap1_obs_rusia"),
    Punto("francia", 0.139, 0.511, "Francia: renos", "cap1_obs_francia"),
]

label cap1:
    $ abrir_capitulo("cap1")
    play music "audio/ambiente/cueva.wav" fadein 2.0 if_changed
    scene cap1_fuego at paneo with fundido
    portada "Capítulo 1. El lejano Paleolítico. Veremos cómo las herramientas, la adaptación y la cooperación ampliaron la capacidad humana para sobrevivir y ejercer presión sobre otros seres vivos." id cap1_portada

    # Escena 1.1 · Antes de la historia
    $ pagina = "p. 10"
    n "Desde la perspectiva ambiental que presenta Ángel Maya, la historia comienza con el Homo sapiens. Antes de ese punto existe una zona ambigua entre la evolución biológica y la historia propiamente dicha." id cap1_01
    n "Los instrumentos rudimentarios, como los raspadores, aparecen en el registro del Pleistoceno. El libro menciona también la posibilidad de que el hombre de Pekín utilizara el fuego como defensa hace unos 500.000 años." id cap1_02
    n "Las herramientas y las pieles ayudaron a enfrentar condiciones ambientales que ya no resultaban propicias. La supervivencia empezó a depender también de recursos técnicos y de formas de adaptación cultural." id cap1_03
    $ pagina = "pp. 10–11"
    n "Al pasar de ambientes boscosos a espacios abiertos, los homínidos tuvieron que recorrer distancias y cooperar. Sin garras ni grandes colmillos, compensaron parte de sus limitaciones mediante instrumentos y organización." id cap1_04

    # Escena 1.2 · La caza, empresa colectiva
    play music "audio/ambiente/bosque.wav" fadein 2.0 if_changed
    scene cap1_caza at paneo with fundido
    $ pagina = "p. 11"
    n "Las primeras formas de depredación incluyeron animales pequeños y carroña. La dieta mixta dio a los grupos mayor autonomía frente a los recursos inmediatos del entorno." id cap1_05
    n "La caza de presas mayores era una empresa colectiva: requería instrumentos, organización y comunicación. Esa cooperación contribuyó a que los grupos pudieran extenderse fuera de regiones tropicales." id cap1_06
    n "La capacidad de cazar no dependía únicamente de la fuerza individual. El grupo compensaba la ausencia de garras o colmillos mediante la coordinación y el uso de herramientas." id cap1_07
    $ pagina = "p. 12"
    n "El libro describe una especialización regional de la caza: ciervos en China; toros y caballos en España; mamuts en Rusia y Europa Central; y renos en Francia." id cap1_08

    # Escena 1.3 · Mapa de la especialización
    scene cap1_mapa with transformacion
    n "Ángel Maya destaca la magnitud de algunos conjuntos de restos animales: cien mil caballos en Solutré y mil mamuts en Predmost. El autor interpreta esos casos como una presión insólita sobre los ecosistemas, que llega a llamar «una especie de ecocidio»." id cap1_09
    call explorar(cap1_puntos_mapa)

    scene cap1_caza at paneo with fundido
    menu (screen="quiz", quiz="cap1_quiz", pagina="p. 11"):
        pregunta "¿Por qué la caza, a diferencia de la primera depredación, exigió organización colectiva?" id cap1_quiz
        "Porque se hacía con instrumentos y no con garras o colmillos, y había que coordinar al grupo." (correcta=True):
            pass
        "Porque ya había cultivos que proteger.":
            pass
        "Porque las presas eran pequeñas y abundantes.":
            pass
    porque "Sin órganos especializados, el grupo compensaba con instrumentos, organización y comunicación. Cuanto mayor y más peligrosa era la presa, más coordinación exigía." id cap1_quiz_porque

    menu (screen="decision", pagina="p. 12"):
        dilema "Cada año, una gran manada de caballos pasa por el mismo valle. ¿Qué hace el grupo?" id cap1_dec
        "Cazar todos los que pueda.":
            segun "El libro presenta los restos de Solutré como señal de una caza selectiva de gran magnitud y de una presión creciente." id cap1_dec_a
        "Cazar solo lo necesario.":
            segun "Esta opción permite discutir el límite, pero el libro no describe cuotas de caza para este periodo; destaca la presión creciente sobre algunas especies." id cap1_dec_b
        "Seguir la manada a nuevas tierras.":
            segun "La extensión hacia nuevas zonas dio origen a culturas prehistóricas y llevó la presión a otros ecosistemas." id cap1_dec_c

    nota "El libro describe a los neandertales encorvados y arrastrando los pies. Esa imagen procede de una reconstrucción de 1911 hecha a partir de un esqueleto con artritis. Hoy se sabe que caminaban erguidos y fabricaban herramientas complejas." (show_fuente="Smithsonian, Human Origins Program") id cap1_nota
    clave "Sin garras ni colmillos, los seres humanos se adaptaron mediante instrumentos y cooperación; al especializarse en la caza, empezaron a ejercer una presión importante sobre algunos ecosistemas." id cap1_clave
    jump cap2

label cap1_obs_china:
    ficha "En la actual China, la caza se concentró en los ciervos. Cada región ofrecía presas distintas y, con ellas, técnicas distintas." (show_lamina="lamina_ciervo", show_titulo="China: ciervos", show_leyenda="Ciervo. Grabado de É. Bayard, 1870.", show_pagina="p. 12") id cap1_obs_china
    return

label cap1_obs_espana:
    ficha "En la península ibérica se cazaron toros y caballos. En cuevas como Altamira quedaron pintados grandes bóvidos." (show_lamina="lamina_bisonte", show_titulo="España: toros y caballos", show_leyenda="Bisonte de la cueva de Altamira (Cantabria).", show_pagina="p. 12") id cap1_obs_espana
    return

label cap1_obs_rusia:
    ficha "En Rusia y Europa Central, el mamut fue la gran presa. En Predmost se hallaron restos de mil mamuts." (show_lamina="lamina_mamut", show_titulo="Rusia y Europa Central: mamuts", show_leyenda="Mamut lanudo. Grabado de É. Riou, 1863.", show_pagina="p. 12") id cap1_obs_rusia
    return

label cap1_obs_francia:
    ficha "En el actual territorio de Francia predominó la caza del reno. Este grabado de 1870 imagina a uno de esos cazadores." (show_lamina="lamina_reno", show_titulo="Francia: renos", show_leyenda="Cazador de la época del reno. Grabado de É. Bayard, 1870.", show_pagina="p. 12") id cap1_obs_francia
    return
