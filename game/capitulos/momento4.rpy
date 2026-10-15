## Momento 4 · Un cambio en la cultura · Presenta Javier Felipe Contreras Díaz.
## Texto sintetizado del Cap. 3, El cercano Neolítico (pp. 18–20).

image m4_collage = Fixed(
    Solid("#EFE7D4"),
    At(montada("laminas/lam_pesca.jpg", 480, 259, "La pesca. É. Bayard, 1870."), pieza_collage(70, 70, -1.0, 0.2)),
    At(montada("laminas/lam_pan.jpg", 480, 316, "El arte de hacer pan. É. Bayard, 1870."), pieza_collage(90, 470, 1.0, 0.5)),
    At(montada("laminas/lam_tejedora.jpg", 417, 635, "La primera tejedora. É. Bayard, 1870."), pieza_collage(630, 150, 1.5, 0.8)),
    xysize=(1920, 1080))

define m4_puntos_poblado = [
    Punto("vivienda", 0.33, 0.40, "Viviendas de madera", "m4_obs_vivienda"),
    Punto("pesca", 0.20, 0.50, "Pesca en el lago", "m4_obs_pesca"),
    Punto("espacio", 0.53, 0.60, "Un espacio construido", "m4_obs_espacio"),
]

label momento4:
    $ abrir_capitulo("m4")
    play music "audio/musica/momento4.ogg" fadein 3.0 if_changed
    play ambiente "audio/ambiente/rio.wav" fadein 2.0 if_changed
    scene m4_collage with fundido
    portada "Momento cuatro. Un cambio en la cultura." id m4_portada

    nl "La caza, la recolección y la pesca siguieron siendo importantes. Pero, poco a poco, la agricultura y la domesticación de animales cambiaron la forma de vivir: fue una de las revoluciones más profundas de la historia." id m4_01
    call montaje(kicker(), [("m4_hombre", "El hombre de la época de la piedra pulimentada, según É. Bayard (1870).")])

    scene cap3_poblado at paneo with fundido
    n "Los poblados se volvieron más permanentes, casi siempre junto a fuentes de agua. Desde allí, las comunidades empezaron a intervenir de forma continua en el entorno para obtener alimento y organizar su vida." id m4_02
    call explorar(m4_puntos_poblado)

    scene cap3_navegantes at paneo with fundido
    n "La seguridad del alimento favoreció el crecimiento de la población: entre el 8000 y el 4000 antes de Cristo, Mesopotamia la multiplicó por cuarenta." id m4_03

    menu (screen="decision"):
        dilema "El poblado crece y la tierra junto al río pierde fertilidad. ¿Qué hacen?" id m4_dec
        "Los jóvenes fundan un nuevo poblado.":
            segun "Así ocurrió: muchos jóvenes debían dejar el poblado y construir su propio espacio, y los poblados se multiplicaron junto al agua." id m4_dec_a
        "Siguen cultivando la misma tierra.":
            segun "Con la azada y un suelo cuya fertilidad había que renovar, una población cada vez mayor no podía alimentarse en un área tan reducida." id m4_dec_b
        "Vuelven a la caza.":
            segun "La caza solo sostenía grupos muy dispersos, de unos tres habitantes por kilómetro cuadrado; un poblado agrícola no podía volver a ese modo de vida." id m4_dec_c

    clave "Al asentarse junto al agua, las comunidades empezaron a intervenir de forma continua en su entorno." id m4_clave
    jump momento5

label m4_obs_vivienda:
    ficha "El hacha pulimentada permitió cortar y trabajar la madera: con ella se levantaron casas para un asentamiento permanente." (show_lamina="lamina_hacha", show_titulo="Viviendas de madera", show_leyenda="Fabricación y pulido de hachas. Grabado de É. Bayard, 1870.") id m4_obs_vivienda
    return

label m4_obs_pesca:
    ficha "La vida sedentaria había empezado antes, con la pesca. En el Neolítico, los poblados se ubicaron por lo general junto a las fuentes de agua." (show_titulo="Pesca en el lago") id m4_obs_pesca
    return

label m4_obs_espacio:
    ficha "El poblado es un espacio construido para vivir y trabajar: con él, el ser humano se separa de las otras especies. Al principio no pasaba de media hectárea." (show_titulo="Un espacio construido") id m4_obs_espacio
    return
