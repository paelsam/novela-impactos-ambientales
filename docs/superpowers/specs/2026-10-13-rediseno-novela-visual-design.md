# Los orígenes: del ecosistema a la cultura · Especificación de diseño

**Fecha:** 2026-10-13 · **Versión:** 2. Incorpora el guion del equipo y el enunciado del taller.

### Fuentes

- **Contenido:** Ángel Maya, A. (2015). *La fragilidad ambiental de la cultura. Historia y medio ambiente* (2.ª ed.), pp. 6–27.
- **Texto narrado:** `references/Guion_novela_visual_El_origenes_ecosistema_cultura.pdf` (el guion del equipo).
- **Requisitos del curso:** `references/taller general.pdf` (Actividad 3, Partes 3–6) y `references/parte-2-tarea.pdf`.
- **Dirección artística de partida:** `prompt.md`.

## 1. Objetivo, contexto y restricciones

Una novela visual en Ren'Py para la **Actividad 3 · Presentación creativa** del curso Impactos Ambientales (Universidad del Valle, docente Diana Marcela Mendoza). La clase es **por Google Meet**: quien presenta comparte una **pestaña de Chrome** con el juego web y su audio, la **voz narra** cada bloque, y cada integrante maneja su parte, pausa para comentar y resuelve los quices con el grupo.

| Parte | Páginas | Presenta |
| --- | --- | --- |
| Introducción | 6–9 | Elkin Samir Angulo Panameño |
| Cap. 1 · El lejano Paleolítico | 10–12 | Sebastián Bolaños Morales |
| Cap. 2 · Del Homo sapiens al Neolítico | 13–17 | María Fernanda Cano Cobo |
| Cap. 3 · El cercano Neolítico | 18–27 | Javier Felipe Contreras Díaz |

**Título:** "Los orígenes: del ecosistema a la cultura" (el bloque temático del equipo).

### Restricciones

- Menos de una semana hasta la presentación.
- Unos 5 minutos por parte (unos 20 en total).
- Equipo sin GPU dedicada.
- Coste cero.

**Criterios de éxito** (incluye la rúbrica de la Parte 6 del taller)

- Identidad visual reconocible y coherente: "cuaderno de campo" con grabados entintados.
- Legible al compartirse por Meet; la voz se oye en Meet al compartir la pestaña.
- La voz arranca sola en cada bloque y quien presenta controla cuándo avanzar.
- **Comprensión conceptual:** fiel al libro, con página citada; las correcciones de la ciencia actual aparecen señaladas.
- **Coherencia del hilo temático:** las 4 ideas clave y el cierre muestran el argumento común.
- **Conexión con la realidad ambiental colombiana:** cierre con Buenaventura, presentado como conexión del equipo.
- **Trabajo colaborativo:** cada integrante aprueba el texto, las imágenes y la voz de su parte, y la presenta.
- Cada imagen tiene licencia y fuente documentadas, y los créditos se generan automáticamente.
- Cada integrante puede saltar directo a su parte.

**Fuera de alcance** (YAGNI)

- Generación de imágenes con IA (solo como último recurso y con aprobación explícita).
- Flujo ComfyUI/LoRA.
- Android o móvil.
- Pantallas de guardar o cargar partida.
- Varios idiomas.
- Etapas III–V del `prompt.md`, salvo como marco en la Introducción y en el cierre.
- Una explicación distinta para cada opción incorrecta de un quiz (hay un "Por qué" compartido).

## 2. Experiencia y flujo

**Menú principal:** título del juego · Comenzar · Capítulos · Créditos · Salir.

- **Capítulos:** índice con 4 tarjetas (número, título, presentador, páginas, "≈ 5 min") que salta directo a cada parte.

**Estructura de cada parte** (orden del guion)

1. **Portada narrada:** el texto de portada del guion, con número, título, presentador y páginas en pantalla.
2. **Escenas:** cada una tiene un fondo, bloques narrados y puntos de observación opcionales.
3. **Quiz.**
4. **Decisión.**
5. **Nota de campo** (si la parte la tiene).
6. **Idea clave**, y luego la siguiente parte.

**Cierre:** dos escenas.

1. **Conexión local:** Buenaventura.
2. **La semilla y el árbol:** la metáfora del equipo, las 4 ideas clave, la tesis de la p. 9, la pregunta abierta y los aciertos del salón. Desde aquí se pasa a los créditos.

### Controles de quien presenta

| Acción | Teclas |
| --- | --- |
| Avanzar | clic · Espacio · → · AvPág (funciona con punteros de presentación) |
| Retroceder | ← · RePág |
| Repetir la voz | R |
| Modo automático (avanza al terminar la voz) | A |
| Elegir opción en quiz o decisión | 1 · 2 · 3 (= A · B · C) |
| Menú de pausa | Esc |

- La voz de cada bloque arranca sola. Al terminar, la escena se queda quieta hasta que se avanza.
- El texto aparece completo de una vez.
- **Menú de pausa:** Continuar · Capítulos · Voz (sí/no y volumen) · Modo automático · Reducir movimiento · Menú principal · Salir.

### Tipos de bloque

- **Narrativo:** tarjeta de papel abajo a la izquierda (escenas a pantalla completa) o en panel lateral derecho (láminas en composición editorial). Lleva el indicador "Cap. 2 · 3/10", una barra de progreso y la página del bloque.
- **Observación:** marcadores numerados sobre el paisaje. Al elegir uno, la narración se oculta y aparece una ficha (lámina opcional, leyenda, título, texto narrado y página) unida al punto por una línea en ángulo, sin taparlo. Los vistos quedan con ✓ y "Continuar" siempre está disponible.
- **Quiz:** 3 opciones grandes. El grupo responde en Meet y quien presenta elige. La retroalimentación marca ✗ "No es así" en la elegida si es incorrecta y ✓ "Correcta" en la correcta (símbolo y palabra, nunca solo color), con un "Por qué" narrado y la página. Cuenta solo el primer intento para los aciertos del salón.
- **Decisión:** ninguna opción es incorrecta. Cada una lleva a una explicación narrada "Según el libro", sin inventar consecuencias.
- **Nota de campo:** "Nota de campo · ciencia actual", narrada, con la fuente científica citada.

## 3. Contenido

**El texto narrado sale del guion del equipo**, tal cual: portadas, bloques, quices con su "Por qué", decisiones con su explicación, notas de campo e ideas clave. El implementador solo completa lo que el guion no redacta:

- Las fichas de observación de las que el guion da solo la etiqueta.
- Los textos del cierre.

**Cada integrante aprueba su parte** antes de generar las voces.

| Parte | Escenas (fondo) | Bloques | Observaciones | Nota de campo |
| --- | --- | --- | --- | --- |
| Introducción | I1 Venecia (Barbari) · I2 testimonios mudos (hachas de mano) · I3 Londres (Doré) | 4 + 4 + 1 | I1: palacio · barcos · laguna | — |
| Cap. 1 | 1.1 fuego (Figuier fig. 7) · 1.2 caza (fig. 16) · 1.3 mapa de Eurasia | 4 + 4 + 1 | 1.3: China · España · Rusia y Europa Central · Francia | Neandertales erguidos (Smithsonian) |
| Cap. 2 | 2.1 abrigo de Bruniquel (fig. 40) · 2.2 paisaje cuaternario (Riou) → caza en el bosque (fig. 52) · 2.3 artes (fig. 68) | 4 + 4 + 2 | 2.2: mamut · alce gigante · rinoceronte · 2.3: Altamira · figuras levantinas | Homo sapiens de 300.000 años (Hublin et al., 2017) |
| Cap. 3 | 3.1 aldea lacustre (fig. 149) · 3.2 mapa mundial · 3.3 huertos (fig. 207) | 5 + 3 + 3 | 3.1: campo de trigo y cebada · alfarero · hacha y vivienda · 3.2: Creciente Fértil · Mesoamérica · istmo y Andes · 3.3: maleza · plaga | Maíz como teosinte domesticado (Matsuoka et al., 2002) |

### Decisiones de reconciliación

- **Ideas clave:** el guion trae dos versiones para los Caps. 1 y 3 (en el capítulo y en el cierre). Se usa la del capítulo en ambos lugares, una sola fuente:
  - **Introducción:** "La historia humana no ocurre en un escenario vacío: sociedad, técnica y ecosistemas se transforman juntos."
  - **Cap. 1:** "Sin garras ni colmillos, los seres humanos se adaptaron mediante instrumentos y cooperación; al especializarse en la caza, empezaron a ejercer una presión importante sobre algunos ecosistemas."
  - **Cap. 2:** "Cada avance técnico transformó el medio, y cada cambio del medio obligó a reorganizar la sociedad."
  - **Cap. 3:** "Con la agricultura, las sociedades pusieron partes del ecosistema al servicio de la producción: ganaron autonomía, pero también alteraron las cadenas tróficas."
- **Escena I2:** se usa la lámina A-17 de *Reliquiae Aquitanicae* (hachas de mano, 1875) en lugar de las figs. 10–15 de Figuier. Es el mismo contenido en mejor calidad y sin texto incrustado.
- **Infanticidio (p. 15):** se omite, como dice el guion. Si María Fernanda decide incluirlo, se añade un bloque.
- **Duración:** el Cap. 3 tiene 11 bloques. Si con las voces generadas pasa de 5 min 30 s (sin contar observaciones), se avisa al integrante para recortar.

**Cierre** (textos propuestos por el implementador; los aprueba el equipo)

- **Escena F1 · Conexión local: Buenaventura**
  - **Fondo:** foto "Manglar Buenaventura" (JulianCandelo, CC BY-SA 4.0), con tinta "bosque".
  - **Indicador:** "Reflexión final · Conexión local del equipo". En lugar de página: "Conexión preparada por el equipo" (el guion pide que no parezca un dato del libro).
  - **Bloque 1:** "Lo que vimos no es solo pasado. En Buenaventura, la vida, la cultura y la identidad dependen del mar, de los ríos y de los manglares."
  - **Bloque 2:** "La expansión portuaria, industrial y minera puede entrar en conflicto con la conservación de los manglares y con la pesca tradicional. Transformar un territorio sin evaluar sus consecuencias perjudica las formas de vida que dependen de él."
- **Escena F2 · La semilla y el árbol**
  - **Fondo:** Figuier fig. 207 con tinta "bosque": un árbol rodeado de cultivos y herramientas.
  - **Bloque 1:** "Elegimos una imagen para resumir este recorrido: una semilla que crece hasta ser un árbol rodeado de cultivos y herramientas. A medida que la humanidad avanza, también cambia su relación con el ambiente del que depende."
  - **Bloque 2:** "Como escribe Ángel Maya, la resiliencia cultural frente al medio es frágil. Y también: la incertidumbre es la raíz de la creatividad cultural." (p. 9)
  - **Bloque 3:** "Les dejamos una pregunta: ¿qué instrumentos culturales, técnicos, sociales y teóricos, necesitamos hoy para responder a la crisis ambiental?" (p. 9)
  - **Pantalla de resumen:** las 4 ideas clave y "Aciertos del salón: X de Y".

## 4. Identidad visual

Validada con una maqueta en el navegador. Concepto: **cuaderno de campo** (bloques de papel, anotaciones y láminas) sobre **paisajes de grabado a pantalla completa**.

**Lienzo:** 1920×1080, con márgenes seguros de 64 px. En la web, Ren'Py escala el lienzo a la pestaña.

**Paleta de interfaz** (contraste del texto: 12,7:1 el principal y 6,1:1 el secundario)

| Rol | HEX | Rol | HEX |
| --- | --- | --- | --- |
| Papel (fondo de lectura) | `#F3ECDC` | Verde bosque (botones, ecosistemas) | `#2E4A3A` |
| Papel 2 (barras, vistos) | `#E9DFC8` | Verde musgo (detalles botánicos, "Por qué") | `#6B7A4B` |
| Borde fino | `#CBBE9F` | Ocre (agricultura) | `#B98A3E` |
| Tinta (texto principal) | `#2A2722` | Tierra (suelo) | `#7A5634` |
| Tinta 2 (texto secundario) | `#5E574B` | Azul grisáceo (agua, frío) | `#5D7486` |
| Correcta (siempre con ✓ + texto) | `#2E6B47` | Terracota (asentamientos) | `#B25C3C` |
| Incorrecta (siempre con ✗ + texto) | `#9E3B2B` | Carbón (industria, solo Intro) | `#33363A` |
| Foco (anillo de 4 px) | `#2F6F8F` | Desactivado | `#A79E8C` |

**Tintas de ilustración por ambiente.** Duotono de tinta a papel, con tono medio y grano de papel. La tinta representa una condición ambiental, no un juicio moral.

| Tinta | Tinta → medio → papel | Uso |
| --- | --- | --- |
| archivo | `#2E2620` → `#8A7A66` → `#F2EBDD` | Introducción y menú |
| sabana | `#3F3020` → `#9C7F55` → `#F2E8D2` | Cap. 1, fuego y sabana |
| glaciación | `#23313C` → `#6F8492` → `#ECEFEB` | Caps. 1–2, estepas y frío |
| bosque | `#1E3327` → `#6C7F59` → `#EEF0E2` | Cap. 2 y cierre |
| neolítico | `#3D291B` → `#A2724A` → `#F3E7D2` | Cap. 3, campos y poblados |
| industria | `#26282B` → `#77787A` → `#E7E5E0` | Solo el marco de la Introducción |

**Tipografía** (ambas OFL, incluidas en `game/fonts/` con su licencia)

- **Literata** (serif): portadas, títulos, narración y citas.
- **Atkinson Hyperlegible** (sans): opciones, botones, indicadores y anotaciones.
- **DejaVu Sans** (incluida en Ren'Py): solo los símbolos ✓ ✗ ← → ≈ ◉ que Atkinson no tiene.

| Uso | Familia | Tamaño / interlineado | Peso |
| --- | --- | --- | --- |
| Portada de capítulo | Literata | 72 / 1.1 | 600 |
| Título de escena, quiz o ficha | Literata | 40–42 / 1.2 | 600 |
| Narración | Literata | 34 / 1.45 (bloque de 800 px) | 400 |
| Texto de ficha y "Por qué" | Literata | 27 / 1.45 | 400 |
| Opciones de quiz o decisión | Atkinson | 28 / 1.3 | 400 |
| Botones | Atkinson | 22 | 700 |
| Indicadores y kicker | Atkinson | 18, mayúsculas, espaciado 0.09 em | 700 |
| Mínimo absoluto | — | 18 px | — |

**Bloques:** radio de 12 px, borde de 1,5 px `#CBBE9F`, relleno de 26/34 px, papel al 96 % de opacidad, **sin sombras**. Las esquinas redondeadas son piezas PNG generadas por script (`game/gui/`).

**Componentes** (los 14 del `prompt.md`)

1. **Inicio:** fondo con tinta "archivo", título y 4 botones.
2. **Índice de capítulos:** 4 tarjetas de papel.
3. **Portada de capítulo:** centrada con velo de papel; narrada.
4. **Escena narrativa:** fondo con paneo lento (zoom 1,00→1,04 en 20 s; ninguno con "reducir movimiento").
5. **Bloque narrativo:** abajo a la izquierda (800 px) o panel lateral derecho (720 px).
6. **Ficha de observación:** lámina de 300 px de alto, leyenda, título, texto narrado y "← Volver al paisaje". Va en la mitad opuesta al punto, unida a él por una línea en ángulo.
7. **Marcador:** círculo de papel de 56 px numerado; anillo de foco, etiqueta al pasar y ✓ verde cuando ya se vio.
8. **Quiz:** tarjeta centrada de 1120 px sobre velo.
9. **Retroalimentación:** misma tarjeta con estados ✗/✓, borde de 3 px y "Por qué" con filete musgo.
10. **Decisión:** como el quiz, sin ✓/✗, con "Según el libro".
11. **Progreso:** kicker "Cap. 2 · 3/10" y barra de 4 px.
12. **Transiciones:** fundido de 0,8 s y transformación del paisaje de 2,5 s; 0,3 s y sin paneo con "reducir movimiento".
13. **Resumen final:** ideas clave y aciertos.
14. **Pausa:** opciones de la sección 2, con confirmaciones en el mismo estilo.

## 5. Ilustraciones

**Estrategia:** grabados y láminas de dominio público, unificados con las tintas de la sección 4. Sin IA salvo aprobación explícita.

**Fuentes confirmadas** (URL exactas en el plan)

- **Figuier, *Primitive Man* (1870), grabados de É. Bayard:** Internet Archive `primitiveman00figuiala`, dominio público, descarga IIIF a 1800 px. Las láminas de lado se giran 90° en sentido horario.
  - Fig. 7 (hoja 71), fuego · fig. 16 (hoja 83), oso y mamuts · fig. 17 (hoja 87), el primer alfarero.
  - Fig. 39 (hoja 123), cazador de la época del reno · fig. 40 (hoja 127), Bruniquel · fig. 52 (hoja 141), caza en el bosque.
  - Fig. 68 (hoja 153), artes · fig. 107 (hoja 205), hachas pulimentadas · fig. 126 (hoja 231), los primeros navegantes.
  - Fig. 149 (hoja 289), aldea lacustre · fig. 207 (hoja 337), huertos.
- **Riou, *La Terre avant le déluge* (1863), lámina 10:** Wellcome Collection, CC BY 4.0. De ella salen los recortes del mamut, el alce gigante y el rinoceronte lanudo.
- **Wikimedia Commons:**
  - Barbari, *Veduta di Venezia* (1500), dominio público.
  - Doré, "Over London – by Rail" (1872), dominio público.
  - *Reliquiae Aquitanicae*, lámina A-17 (1875), dominio público.
  - Thomé, *Triticum aestivum*, dominio público.
  - Köhler, *Papaver rhoeas*, dominio público.
  - *Encyclopaedia Britannica* (1911), langosta, dominio público.
  - Bisonte de Altamira, dominio público.
  - "Cova dels cavalls" (EmparMM, CC BY-SA 4.0).
  - Llama (Wellcome, CC BY 4.0).
  - "Aztecs storing maize" (Códice Florentino), dominio público.
  - "Manglar Buenaventura" (JulianCandelo, CC BY-SA 4.0).
- **Mapas:** Natural Earth 1:110m (dominio público), dibujados por script.

**Registro `fuentes.toml`:** una entrada por imagen y única fuente de los créditos. Campos: `id`, `uso` (fondo | lamina | mapa), `tinta`, `url`, `pagina_fuente`, `autor`, `obra`, `anio`, `licencia`, `atribucion`, y los opcionales `recorte` ([x, y, ancho, alto] o "auto"), `rotar` (grados horarios), `encaje` (cubrir | editorial), `centrado` y `mapa`.

### Script `ilustraciones.py`

1. Valida el registro y **se detiene** si falta la licencia, la atribución o la fuente.
2. Descarga con caché y reintentos.
3. Gira, recorta (manual o automático: detecta el grabado y deja fuera márgenes y pie) y aplica la tinta.
4. Exporta los fondos a 1920×1080 y las láminas a un máximo de 900 px.
5. Dibuja los mapas y genera las piezas de interfaz y `game/creditos_generados.rpy`.
6. `--rejilla <id>` guarda una copia con rejilla del 5 % para medir la posición de los marcadores.

**Reglas de aceptación:** técnica de grabado o litografía con la tinta aplicada; sin texto incrustado; zona libre para el bloque; contexto correcto (nada de caballos despeñados en Solutré ni neandertales encorvados presentados como hecho); licencia registrada; se ve bien a 1920×1080. Las láminas con desnudos se recortan o se descartan.

## 6. Voz

- **Convención:** toda línea hablada es una sentencia `say` con `id` explícito.
  - Narración: `intro_01`, `cap1_01`… y `final_01`…
  - Otros: `capN_portada`, `capN_obs_<punto>`, `capN_quiz`, `capN_quiz_porque`, `capN_dec`, `capN_dec_<a|b|c>`, `capN_nota`, `capN_clave`.
- **En el juego:** `config.auto_voice` usa `audio/voz/grabadas/<id>.ogg` si existe y, si no, `audio/voz/<id>.ogg`. Si falta el archivo, la línea se muestra sin voz.
  - `VoiceReplay` se asigna a la tecla R.
  - El modo automático espera a que termine la voz.
  - El texto aparece al instante.
- **`generar_voz.py`** (`uv run --group voz`): lee las líneas con `id` de `game/**/*.rpy`, aplica el diccionario de pronunciación y genera con Kokoro `em_alex` (velocidad 0,92) solo las voces nuevas o con texto cambiado (por hash). Escribe OGG Vorbis a 24 kHz. `--revisar` muestra los cambios sin generar nada y `--duracion` informa los minutos de voz por parte.
- **Grabaciones propias (opcional):** en `audio/voz/grabadas/<id>.ogg`, con prioridad sobre la voz sintética.
- Se eliminan los 16 WAV actuales.

## 7. Arquitectura técnica

```text
game/
  options.rpy                   config (1920×1080, teclas, paquetes)
  estilo.rpy                    paleta, fuentes, estilos, paneo y transiciones
  pantallas/                    menu.rpy (inicio, índice, créditos, portada) · narracion.rpy · observacion.rpy
                                quiz.rpy · notas.rpy (nota, idea clave, resumen, fin) · pausa.rpy (pausa, confirmación)
  sistema/                      capitulos.rpy (partes, ideas, inicio) · voz.rpy (voz, progreso)
                                explorar.rpy (puntos) · respuestas.rpy (aciertos)
  capitulos/                    intro.rpy · cap1.rpy · cap2.rpy · cap3.rpy · final.rpy
  creditos_generados.rpy        generado por ilustraciones.py
  tl/None/common.rpym           textos internos de Ren'Py en español (se conserva)
  images/fondos/ · images/laminas/ · gui/   generados
  audio/voz/ · audio/voz/grabadas/ · audio/ambiente/ · audio/sfx/
  fonts/                        Literata, Atkinson Hyperlegible + OFL.txt
  tests/                        recorridos automáticos (no viajan en los paquetes)
fuentes.toml · ilustraciones.py · generar_voz.py · probar_juego.sh
tests/                          pytest de los scripts y reglas del guion
pyproject.toml                  Python >=3.11,<3.13 · pillow, pyshp · grupo "voz": kokoro, soundfile, torch (CPU) · grupo "dev": pytest
```

### Piezas

- `CAPITULOS` e `IDEAS` (una sola fuente para el índice, las portadas, los indicadores y el resumen).
- **Personajes con pantalla propia:** `n` / `nl` (narración), `portada`, `ficha`, `pregunta` / `dilema`, `porque`, `segun`, `nota`, `clave`.
- **Quiz y decisión:** `menu` nativo con `screen="quiz"` o `"decision"`; `(correcta=True)` marca la opción correcta.
- **Observación:** `call explorar(lista_de_Punto)`.
- **Progreso:** se cuentan los `id` `<parte>_##` del guion al iniciar el juego.
- **Teclas:** `dismiss` += AvPág y →; `rollback` += ←.

### Entrega

1. **Principal:** compilación web (`renpy.sh <sdk>/launcher web_build`), servida en local y abierta en Chrome. En Meet se comparte la pestaña con "Compartir también el audio de la pestaña".
2. **Respaldo:** paquete de escritorio Windows/Linux.
3. Se excluyen de los paquetes los `.py`, `tests/`, el registro, el manifiesto de voces y la documentación.

## 8. Errores y pruebas

- Una voz faltante deja la línea sin audio. Una licencia faltante detiene `ilustraciones.py`. El lint de Ren'Py debe dar 0 avisos.
- **pytest, sin red:**
  - Lectura de ids, pronunciación y detección de cambios.
  - Registro, tinta, recorte automático, mapa, interfaz y créditos.
  - Reglas del guion: texto ≥ 18 px, ideas clave coherentes, un `(correcta=True)` por quiz, longitud de los bloques.
- **Recorridos automáticos de Ren'Py** (`./probar_juego.sh`, sin pantalla): navegación, narración, observación, quiz y decisión, pausa, cierre, y un recorrido por cada parte.
- **Prueba web:** el juego carga en Chrome, la voz suena tras el primer clic y las teclas funcionan.
- **Ensayo en Meet:** compartir la pestaña con audio y comprobar desde otra cuenta que la voz y el texto llegan.
- **Revisión humana:** cada integrante aprueba el texto, las imágenes y la voz de su parte y ensaya con cronómetro (≈ 5 min).

## 9. Entrega, roles y riesgos

### Roles

- **Implementador (Claude):** código, scripts, curaduría propuesta, textos de fichas y cierre, y pruebas.
- **Cada integrante:** aprueba su parte, la presenta y ensaya.

### Hitos

1. Sistema base más el Cap. 2 completo como prototipo validado.
2. Las otras tres partes y el cierre.
3. Pruebas, versión web y ensayo en Meet.
4. Copias de respaldo (paquete de escritorio).

### Riesgos y mitigación

- **Audio en Meet:** versión web en una pestaña con audio, comprobada en el ensayo.
- **Duración del Cap. 3:** se mide con `--duracion` y se recorta si hace falta.
- **Pronunciación de la voz sintética:** diccionario de pronunciación o grabación de esa línea.
- **Imagen sin alternativa:** un recorte de otra lámina aprobada. Si no hay ninguna, IA con aprobación.
- **Servidores de imágenes inestables:** reintentos y caché local.

**Limpieza:** `.superpowers/` y `.cache/` van a `.gitignore`. Al terminar, lo relevante de esta spec pasa al `README.md` y `docs/` se elimina.
