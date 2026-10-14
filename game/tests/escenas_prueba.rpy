## Escenas mínimas para los recorridos automáticos. No viajan en los paquetes.

label prueba_narracion:
    $ abrir_capitulo("cap2")
    scene expression Solid(PAPEL)
    n "Primera línea de prueba." id prueba_01
    nl "Segunda línea, en el panel lateral." id prueba_02
    n "Tercera línea." id prueba_03
    return

define prueba_puntos = [
    Punto("uno", 0.70, 0.40, "Punto uno", "prueba_obs_uno"),
    Punto("dos", 0.30, 0.60, "Punto dos", "prueba_obs_dos"),
]

label prueba_observacion:
    $ abrir_capitulo("cap2")
    scene menu_fondo
    call explorar(prueba_puntos)
    n "Después de explorar." id prueba_obs_fin
    return

label prueba_obs_uno:
    ficha "Texto de la ficha uno." (show_lamina="menu_fondo", show_titulo="Uno", show_leyenda="Leyenda de prueba.", show_pagina="p. 1") id prueba_obs_uno
    return

label prueba_obs_dos:
    ficha "Texto de la ficha dos, sin lámina." (show_titulo="Dos", show_pagina="p. 2") id prueba_obs_dos
    return

label prueba_quiz:
    $ abrir_capitulo("cap2")
    scene menu_fondo
    call prueba_quiz_bloque
    call prueba_quiz_bloque
    menu (screen="decision", pagina="p. 14"):
        dilema "¿Decisión de prueba?" id prueba_dec
        "Camino A":
            segun "Según el libro, A." id prueba_dec_a
        "Camino B":
            segun "Según el libro, B." id prueba_dec_b
    n "Fin de la prueba." id prueba_dec_fin
    return

label prueba_quiz_bloque:
    menu (screen="quiz", quiz="prueba_quiz", pagina="p. 15"):
        pregunta "¿Pregunta de prueba?" id prueba_quiz
        "Opción incorrecta":
            pass
        "Opción correcta" (correcta=True):
            pass
        "Otra incorrecta":
            pass
    porque "Explicación de prueba." id prueba_quiz_porque
    return
