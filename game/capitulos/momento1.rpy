## Momento 1 · Una humanidad dentro del ecosistema · Presenta Elkin Samir Angulo Panameño.
## Texto sintetizado de la Introducción (pp. 6–9).

image m1_collage = Fixed(
    Solid("#EFE7D4"),
    At(montada("laminas/lam_abrigo.jpg", 419, 640, "Abrigo rocoso de Bruniquel. É. Bayard, 1870."), pieza_collage(80, 150, -1.5, 0.2)),
    At(montada("laminas/lam_hachas.jpg", 463, 640, "Hachas de piedra de Le Moustier. Lartet y Christy, 1875."), pieza_collage(580, 210, 1.2, 0.6)),
    xysize=(1920, 1080))

define m1_puntos_venecia = [
    Punto("palacio", 0.34, 0.37, "Palacio Ducal y San Marcos", "m1_obs_palacio"),
    Punto("barcos", 0.57, 0.52, "Barcos y mercancías", "m1_obs_barcos"),
    Punto("laguna", 0.78, 0.84, "La laguna", "m1_obs_laguna"),
]

label momento1:
    $ abrir_capitulo("m1")
    play music "audio/ambiente/rio.wav" fadein 2.0 if_changed
    scene m1_collage with fundido
    portada "Momento uno. Una humanidad dentro del ecosistema." id m1_portada

    nl "Desde sus orígenes, los seres humanos han dependido de la naturaleza para alimentarse, protegerse y sobrevivir. Los ecosistemas les dan lo esencial para vivir, pero también son un entorno al que deben adaptarse." id m1_01

    scene intro_venecia at paneo with fundido
    n "Durante siglos, la historia se contó desde la cúspide. Sabellicus escribió la historia de Venecia sin mencionar el comercio de la sal, aunque ese recurso sostenía su poder." id m1_02
    call explorar(m1_puntos_venecia)

    scene intro_londres at paneo with transformacion
    n "Las herramientas, esos «testimonios mudos de la historia», cuentan otra cosa: sociedad, técnica y naturaleza no son historias separadas. Comprender la historia humana implica reconocer que siempre ha estado ligada al ambiente." id m1_03

    clave "La historia humana no ocurre en un escenario vacío: sociedad, técnica y ecosistemas se transforman juntos." id m1_clave
    jump momento2

label m1_obs_palacio:
    ficha "Representan el poder político que solían destacar las crónicas." (show_titulo="Palacio Ducal y San Marcos") id m1_obs_palacio
    return

label m1_obs_barcos:
    ficha "Permiten observar el comercio que la narración histórica dejó fuera." (show_titulo="Barcos y mercancías") id m1_obs_barcos
    return

label m1_obs_laguna:
    ficha "Muestra el medio natural que hizo posible la ciudad y parte de su actividad comercial." (show_titulo="La laguna") id m1_obs_laguna
    return
