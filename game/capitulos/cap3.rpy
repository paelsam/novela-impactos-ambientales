## Capítulo 3 · El cercano Neolítico · pp. 18–27 · Presenta Javier Felipe Contreras Díaz.
## Texto: guion del equipo. Fichas: redactadas a partir de las pp. 18–26.
## Posiciones del mapa: ilustraciones.posicion_en_mapa(lon, lat, (-120, -40, 80, 60)).

define cap3_puntos_poblado = [
    Punto("vivienda", 0.33, 0.40, "Viviendas de madera", "cap3_obs_vivienda"),
    Punto("pesca", 0.20, 0.50, "Pesca en el lago", "cap3_obs_pesca"),
    Punto("pilotes", 0.53, 0.60, "Casas sobre pilotes", "cap3_obs_pilotes"),
]
define cap3_puntos_mapa = [
    Punto("creciente", 0.789, 0.301, "Creciente Fértil", "cap3_obs_creciente"),
    Punto("mesoamerica", 0.131, 0.425, "Mesoamérica", "cap3_obs_mesoamerica"),
    Punto("andes", 0.234, 0.566, "Istmo de Panamá y Andes", "cap3_obs_andes"),
]
define cap3_puntos_huertos = [
    Punto("maleza", 0.30, 0.76, "Maleza: compite con el cultivo", "cap3_obs_maleza"),
    Punto("plaga", 0.86, 0.70, "Plaga: se alimenta del cultivo", "cap3_obs_plaga"),
]

label cap3:
    $ abrir_capitulo("cap3")
    play music "audio/ambiente/rio.wav" fadein 2.0 if_changed
    scene cap3_poblado at paneo with fundido
    portada "Capítulo 3. El cercano Neolítico. Veremos cómo la agricultura y la domesticación permitieron construir un medio cada vez más organizado por las sociedades humanas, y qué consecuencias tuvo ese cambio para los ecosistemas." id cap3_portada

    # Escena 3.1 · Un poblado junto al agua
    $ pagina = "p. 18"
    scene cap3_hombre at paneo with fundido
    nl "La domesticación y la agricultura constituyen una de las revoluciones más profundas de la historia humana; solo la época moderna puede compararse con ese cambio." id cap3_01
    scene cap3_pan at paneo with fundido
    n "Muchas de las plantas y animales que todavía alimentan a las sociedades actuales proceden de procesos de domesticación neolíticos. El trigo y la cebada siguen siendo ejemplos esenciales." id cap3_02
    $ pagina = "pp. 18–19"
    n "Con la agricultura, las comunidades empezaron a ganar autonomía respecto de algunas condiciones inmediatas del ecosistema: ya no solo aprovechaban recursos disponibles, sino que construían un medio ajustado a sus necesidades." id cap3_03
    $ pagina = "p. 19"
    scene cap3_pesca at paneo with fundido
    n "La mayor seguridad alimentaria permitió el crecimiento de la población. En Mesopotamia, por ejemplo, se estima que la población se multiplicó por cuarenta entre el 8000 y el 4000 antes de Cristo." id cap3_04
    $ pagina = "pp. 19–20"
    n "Los poblados se establecieron cerca del agua. Cuando el suelo se agotaba, algunos jóvenes fundaban nuevos asentamientos, lo que contribuía a extender los poblados por el territorio." id cap3_05
    scene cap3_poblado at paneo with fundido
    call explorar(cap3_puntos_poblado)

    # Escena 3.2 · Dos continentes, dos caminos
    $ pagina = "pp. 20–21"
    scene cap3_tejedora at paneo with transformacion
    nl "Los excedentes alimentarios favorecieron la división del trabajo y la aparición de nuevas técnicas: alfarería, tejidos de lino y lana, hachas pulimentadas, arado, rueda, vela y trabajo de metales como el cobre y el bronce." id cap3_06
    $ pagina = "pp. 21–25"
    scene cap3_mapa with transformacion
    n "La domesticación no ocurrió de la misma manera en todas partes. En Eurasia se domesticaron, entre otras especies, trigo, cebada, cabras, ovejas, bueyes y caballos." id cap3_07
    n "En América se desarrollaron otros conjuntos de cultivos y animales, entre ellos maíz, calabaza, frijol, chile y llama. En cambio, no existían grandes herbívoros de tiro equivalentes a los de Eurasia." id cap3_08
    call explorar(cap3_puntos_mapa)

    # Escena 3.3 · Maleza y plaga
    scene cap2_bosque at paneo with fundido
    $ pagina = "pp. 25–26"
    n "Al transformar el entorno en campos de cultivo, las sociedades alteraron las relaciones entre especies. Las plantas que competían con el cultivo empezaron a llamarse «maleza», mientras que algunos animales pasaron a considerarse «plagas»." id cap3_09
    scene cap3_huertos at paneo with transformacion
    n "Esos términos no son conceptos ecosistémicos neutrales: clasifican a las especies desde las necesidades del nuevo orden agrícola, es decir, desde aquello que favorece o perjudica la producción humana." id cap3_10
    n "La agricultura aumentó la capacidad humana de organizar el medio, pero también desarticuló cadenas tróficas y subordinó partes del ecosistema a los objetivos de la producción." id cap3_11
    call explorar(cap3_puntos_huertos)

    menu (screen="quiz", quiz="cap3_quiz", pagina="pp. 25–26"):
        pregunta "¿Por qué «maleza» y «plaga» no son conceptos ecosistémicos?" id cap3_quiz
        "Porque nombran a las especies que sobran en el nuevo orden agrícola, no una función en el ecosistema." (correcta=True):
            pass
        "Porque son especies que no existían antes del Neolítico.":
            pass
        "Porque solo afectan a cultivos de otros continentes.":
            pass
    porque "Una planta es considerada maleza porque compite con un cultivo; una plaga aparece cuando el cultivo favorece en exceso a ciertas especies. Son categorías del orden tecnológico agrícola, no categorías neutrales de la naturaleza." id cap3_quiz_porque

    scene cap3_navegantes at paneo with fundido
    menu (screen="decision", pagina="pp. 15, 19–20"):
        dilema "El poblado crece y el suelo junto al río se agota. ¿Qué hacen?" id cap3_dec
        "Los jóvenes fundan un nuevo poblado.":
            segun "Así ocurrió: este proceso explica la multiplicación de asentamientos junto al agua." id cap3_dec_a
        "Siguen cultivando la misma tierra.":
            segun "Con la azada, la población dependía del área cultivable y la fertilidad debía renovarse." id cap3_dec_b
        "Vuelven a la caza.":
            segun "La vida cazadora exigía una densidad de población muy baja; un poblado agrícola más denso no podía alimentarse de ese modo con facilidad." id cap3_dec_c

    scene cap3_fundicion at paneo with fundido
    nota "Durante mucho tiempo se habló de una hibridación del maíz con el teosinte. La investigación genética muestra que el maíz fue domesticado a partir del teosinte en el valle del río Balsas, México, hace unos 9.000 años." (show_fuente="Matsuoka et al. (2002), PNAS") id cap3_nota
    clave "Con la agricultura, las sociedades pusieron partes del ecosistema al servicio de la producción: ganaron autonomía, pero también alteraron las cadenas tróficas." id cap3_clave
    jump final

label cap3_obs_pesca:
    ficha "Los poblados se instalaban junto al agua. Además de cultivar y criar animales, sus habitantes pescaban con redes y anzuelos." (show_lamina="cap3_pesca", show_titulo="Pesca en el lago", show_leyenda="La pesca en la época de la piedra pulimentada. Grabado de É. Bayard, 1870.") id cap3_obs_pesca
    return

label cap3_obs_pilotes:
    ficha "En las orillas de los lagos de Suiza se han hallado restos de aldeas levantadas sobre pilotes de madera, como la que muestra este grabado." (show_titulo="Casas sobre pilotes") id cap3_obs_pilotes
    return

label cap3_obs_vivienda:
    ficha "El hacha pulimentada permitió cortar y trabajar la madera: con ella se levantaron casas para un asentamiento permanente." (show_lamina="lamina_hacha", show_titulo="Viviendas de madera", show_leyenda="Fabricación y pulido de hachas. Grabado de É. Bayard, 1870.", show_pagina="p. 20") id cap3_obs_vivienda
    return

label cap3_obs_creciente:
    ficha "Región asociada con trigo, cebada y animales domesticados." (show_lamina="lamina_cebada", show_titulo="Creciente Fértil", show_leyenda="Cebada. Lámina de O. W. Thomé, 1885.", show_pagina="p. 22") id cap3_obs_creciente
    return

label cap3_obs_mesoamerica:
    ficha "Maíz y otros cultivos americanos." (show_lamina="lamina_maiz", show_titulo="Mesoamérica", show_leyenda="Almacenamiento del maíz. Códice Florentino, siglo XVI.", show_pagina="pp. 23–24") id cap3_obs_mesoamerica
    return

label cap3_obs_andes:
    ficha "Tubérculos, algodón y llama." (show_lamina="lamina_llama", show_titulo="Istmo de Panamá y Andes", show_leyenda="Llama. Grabado, Wellcome Collection, CC BY 4.0.", show_pagina="p. 25") id cap3_obs_andes
    return

label cap3_obs_maleza:
    ficha "Se llama maleza a la planta que compite con el trigo, la cebada o el maíz y no entra en los propósitos agrarios. En la lámina, una amapola, frecuente en los campos de cereal." (show_lamina="lamina_amapola", show_titulo="Maleza", show_leyenda="Amapola. Lámina de F. E. Köhler, 1887.", show_pagina="pp. 25–26") id cap3_obs_maleza
    return

label cap3_obs_plaga:
    ficha "Al favorecer solo algunas plantas, el cultivo alimenta en exceso a las especies que viven de ellas. Sus poblaciones se desajustan y aparece lo que el ser humano llama plaga." (show_lamina="lamina_langosta", show_titulo="Plaga", show_leyenda="Langosta migratoria. Encyclopaedia Britannica, 1911.", show_pagina="p. 26") id cap3_obs_plaga
    return
