## Momento 5 · La transformación de un paisaje · Presenta Javier Felipe Contreras Díaz.
## Texto sintetizado del Cap. 3, El cercano Neolítico (pp. 18, 21–26).

define m5_puntos_huertos = [
    Punto("maleza", 0.30, 0.76, "Maleza: compite con el cultivo", "m5_obs_maleza"),
    Punto("plaga", 0.86, 0.70, "Plaga: se alimenta del cultivo", "m5_obs_plaga"),
]

label momento5:
    $ abrir_capitulo("m5")
    play music "audio/ambiente/bosque.wav" fadein 2.0 if_changed
    scene cap3_mapa with fundido
    portada "Momento cinco. La transformación de un paisaje." id m5_portada

    n "Casi todas las plantas y animales que aún forman la base de la alimentación se domesticaron entonces: trigo, cebada, cabras y ovejas en Eurasia; maíz, frijol, calabaza y llama en América." id m5_01

    scene cap3_huertos at paneo with transformacion
    n "Preparar los suelos, sembrar y criar animales permitió producir alimentos, pero también obligó a adaptar los ecosistemas a las necesidades humanas. Al seleccionar unas especies, la sociedad transformó el paisaje." id m5_02
    n "Las plantas que competían con el cultivo pasaron a llamarse «maleza», y los animales que se alimentaban de él, «plaga». No son conceptos del ecosistema: nombran lo que sobra en el nuevo orden agrícola." id m5_03
    call explorar(m5_puntos_huertos)

    menu (screen="quiz", quiz="m5_quiz"):
        pregunta "¿Por qué «maleza» y «plaga» no describen la función de una especie en el ecosistema?" id m5_quiz
        "Porque nombran a las especies según convienen o estorban al cultivo humano." (correcta=True):
            pass
        "Porque son especies que aparecieron después del Neolítico.":
            pass
        "Porque solo existen en otros continentes.":
            pass
    porque "Al favorecer unas pocas plantas, el cultivo desajusta las relaciones entre especies. «Maleza» y «plaga» son categorías del orden agrícola, no de la naturaleza." id m5_quiz_porque

    clave "Con la agricultura, las sociedades pusieron partes del ecosistema al servicio de la producción: ganaron autonomía, pero alteraron las cadenas tróficas." id m5_clave
    jump momento6

label m5_obs_maleza:
    ficha "Se llama maleza a la planta que compite con el trigo, la cebada o el maíz y no entra en los propósitos agrarios. En la lámina, una amapola de los campos de cereal." (show_lamina="lamina_amapola", show_titulo="Maleza", show_leyenda="Amapola. Lámina de F. E. Köhler, 1887.") id m5_obs_maleza
    return

label m5_obs_plaga:
    ficha "Al favorecer solo algunas plantas, el cultivo alimenta en exceso a las especies que viven de ellas. Sus poblaciones se desajustan y aparece lo que el ser humano llama plaga." (show_lamina="lamina_langosta", show_titulo="Plaga", show_leyenda="Langosta migratoria. Encyclopaedia Britannica, 1911.") id m5_obs_plaga
    return
