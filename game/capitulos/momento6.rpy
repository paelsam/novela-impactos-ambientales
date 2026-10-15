## Momento 6 · Del pasado al presente · Todo el equipo.
## Buenaventura es una conexión preparada por el equipo; la semilla es la analogía del taller.

label momento6:
    $ abrir_capitulo("m6")
    play music "audio/ambiente/rio.wav" fadein 2.0 if_changed
    scene final_buenaventura at paneo with transformacion
    portada "Momento seis. Del pasado al presente." id m6_portada

    $ seccion = "Conexión local del equipo"
    n "Como una semilla que crece hasta ser árbol, cada técnica cambió nuestra relación con el ambiente. Hoy, en Buenaventura, la vida depende del mar, de los ríos y de los manglares. ¿Qué instrumentos culturales necesitamos para que esa transformación no destruya lo que nos sostiene?" id m6_01
    $ seccion = ""

    call screen fin
    return
