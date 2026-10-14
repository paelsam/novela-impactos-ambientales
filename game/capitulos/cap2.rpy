## Capítulo 2 · Del Homo sapiens al Neolítico · pp. 13–17 · Presenta María Fernanda Cano Cobo.
## Texto: guion del equipo. Fichas de observación: redactadas a partir de las pp. 13–17.

define cap2_puntos_glaciacion = [
    Punto("mamut", 0.660, 0.517, "Mamut lanudo", "cap2_obs_mamut"),
    Punto("alce", 0.825, 0.583, "Alce gigante", "cap2_obs_alce"),
    Punto("rinoceronte", 0.692, 0.649, "Rinoceronte lanudo", "cap2_obs_rinoceronte"),
]
define cap2_puntos_arte = [
    Punto("realismo", 0.275, 0.270, "Bisonte de Altamira: realismo", "cap2_obs_realismo"),
    Punto("abstraccion", 0.200, 0.720, "Figuras levantinas: abstracción", "cap2_obs_abstraccion"),
]

label cap2:
    $ abrir_capitulo("cap2")
    play music "audio/ambiente/rio.wav" fadein 2.0 if_changed
    scene cap2_rio at paneo with fundido
    portada "Capítulo 2. Del Homo sapiens al Neolítico. Esta parte sigue los cambios del ambiente, las técnicas de caza y la cultura, hasta el problema de cómo regular el medio cuando la fauna empieza a agotarse." id cap2_portada

    # Escena 2.1 · Junto a los ríos
    $ pagina = "p. 13"
    nl "Para Ángel Maya, con el Homo sapiens se consolida la evolución histórica y se acelera la cultura. Las formas de vida cambian junto con las capacidades técnicas y sociales." id cap2_01
    nl "Los ríos ofrecieron condiciones favorables para asentarse temporalmente o permanecer en ciertos lugares. En los periodos que menciona el libro, la población creció y se desarrollaron distintas formas de organización." id cap2_02
    $ pagina = "pp. 13–14"
    nl "El arco y el lanzador de venablos ampliaron las posibilidades de caza. La obtención de alimento dependía menos de una sola presa o de un único ambiente, aunque seguía ligada a los recursos disponibles." id cap2_03
    $ pagina = "p. 14"
    nl "El autor cuestiona la idea de que el cazador viviera necesariamente al borde del hambre: estima entre tres y cuatro horas diarias de caza, frente a unas sesenta horas semanales de trabajo para un agricultor." id cap2_04

    # Escena 2.2 · El fin de la glaciación
    play music "audio/ambiente/bosque.wav" fadein 2.0 if_changed
    scene cap2_glaciacion at paneo with transformacion
    $ pagina = "pp. 14–15"
    n "Para mantener las cuotas de caza, la densidad de población debía ser muy baja. El libro ofrece como referencia unos tres habitantes por kilómetro cuadrado." id cap2_05
    $ pagina = "p. 15"
    n "El fin de la glaciación, hace unos 13.000 años según el texto, llevó los bosques a las llanuras. Desaparecieron animales como el mamut lanudo, el rinoceronte lanudo y el alce gigante." id cap2_06
    call explorar(cap2_puntos_glaciacion)
    scene cap2_bosque at paneo with transformacion
    n "El autor plantea que la actividad humana pudo influir en esas desapariciones, por ejemplo mediante el uso del fuego para acorralar manadas. La explicación no atribuye todo al ser humano: el cambio climático también forma parte del contexto." id cap2_07
    $ pagina = "pp. 15–16"
    n "El capítulo describe un círculo de agotamiento y técnica: de la lanza se pasó a los dardos y luego a las flechas, aumentando la eficacia de la caza. También cambiaron las relaciones sociales, con alianzas, comercio y guerra." id cap2_08

    # Escena 2.3 · La cueva pintada
    play music "audio/ambiente/cueva.wav" fadein 2.0 if_changed
    scene cap2_arte at paneo with fundido
    $ pagina = "pp. 16–17"
    nl "El capítulo presenta al ser humano como constructor de símbolos. Las imágenes pasan del realismo asociado al arte magdaleniense a formas más abstractas en el arte levantino." id cap2_09
    $ pagina = "p. 17"
    nl "El autor vincula el instrumento y el símbolo: el instrumento condensa una teoría práctica, mientras que el símbolo puede abrir un camino hacia nuevas formas de acción." id cap2_10
    call explorar(cap2_puntos_arte)

    # Quiz, decisión, nota de campo e idea clave
    scene cap2_bosque at paneo with fundido
    menu (screen="quiz", quiz="cap2_quiz", pagina="p. 15"):
        pregunta "¿Qué relación plantea el capítulo entre las armas y la fauna?" id cap2_quiz
        "Las mejores armas permitieron cazar menos y proteger las manadas.":
            pass
        "Cuando la fauna se agota se crean armas más potentes, que la agotan aún más." (correcta=True):
            pass
        "Las armas no influyeron: la fauna desapareció solo por el clima.":
            pass
    porque "El autor describe un círculo en el que la lanza da paso a dardos y flechas cada vez más eficaces para agotar los cotos de caza. El clima también influyó, pero no explica por sí solo el proceso." id cap2_quiz_porque

    menu (screen="decision", pagina="pp. 14–15"):
        dilema "¿Por qué crees que el ser humano empezó a cultivar?" id cap2_dec
        "Porque cazar era agotador y pasaban hambre.":
            segun "El libro cuestiona esta explicación: estima que la caza podía ocupar entre tres y cuatro horas diarias." id cap2_dec_a
        "Para tener más tiempo libre.":
            segun "El texto compara esa actividad con unas sesenta horas semanales de trabajo agrícola." id cap2_dec_b
        "Porque la fauna se agotaba y hacía falta otra forma de regular el medio.":
            segun "Es la lectura del autor: la agricultura como una forma más compleja de regular el medio." id cap2_dec_c

    nota "El libro sitúa al Homo sapiens hace unos 50.000 años. Los fósiles más antiguos conocidos de Homo sapiens, en Jebel Irhoud (Marruecos), tienen unos 300.000 años." (show_fuente="Hublin et al. (2017), Nature") id cap2_nota
    clave "Cada avance técnico transformó el medio, y cada cambio del medio obligó a reorganizar la sociedad." id cap2_clave
    jump cap3

label cap2_obs_mamut:
    ficha "El mamut lanudo había sido parte fundamental de la dieta en el periodo anterior. Con el cambio de clima y el avance de los bosques, desapareció." (show_lamina="lamina_mamut", show_titulo="Mamut lanudo", show_leyenda="Grabado de É. Riou, 1863.", show_pagina="pp. 13–15") id cap2_obs_mamut
    return

label cap2_obs_alce:
    ficha "Desapareció al terminar la glaciación, junto al mamut y al rinoceronte lanudos. El autor sugiere que la caza con fuego pudo influir." (show_lamina="menu_fondo", show_titulo="Alce gigante", show_leyenda="Megaloceros. Grabado de É. Riou, 1863.", show_pagina="p. 15") id cap2_obs_alce
    return

label cap2_obs_rinoceronte:
    ficha "El rinoceronte lanudo tampoco sobrevivió. En cambio, según el libro, el caballo, el ganado vacuno, los elefantes y los rinocerontes sí lo hicieron." (show_lamina="lamina_rinoceronte", show_titulo="Rinoceronte lanudo", show_leyenda="Grabado de É. Riou, 1863.", show_pagina="p. 15") id cap2_obs_rinoceronte
    return

label cap2_obs_realismo:
    ficha "Las pinturas magdalenienses aludían a una actividad inmediata, casi identificable: un animal concreto, observado con precisión de cazador." (show_lamina="lamina_bisonte", show_titulo="Realismo", show_leyenda="Bisonte pintado en la cueva de Altamira (Cantabria).", show_pagina="p. 16") id cap2_obs_realismo
    return

label cap2_obs_abstraccion:
    ficha "Las figuras más tardías de la España oriental son símbolos que relacionan muchas actividades. Para el autor, la abstracción es una conquista posterior, no una decadencia." (show_lamina="lamina_levante", show_titulo="Abstracción", show_leyenda="Cova dels Cavalls (Castellón). Foto: EmparMM, CC BY-SA 4.0.", show_pagina="p. 16") id cap2_obs_abstraccion
    return
