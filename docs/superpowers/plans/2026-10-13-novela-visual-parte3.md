# Plan de implementación · parte 3 de 3: contenido, web y entrega (Tareas 13–19)

> Continúa `2026-10-13-novela-visual-parte2.md`, con las mismas restricciones globales.

**Reglas de contenido**
- Los textos narrados son los del guion (`references/Guion_novela_visual_El_origenes_ecosistema_cultura.pdf`), copiados tal cual en cada `say` de una sola línea.
- Las fichas que el guion no redacta y el cierre van redactados aquí y los aprueba el equipo.
- Las posiciones de los marcadores se midieron sobre las imágenes ya procesadas (rejilla del 5 %). Si al verlas un marcador no cae sobre su elemento, se corrige con `uv run ilustraciones.py --rejilla <id>`.

**Plantilla de entrada de Internet Archive** (Figuier, *Primitive Man*, 1870). En cada tarea solo cambian `id`, `uso`, `tinta`, la hoja (`$NNN`), la figura y `rotar`/`recorte`/`encaje`/`centrado`:
```toml
url = "https://iiif.archive.org/iiif/primitiveman00figuiala$NNN/full/1800,/0/default.jpg"
pagina_fuente = "https://archive.org/details/primitiveman00figuiala"
autor = "Émile Bayard (dibujo); Louis Figuier (obra)"
anio = 1870
licencia = "Dominio público"
```
(Se usa `full/1800,` porque `full/full` da error 500 en algunas hojas.)

### Task 13: Capítulo 2 completo (prototipo) y aprobación del equipo

**Files:**
- Modify: `fuentes.toml`, `game/capitulos/cap2.rpy`, `tests/test_guion.py`, `game/tests/pruebas.rpy`
- Generated: imágenes de `cap2_*` y láminas, `game/audio/voz/cap2_*.ogg`, `manifest.json`

**Interfaces:**
- Consumes: todo el sistema (Tareas 8–12).
- Produces: el label `cap2` completo, que termina en `jump cap3`; ids `cap2_01`…`cap2_10`, `cap2_obs_*`, `cap2_quiz`, `cap2_quiz_porque`, `cap2_dec`, `cap2_dec_a/b/c`, `cap2_nota`, `cap2_clave`.

- [ ] **Step 1: Añadir la regla de longitud (Review Focus 4)**

Añadir a `tests/test_guion.py`:
```python
def test_bloques_caben_en_la_tarjeta():
    from generar_voz import leer_guion
    for ident, texto in leer_guion(JUEGO).items():
        limite = 55 if re.search(r"_\d\d$", ident) else 60
        assert len(texto.split()) <= limite, f"{ident} tiene {len(texto.split())} palabras (máximo {limite})"
```

- [ ] **Step 2: Registrar las imágenes del capítulo**

Añadir a `fuentes.toml`:
```toml
[[imagen]]
id = "cap2_rio"
uso = "fondo"
tinta = "glaciacion"
encaje = "editorial"
recorte = "auto"
url = "https://iiif.archive.org/iiif/primitiveman00figuiala$127/full/1800,/0/default.jpg"
pagina_fuente = "https://archive.org/details/primitiveman00figuiala"
autor = "Émile Bayard (dibujo); Louis Figuier (obra)"
obra = "Primitive Man, fig. 40: abrigo rocoso de Bruniquel (época del reno)"
anio = 1870
licencia = "Dominio público"
atribucion = "É. Bayard en L. Figuier, Primitive Man (1870), fig. 40. Internet Archive, dominio público."

[[imagen]]
id = "cap2_glaciacion"
uso = "fondo"
tinta = "glaciacion"
recorte = [63, 180, 2960, 1665]
url = "https://upload.wikimedia.org/wikipedia/commons/7/74/An_ideal_landscape_in_the_Quaternary_epoch_with_bears%2C_elks_Wellcome_V0023204.jpg"
pagina_fuente = "https://commons.wikimedia.org/wiki/File:An_ideal_landscape_in_the_Quaternary_epoch_with_bears,_elks_Wellcome_V0023204.jpg"
autor = "Édouard Riou (grabado, a partir de E. Meunier)"
obra = "La Terre avant le déluge (L. Figuier), lámina 10: paisaje ideal del Cuaternario"
anio = 1863
licencia = "CC BY 4.0"
atribucion = "É. Riou, La Terre avant le déluge (1863), lámina 10. Wellcome Collection, CC BY 4.0."

[[imagen]]
id = "cap2_bosque"
uso = "fondo"
tinta = "bosque"
recorte = "auto"
centrado = [0.5, 0.75]
url = "https://iiif.archive.org/iiif/primitiveman00figuiala$141/full/1800,/0/default.jpg"
pagina_fuente = "https://archive.org/details/primitiveman00figuiala"
autor = "Émile Bayard (dibujo); Louis Figuier (obra)"
obra = "Primitive Man, fig. 52: la caza en la época del reno"
anio = 1870
licencia = "Dominio público"
atribucion = "É. Bayard en L. Figuier, Primitive Man (1870), fig. 52. Internet Archive, dominio público."

[[imagen]]
id = "cap2_arte"
uso = "fondo"
tinta = "bosque"
encaje = "editorial"
recorte = "auto"
url = "https://iiif.archive.org/iiif/primitiveman00figuiala$153/full/1800,/0/default.jpg"
pagina_fuente = "https://archive.org/details/primitiveman00figuiala"
autor = "Émile Bayard (dibujo); Louis Figuier (obra)"
obra = "Primitive Man, fig. 68: artes del dibujo y la escultura en la época del reno"
anio = 1870
licencia = "Dominio público"
atribucion = "É. Bayard en L. Figuier, Primitive Man (1870), fig. 68. Internet Archive, dominio público."

[[imagen]]
id = "lamina_mamut"
uso = "lamina"
tinta = "glaciacion"
recorte = [1760, 880, 440, 320]
url = "https://upload.wikimedia.org/wikipedia/commons/7/74/An_ideal_landscape_in_the_Quaternary_epoch_with_bears%2C_elks_Wellcome_V0023204.jpg"
pagina_fuente = "https://commons.wikimedia.org/wiki/File:An_ideal_landscape_in_the_Quaternary_epoch_with_bears,_elks_Wellcome_V0023204.jpg"
autor = "Édouard Riou (grabado, a partir de E. Meunier)"
obra = "La Terre avant le déluge (L. Figuier), lámina 10: paisaje ideal del Cuaternario"
anio = 1863
licencia = "CC BY 4.0"
atribucion = "É. Riou, La Terre avant le déluge (1863), lámina 10. Wellcome Collection, CC BY 4.0."

[[imagen]]
id = "lamina_alce"
uso = "lamina"
tinta = "glaciacion"
recorte = [2340, 980, 340, 380]
url = "https://upload.wikimedia.org/wikipedia/commons/7/74/An_ideal_landscape_in_the_Quaternary_epoch_with_bears%2C_elks_Wellcome_V0023204.jpg"
pagina_fuente = "https://commons.wikimedia.org/wiki/File:An_ideal_landscape_in_the_Quaternary_epoch_with_bears,_elks_Wellcome_V0023204.jpg"
autor = "Édouard Riou (grabado, a partir de E. Meunier)"
obra = "La Terre avant le déluge (L. Figuier), lámina 10: paisaje ideal del Cuaternario"
anio = 1863
licencia = "CC BY 4.0"
atribucion = "É. Riou, La Terre avant le déluge (1863), lámina 10. Wellcome Collection, CC BY 4.0."

[[imagen]]
id = "lamina_rinoceronte"
uso = "lamina"
tinta = "glaciacion"
recorte = [1920, 1180, 420, 240]
url = "https://upload.wikimedia.org/wikipedia/commons/7/74/An_ideal_landscape_in_the_Quaternary_epoch_with_bears%2C_elks_Wellcome_V0023204.jpg"
pagina_fuente = "https://commons.wikimedia.org/wiki/File:An_ideal_landscape_in_the_Quaternary_epoch_with_bears,_elks_Wellcome_V0023204.jpg"
autor = "Édouard Riou (grabado, a partir de E. Meunier)"
obra = "La Terre avant le déluge (L. Figuier), lámina 10: paisaje ideal del Cuaternario"
anio = 1863
licencia = "CC BY 4.0"
atribucion = "É. Riou, La Terre avant le déluge (1863), lámina 10. Wellcome Collection, CC BY 4.0."

[[imagen]]
id = "lamina_bisonte"
uso = "lamina"
tinta = "archivo"
url = "https://upload.wikimedia.org/wikipedia/commons/2/2b/Altamira%2C_bison.jpg"
pagina_fuente = "https://commons.wikimedia.org/wiki/File:Altamira,_bison.jpg"
autor = "Artista del Paleolítico superior (cueva de Altamira)"
obra = "Bisonte de la cueva de Altamira (Cantabria)"
anio = "c. 15.000 a. C."
licencia = "Dominio público"
atribucion = "Bisonte de la cueva de Altamira. Wikimedia Commons, dominio público."

[[imagen]]
id = "lamina_levante"
uso = "lamina"
tinta = "archivo"
url = "https://upload.wikimedia.org/wikipedia/commons/6/65/Cova_dels_cavalls.jpg"
pagina_fuente = "https://commons.wikimedia.org/wiki/File:Cova_dels_cavalls.jpg"
autor = "EmparMM (fotografía)"
obra = "Figura antropomorfa, pintura rupestre de la Cova dels Cavalls (La Valltorta, Castellón)"
anio = "s. f."
licencia = "CC BY-SA 4.0"
atribucion = "EmparMM, «Cova dels cavalls». Wikimedia Commons, CC BY-SA 4.0 (imagen entintada, misma licencia)."
```
Run: `uv run ilustraciones.py`
Expected: `✓` en las 9 imágenes nuevas. Abre `game/images/fondos/cap2_*.jpg` y `game/images/laminas/*.jpg` y comprueba que:
- no hay pies de imagen;
- el mamut, el alce y el rinoceronte quedan centrados en sus láminas;
- `cap2_rio` y `cap2_arte` dejan papel liso a la derecha.

Si un recorte de lámina queda corrido, se ajusta su `recorte` (coordenadas del original de 3150×2133).

- [ ] **Step 3: Escribir el capítulo**

`game/capitulos/cap2.rpy` (reemplaza el esqueleto):
```renpy
## Capítulo 2 · Del Homo sapiens al Neolítico · pp. 13–17 · Presenta María Fernanda Cano Cobo.
## Texto: guion del equipo. Fichas de observación: redactadas a partir de las pp. 13–17.

define cap2_puntos_glaciacion = [
    Punto("mamut", 0.660, 0.517, "Mamut lanudo", "cap2_obs_mamut"),
    Punto("alce", 0.825, 0.583, "Alce gigante", "cap2_obs_alce"),
    Punto("rinoceronte", 0.692, 0.649, "Rinoceronte lanudo", "cap2_obs_rinoceronte"),
]
define cap2_puntos_arte = [
    Punto("realismo", 0.275, 0.270, "Bisonte de Altamira: realismo", "cap2_obs_realismo"),
    Punto("abstraccion", 0.200, 0.720, "Figuras levantinas: abstracción", "cap2_obs_abstraccion"),
]

label cap2:
    $ abrir_capitulo("cap2")
    play music "audio/ambiente/rio.wav" fadein 2.0 if_changed
    scene cap2_rio at paneo with fundido
    portada "Capítulo 2. Del Homo sapiens al Neolítico. Esta parte sigue los cambios del ambiente, las técnicas de caza y la cultura, hasta el problema de cómo regular el medio cuando la fauna empieza a agotarse." id cap2_portada

    # Escena 2.1 · Junto a los ríos
    $ pagina = "p. 13"
    nl "Para Ángel Maya, con el Homo sapiens se consolida la evolución histórica y se acelera la cultura. Las formas de vida cambian junto con las capacidades técnicas y sociales." id cap2_01
    nl "Los ríos ofrecieron condiciones favorables para asentarse temporalmente o permanecer en ciertos lugares. En los periodos que menciona el libro, la población creció y se desarrollaron distintas formas de organización." id cap2_02
    $ pagina = "pp. 13–14"
    nl "El arco y el lanzador de venablos ampliaron las posibilidades de caza. La obtención de alimento dependía menos de una sola presa o de un único ambiente, aunque seguía ligada a los recursos disponibles." id cap2_03
    $ pagina = "p. 14"
    nl "El autor cuestiona la idea de que el cazador viviera necesariamente al borde del hambre: estima entre tres y cuatro horas diarias de caza, frente a unas sesenta horas semanales de trabajo para un agricultor." id cap2_04

    # Escena 2.2 · El fin de la glaciación
    play music "audio/ambiente/bosque.wav" fadein 2.0 if_changed
    scene cap2_glaciacion at paneo with transformacion
    $ pagina = "pp. 14–15"
    n "Para mantener las cuotas de caza, la densidad de población debía ser muy baja. El libro ofrece como referencia unos tres habitantes por kilómetro cuadrado." id cap2_05
    $ pagina = "p. 15"
    n "El fin de la glaciación, hace unos 13.000 años según el texto, llevó los bosques a las llanuras. Desaparecieron animales como el mamut lanudo, el rinoceronte lanudo y el alce gigante." id cap2_06
    call explorar(cap2_puntos_glaciacion)
    scene cap2_bosque at paneo with transformacion
    n "El autor plantea que la actividad humana pudo influir en esas desapariciones, por ejemplo mediante el uso del fuego para acorralar manadas. La explicación no atribuye todo al ser humano: el cambio climático también forma parte del contexto." id cap2_07
    $ pagina = "pp. 15–16"
    n "El capítulo describe un círculo de agotamiento y técnica: de la lanza se pasó a los dardos y luego a las flechas, aumentando la eficacia de la caza. También cambiaron las relaciones sociales, con alianzas, comercio y guerra." id cap2_08

    # Escena 2.3 · La cueva pintada
    play music "audio/ambiente/cueva.wav" fadein 2.0 if_changed
    scene cap2_arte at paneo with fundido
    $ pagina = "pp. 16–17"
    nl "El capítulo presenta al ser humano como constructor de símbolos. Las imágenes pasan del realismo asociado al arte magdaleniense a formas más abstractas en el arte levantino." id cap2_09
    $ pagina = "p. 17"
    nl "El autor vincula el instrumento y el símbolo: el instrumento condensa una teoría práctica, mientras que el símbolo puede abrir un camino hacia nuevas formas de acción." id cap2_10
    call explorar(cap2_puntos_arte)

    # Quiz, decisión, nota de campo e idea clave
    scene cap2_bosque at paneo with fundido
    menu (screen="quiz", quiz="cap2_quiz", pagina="p. 15"):
        pregunta "¿Qué relación plantea el capítulo entre las armas y la fauna?" id cap2_quiz
        "Las mejores armas permitieron cazar menos y proteger las manadas.":
            pass
        "Cuando la fauna se agota se crean armas más potentes, que la agotan aún más." (correcta=True):
            pass
        "Las armas no influyeron: la fauna desapareció solo por el clima.":
            pass
    porque "El autor describe un círculo en el que la lanza da paso a dardos y flechas cada vez más eficaces para agotar los cotos de caza. El clima también influyó, pero no explica por sí solo el proceso." id cap2_quiz_porque

    menu (screen="decision", pagina="pp. 14–15"):
        dilema "¿Por qué crees que el ser humano empezó a cultivar?" id cap2_dec
        "Porque cazar era agotador y pasaban hambre.":
            segun "El libro cuestiona esta explicación: estima que la caza podía ocupar entre tres y cuatro horas diarias." id cap2_dec_a
        "Para tener más tiempo libre.":
            segun "El texto compara esa actividad con unas sesenta horas semanales de trabajo agrícola." id cap2_dec_b
        "Porque la fauna se agotaba y hacía falta otra forma de regular el medio.":
            segun "Es la lectura del autor: la agricultura como una forma más compleja de regular el medio." id cap2_dec_c

    nota "El libro sitúa al Homo sapiens hace unos 50.000 años. Los fósiles más antiguos conocidos de Homo sapiens, en Jebel Irhoud, Marruecos, tienen unos 300.000 años." (show_fuente="Hublin et al. (2017), Nature") id cap2_nota
    clave "Cada avance técnico transformó el medio, y cada cambio del medio obligó a reorganizar la sociedad." id cap2_clave
    jump cap3

label cap2_obs_mamut:
    ficha "El mamut lanudo había sido parte fundamental de la dieta en el periodo anterior. Con el cambio de clima y el avance de los bosques, desapareció." (show_lamina="lamina_mamut", show_titulo="Mamut lanudo", show_leyenda="Grabado de É. Riou, 1863.", show_pagina="pp. 13–15") id cap2_obs_mamut
    return

label cap2_obs_alce:
    ficha "Desapareció al terminar la glaciación, junto al mamut y al rinoceronte lanudos. El autor sugiere que la caza con fuego pudo influir." (show_lamina="lamina_alce", show_titulo="Alce gigante", show_leyenda="Megaloceros. Grabado de É. Riou, 1863.", show_pagina="p. 15") id cap2_obs_alce
    return

label cap2_obs_rinoceronte:
    ficha "El rinoceronte lanudo tampoco sobrevivió. En cambio, según el libro, el caballo, el ganado vacuno, los elefantes y los rinocerontes sí lo hicieron." (show_lamina="lamina_rinoceronte", show_titulo="Rinoceronte lanudo", show_leyenda="Grabado de É. Riou, 1863.", show_pagina="p. 15") id cap2_obs_rinoceronte
    return

label cap2_obs_realismo:
    ficha "Las pinturas magdalenienses aludían a una actividad inmediata, casi identificable: un animal concreto, observado con precisión de cazador." (show_lamina="lamina_bisonte", show_titulo="Realismo", show_leyenda="Bisonte pintado en la cueva de Altamira (Cantabria).", show_pagina="p. 16") id cap2_obs_realismo
    return

label cap2_obs_abstraccion:
    ficha "Las figuras más tardías de la España oriental son símbolos que relacionan muchas actividades. Para el autor, la abstracción es una conquista posterior, no una decadencia." (show_lamina="lamina_levante", show_titulo="Abstracción", show_leyenda="Cova dels Cavalls (Castellón). Foto: EmparMM, CC BY-SA 4.0.", show_pagina="p. 16") id cap2_obs_abstraccion
    return
```

- [ ] **Step 4: Comprobar las reglas del guion**

Run: `uv run pytest -q`
Expected: `39 passed`.

- [ ] **Step 5: Generar las voces del capítulo**

Run: `uv run --group voz generar_voz.py --revisar`
Expected: lista con `intro_portada`, `cap1_portada`, `cap2_*`… (la primera vez instala Kokoro y PyTorch para CPU, unos minutos).
Run: `uv run --group voz generar_voz.py && uv run --group voz generar_voz.py --duracion`
Expected: `Generada: cap2_01.ogg`, etc. La duración de `cap2` debería ser de unos 4–5 min. Si pasa de 5,5 min, avisar a María Fernanda antes de seguir.

- [ ] **Step 6: Añadir el recorrido del capítulo y las capturas**

Añadir a `game/tests/pruebas.rpy`:
```renpy
    testcase cap2:
        run Start("cap2")
        assert screen "portada" timeout 10
        advance until screen "explorar" timeout 180
        click "Alce gigante"
        assert screen "ficha" timeout 5
        click "Volver al paisaje"
        click "Continuar"
        advance until screen "explorar" timeout 180
        click "Continuar"
        advance until screen "quiz" timeout 180
        click "Cuando la fauna se agota"
        assert eval (respondidas.get("cap2_quiz") is True) timeout 5
        advance until screen "decision" timeout 60
        click "Porque la fauna se agotaba"
        assert screen "segun" timeout 5
        advance until label cap3 timeout 180

    testcase capturas_cap2:
        run Start("cap2")
        assert screen "portada" timeout 10
        pause 1.5
        $ renpy.screenshot(config.basedir + "/.cache/capturas/cap2_1_portada.png")
        advance
        pause 1.5
        $ renpy.screenshot(config.basedir + "/.cache/capturas/cap2_2_bloque_lateral.png")
        advance until screen "explorar" timeout 180
        pause 1.5
        $ renpy.screenshot(config.basedir + "/.cache/capturas/cap2_3_explorar.png")
        click "Alce gigante"
        pause 1.5
        $ renpy.screenshot(config.basedir + "/.cache/capturas/cap2_4_ficha.png")
        click "Volver al paisaje"
        click "Continuar"
        advance until screen "quiz" timeout 240
        pause 1.0
        $ renpy.screenshot(config.basedir + "/.cache/capturas/cap2_5_quiz.png")
        click "Las mejores armas"
        pause 1.0
        $ renpy.screenshot(config.basedir + "/.cache/capturas/cap2_6_retro.png")
```
Run: `./probar_juego.sh cap2 && ./probar_juego.sh capturas_cap2`
Expected: `Status: PASSED` en ambos y 6 PNG en `.cache/capturas/`.

- [ ] **Step 7: Puerta de aprobación (humana)**

Mostrar las 6 capturas (en el compañero visual o con la ruta) y la duración del Cap. 2. **No seguir hasta que el usuario confirme**, en nombre de María Fernanda, el estilo, el texto y la voz. Los ajustes que pida se aplican aquí y se repiten los Steps 4–6.

- [ ] **Step 8: Commit**

```bash
git add -A
git commit -q -m "feat(cap2): Del Homo sapiens al Neolítico completo con voces, observaciones, quiz y decisión" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 14: Introducción

**Files:** Modify `fuentes.toml`, `game/capitulos/intro.rpy`, `game/tests/pruebas.rpy`.

- [ ] **Step 1: Registrar las imágenes**

```toml
[[imagen]]
id = "intro_venecia"
uso = "fondo"
tinta = "archivo"
recorte = [1000, 650, 1938, 1090]
url = "https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e2/Jacopo_de%27_Barbari_-_View_of_Venice_-_Google_Art_Project.jpg/3840px-Jacopo_de%27_Barbari_-_View_of_Venice_-_Google_Art_Project.jpg"
pagina_fuente = "https://commons.wikimedia.org/wiki/File:Jacopo_de%27_Barbari_-_View_of_Venice_-_Google_Art_Project.jpg"
autor = "Jacopo de' Barbari"
obra = "Veduta di Venezia (vista de Venecia)"
anio = 1500
licencia = "Dominio público"
atribucion = "Jacopo de' Barbari, vista de Venecia (1500). Google Art Project, dominio público."
notas = "Recorte sin el título VENETIE MD ni los vientos de la parte inferior."

[[imagen]]
id = "intro_herramientas"
uso = "fondo"
tinta = "archivo"
encaje = "editorial"
recorte = [250, 470, 2000, 2760]
url = "https://upload.wikimedia.org/wikipedia/commons/8/82/Reliquiae_aquitanicae--pl._A-17--BHL20495702.jpg"
pagina_fuente = "https://commons.wikimedia.org/wiki/File:Reliquiae_aquitanicae--pl._A-17--BHL20495702.jpg"
autor = "Édouard Lartet y Henry Christy (ed. T. R. Jones)"
obra = "Reliquiae Aquitanicae, lámina A-17: hachas de piedra de Le Moustier"
anio = 1875
licencia = "Dominio público"
atribucion = "Lartet y Christy, Reliquiae Aquitanicae (1875), lám. A-17. Biodiversity Heritage Library, dominio público."
notas = "Sin el encabezado ni los nombres del impresor."

[[imagen]]
id = "intro_londres"
uso = "fondo"
tinta = "industria"
centrado = [0.5, 0.45]
url = "https://upload.wikimedia.org/wikipedia/commons/0/0f/YCBA_London_a_Pilgrimage_06_%28cropped%29.jpg"
pagina_fuente = "https://commons.wikimedia.org/wiki/File:YCBA_London_a_Pilgrimage_06_(cropped).jpg"
autor = "Gustave Doré (grabado de A. F. Pannemaker)"
obra = "London: A Pilgrimage, «Over London – by Rail»"
anio = 1872
licencia = "Dominio público"
atribucion = "G. Doré, «Over London – by Rail», London: A Pilgrimage (1872). Yale Center for British Art, dominio público."
```
Run: `uv run ilustraciones.py && uv run ilustraciones.py --rejilla intro_venecia`
Expected: 3 fondos nuevos. En `.cache/rejilla_intro_venecia.png`, el Palacio Ducal (edificio blanco con arcadas junto al campanario) queda cerca de (34 %, 37 %), los barcos de (57 %, 52 %) y el agua abierta de (78 %, 84 %). Si no, se corrigen los `Punto`. En `intro_herramientas` no debe verse el encabezado "RELIQUIÆ AQUITANICÆ"; si se ve, se sube el `y` del recorte.

- [ ] **Step 2: Escribir la Introducción**

`game/capitulos/intro.rpy`:
```renpy
## Introducción · pp. 6–9 · Presenta Elkin Samir Angulo Panameño.
## Texto: guion del equipo. Fichas: descripciones del guion para cada punto.

define intro_puntos_venecia = [
    Punto("palacio", 0.34, 0.37, "Palacio Ducal y San Marcos", "intro_obs_palacio"),
    Punto("barcos", 0.57, 0.52, "Barcos y mercancías", "intro_obs_barcos"),
    Punto("laguna", 0.78, 0.84, "La laguna", "intro_obs_laguna"),
]

label intro:
    $ abrir_capitulo("intro")
    play music "audio/ambiente/rio.wav" fadein 2.0 if_changed
    scene intro_venecia at paneo with fundido
    portada "Introducción: Los orígenes, del ecosistema a la cultura. En esta parte veremos por qué la historia humana no puede comprenderse sin considerar la relación entre sociedad, tecnología y ecosistemas." id intro_portada

    # Escena I1 · La historia vista desde arriba
    $ pagina = "p. 6"
    n "La dimensión ambiental apenas empieza a incorporarse a los métodos con los que estudiamos la historia. Mirar el pasado exige preguntarse no solo qué hicieron las personas, sino también en qué condiciones vivían." id intro_01
    n "Cada época interpreta el pasado desde las ideas de su propio tiempo. Ángel Maya recuerda que Tito Livio estudiaba la historia antigua buscando comprender los males de su presente." id intro_02
    $ pagina = "p. 8"
    n "Durante mucho tiempo, la historia se narró desde la cúspide: caudillos, gobernantes y clases dirigentes ocupaban el centro del relato, mientras otras condiciones quedaban en segundo plano." id intro_03
    n "El ejemplo de Venecia lo muestra con claridad: Sabellicus narró su historia sin mencionar el comercio de la sal, aunque ese recurso ayudaba a sostener su poder." id intro_04
    call explorar(intro_puntos_venecia)

    # Escena I2 · Testimonios mudos
    stop music fadeout 2.0
    scene intro_herramientas at paneo with fundido
    nl "Los hallazgos arqueológicos añadieron otra clase de evidencia: herramientas y objetos que permiten reconstruir aspectos de la vida de sociedades que no dejaron relatos escritos." id intro_05
    nl "Ángel Maya llama a estos objetos «testimonios mudos de la historia». Su presencia ayuda a estudiar cómo las sociedades desarrollaron técnicas para relacionarse con el entorno." id intro_06
    nl "La tesis que guía el libro es que la organización social está íntimamente vinculada a la transformación tecnológica de los ecosistemas. Sociedad, técnica y naturaleza no son historias separadas." id intro_07
    $ pagina = "p. 9"
    nl "Por eso, imaginar la historia como un escenario sin raíces en el medio es una trampa cultural. La crisis ambiental tampoco se resuelve únicamente con más tecnología: requiere pensar qué tipo de sociedad la utiliza." id intro_08

    # Escena I3 · Una crisis planetaria
    scene intro_londres at paneo with transformacion
    n "El problema ambiental actual obliga a revisar cómo contamos la historia. No basta con describir los cambios técnicos: hay que comprender cómo se relacionan con la organización de la sociedad y con los ecosistemas que la sostienen." id intro_09

    menu (screen="quiz", quiz="intro_quiz", pagina="p. 8"):
        pregunta "Sabellicus escribió la historia de Venecia sin mencionar el comercio de la sal. ¿Qué problema señala el autor con ese ejemplo?" id intro_quiz
        "Una historia contada solo desde la política, que deja fuera la economía y los recursos que la sostenían." (correcta=True):
            pass
        "Que la sal no era importante para Venecia.":
            pass
        "Que los historiadores antiguos no usaban documentos escritos.":
            pass
    porque "El ejemplo muestra cómo una historia escrita desde la cúspide puede omitir fenómenos económicos y recursos del medio que sostienen el poder." id intro_quiz_porque

    menu (screen="decision", pagina="pp. 7–9"):
        dilema "Para entender la crisis ambiental de hoy, ¿por dónde empezarías?" id intro_dec
        "Por la tecnología.":
            segun "Según el libro, el problema no se resuelve simplemente con medidas tecnológicas." id intro_dec_a
        "Por la naturaleza.":
            segun "El autor critica el reduccionismo ecologista: no es un problema exclusivo de los ecosistemas naturales." id intro_dec_b
        "Por la relación entre sociedad, tecnología y ecosistemas.":
            segun "Es el enfoque que propone el libro." id intro_dec_c

    clave "La historia humana no ocurre en un escenario vacío: sociedad, técnica y ecosistemas se transforman juntos." id intro_clave
    jump cap1

label intro_obs_palacio:
    ficha "El Palacio Ducal y la plaza de San Marcos representan el poder político que solían destacar las crónicas." (show_titulo="Palacio Ducal y San Marcos", show_pagina="p. 8") id intro_obs_palacio
    return

label intro_obs_barcos:
    ficha "Los barcos y las mercancías permiten observar el comercio que la narración histórica dejó fuera, como el de la sal." (show_titulo="Barcos y mercancías", show_pagina="p. 8") id intro_obs_barcos
    return

label intro_obs_laguna:
    ficha "La laguna muestra el medio natural que hizo posible la ciudad y parte de su actividad comercial." (show_titulo="La laguna", show_pagina="pp. 8–9") id intro_obs_laguna
    return
```

- [ ] **Step 3: Pruebas, voces y recorrido**

Añadir a `pruebas.rpy`:
```renpy
    testcase intro:
        run Start("intro")
        assert screen "portada" timeout 10
        advance until screen "explorar" timeout 180
        click "La laguna"
        assert screen "ficha" timeout 5
        click "Volver al paisaje"
        click "Continuar"
        advance until screen "quiz" timeout 240
        click "Una historia contada solo desde la política"
        assert eval (respondidas.get("intro_quiz") is True) timeout 5
        advance until screen "decision" timeout 60
        click "Por la relación"
        advance until label cap1 timeout 120
```
Run: `uv run pytest -q && uv run --group voz generar_voz.py && ./probar_juego.sh intro`
Expected: `39 passed`, voces `intro_*` generadas y `Status: PASSED`.

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -q -m "feat(intro): Introducción completa con Venecia, testimonios mudos y crisis planetaria" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 15: Capítulo 1

**Files:** Modify `fuentes.toml`, `game/capitulos/cap1.rpy`, `game/tests/pruebas.rpy`.

- [ ] **Step 1: Registrar las imágenes**

Usa la plantilla de Internet Archive para `cap1_fuego` (hoja 71, `rotar = 90`, `recorte = "auto"`, tinta `sabana`, obra "Primitive Man, fig. 7: la producción del fuego"), `cap1_caza` (hoja 83, `rotar = 90`, `recorte = "auto"`, tinta `glaciacion`, obra "Primitive Man, fig. 16: el hombre en la época del gran oso y el mamut"), `lamina_ciervo` (`uso = "lamina"`, hoja 141, `recorte = [100, 1560, 800, 560]`, tinta `glaciacion`, obra "Primitive Man, fig. 52: la caza en la época del reno (detalle del ciervo)") y `lamina_reno` (`uso = "lamina"`, hoja 123, `recorte = [160, 560, 860, 1100]`, tinta `glaciacion`, obra "Primitive Man, fig. 39: el hombre de la época del reno (detalle)"). La atribución sigue el patrón "É. Bayard en L. Figuier, Primitive Man (1870), fig. N. Internet Archive, dominio público.". Y el mapa:
```toml
[[imagen]]
id = "cap1_mapa"
uso = "mapa"
tinta = "glaciacion"
mapa = [-15, 20, 135, 75]
url = "https://naciscdn.org/naturalearth/110m/physical/ne_110m_land.zip"
pagina_fuente = "https://www.naturalearthdata.com/downloads/110m-physical-vectors/"
autor = "Natural Earth"
obra = "Land, 1:110m"
anio = "s. f."
licencia = "Dominio público"
atribucion = "Mapa dibujado con datos de Natural Earth (naturalearthdata.com), dominio público."
```
Run: `uv run ilustraciones.py`
Expected: el ciervo centrado en `lamina_ciervo` y el cazador en `lamina_reno`, ajustando los recortes si hace falta. El mapa muestra Europa, Asia y el norte de África con retícula.

- [ ] **Step 2: Escribir el capítulo**

`game/capitulos/cap1.rpy`:
```renpy
## Capítulo 1 · El lejano Paleolítico · pp. 10–12 · Presenta Sebastián Bolaños Morales.
## Texto: guion del equipo. Fichas del mapa: redactadas a partir de la p. 12.
## Posiciones del mapa: ilustraciones.posicion_en_mapa(lon, lat, (-15, 20, 135, 75)).

define cap1_puntos_mapa = [
    Punto("china", 0.811, 0.638, "China: ciervos", "cap1_obs_china"),
    Punto("espana", 0.102, 0.583, "España: toros y caballos", "cap1_obs_espana"),
    Punto("rusia", 0.313, 0.450, "Rusia y Europa Central: mamuts", "cap1_obs_rusia"),
    Punto("francia", 0.139, 0.511, "Francia: renos", "cap1_obs_francia"),
]

label cap1:
    $ abrir_capitulo("cap1")
    play music "audio/ambiente/cueva.wav" fadein 2.0 if_changed
    scene cap1_fuego at paneo with fundido
    portada "Capítulo 1. El lejano Paleolítico. Veremos cómo las herramientas, la adaptación y la cooperación ampliaron la capacidad humana para sobrevivir y ejercer presión sobre otros seres vivos." id cap1_portada

    # Escena 1.1 · Antes de la historia
    $ pagina = "p. 10"
    n "Desde la perspectiva ambiental que presenta Ángel Maya, la historia comienza con el Homo sapiens. Antes de ese punto existe una zona ambigua entre la evolución biológica y la historia propiamente dicha." id cap1_01
    n "Los instrumentos rudimentarios, como los raspadores, aparecen en el registro del Pleistoceno. El libro menciona también la posibilidad de que el hombre de Pekín utilizara el fuego como defensa hace unos 500.000 años." id cap1_02
    n "Las herramientas y las pieles ayudaron a enfrentar condiciones ambientales que ya no resultaban propicias. La supervivencia empezó a depender también de recursos técnicos y de formas de adaptación cultural." id cap1_03
    $ pagina = "pp. 10–11"
    n "Al pasar de ambientes boscosos a espacios abiertos, los homínidos tuvieron que recorrer distancias y cooperar. Sin garras ni grandes colmillos, compensaron parte de sus limitaciones mediante instrumentos y organización." id cap1_04

    # Escena 1.2 · La caza, empresa colectiva
    play music "audio/ambiente/bosque.wav" fadein 2.0 if_changed
    scene cap1_caza at paneo with fundido
    $ pagina = "p. 11"
    n "Las primeras formas de depredación incluyeron animales pequeños y carroña. La dieta mixta dio a los grupos mayor autonomía frente a los recursos inmediatos del entorno." id cap1_05
    n "La caza de presas mayores era una empresa colectiva: requería instrumentos, organización y comunicación. Esa cooperación contribuyó a que los grupos pudieran extenderse fuera de regiones tropicales." id cap1_06
    n "La capacidad de cazar no dependía únicamente de la fuerza individual. El grupo compensaba la ausencia de garras o colmillos mediante la coordinación y el uso de herramientas." id cap1_07
    $ pagina = "p. 12"
    n "El libro describe una especialización regional de la caza: ciervos en China; toros y caballos en España; mamuts en Rusia y Europa Central; y renos en Francia." id cap1_08

    # Escena 1.3 · Mapa de la especialización
    scene cap1_mapa with transformacion
    n "Ángel Maya destaca la magnitud de algunos conjuntos de restos animales: cien mil caballos en Solutré y mil mamuts en Predmost. El autor interpreta esos casos como una presión insólita sobre los ecosistemas, que llega a llamar «una especie de ecocidio»." id cap1_09
    call explorar(cap1_puntos_mapa)

    scene cap1_caza at paneo with fundido
    menu (screen="quiz", quiz="cap1_quiz", pagina="p. 11"):
        pregunta "¿Por qué la caza, a diferencia de la primera depredación, exigió organización colectiva?" id cap1_quiz
        "Porque se hacía con instrumentos y no con garras o colmillos, y había que coordinar al grupo." (correcta=True):
            pass
        "Porque ya había cultivos que proteger.":
            pass
        "Porque las presas eran pequeñas y abundantes.":
            pass
    porque "Sin órganos especializados, el grupo compensaba con instrumentos, organización y comunicación. Cuanto mayor y más peligrosa era la presa, más coordinación exigía." id cap1_quiz_porque

    menu (screen="decision", pagina="p. 12"):
        dilema "Cada año, una gran manada de caballos pasa por el mismo valle. ¿Qué hace el grupo?" id cap1_dec
        "Cazar todos los que pueda.":
            segun "El libro presenta los restos de Solutré como señal de una caza selectiva de gran magnitud y de una presión creciente." id cap1_dec_a
        "Cazar solo lo necesario.":
            segun "Esta opción permite discutir el límite, pero el libro no describe cuotas de caza para este periodo; destaca la presión creciente sobre algunas especies." id cap1_dec_b
        "Seguir la manada a nuevas tierras.":
            segun "La extensión hacia nuevas zonas dio origen a culturas prehistóricas y llevó la presión a otros ecosistemas." id cap1_dec_c

    nota "El libro describe a los neandertales encorvados y arrastrando los pies. Esa imagen procede de una reconstrucción de 1911 hecha a partir de un esqueleto con artritis. Hoy se sabe que caminaban erguidos y fabricaban herramientas complejas." (show_fuente="Smithsonian, Human Origins Program") id cap1_nota
    clave "Sin garras ni colmillos, los seres humanos se adaptaron mediante instrumentos y cooperación; al especializarse en la caza, empezaron a ejercer una presión importante sobre algunos ecosistemas." id cap1_clave
    jump cap2

label cap1_obs_china:
    ficha "En la actual China, la caza se concentró en los ciervos. Cada región ofrecía presas distintas y, con ellas, técnicas distintas." (show_lamina="lamina_ciervo", show_titulo="China: ciervos", show_leyenda="Ciervo. Grabado de É. Bayard, 1870.", show_pagina="p. 12") id cap1_obs_china
    return

label cap1_obs_espana:
    ficha "En la península ibérica se cazaron toros y caballos. En cuevas como Altamira quedaron pintados grandes bóvidos." (show_lamina="lamina_bisonte", show_titulo="España: toros y caballos", show_leyenda="Bisonte de la cueva de Altamira (Cantabria).", show_pagina="p. 12") id cap1_obs_espana
    return

label cap1_obs_rusia:
    ficha "En Rusia y Europa Central, el mamut fue la gran presa. En Predmost se hallaron restos de mil mamuts." (show_lamina="lamina_mamut", show_titulo="Rusia y Europa Central: mamuts", show_leyenda="Mamut lanudo. Grabado de É. Riou, 1863.", show_pagina="p. 12") id cap1_obs_rusia
    return

label cap1_obs_francia:
    ficha "En el actual territorio de Francia predominó la caza del reno. Este grabado de 1870 imagina a uno de esos cazadores." (show_lamina="lamina_reno", show_titulo="Francia: renos", show_leyenda="Cazador de la época del reno. Grabado de É. Bayard, 1870.", show_pagina="p. 12") id cap1_obs_francia
    return
```

- [ ] **Step 3: Pruebas, voces y recorrido**

Añadir a `pruebas.rpy`:
```renpy
    testcase cap1:
        run Start("cap1")
        assert screen "portada" timeout 10
        advance until screen "explorar" timeout 240
        click "China: ciervos"
        assert screen "ficha" timeout 5
        click "Volver al paisaje"
        click "Continuar"
        advance until screen "quiz" timeout 60
        click "Porque se hacía con instrumentos"
        assert eval (respondidas.get("cap1_quiz") is True) timeout 5
        advance until screen "decision" timeout 60
        click "Seguir la manada"
        advance until label cap2 timeout 120
```
Run: `uv run pytest -q && uv run --group voz generar_voz.py && ./probar_juego.sh cap1`
Expected: `39 passed` y `Status: PASSED`.

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -q -m "feat(cap1): El lejano Paleolítico completo con mapa de especialización" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 16: Capítulo 3

**Files:** Modify `fuentes.toml`, `game/capitulos/cap3.rpy`, `game/tests/pruebas.rpy`.

- [ ] **Step 1: Registrar las imágenes**

Con la plantilla de Internet Archive:
- `cap3_poblado`: hoja 289, `rotar = 90`, `recorte = "auto"`, tinta `neolitico`, obra "Primitive Man, fig. 149: aldea lacustre suiza (Edad del Bronce)".
- `cap3_huertos`: hoja 337, `rotar = 90`, `recorte = "auto"`, tinta `neolitico`, obra "Primitive Man, fig. 207: el cultivo de huertos (Edad del Bronce)".
- `lamina_alfarero`: `uso = "lamina"`, hoja 87, `rotar = 90`, `recorte = "auto"`, tinta `neolitico`, obra "Primitive Man, fig. 17: el primer alfarero".
- `lamina_hacha`: `uso = "lamina"`, hoja 205, `rotar = 90`, `recorte = "auto"`, tinta `neolitico`, obra "Primitive Man, fig. 107: fabricación y pulido de las hachas de piedra".

Y además:
```toml
[[imagen]]
id = "cap3_mapa"
uso = "mapa"
tinta = "neolitico"
mapa = [-120, -40, 80, 60]
url = "https://naciscdn.org/naturalearth/110m/physical/ne_110m_land.zip"
pagina_fuente = "https://www.naturalearthdata.com/downloads/110m-physical-vectors/"
autor = "Natural Earth"
obra = "Land, 1:110m"
anio = "s. f."
licencia = "Dominio público"
atribucion = "Mapa dibujado con datos de Natural Earth (naturalearthdata.com), dominio público."

[[imagen]]
id = "lamina_trigo"
uso = "lamina"
tinta = "neolitico"
url = "https://upload.wikimedia.org/wikipedia/commons/c/cb/Illustration_Triticum_aestivum0.jpg"
pagina_fuente = "https://commons.wikimedia.org/wiki/File:Illustration_Triticum_aestivum0.jpg"
autor = "Otto Wilhelm Thomé"
obra = "Flora von Deutschland, Österreich und der Schweiz: Triticum aestivum"
anio = 1885
licencia = "Dominio público"
atribucion = "O. W. Thomé, Flora von Deutschland (1885), trigo. Wikimedia Commons, dominio público."

[[imagen]]
id = "lamina_cebada"
uso = "lamina"
tinta = "neolitico"
url = "https://upload.wikimedia.org/wikipedia/commons/c/c4/Illustration_Hordeum_vulgare0.jpg"
pagina_fuente = "https://commons.wikimedia.org/wiki/File:Illustration_Hordeum_vulgare0.jpg"
autor = "Otto Wilhelm Thomé"
obra = "Flora von Deutschland, Österreich und der Schweiz: Hordeum vulgare"
anio = 1885
licencia = "Dominio público"
atribucion = "O. W. Thomé, Flora von Deutschland (1885), cebada. Wikimedia Commons, dominio público."

[[imagen]]
id = "lamina_maiz"
uso = "lamina"
tinta = "neolitico"
url = "https://upload.wikimedia.org/wikipedia/commons/7/78/Aztecs_storing_maize.jpg"
pagina_fuente = "https://commons.wikimedia.org/wiki/File:Aztecs_storing_maize.jpg"
autor = "Bernardino de Sahagún y colaboradores nahuas"
obra = "Códice Florentino: almacenamiento del maíz"
anio = "c. 1577"
licencia = "Dominio público"
atribucion = "Códice Florentino (c. 1577), almacenamiento del maíz. Wikimedia Commons, dominio público."

[[imagen]]
id = "lamina_llama"
uso = "lamina"
tinta = "neolitico"
url = "https://thumb.wikimedia.org/wikipedia/commons/thumb/2/28/Engraving_of_a_Llama_Wellcome_L0032831.jpg/3840px-Engraving_of_a_Llama_Wellcome_L0032831.jpg"
pagina_fuente = "https://commons.wikimedia.org/wiki/File:Engraving_of_a_Llama_Wellcome_L0032831.jpg"
autor = "Grabado anónimo (Wellcome Collection)"
obra = "Engraving of a Llama"
anio = "s. f."
licencia = "CC BY 4.0"
atribucion = "Grabado de una llama. Wellcome Collection, CC BY 4.0."

[[imagen]]
id = "lamina_amapola"
uso = "lamina"
tinta = "neolitico"
url = "https://upload.wikimedia.org/wikipedia/commons/9/93/Papaver_rhoeas_-_K%C3%B6hler%E2%80%93s_Medizinal-Pflanzen-101.jpg"
pagina_fuente = "https://commons.wikimedia.org/wiki/File:Papaver_rhoeas_-_K%C3%B6hler%E2%80%93s_Medizinal-Pflanzen-101.jpg"
autor = "Franz Eugen Köhler"
obra = "Köhler's Medizinal-Pflanzen: Papaver rhoeas (amapola)"
anio = 1887
licencia = "Dominio público"
atribucion = "F. E. Köhler, Medizinal-Pflanzen (1887), amapola. Wikimedia Commons, dominio público."

[[imagen]]
id = "lamina_langosta"
uso = "lamina"
tinta = "neolitico"
url = "https://upload.wikimedia.org/wikipedia/commons/6/63/EB1911_Locust_-_Pachytylus_migratorius.jpg"
pagina_fuente = "https://commons.wikimedia.org/wiki/File:EB1911_Locust_-_Pachytylus_migratorius.jpg"
autor = "Encyclopaedia Britannica (11.ª edición)"
obra = "Locust: Pachytylus migratorius (langosta migratoria)"
anio = 1911
licencia = "Dominio público"
atribucion = "Encyclopaedia Britannica (1911), langosta migratoria. Wikimedia Commons, dominio público."
```
Run: `uv run ilustraciones.py && uv run ilustraciones.py --rejilla cap3_poblado && uv run ilustraciones.py --rejilla cap3_huertos`
Expected:
- **`cap3_poblado`:** la casa grande cerca de (33 %, 40 %), las personas de la plataforma derecha cerca de (86 %, 36 %) y las laderas cerca de (40 %, 17 %).
- **`cap3_huertos`:** el suelo con plantas junto a la azada cerca de (30 %, 76 %) y la vegetación junto a la cabra cerca de (86 %, 70 %).
- Si las láminas de Thomé o Köhler traen el nombre impreso, se recortan.

- [ ] **Step 2: Escribir el capítulo**

`game/capitulos/cap3.rpy`:
```renpy
## Capítulo 3 · El cercano Neolítico · pp. 18–27 · Presenta Javier Felipe Contreras Díaz.
## Texto: guion del equipo. Fichas: redactadas a partir de las pp. 18–26.
## Posiciones del mapa: ilustraciones.posicion_en_mapa(lon, lat, (-120, -40, 80, 60)).

define cap3_puntos_poblado = [
    Punto("campo", 0.40, 0.17, "Campo de trigo y cebada", "cap3_obs_campo"),
    Punto("alfarero", 0.86, 0.36, "Alfarero", "cap3_obs_alfarero"),
    Punto("vivienda", 0.33, 0.40, "Hacha pulimentada y vivienda", "cap3_obs_vivienda"),
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
    n "La domesticación y la agricultura constituyen, para el autor, una de las revoluciones más profundas de la historia humana; solo la época moderna puede compararse con ese cambio." id cap3_01
    n "Muchas de las plantas y animales que todavía alimentan a las sociedades actuales proceden de procesos de domesticación neolíticos. El trigo y la cebada siguen siendo ejemplos esenciales." id cap3_02
    $ pagina = "pp. 18–19"
    n "Con la agricultura, las comunidades empezaron a ganar autonomía respecto de algunas condiciones inmediatas del ecosistema: ya no solo aprovechaban recursos disponibles, sino que construían un medio ajustado a sus necesidades." id cap3_03
    $ pagina = "p. 19"
    n "La mayor seguridad alimentaria permitió el crecimiento de la población. El libro ofrece como ejemplo Mesopotamia, donde estima que la población se multiplicó por cuarenta entre el 8000 y el 4000 antes de Cristo." id cap3_04
    $ pagina = "pp. 19–20"
    n "Los poblados se establecieron cerca del agua. Cuando el suelo se agotaba, algunos jóvenes fundaban nuevos asentamientos, lo que contribuía a extender los poblados por el territorio." id cap3_05
    call explorar(cap3_puntos_poblado)

    # Escena 3.2 · Dos continentes, dos caminos
    scene cap3_mapa with transformacion
    $ pagina = "pp. 20–21"
    n "Los excedentes alimentarios favorecieron la división del trabajo y la aparición de nuevas técnicas: alfarería, tejidos de lino y lana, hachas pulimentadas, arado, rueda, vela y trabajo de metales como el cobre y el bronce." id cap3_06
    $ pagina = "pp. 21–25"
    n "La domesticación no ocurrió de la misma manera en todas partes. En Eurasia se domesticaron, entre otras especies, trigo, cebada, cabras, ovejas, bueyes y caballos." id cap3_07
    n "En América se desarrollaron otros conjuntos de cultivos y animales, entre ellos maíz, calabaza, frijol, chile y llama. El libro destaca que no existían grandes herbívoros de tiro equivalentes a los de Eurasia." id cap3_08
    call explorar(cap3_puntos_mapa)
    nota "El libro describe una hibridación del maíz con el teosinte. La investigación genética muestra que el maíz fue domesticado a partir del teosinte en el valle del río Balsas, México, hace unos 9.000 años." (show_fuente="Matsuoka et al. (2002), PNAS") id cap3_nota

    # Escena 3.3 · Maleza y plaga
    scene cap2_bosque at paneo with fundido
    $ pagina = "pp. 25–26"
    n "Al transformar el entorno en campos de cultivo, las sociedades alteraron las relaciones entre especies. Las plantas que competían con el cultivo empezaron a llamarse «maleza», mientras que algunos animales pasaron a considerarse «plagas»." id cap3_09
    scene cap3_huertos at paneo with transformacion
    n "Según el argumento del autor, esos términos no son conceptos ecosistémicos neutrales: clasifican a las especies desde las necesidades del nuevo orden agrícola, es decir, desde aquello que favorece o perjudica la producción humana." id cap3_10
    n "La agricultura aumentó la capacidad humana de organizar el medio, pero también desarticuló cadenas tróficas y subordinó partes del ecosistema a los objetivos de la producción." id cap3_11
    call explorar(cap3_puntos_huertos)

    menu (screen="quiz", quiz="cap3_quiz", pagina="pp. 25–26"):
        pregunta "Según el autor, ¿por qué «maleza» y «plaga» no son conceptos ecosistémicos?" id cap3_quiz
        "Porque nombran a las especies que sobran en el nuevo orden agrícola, no una función en el ecosistema." (correcta=True):
            pass
        "Porque son especies que no existían antes del Neolítico.":
            pass
        "Porque solo afectan a cultivos de otros continentes.":
            pass
    porque "Una planta es considerada maleza porque compite con un cultivo; una plaga aparece cuando el cultivo favorece en exceso a ciertas especies. Son categorías del orden tecnológico agrícola, no categorías neutrales de la naturaleza." id cap3_quiz_porque

    menu (screen="decision", pagina="pp. 15, 19–20"):
        dilema "El poblado crece y el suelo junto al río se agota. ¿Qué hacen?" id cap3_dec
        "Los jóvenes fundan un nuevo poblado.":
            segun "Es el proceso que describe el libro para explicar la multiplicación de asentamientos junto al agua." id cap3_dec_a
        "Siguen cultivando la misma tierra.":
            segun "Con la azada, la población dependía del área cultivable y la fertilidad debía renovarse." id cap3_dec_b
        "Vuelven a la caza.":
            segun "El libro indica una densidad de población muy baja para sostener la vida cazadora; un poblado agrícola más denso no podía alimentarse de ese modo con facilidad." id cap3_dec_c

    clave "Con la agricultura, las sociedades pusieron partes del ecosistema al servicio de la producción: ganaron autonomía, pero también alteraron las cadenas tróficas." id cap3_clave
    jump final

label cap3_obs_campo:
    ficha "Alrededor de poblados como este se cultivaban trigo y cebada, cultivos domesticados que siguen siendo básicos en la alimentación." (show_lamina="lamina_trigo", show_titulo="Campo de trigo y cebada", show_leyenda="Trigo. Lámina de O. W. Thomé, 1885.", show_pagina="p. 18") id cap3_obs_campo
    return

label cap3_obs_alfarero:
    ficha "La alfarería muestra la especialización y el trabajo con materiales. Para el autor, fue el primer descubrimiento químico del ser humano." (show_lamina="lamina_alfarero", show_titulo="Alfarero", show_leyenda="El primer alfarero. Grabado de É. Bayard, 1870.", show_pagina="p. 20") id cap3_obs_alfarero
    return

label cap3_obs_vivienda:
    ficha "El hacha pulimentada dio la base técnica para la carpintería. Con ella, la casa de junco dio paso a la de madera, propia de un asentamiento permanente." (show_lamina="lamina_hacha", show_titulo="Hacha pulimentada y vivienda", show_leyenda="Fabricación y pulido de hachas. Grabado de É. Bayard, 1870.", show_pagina="p. 20") id cap3_obs_vivienda
    return

label cap3_obs_creciente:
    ficha "En el Oriente Medio crecían en estado salvaje el trigo, la cebada y la avena, junto a cabras, ovejas y bueyes. Desde allí se difundió la revolución neolítica hacia el año 7000 a.C." (show_lamina="lamina_cebada", show_titulo="Creciente Fértil", show_leyenda="Cebada. Lámina de O. W. Thomé, 1885.", show_pagina="p. 22") id cap3_obs_creciente
    return

label cap3_obs_mesoamerica:
    ficha "El maíz fue la base de las culturas americanas, junto a la calabaza, el chile y el frijol. Su domesticación fue difícil y lenta." (show_lamina="lamina_maiz", show_titulo="Mesoamérica", show_leyenda="Almacenamiento del maíz. Códice Florentino, siglo XVI.", show_pagina="pp. 23–24") id cap3_obs_mesoamerica
    return

label cap3_obs_andes:
    ficha "Hacia finales del tercer milenio hubo una civilización agraria en el istmo de Panamá. Más al sur se domesticaron tubérculos, el algodón y la llama." (show_lamina="lamina_llama", show_titulo="Istmo de Panamá y Andes", show_leyenda="Llama. Grabado, Wellcome Collection, CC BY 4.0.", show_pagina="p. 25") id cap3_obs_andes
    return

label cap3_obs_maleza:
    ficha "Para el autor, se llama maleza a la planta que compite con el trigo, la cebada o el maíz y no entra en los propósitos agrarios. En la lámina, una amapola, frecuente en los campos de cereal." (show_lamina="lamina_amapola", show_titulo="Maleza", show_leyenda="Amapola. Lámina de F. E. Köhler, 1887.", show_pagina="pp. 25–26") id cap3_obs_maleza
    return

label cap3_obs_plaga:
    ficha "Al favorecer solo algunas plantas, el cultivo alimenta en exceso a las especies que viven de ellas. Sus poblaciones se desajustan y aparece lo que el ser humano llama plaga." (show_lamina="lamina_langosta", show_titulo="Plaga", show_leyenda="Langosta migratoria. Encyclopaedia Britannica, 1911.", show_pagina="p. 26") id cap3_obs_plaga
    return
```

- [ ] **Step 3: Pruebas, voces, duración y recorrido**

Añadir a `pruebas.rpy`:
```renpy
    testcase cap3:
        run Start("cap3")
        assert screen "portada" timeout 10
        advance until screen "explorar" timeout 240
        click "Alfarero"
        assert screen "ficha" timeout 5
        click "Volver al paisaje"
        click "Continuar"
        advance until screen "explorar" timeout 180
        click "Continuar"
        advance until screen "explorar" timeout 180
        click "Continuar"
        advance until screen "quiz" timeout 60
        click "Porque nombran a las especies que sobran"
        assert eval (respondidas.get("cap3_quiz") is True) timeout 5
        advance until screen "decision" timeout 60
        click "Los jóvenes fundan"
        advance until label final timeout 120
```
Run: `uv run pytest -q && uv run --group voz generar_voz.py && uv run --group voz generar_voz.py --duracion && ./probar_juego.sh cap3`
Expected: `39 passed` y `Status: PASSED`. Si `cap3` pasa de 5,5 min, avisar a Javier Felipe con la lista de bloques para recortar.

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -q -m "feat(cap3): El cercano Neolítico completo con poblado, mapa mundial y maleza y plaga" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 17: Cierre con Buenaventura y la semilla

**Files:** Modify `fuentes.toml`, `game/capitulos/final.rpy`, `game/tests/pruebas.rpy`.

- [ ] **Step 1: Registrar las imágenes**

```toml
[[imagen]]
id = "final_buenaventura"
uso = "fondo"
tinta = "bosque"
url = "https://upload.wikimedia.org/wikipedia/commons/8/87/Manglar_Buenaventura.jpg"
pagina_fuente = "https://commons.wikimedia.org/wiki/File:Manglar_Buenaventura.jpg"
autor = "JulianCandelo (fotografía)"
obra = "Manglar en Buenaventura (Valle del Cauca, Colombia)"
anio = "s. f."
licencia = "CC BY-SA 4.0"
atribucion = "JulianCandelo, «Manglar Buenaventura». Wikimedia Commons, CC BY-SA 4.0 (imagen entintada, misma licencia)."
```
Y `final_semilla` con la plantilla de Internet Archive: hoja 337, `rotar = 90`, `recorte = "auto"`, tinta `bosque`, obra "Primitive Man, fig. 207: el cultivo de huertos (la semilla y el árbol)".
Run: `uv run ilustraciones.py`

- [ ] **Step 2: Escribir el cierre** (textos de la spec §3, a aprobar por el equipo)

`game/capitulos/final.rpy`:
```renpy
## Reflexión final · Todo el equipo. Textos propuestos a partir de las Partes 2 y 3 del taller.
## Buenaventura es una conexión preparada por el equipo, no un dato del libro.

label final:
    $ abrir_capitulo("final")
    play music "audio/ambiente/rio.wav" fadein 2.0 if_changed

    # Escena F1 · Conexión local: Buenaventura
    scene final_buenaventura at paneo with fundido
    $ pagina = "Conexión preparada por el equipo"
    n "Lo que vimos no es solo pasado. En Buenaventura, la vida, la cultura y la identidad dependen del mar, de los ríos y de los manglares." id final_01
    n "La expansión portuaria, industrial y minera puede entrar en conflicto con la conservación de los manglares y con la pesca tradicional. Transformar un territorio sin evaluar sus consecuencias perjudica las formas de vida que dependen de él." id final_02

    # Escena F2 · La semilla y el árbol
    scene final_semilla at paneo with transformacion
    show screen resumen
    $ pagina = "p. 9"
    nl "Elegimos una imagen para resumir este recorrido: una semilla que crece hasta ser un árbol rodeado de cultivos y herramientas. A medida que la humanidad avanza, también cambia su relación con el ambiente del que depende." id final_03
    nl "Como escribe Ángel Maya, la resiliencia cultural frente al medio es frágil. Y también: la incertidumbre es la raíz de la creatividad cultural." id final_04
    nl "Les dejamos una pregunta: ¿qué instrumentos culturales, técnicos, sociales y teóricos, necesitamos hoy para responder a la crisis ambiental?" id final_05
    call screen fin
    hide screen resumen
    return
```

- [ ] **Step 3: Pruebas, voces y recorrido**

Añadir a `pruebas.rpy`:
```renpy
    testcase final:
        run Start("final")
        assert screen "bloque" timeout 10
        advance until screen "resumen" timeout 60
        assert eval (len(respondidas) == 0)
        advance until screen "fin" timeout 120
        click "Volver al menú"
        assert screen "main_menu" timeout 10
```
Run: `uv run pytest -q && uv run --group voz generar_voz.py && ./probar_juego.sh final`
Expected: `39 passed` y `Status: PASSED`.

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -q -m "feat(final): cierre con Buenaventura, la semilla y el árbol, ideas clave y aciertos" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 18: Recorrido completo, duración y versión web

**Files:** Create `progressive_download.txt` (lo genera el Launcher) y `game/tests/pruebas.rpy` (testcase `completo`).

- [ ] **Step 1: Recorrido completo**

Añadir a `pruebas.rpy`:
```renpy
    testcase completo:
        click "Comenzar"
        advance until screen "explorar" timeout 240
        click "Continuar"
        advance until screen "quiz" timeout 240
        click "Una historia contada solo desde la política"
        advance until screen "decision" timeout 60
        click "Por la relación"
        advance until label cap1 timeout 120
        advance until screen "explorar" timeout 240
        click "Continuar"
        advance until screen "quiz" timeout 60
        click "Porque ya había cultivos"
        assert eval (respondidas.get("cap1_quiz") is False) timeout 5
        advance until screen "decision" timeout 60
        click "Cazar todos"
        advance until label cap2 timeout 120
        advance until screen "explorar" timeout 240
        click "Continuar"
        advance until screen "explorar" timeout 240
        click "Continuar"
        advance until screen "quiz" timeout 120
        click "Cuando la fauna se agota"
        advance until screen "decision" timeout 60
        click "Para tener más tiempo libre"
        advance until label cap3 timeout 120
        advance until screen "explorar" timeout 240
        click "Continuar"
        advance until screen "explorar" timeout 240
        click "Continuar"
        advance until screen "explorar" timeout 240
        click "Continuar"
        advance until screen "quiz" timeout 120
        click "Porque nombran a las especies que sobran"
        advance until screen "decision" timeout 60
        click "Vuelven a la caza"
        advance until label final timeout 120
        advance until screen "fin" timeout 240
        assert eval (aciertos == 3 and len(respondidas) == 4)
        click "Créditos"
        assert screen "creditos" timeout 5
```
Run: `./probar_juego.sh`
Expected: `Status: PASSED` y `Test cases: 14 | 14 passed` (navegacion, creditos, narracion, observacion, quiz, pausa, cierre, cap2, capturas_cap2, intro, cap1, cap3, final, completo).

- [ ] **Step 2: Duración total**

Run: `uv run --group voz generar_voz.py --duracion`
Expected: cada parte, 3–5,5 min de voz. Si alguna se pasa, se comunica al integrante antes de recortar.

- [ ] **Step 3: Instalar el soporte web del SDK**

```bash
cd ~/renpy-8.5.3-sdk
curl -sSLO https://www.renpy.org/dl/8.5.3/renpy-8.5.3-web.zip
unzip -q -o renpy-8.5.3-web.zip && rm renpy-8.5.3-web.zip
ls web | head -3        # Expected: archivos de renpyweb
cd -
```

- [ ] **Step 4: Compilar y servir la versión web**

```bash
~/renpy-8.5.3-sdk/renpy.sh ~/renpy-8.5.3-sdk/launcher web_build "$PWD" --destination "$PWD/.cache/web"
python3 -m http.server 8000 --directory .cache/web
```
Expected: `.cache/web/index.html` existe. En Chrome, `http://localhost:8000`:
- el menú carga;
- tras "Comenzar", la voz de la portada suena;
- AvPág y → avanzan, R repite la voz y Esc abre la pausa.

**Esta verificación es manual**: pedir al usuario que la haga y confirme.

- [ ] **Step 5: Ensayo en Google Meet (humano)**

1. Abrir el juego web en Chrome y entrar a Meet desde otra pestaña.
2. En Meet, "Presentar" → "Una pestaña" → elegir la del juego y activar **"Compartir también el audio de la pestaña"**.
3. Desde otra cuenta o dispositivo, comprobar que la voz y el texto llegan nítidos.
4. Cada integrante pasa su parte con cronómetro (unos 5 min).

Anotar los ajustes pedidos.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -q -m "test: recorrido completo del juego; versión web compilada y probada" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 19: Paquete de respaldo, README y limpieza

**Files:** Modify `README.md`. Delete `docs/` (al final). Generated `.cache/dist/`.

- [ ] **Step 1: Paquete de escritorio de respaldo**

```bash
~/renpy-8.5.3-sdk/renpy.sh ~/renpy-8.5.3-sdk/launcher distribute --package pc --destination "$PWD/.cache/dist" "$PWD"
unzip -l .cache/dist/*-pc.zip | grep -E "\.py$|fuentes\.toml|manifest\.json|/tests/" || echo "Sin archivos de desarrollo: OK"
```
Expected: un zip `LosOrigenes-2.0-pc.zip` y "Sin archivos de desarrollo: OK".

- [ ] **Step 2: Reescribir `README.md`**

Reúne lo útil de la spec y del plan, en este orden:
1. Qué es (título, curso, libro, equipo y partes).
2. **Cómo presentarlo en Google Meet:** versión web, compartir pestaña con audio; el paquete de escritorio como respaldo.
3. Controles (la tabla de la spec §2).
4. Estructura del proyecto (spec §7).
5. Cómo editar un capítulo: las reglas de una línea por `say` con `id`, `Punto`, `menu (screen="quiz"…)` y `(correcta=True)`.
6. Regenerar imágenes (`uv run ilustraciones.py`, `--rejilla`) y voces (`uv run --group voz generar_voz.py`, `--revisar`, `--duracion`, grabaciones propias).
7. Pruebas (`uv run pytest`, `./probar_juego.sh`).
8. Compilar la versión web y el paquete.
9. Créditos y licencias (el libro, las imágenes vía `fuentes.toml`, la voz, las tipografías y Ren'Py).

- [ ] **Step 3: Limpieza**

```bash
bash /home/fangulo/.claude/plugins/cache/claude-plugins-official/superpowers/6.4.1/skills/brainstorming/scripts/stop-server.sh "$PWD/.superpowers/brainstorm/"* 2>/dev/null || true
git rm -q -r docs
uv run pytest -q && ./probar_juego.sh navegacion
```
Expected: `39 passed` y `Status: PASSED`.

- [ ] **Step 4: Commit final**

```bash
git add -A
git commit -q -m "docs: README único con presentación por Meet, edición, recursos y pruebas" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```
