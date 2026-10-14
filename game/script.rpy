# Adaptación educativa basada en la Introducción y los tres primeros capítulos
# de La fragilidad ambiental de la cultura, de Augusto Ángel Maya.

define guide = Character("GUÍA", color="#f3c86a")

image bg title = "images/bg_title.png"
image bg cave = "images/bg_cave.png"
image bg hunt = "images/bg_hunt.png"
image bg village = "images/bg_village.png"
image bg city = "images/bg_city.png"
image bg victory = "images/bg_victory.png"

default score = 0
default hints_used = 0

label start:
    scene bg title with fade
    show screen hud("PRÓLOGO")
    guide "¡Explorador/a, bienvenida/o al archivo del tiempo!"
    guide "Tu misión es descubrir cómo la historia humana y el medio ambiente se han transformado mutuamente."
    guide "Cada etapa contiene una pista y una pregunta. Responde correctamente para desbloquear la siguiente zona."
    guide "Este recorrido se basa en la introducción y los tres primeros capítulos de La fragilidad ambiental de la cultura, de Augusto Ángel Maya."
    hide screen hud
    jump intro

label intro:
    scene bg title with dissolve
    call screen mini_story("INTRODUCCIÓN · 1/4 · UNA HISTORIA COMPARTIDA", "images/bg_title.png", "PRIMERA PISTA: la historia no ocurre en un escenario vacío.", "audio/voice/intro_01.wav")
    call screen mini_story("INTRODUCCIÓN · 2/4 · SOCIEDAD Y AMBIENTE", "images/bg_village.png", "El autor propone estudiar las sociedades junto con el ambiente que habitan. La organización social, la economía y la política están vinculadas a las tecnologías con las que transformamos los ecosistemas.", "audio/voice/intro_02.wav")
    call screen mini_story("INTRODUCCIÓN · 3/4 · MÁS QUE TECNOLOGÍA", "images/bg_city.png", "Por eso, la crisis ambiental no se resuelve únicamente con tecnología: también exige revisar cómo organizamos la sociedad.", "audio/voice/intro_03.wav")
    call screen mini_story("INTRODUCCIÓN · 4/4 · LA FRAGILIDAD CULTURAL", "images/bg_title.png", "La cultura es frágil porque sus soluciones pueden no ser suficientes para superar una crisis que hoy tiene alcance planetario.", "audio/voice/intro_04.wav")
    call quiz(
        "Según la introducción, ¿cómo debe estudiarse la crisis ambiental?",
        ["A. Como un problema exclusivo de la naturaleza",
         "B. Relacionando ambiente, tecnología y organización social",
         "C. Solo mediante nuevos inventos"],
        correct=1,
        praise="¡Correcto! Has encontrado la primera clave: sociedad y ambiente no pueden separarse.",
        hint="Pista: el autor critica las explicaciones que separan la sociedad de su entorno.",
    )
    jump paleolitico

label paleolitico:
    play music "audio/amb_forest.wav" fadein 1.0
    call screen mini_story("PALEOLÍTICO · 1/4 · UN MUNDO POR EXPLORAR", "images/scenes/paleo_01_explorar.png", "Hace miles de años, pequeños grupos humanos recorrían el paisaje buscando agua, frutos y refugio. Cada desplazamiento dependía de conocer las señales del entorno.", "audio/voice/scene_01.wav")
    call screen mini_story("PALEOLÍTICO · 2/4 · CONSEGUIR ALIMENTO", "images/scenes/paleo_02_caceria.png", "La caza exigía observar huellas, elegir herramientas y coordinarse. No era una acción aislada: la cooperación y la comunicación aumentaban las posibilidades de sobrevivir.", "audio/voice/scene_02.wav")
    play music "audio/amb_cave.wav" fadein 0.8
    call screen mini_story("PALEOLÍTICO · 3/4 · EL FUEGO REÚNE AL GRUPO", "images/scenes/paleo_03_fuego.png", "Alrededor del fuego, el grupo encontraba calor y protección. Compartir alimentos y conocimientos fortalecía la vida colectiva.", "audio/voice/scene_03.wav")
    play music "audio/amb_river.wav" fadein 0.8
    call screen mini_story("PALEOLÍTICO · 4/4 · VIVIR CON LOS RECURSOS", "images/scenes/paleo_04_recoleccion.png", "La naturaleza ofrecía alimento, agua y refugio, pero también imponía límites. Comprender el territorio era esencial para evitar riesgos y mantener al grupo.", "audio/voice/scene_04.wav")
    stop music fadeout 0.8
    scene bg cave with dissolve
    show screen hud("NIVEL 1 · PALEOLÍTICO")
    guide "NIVEL 1 DESBLOQUEADO: EL LEJANO PALEOLÍTICO."
    guide "Los primeros grupos humanos fabricaron herramientas rudimentarias, utilizaron pieles para protegerse y, posiblemente, aprendieron a manejar el fuego."
    guide "Pasar de la recolección a la caza exigió herramientas más precisas, cooperación y comunicación. La caza no era solo una hazaña individual: requería organización colectiva."
    guide "Pero la especialización de la caza también aumentó la presión sobre los ecosistemas. El libro menciona grandes acumulaciones de restos de animales como señales de una presión muy intensa sobre algunas especies."
    hide screen hud
    call quiz(
        "¿Qué hizo posible la caza organizada entre los primeros humanos?",
        ["A. La cooperación, la comunicación y herramientas",
         "B. La agricultura mecanizada",
         "C. La escritura de leyes"],
        correct=0,
        praise="¡Bien hecho! La supervivencia dependía tanto de la técnica como del trabajo colectivo.",
        hint="Pista: piensa en lo que necesita un grupo para coordinarse y cazar una presa.",
    )
    jump homo_sapiens

label homo_sapiens:
    play music "audio/amb_forest.wav" fadein 1.0
    call screen mini_story("HOMO SAPIENS · 1/4 · NUEVAS HABILIDADES", "images/scenes/homo_01_habilidades.png", "Con el tiempo, los grupos humanos perfeccionaron herramientas y aprendieron a aprovechar distintos recursos. La técnica amplió sus posibilidades de adaptación.", "audio/voice/scene_05.wav")
    play music "audio/amb_cave.wav" fadein 0.8
    call screen mini_story("HOMO SAPIENS · 2/4 · FABRICAR Y APRENDER", "images/scenes/homo_02_herramientas.png", "Golpear, tallar y dar forma a la piedra requería práctica. Las habilidades se compartían entre personas y generaciones, convirtiendo el aprendizaje en una ventaja colectiva.", "audio/voice/scene_06.wav")
    play music "audio/amb_forest.wav" fadein 0.8
    call screen mini_story("HOMO SAPIENS · 3/4 · COOPERAR", "images/scenes/homo_03_cooperacion.png", "La cooperación ayudaba a organizar la búsqueda de alimentos y a responder a los cambios del paisaje. La cultura no era solo una herramienta: también era conocimiento compartido.", "audio/voice/scene_07.wav")
    play music "audio/amb_river.wav" fadein 0.8
    call screen mini_story("HOMO SAPIENS · 4/4 · UN IMPACTO CRECIENTE", "images/scenes/homo_04_impacto.png", "Las técnicas más eficaces también podían aumentar la presión sobre las presas. Una innovación puede facilitar la supervivencia y, a la vez, transformar el equilibrio ecológico.", "audio/voice/scene_08.wav")
    stop music fadeout 0.8
    scene bg hunt with dissolve
    show screen hud("NIVEL 2 · HOMO SAPIENS")
    guide "NIVEL 2 DESBLOQUEADO: DEL HOMO SAPIENS AL NEOLÍTICO."
    guide "Según el recorrido del libro, el desarrollo cultural se aceleró con el Homo sapiens. Las herramientas ayudaron a adaptarse a ambientes distintos y a reducir la dependencia de una sola presa."
    guide "El final de la última glaciación transformó los paisajes: se expandieron los bosques y disminuyeron varias especies de grandes mamíferos. El agotamiento de la fauna pudo relacionarse con el perfeccionamiento de los instrumentos de caza."
    guide "También crecieron las expresiones simbólicas: las pinturas y los signos muestran que el ser humano no solo modificaba su entorno, sino que lo imaginaba y lo representaba."
    hide screen hud
    call quiz(
        "¿Qué relación plantea el capítulo entre herramientas y fauna?",
        ["A. Las herramientas no afectaban la caza",
         "B. El perfeccionamiento técnico pudo aumentar la presión sobre la fauna",
         "C. La fauna desapareció únicamente por la agricultura"],
        correct=1,
        praise="¡Correcto! Una innovación puede mejorar la adaptación y, al mismo tiempo, intensificar el impacto ambiental.",
        hint="Pista: el capítulo relaciona mejores instrumentos de caza con un rendimiento creciente sobre las presas.",
    )
    jump neolitico

label neolitico:
    play music "audio/amb_river.wav" fadein 1.0
    call screen mini_story("NEOLÍTICO · 1/4 · CULTIVAR", "images/scenes/neo_01_cultivar.png", "Algunas comunidades comenzaron a cuidar plantas y aprovechar sus ciclos. La obtención de alimentos dejó de depender únicamente de encontrar recursos silvestres.", "audio/voice/scene_09.wav")
    play music "audio/amb_forest.wav" fadein 0.8
    call screen mini_story("NEOLÍTICO · 2/4 · ANIMALES Y ALDEAS", "images/scenes/neo_02_domesticar.png", "La domesticación de animales y el cultivo favorecieron asentamientos más estables. Las personas construyeron viviendas y organizaron tareas para mantener a la comunidad.", "audio/voice/scene_10.wav")
    call screen mini_story("NEOLÍTICO · 3/4 · CAMBIAR EL PAISAJE", "images/scenes/neo_03_paisaje.png", "Los campos y las viviendas modificaron el territorio. Al seleccionar las especies útiles, las sociedades también cambiaron qué plantas y animales podían prosperar cerca de ellas.", "audio/voice/scene_11.wav")
    play music "audio/amb_river.wav" fadein 0.8
    call screen mini_story("NEOLÍTICO · 4/4 · BENEFICIOS Y COSTOS", "images/scenes/neo_04_costos.png", "Una producción más estable favoreció el crecimiento y nuevas formas de trabajo, pero también generó nuevas presiones sobre el suelo y los ecosistemas. Toda transformación trae oportunidades y responsabilidades.", "audio/voice/scene_12.wav")
    stop music fadeout 0.8
    scene bg village with dissolve
    show screen hud("NIVEL 3 · NEOLÍTICO")
    guide "NIVEL 3 DESBLOQUEADO: EL CERCANO NEOLÍTICO."
    guide "La domesticación de animales y la agricultura transformaron profundamente la subsistencia. Se aprovecharon plantas y animales, y surgieron herramientas como el arado, la rueda, los botes de vela y técnicas para trabajar metales."
    guide "La producción más estable favoreció el crecimiento de la población, el sedentarismo, los poblados y la acumulación de excedentes. Con ella se desarrolló una división del trabajo: alfarería, tejido, carpintería y minería, entre otras actividades."
    guide "El proceso no fue igual en todas partes: las condiciones de los ecosistemas influyeron en qué especies podían domesticarse y qué tecnologías se desarrollaban."
    guide "El cambio también tuvo costos. Al seleccionar plantas útiles, las sociedades empezaron a eliminar otras como 'malezas' y a llamar 'plagas' a especies que aprovechaban los cultivos. Son categorías ligadas al nuevo orden humano, no etiquetas neutrales de la naturaleza."
    hide screen hud
    call quiz(
        "¿Cuál fue una consecuencia importante de la revolución neolítica?",
        ["A. Desapareció toda transformación ambiental",
         "B. Agricultura y domesticación favorecieron sedentarismo y excedentes",
         "C. Todos los continentes desarrollaron exactamente la misma agricultura"],
        correct=1,
        praise="¡Exacto! La agricultura transformó la relación con el entorno y también la organización social.",
        hint="Pista: recuerda qué permitió producir alimentos con mayor estabilidad.",
    )
    jump final_reflexion

label final_reflexion:
    scene bg city with dissolve
    show screen hud("REFLEXIÓN FINAL")
    guide "ÚLTIMA PISTA: cada avance cultural abre posibilidades, pero también puede alterar los ecosistemas."
    guide "Desde la caza hasta la agricultura, las herramientas y las formas de organización cambiaron la relación humana con el medio."
    guide "La idea central de este recorrido es que la cultura y la naturaleza no son mundos separados: se transforman mutuamente."
    guide "La pregunta que deja el texto es cómo crear formas de organización y conocimientos capaces de sostener la vida sin profundizar la crisis ambiental."
    hide screen hud
    scene bg victory with fade
    call screen end_card
    return

# Repite la pregunta hasta acertar. Cada error cuenta como pista usada;
# el acierto suma 100 puntos.
label quiz(question, answers, correct, praise, hint):
    while renpy.call_screen("quiz_card", question, answers) != correct:
        play sound "audio/sfx_error.wav"
        $ hints_used += 1
        guide "[hint]"
    play sound "audio/sfx_correct.wav"
    $ score += 100
    guide "[praise]"
    return
