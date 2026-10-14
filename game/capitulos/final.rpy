## Reflexión final · Todo el equipo. Textos propuestos a partir de las Partes 2 y 3 del taller.
## Buenaventura es una conexión preparada por el equipo, no un dato del libro.

label final:
    $ abrir_capitulo("final")
    play music "audio/ambiente/rio.wav" fadein 2.0 if_changed

    # Escena F1 · Conexión local: Buenaventura
    scene final_buenaventura at paneo with fundido
    $ pagina = "Conexión preparada por el equipo"
    $ seccion = "Conexión local del equipo"
    n "Lo que vimos no es solo pasado. En Buenaventura, la vida, la cultura y la identidad dependen del mar, de los ríos y de los manglares." id final_01
    n "La expansión portuaria, industrial y minera puede entrar en conflicto con la conservación de los manglares y con la pesca tradicional. Transformar un territorio sin evaluar sus consecuencias perjudica las formas de vida que dependen de él." id final_02

    # Escena F2 · La semilla y el árbol
    scene final_semilla at paneo with transformacion
    $ seccion = ""
    show screen resumen
    $ pagina = "p. 9"
    nl "Elegimos una imagen para resumir este recorrido: una semilla que crece hasta ser un árbol rodeado de cultivos y herramientas. A medida que la humanidad avanza, también cambia su relación con el ambiente del que depende." id final_03
    nl "La resiliencia cultural frente al medio es frágil. Y, al mismo tiempo, la incertidumbre es la raíz de la creatividad cultural." id final_04
    nl "Les dejamos una pregunta: ¿qué instrumentos culturales, técnicos, sociales y teóricos, necesitamos hoy para responder a la crisis ambiental?" id final_05
    call screen fin
    hide screen resumen
    return
