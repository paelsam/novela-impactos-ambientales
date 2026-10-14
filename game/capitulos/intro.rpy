## Introducción · pp. 6–9 · Presenta Elkin Samir Angulo Panameño.
## Texto: guion del equipo. Fichas: descripciones del guion para cada punto.

define intro_puntos_venecia = [
    Punto("palacio", 0.34, 0.37, "Palacio Ducal y San Marcos", "intro_obs_palacio"),
    Punto("barcos", 0.57, 0.52, "Barcos y mercancías", "intro_obs_barcos"),
    Punto("laguna", 0.78, 0.84, "La laguna", "intro_obs_laguna"),
]

label intro:
    $ abrir_capitulo("intro")
    play music "audio/ambiente/rio.wav" fadein 2.0 if_changed
    scene intro_venecia at paneo with fundido
    portada "Introducción: Los orígenes, del ecosistema a la cultura. En esta parte veremos por qué la historia humana no puede comprenderse sin considerar la relación entre sociedad, tecnología y ecosistemas." id intro_portada

    # Escena I1 · La historia vista desde arriba
    $ pagina = "p. 6"
    n "La dimensión ambiental apenas empieza a incorporarse a los métodos con los que estudiamos la historia. Mirar el pasado exige preguntarse no solo qué hicieron las personas, sino también en qué condiciones vivían." id intro_01
    n "Cada época interpreta el pasado desde las ideas de su propio tiempo. Ángel Maya recuerda que Tito Livio estudiaba la historia antigua buscando comprender los males de su presente." id intro_02
    $ pagina = "p. 8"
    n "Durante mucho tiempo, la historia se narró desde la cúspide: caudillos, gobernantes y clases dirigentes ocupaban el centro del relato, mientras otras condiciones quedaban en segundo plano." id intro_03
    n "El ejemplo de Venecia lo muestra con claridad: Sabellicus narró su historia sin mencionar el comercio de la sal, aunque ese recurso ayudaba a sostener su poder." id intro_04
    call explorar(intro_puntos_venecia)

    # Escena I2 · Testimonios mudos
    stop music fadeout 2.0
    scene intro_herramientas at paneo with fundido
    nl "Los hallazgos arqueológicos añadieron otra clase de evidencia: herramientas y objetos que permiten reconstruir aspectos de la vida de sociedades que no dejaron relatos escritos." id intro_05
    nl "Ángel Maya llama a estos objetos «testimonios mudos de la historia». Su presencia ayuda a estudiar cómo las sociedades desarrollaron técnicas para relacionarse con el entorno." id intro_06
    scene intro_pulido at paneo with fundido
    nl "La tesis que guía el libro es que la organización social está íntimamente vinculada a la transformación tecnológica de los ecosistemas. Sociedad, técnica y naturaleza no son historias separadas." id intro_07
    $ pagina = "p. 9"
    nl "Por eso, imaginar la historia como un escenario sin raíces en el medio es una trampa cultural. La crisis ambiental tampoco se resuelve únicamente con más tecnología: requiere pensar qué tipo de sociedad la utiliza." id intro_08

    # Escena I3 · Una crisis planetaria
    scene intro_londres at paneo with transformacion
    n "El problema ambiental actual obliga a revisar cómo contamos la historia. No basta con describir los cambios técnicos: hay que comprender cómo se relacionan con la organización de la sociedad y con los ecosistemas que la sostienen." id intro_09

    menu (screen="quiz", quiz="intro_quiz", pagina="p. 8"):
        pregunta "Sabellicus escribió la historia de Venecia sin mencionar el comercio de la sal. ¿Qué problema señala el autor con ese ejemplo?" id intro_quiz
        "Una historia contada solo desde la política, que deja fuera la economía y los recursos que la sostenían." (correcta=True):
            pass
        "Que la sal no era importante para Venecia.":
            pass
        "Que los historiadores antiguos no usaban documentos escritos.":
            pass
    porque "El ejemplo muestra cómo una historia escrita desde la cúspide puede omitir fenómenos económicos y recursos del medio que sostienen el poder." id intro_quiz_porque

    menu (screen="decision", pagina="pp. 7–9"):
        dilema "Para entender la crisis ambiental de hoy, ¿por dónde empezarías?" id intro_dec
        "Por la tecnología.":
            segun "Según el libro, el problema no se resuelve simplemente con medidas tecnológicas." id intro_dec_a
        "Por la naturaleza.":
            segun "El autor critica el reduccionismo ecologista: no es un problema exclusivo de los ecosistemas naturales." id intro_dec_b
        "Por la relación entre sociedad, tecnología y ecosistemas.":
            segun "Es el enfoque que propone el libro." id intro_dec_c

    clave "La historia humana no ocurre en un escenario vacío: sociedad, técnica y ecosistemas se transforman juntos." id intro_clave
    jump cap1

label intro_obs_palacio:
    ficha "Representan el poder político que solían destacar las crónicas." (show_titulo="Palacio Ducal y San Marcos", show_pagina="p. 8") id intro_obs_palacio
    return

label intro_obs_barcos:
    ficha "Permiten observar el comercio que la narración histórica dejó fuera." (show_titulo="Barcos y mercancías", show_pagina="p. 8") id intro_obs_barcos
    return

label intro_obs_laguna:
    ficha "Muestra el medio natural que hizo posible la ciudad y parte de su actividad comercial." (show_titulo="La laguna", show_pagina="pp. 8–9") id intro_obs_laguna
    return
