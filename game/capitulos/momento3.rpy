## Momento 3 · Cuando sobrevivir también transforma el entorno · Presenta María Fernanda Cano Cobo.
## Texto sintetizado de los Caps. 1 y 2 (pp. 12–15).

define m3_puntos_glaciacion = [
    Punto("mamut", 0.660, 0.517, "Mamut lanudo", "m3_obs_mamut"),
    Punto("alce", 0.825, 0.583, "Alce gigante", "m3_obs_alce"),
    Punto("rinoceronte", 0.692, 0.649, "Rinoceronte lanudo", "m3_obs_rinoceronte"),
]

label momento3:
    $ abrir_capitulo("m3")
    play music "audio/ambiente/bosque.wav" fadein 2.0 if_changed
    scene cap1_mapa with fundido
    portada "Momento tres. Cuando sobrevivir también transforma el entorno." id m3_portada

    n "Con mejores herramientas y más cooperación, la caza se volvió cada vez más organizada y selectiva: ciervos en China, toros y caballos en España, mamuts en Europa Central y renos en Francia." id m3_01

    scene cap2_glaciacion at paneo with transformacion
    n "El número de presas creció. Los restos de cien mil caballos en Solutré y de mil mamuts en Predmost representan ya una especie de ecocidio: una presión insólita sobre otras especies." id m3_02
    n "Hace trece mil años, al terminar la glaciación, desaparecieron el mamut, el rinoceronte lanudo y el alce gigante. El clima influyó, pero también una caza que usaba el fuego para acorralar manadas." id m3_03
    call explorar(m3_puntos_glaciacion)

    scene cap2_bosque at paneo with fundido
    menu (screen="quiz", quiz="m3_quiz"):
        pregunta "¿Qué muestran los restos de Solutré y Predmost?" id m3_quiz
        "Que los cazadores cuidaban las manadas para no agotarlas.":
            pass
        "Que esos animales desaparecieron solo por el clima.":
            pass
        "Que la presión humana sobre otras especies comenzó mucho antes de la industria." (correcta=True):
            pass
    porque "Son huellas de una caza cada vez más selectiva y numerosa. La intervención sobre la naturaleza no empezó con la industria moderna: tiene antecedentes en las primeras sociedades." id m3_quiz_porque

    clave "Al perfeccionar la caza, los grupos humanos presionaron a otras especies: la intervención sobre la naturaleza tiene raíces en las primeras sociedades." id m3_clave
    jump momento4

label m3_obs_mamut:
    ficha "Había sido parte fundamental de la dieta de los cazadores. Con el cambio de clima y el avance de los bosques, desapareció." (show_lamina="lamina_mamut", show_titulo="Mamut lanudo", show_leyenda="Grabado de É. Riou, 1863.") id m3_obs_mamut
    return

label m3_obs_alce:
    ficha "Desapareció al terminar la glaciación, junto al mamut y al rinoceronte lanudos. La caza con fuego pudo influir." (show_lamina="lamina_alce", show_titulo="Alce gigante", show_leyenda="Megaloceros. Grabado de É. Riou, 1863.") id m3_obs_alce
    return

label m3_obs_rinoceronte:
    ficha "Tampoco sobrevivió. En cambio, el caballo, el ganado vacuno, los elefantes y los rinocerontes sí lo hicieron." (show_lamina="lamina_rinoceronte", show_titulo="Rinoceronte lanudo", show_leyenda="Grabado de É. Riou, 1863.") id m3_obs_rinoceronte
    return
