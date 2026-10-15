## Momento 2 · Persistir y adaptarse · Presenta Sebastián Bolaños Morales.
## Texto sintetizado del Cap. 1, El lejano Paleolítico (pp. 10–12).

label momento2:
    $ abrir_capitulo("m2")
    play music "audio/ambiente/cueva.wav" fadein 2.0 if_changed
    scene cap1_fuego at paneo with fundido
    portada "Momento dos. Persistir y adaptarse." id m2_portada

    n "En el Paleolítico, el ambiente ya no era del todo propicio. Sin garras ni grandes colmillos, los primeros homínidos sobrevivieron con instrumentos como los raspadores, con pieles para protegerse y, posiblemente, con el fuego." id m2_01

    play music "audio/ambiente/bosque.wav" fadein 2.0 if_changed
    scene cap1_caza at paneo with fundido
    n "Cazar presas grandes no podía ser una hazaña individual: era una empresa colectiva que exigía instrumentos, organización y comunicación dentro del grupo." id m2_02

    scene cap1_hombre at paneo with fundido
    n "Esa cooperación les permitió dejar el trópico y ocupar las estepas de tierras templadas. Así, sus capacidades técnicas y sociales empezaron a cambiar su relación con el ecosistema." id m2_03

    menu (screen="quiz", quiz="m2_quiz"):
        pregunta "Sin garras ni grandes colmillos, ¿qué permitió a los primeros grupos humanos sobrevivir y ocupar nuevos territorios?" id m2_quiz
        "Una fuerza física mayor que la de otros depredadores.":
            pass
        "Los instrumentos, el fuego, las pieles y la cooperación del grupo." (correcta=True):
            pass
        "Permanecer siempre en el mismo bosque.":
            pass
    porque "El grupo compensaba la falta de órganos especializados con instrumentos y organización. Esa cooperación fue la que le permitió salir del trópico." id m2_quiz_porque

    clave "Sin garras ni colmillos, los seres humanos persistieron gracias a sus instrumentos y a la cooperación, y empezaron a cambiar su relación con el ecosistema." id m2_clave
    jump momento3
