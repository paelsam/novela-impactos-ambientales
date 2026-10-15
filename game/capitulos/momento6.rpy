## Momento 6 · Del pasado al presente · Todo el equipo.
## Buenaventura es una conexión preparada por el equipo; la semilla es la analogía del taller.

label momento6:
    $ abrir_capitulo("m6")
    play music "audio/musica/momento6.ogg" fadein 3.0 if_changed
    play ambiente "audio/ambiente/rio.wav" fadein 2.0 if_changed
    scene m6_manglar at paneo with transformacion
    portada "Momento seis. Del pasado al presente." id m6_portada

    call montaje("LO QUE NOS SOSTIENE", [
        ("m6_pescadores", "Pescadores del Pacífico colombiano."),
        ("m6_pesca", "Pesca artesanal en Juanchaco, Buenaventura."),
        ("m6_botes", "Botes de pesca en Juanchaco."),
        ("m6_ballena", "Ballena jorobada y su cría en Bahía Málaga."),
        ("m6_cultivos", "Cultivos en las laderas de la Sierra Nevada de Santa Marta."),
    ])
    call montaje("LO QUE LO AMENAZA", [
        ("m6_puerto", "La expansión del puerto de Buenaventura."),
        ("m6_mineria", "Minería ilegal en Santander de Quilichao, Cauca."),
        ("m6_retroexcavadora", "Maquinaria en una mina ilegal."),
        ("m6_tala", "Tala y quema de selva en la Amazonía colombiana."),
        ("m6_deforestacion", "Deforestación en el piedemonte amazónico."),
        ("m6_contaminacion", "Basura en el río Magdalena, a la altura de Neiva."),
    ])

    scene final_buenaventura at paneo with transformacion

    $ seccion = "Conexión local del equipo"
    n "Como una semilla que crece hasta ser árbol, cada técnica cambió nuestra relación con el ambiente. Hoy, en Buenaventura, la vida depende del mar, de los ríos y de los manglares. ¿Qué instrumentos culturales necesitamos para que esa transformación no destruya lo que nos sostiene?" id m6_01
    $ seccion = ""

    call screen fin
    return
