# Los orígenes: del ecosistema a la cultura · Plan de implementación (parte 1 de 3)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rehacer la novela visual en Ren'Py según la spec v2: identidad de cuaderno de campo con grabados entintados, narración por voz con `id`, observaciones, quices y decisiones, versión web para Google Meet.

**Architecture:** Dos scripts de Python (uv) producen los recursos: `ilustraciones.py` (registro de licencias → imágenes entintadas, mapas, piezas de interfaz y créditos) y `generar_voz.py` (guion → voces OGG con Kokoro). El juego Ren'Py separa sistema (`game/sistema/`), pantallas (`game/pantallas/`) y contenido (`game/capitulos/`, uno por integrante). Las pruebas: pytest para los scripts y las reglas del guion, y recorridos automáticos de Ren'Py sin pantalla (`probar_juego.sh`).

**Tech Stack:** Ren'Py 8.5.3 (SDK en `~/renpy-8.5.3-sdk`), Python 3.12 con uv, Pillow, pyshp, Kokoro-82M (grupo opcional `voz`), pytest, mutter headless para las pruebas.

**Spec:** `docs/superpowers/specs/2026-10-13-rediseno-novela-visual-design.md` (v2). Guion del equipo: `references/Guion_novela_visual_El_origenes_ecosistema_cultura.pdf`.

**Partes del plan**
- **Este archivo:** tareas 1–7 (scripts).
- `2026-10-13-novela-visual-parte2.md`: tareas 8–12 (sistema del juego).
- `2026-10-13-novela-visual-parte3.md`: tareas 13–19 (contenido, web y entrega).

## Global Constraints

- SDK de Ren'Py: `${RENPY_SDK:-$HOME/renpy-8.5.3-sdk}` (ya instalado en `/home/fangulo/renpy-8.5.3-sdk`).
- Python `>=3.11,<3.13` con uv. `uv run pytest` no usa red. La voz solo con `uv run --group voz`.
- Lienzo 1920×1080. Ningún texto menor de 18 px. Paleta, tintas y tipografías exactamente como la spec §4.
- Toda línea hablada es una sentencia `say` **en una sola línea** con `id` único y sin `[...]`.
- Toda imagen entra por `fuentes.toml` con licencia y atribución. Nada de texto incrustado salvo inscripciones históricas del original.
- Textos narrados: los del guion, sin reescribir. Solo se redactan las fichas sin texto en el guion y el cierre.
- Mensajes de commit en español, terminados con la línea `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- Nunca se modifica `game/audio/voz/grabadas/`.

## Review Focus

1. **Recorte fuera de la imagen** en `fuentes.toml`. Comportamiento esperado: error que nombre el `id`, no un relleno negro. Prueba: Tarea 2, `test_recorte_fuera_de_la_imagen_falla`.
2. **Quiz sin `(correcta=True)`.** Esperado: lo detecta pytest antes de jugar y Ren'Py da un error claro. Pruebas: Tarea 11, `test_cada_quiz_tiene_una_correcta` y la excepción en `responder_quiz`.
3. **Cierre abierto desde el índice sin preguntas respondidas.** Esperado: muestra "0 de 0" sin fallar. Prueba: Tarea 12, testcase `cierre`.
4. **Bloque demasiado largo para la tarjeta.** Esperado: pytest lo marca (más de 55 palabras). Prueba: Tarea 13, `test_bloques_caben_en_la_tarjeta`.
5. **Error 500 o caída momentánea del servidor de imágenes.** Esperado: reintento con espera. Prueba: Tarea 5, `test_descargar_reintenta_ante_un_error`.

## Mapa de archivos

| Archivo | Responsabilidad | Tarea |
| --- | --- | --- |
| `pyproject.toml`, `.gitignore` | dependencias y grupos (`dev`, `voz`), pytest, ignorados | 1 |
| `ilustraciones.py` | registro → imágenes entintadas, mapas, piezas de interfaz, créditos, rejilla | 1–5 |
| `tests/test_ilustraciones.py` | pruebas de `ilustraciones.py` | 1–5 |
| `generar_voz.py` | guion → voces OGG, manifiesto, duración por parte | 6–7 |
| `tests/test_generar_voz.py` | pruebas de `generar_voz.py` | 6–7 |
| `fuentes.toml` | registro de imágenes y licencias | 8, 13–17 |
| `probar_juego.sh` | lint + recorridos de Ren'Py sin pantalla | 8 |
| `tests/test_guion.py` | reglas del guion (tamaños, ideas, quices, longitud) | 8, 11, 13 |
| `game/options.rpy` | configuración, teclas, exclusiones de paquetes | 8 |
| `game/estilo.rpy` | paleta, fuentes, estilos, paneo, transiciones | 8 |
| `game/sistema/capitulos.rpy` | partes, ideas clave, referencias, `abrir_capitulo`, `start` | 8 |
| `game/pantallas/menu.rpy` | inicio, índice, créditos, portada | 8 |
| `game/sistema/voz.rpy` | `voz_de`, `progreso`, `kicker`, `TOTAL_BLOQUES` | 9 |
| `game/pantallas/narracion.rpy` | `bloque` (`n`, `nl`), `say` | 9 |
| `game/sistema/explorar.rpy` | `Punto`, `explorar` | 10 |
| `game/pantallas/observacion.rpy` | `explorar`, `ficha` | 10 |
| `game/sistema/respuestas.rpy` | aciertos y estado de respuestas | 11 |
| `game/pantallas/quiz.rpy` | pregunta, quiz, decisión, retroalimentación, según | 11 |
| `game/pantallas/notas.rpy` | nota de campo, idea clave, resumen, fin | 12 |
| `game/pantallas/pausa.rpy` | pausa y confirmación | 12 |
| `game/capitulos/*.rpy` | contenido de cada parte | 8 (esqueleto), 13–17 |
| `game/tests/pruebas.rpy`, `game/tests/escenas_prueba.rpy` | recorridos automáticos y escenas de prueba | 8–17 |
| `README.md` | documentación final | 19 |

---

### Task 1: Repositorio, entorno y registro de fuentes

**Files:**
- Modify: `.gitignore`, `pyproject.toml`
- Create: `ilustraciones.py`, `tests/test_ilustraciones.py`

**Interfaces:**
- Produces: `ilustraciones.cargar_registro(ruta: Path) -> list[Imagen]`, `ErrorRegistro(ValueError)`, `Imagen` (dataclass congelada con `id, uso, tinta, url, pagina_fuente, autor, obra, anio: str, licencia, atribucion, recorte: tuple|str|None, rotar: int, encaje: str, centrado: tuple[float, float], mapa: tuple|None, notas`), constantes `TINTAS`, `USOS`, `ENCAJES`, `RAIZ`, `REGISTRO`.

- [ ] **Step 1: Inicializar git con el estado actual como punto de partida**

```bash
cd "/home/fangulo/Escritorio/Impactos Ambientales/Proyecto"
git init -b main
git add -A
git commit -q -m "chore: estado inicial del proyecto" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```
Expected: un commit en `main`.

- [ ] **Step 2: Reemplazar `.gitignore`**

```gitignore
# Python / uv
.venv/
__pycache__/
.pytest_cache/

# Herramientas locales: caché de descargas, capturas, compañero visual
.cache/
.superpowers/

# Ren'Py: caché, partidas y scripts compilados
/game/cache/
/game/saves/
*.rpyc
*.rpymc
*.bak
*.new
*.old

# Ren'Py: logs y archivos generados por el launcher
/log.txt
/errors.txt
/traceback.txt
/files.txt
/image_cache.txt
/save_dump.txt
/dialogue.tab
/dialogue.txt
/strings.json
```

- [ ] **Step 3: Reemplazar `pyproject.toml`**

```toml
[project]
name = "fragilidad-ambiental"
version = "2.0.0"
description = "Los orígenes: del ecosistema a la cultura. Novela visual en Ren'Py sobre La fragilidad ambiental de la cultura (Introducción y capítulos 1–3)."
readme = "README.md"
requires-python = ">=3.11,<3.13"
dependencies = [
    "pillow>=11.0",
    "pyshp>=2.3",
]

[dependency-groups]
dev = ["pytest>=8.3"]
voz = [
    "kokoro>=0.9.4",
    "numpy>=1.26",
    "soundfile>=0.13",
    "torch>=2.4",
]

# PyTorch solo para CPU: evita descargar varios GB de librerías CUDA que la
# generación de voz no necesita.
[tool.uv.sources]
torch = { index = "pytorch-cpu" }

[[tool.uv.index]]
name = "pytorch-cpu"
url = "https://download.pytorch.org/whl/cpu"
explicit = true

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

Run: `uv lock && uv sync`
Expected: `Resolved N packages` sin errores; `.venv` con pillow, pyshp y pytest (sin torch).

- [ ] **Step 4: Escribir las pruebas del registro**

`tests/test_ilustraciones.py`:
```python
import pytest

from ilustraciones import ErrorRegistro, cargar_registro

ENTRADA = '''
[[imagen]]
id = "cap2_glaciacion"
uso = "fondo"
tinta = "glaciacion"
url = "https://example.org/riou.jpg"
pagina_fuente = "https://example.org/riou"
autor = "Édouard Riou"
obra = "La Terre avant le déluge, lámina 10"
anio = 1863
licencia = "CC BY 4.0"
atribucion = "É. Riou (1863). Wellcome Collection, CC BY 4.0"
recorte = [63, 180, 2960, 1665]
'''


def escribir(tmp_path, texto):
    ruta = tmp_path / "fuentes.toml"
    ruta.write_text(texto, encoding="utf-8")
    return ruta


def test_carga_entrada_valida(tmp_path):
    [img] = cargar_registro(escribir(tmp_path, ENTRADA))
    assert img.id == "cap2_glaciacion"
    assert img.recorte == (63, 180, 2960, 1665)
    assert img.anio == "1863"
    assert (img.encaje, img.rotar, img.centrado) == ("cubrir", 0, (0.5, 0.5))


def test_acepta_recorte_automatico(tmp_path):
    texto = ENTRADA.replace("recorte = [63, 180, 2960, 1665]", 'recorte = "auto"')
    assert cargar_registro(escribir(tmp_path, texto))[0].recorte == "auto"


def test_rechaza_entrada_sin_licencia(tmp_path):
    texto = ENTRADA.replace('licencia = "CC BY 4.0"\n', "")
    with pytest.raises(ErrorRegistro, match="cap2_glaciacion: faltan licencia"):
        cargar_registro(escribir(tmp_path, texto))


def test_rechaza_tinta_inexistente(tmp_path):
    with pytest.raises(ErrorRegistro, match="tinta 'sepia' no existe"):
        cargar_registro(escribir(tmp_path, ENTRADA.replace('tinta = "glaciacion"', 'tinta = "sepia"')))


def test_rechaza_id_repetido(tmp_path):
    with pytest.raises(ErrorRegistro, match="id repetido"):
        cargar_registro(escribir(tmp_path, ENTRADA + ENTRADA))


def test_mapa_exige_limites(tmp_path):
    with pytest.raises(ErrorRegistro, match="mapa necesita"):
        cargar_registro(escribir(tmp_path, ENTRADA.replace('uso = "fondo"', 'uso = "mapa"')))


def test_reune_todos_los_errores(tmp_path):
    texto = (ENTRADA.replace('tinta = "glaciacion"', 'tinta = "sepia"')
             + ENTRADA.replace('id = "cap2_glaciacion"', 'id = "otra"').replace('autor = "Édouard Riou"\n', ""))
    with pytest.raises(ErrorRegistro) as error:
        cargar_registro(escribir(tmp_path, texto))
    assert "sepia" in str(error.value) and "otra: faltan autor" in str(error.value)
```

- [ ] **Step 5: Ejecutar y ver que fallan**

Run: `uv run pytest tests/test_ilustraciones.py -q`
Expected: FAIL con `ModuleNotFoundError: No module named 'ilustraciones'`.

- [ ] **Step 6: Implementar el registro**

`ilustraciones.py`:
```python
"""Procesa las ilustraciones del juego a partir de fuentes.toml (spec §5).

Uso:
    uv run ilustraciones.py                 descarga, trata y exporta todo; genera interfaz y créditos
    uv run ilustraciones.py --rejilla ID    guarda .cache/rejilla_ID.png para medir posiciones (en %)

Cada imagen del registro se descarga (con caché), se gira y recorta, recibe la
tinta de su ambiente y se exporta a game/images/. Si falta su licencia, se detiene.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

RAIZ = Path(__file__).parent
REGISTRO = RAIZ / "fuentes.toml"

USOS = ("fondo", "lamina", "mapa")
ENCAJES = ("cubrir", "editorial")
OBLIGATORIOS = ("id", "uso", "tinta", "url", "pagina_fuente", "autor", "obra", "anio", "licencia", "atribucion")

TINTAS = {  # tinta, tono medio, papel (spec §4)
    "archivo": ("#2E2620", "#8A7A66", "#F2EBDD"),
    "sabana": ("#3F3020", "#9C7F55", "#F2E8D2"),
    "glaciacion": ("#23313C", "#6F8492", "#ECEFEB"),
    "bosque": ("#1E3327", "#6C7F59", "#EEF0E2"),
    "neolitico": ("#3D291B", "#A2724A", "#F3E7D2"),
    "industria": ("#26282B", "#77787A", "#E7E5E0"),
}


class ErrorRegistro(ValueError):
    """El registro de fuentes tiene entradas incompletas o inválidas."""


@dataclass(frozen=True)
class Imagen:
    id: str
    uso: str
    tinta: str
    url: str
    pagina_fuente: str
    autor: str
    obra: str
    anio: str
    licencia: str
    atribucion: str
    recorte: tuple[int, int, int, int] | str | None = None
    rotar: int = 0
    encaje: str = "cubrir"
    centrado: tuple[float, float] = (0.5, 0.5)
    mapa: tuple[float, float, float, float] | None = None
    notas: str = ""


def _validar(e: dict, nombre: str) -> list[str]:
    errores = []
    if e["uso"] not in USOS:
        errores.append(f"{nombre}: uso '{e['uso']}' no es uno de {', '.join(USOS)}")
    if e["tinta"] not in TINTAS:
        errores.append(f"{nombre}: tinta '{e['tinta']}' no existe")
    if e.get("encaje", "cubrir") not in ENCAJES:
        errores.append(f"{nombre}: encaje '{e['encaje']}' no es uno de {', '.join(ENCAJES)}")
    if e.get("rotar", 0) not in (0, 90, 180, 270):
        errores.append(f"{nombre}: rotar debe ser 0, 90, 180 o 270 (sentido horario)")
    recorte = e.get("recorte")
    if recorte is not None and recorte != "auto" and (not isinstance(recorte, list) or len(recorte) != 4):
        errores.append(f'{nombre}: recorte debe ser [x, y, ancho, alto] o "auto"')
    if e["uso"] == "mapa" and len(e.get("mapa", [])) != 4:
        errores.append(f"{nombre}: un mapa necesita mapa = [lon_min, lat_min, lon_max, lat_max]")
    return errores


def cargar_registro(ruta: Path = REGISTRO) -> list[Imagen]:
    """Lee y valida fuentes.toml; reúne todos los problemas en un solo error."""
    datos = tomllib.loads(ruta.read_text(encoding="utf-8"))
    errores: list[str] = []
    imagenes: list[Imagen] = []
    vistos: set[str] = set()
    for n, e in enumerate(datos.get("imagen", []), start=1):
        nombre = e.get("id", f"entrada {n}")
        faltan = [c for c in OBLIGATORIOS if not str(e.get(c, "")).strip()]
        if faltan:
            errores.append(f"{nombre}: faltan {', '.join(faltan)}")
            continue
        if nombre in vistos:
            errores.append(f"{nombre}: id repetido")
        vistos.add(nombre)
        errores.extend(_validar(e, nombre))
        recorte = e.get("recorte")
        imagenes.append(Imagen(
            id=e["id"], uso=e["uso"], tinta=e["tinta"], url=e["url"], pagina_fuente=e["pagina_fuente"],
            autor=e["autor"], obra=e["obra"], anio=str(e["anio"]), licencia=e["licencia"],
            atribucion=e["atribucion"],
            recorte=tuple(recorte) if isinstance(recorte, list) else recorte,
            rotar=e.get("rotar", 0), encaje=e.get("encaje", "cubrir"),
            centrado=tuple(e.get("centrado", (0.5, 0.5))),
            mapa=tuple(e["mapa"]) if "mapa" in e else None, notas=e.get("notas", ""),
        ))
    if errores:
        raise ErrorRegistro("Registro de fuentes inválido:\n- " + "\n- ".join(errores))
    return imagenes
```

- [ ] **Step 7: Ejecutar y ver que pasan**

Run: `uv run pytest tests/test_ilustraciones.py -q`
Expected: `7 passed`.

- [ ] **Step 8: Commit**

```bash
git add .gitignore pyproject.toml uv.lock ilustraciones.py tests/test_ilustraciones.py
git commit -q -m "feat: registro de fuentes de imágenes con validación de licencias" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 2: Rotación, recorte, tinta y encaje

**Files:**
- Modify: `ilustraciones.py` (añadir imports y funciones)
- Test: `tests/test_ilustraciones.py` (añadir pruebas)

**Interfaces:**
- Consumes: `Imagen`, `TINTAS` (Tarea 1).
- Produces: `_hex(color) -> tuple[int, ...]`, `recorte_automatico(img) -> (x, y, w, h)`, `rotar_y_recortar(img, imagen) -> Image` (lanza `ValueError` si el recorte se sale), `aplicar_tinta(img, tinta) -> Image RGB`, `encajar(img, imagen) -> Image`, constantes `LIENZO=(1920, 1080)`, `MARGEN=64`, `ANCHO_EDITORIAL=1008`, `LAMINA_MAX=900`.

- [ ] **Step 1: Escribir las pruebas**

Añadir al final de `tests/test_ilustraciones.py`:
```python
from PIL import Image, ImageDraw

from ilustraciones import (
    TINTAS, Imagen, _hex, aplicar_tinta, encajar, recorte_automatico, rotar_y_recortar,
)


def entrada(**cambios):
    base = dict(id="x", uso="fondo", tinta="bosque", url="u", pagina_fuente="p", autor="a",
                obra="o", anio="1870", licencia="Dominio público", atribucion="a")
    base.update(cambios)
    return Imagen(**base)


def degradado(w=400, h=300):
    img = Image.new("L", (w, h))
    img.putdata([int(255 * (i % w) / (w - 1)) for i in range(w * h)])
    return img.convert("RGB")


def cerca(c1, c2, tol=24):
    return all(abs(a - b) <= tol for a, b in zip(c1, c2))


def test_tinta_lleva_negro_a_tinta_y_blanco_a_papel():
    img = aplicar_tinta(degradado(), "bosque")
    assert img.mode == "RGB" and img.size == (400, 300)
    assert cerca(img.getpixel((0, 150)), _hex(TINTAS["bosque"][0]))
    assert cerca(img.getpixel((399, 150)), _hex(TINTAS["bosque"][2]))


def test_tinta_es_determinista():
    assert aplicar_tinta(degradado(), "neolitico").tobytes() == aplicar_tinta(degradado(), "neolitico").tobytes()


def test_rotar_90_es_sentido_horario():
    img = Image.new("RGB", (40, 20), "white")
    img.putpixel((0, 0), (255, 0, 0))
    girada = rotar_y_recortar(img, entrada(rotar=90))
    assert girada.size == (20, 40)
    assert girada.getpixel((19, 0)) == (255, 0, 0)


def test_recorte_usa_x_y_ancho_alto():
    assert rotar_y_recortar(Image.new("RGB", (100, 80)), entrada(recorte=(10, 20, 30, 40))).size == (30, 40)


def test_recorte_fuera_de_la_imagen_falla():
    with pytest.raises(ValueError, match="x: el recorte .* se sale de la imagen"):
        rotar_y_recortar(Image.new("RGB", (100, 80)), entrada(recorte=(50, 0, 80, 40)))


def test_recorte_automatico_deja_fuera_margen_y_pie():
    pagina = Image.new("RGB", (1000, 1400), (240, 230, 210))
    d = ImageDraw.Draw(pagina)
    d.rectangle([100, 100, 900, 1100], fill=(40, 40, 40))       # el grabado
    d.rectangle([400, 1200, 600, 1215], fill=(40, 40, 40))      # el pie de imagen
    x, y, w, h = recorte_automatico(pagina)
    assert 100 <= x <= 110 and 100 <= y <= 110
    assert 1090 <= y + h <= 1100 and 890 <= x + w <= 900


def test_fondo_cubrir_llena_el_lienzo():
    assert encajar(degradado(1000, 1000), entrada()).size == (1920, 1080)


def test_fondo_editorial_deja_libre_el_panel_derecho():
    img = encajar(degradado(600, 900), entrada(encaje="editorial"))
    assert img.size == (1920, 1080)
    assert img.getpixel((1900, 540)) == _hex(TINTAS["bosque"][2])


def test_lamina_cabe_en_900():
    assert max(encajar(degradado(2000, 1000), entrada(uso="lamina")).size) == 900
```

- [ ] **Step 2: Ejecutar y ver que fallan**

Run: `uv run pytest tests/test_ilustraciones.py -q`
Expected: FAIL con `ImportError: cannot import name 'TINTAS'…'_hex'`.

- [ ] **Step 3: Implementar**

En `ilustraciones.py`, añadir a los imports:
```python
import random

from PIL import Image, ImageFilter, ImageOps
```
y después de `TINTAS`:
```python
LIENZO = (1920, 1080)
MARGEN = 64
ANCHO_EDITORIAL = LIENZO[0] - 3 * MARGEN - 720   # deja libre el panel lateral derecho (720 px)
LAMINA_MAX = 900
```
Al final del archivo:
```python
def _hex(color: str) -> tuple[int, ...]:
    """'#RRGGBB' o '#RRGGBBAA' → tupla de enteros."""
    return tuple(int(color[i:i + 2], 16) for i in range(1, len(color), 2))


def _tramo_mas_largo(valores: list[int], limite: float, hueco: int) -> tuple[int, int]:
    """Primer y último índice del tramo más largo por encima del límite, tolerando huecos cortos."""
    mejor, inicio, ultimo, largo = (0, len(valores) - 1), None, None, -1
    for i, v in enumerate(valores):
        if v > limite:
            if inicio is None or i - ultimo > hueco:
                inicio = i
            ultimo = i
            if ultimo - inicio > largo:
                largo, mejor = ultimo - inicio, (inicio, ultimo)
    return mejor


def recorte_automatico(img: Image.Image, umbral: int = 120, minimo: float = 0.08) -> tuple[int, int, int, int]:
    """Caja (x, y, ancho, alto) del grabado: deja fuera los márgenes de la página y el pie de imagen."""
    gris = ImageOps.grayscale(img).filter(ImageFilter.MedianFilter(5))
    w, h = gris.size
    oscuro = gris.point(lambda v: 255 if v < umbral else 0)
    filas = list(oscuro.resize((1, h), Image.BOX).tobytes())
    y0, y1 = _tramo_mas_largo(filas, minimo * 255, h // 50)
    columnas = list(oscuro.crop((0, y0, w, y1 + 1)).resize((w, 1), Image.BOX).tobytes())
    x0, x1 = _tramo_mas_largo(columnas, minimo * 255, w // 50)
    borde = max(4, (x1 - x0) // 200)   # quita la línea que enmarca el grabado
    return x0 + borde, y0 + borde, x1 - x0 - 2 * borde, y1 - y0 - 2 * borde


def rotar_y_recortar(img: Image.Image, imagen: Imagen) -> Image.Image:
    if imagen.rotar:
        img = img.rotate(-imagen.rotar, expand=True)   # rotar va en sentido horario
    if imagen.recorte == "auto":
        x, y, w, h = recorte_automatico(img)
    elif imagen.recorte:
        x, y, w, h = imagen.recorte
        if x < 0 or y < 0 or x + w > img.width or y + h > img.height:
            raise ValueError(f"{imagen.id}: el recorte {list(imagen.recorte)} se sale de la imagen ({img.width}×{img.height})")
    else:
        return img.convert("RGB")
    return img.crop((x, y, x + w, y + h)).convert("RGB")


def aplicar_tinta(img: Image.Image, tinta: str) -> Image.Image:
    """Duotono de la tinta del ambiente con grano de papel determinista (spec §4)."""
    oscuro, medio, papel = TINTAS[tinta]
    gris = ImageOps.autocontrast(ImageOps.grayscale(img), cutoff=(1, 3))
    entintada = ImageOps.colorize(gris, black=oscuro, mid=medio, white=papel, midpoint=110)
    w, h = entintada.size
    azar = random.Random(0)
    semilla = Image.new("L", (max(1, w // 4), max(1, h // 4)))
    semilla.putdata([128 + azar.randint(-10, 10) for _ in range(semilla.width * semilla.height)])
    grano = semilla.resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(1.2))
    return Image.blend(entintada, ImageOps.colorize(grano, black=oscuro, white=papel), 0.06)


def encajar(img: Image.Image, imagen: Imagen) -> Image.Image:
    """Formato final: lámina (≤ 900 px), fondo a pantalla completa o composición editorial."""
    if imagen.uso == "lamina":
        img = img.copy()
        img.thumbnail((LAMINA_MAX, LAMINA_MAX), Image.LANCZOS)
        return aplicar_tinta(img, imagen.tinta)
    if imagen.encaje == "editorial":
        alto = LIENZO[1] - 2 * MARGEN
        ancho = round(img.width * alto / img.height)
        if ancho > ANCHO_EDITORIAL:
            ancho, alto = ANCHO_EDITORIAL, round(img.height * ANCHO_EDITORIAL / img.width)
        grabado = aplicar_tinta(img.resize((ancho, alto), Image.LANCZOS), imagen.tinta)
        lienzo = Image.new("RGB", LIENZO, TINTAS[imagen.tinta][2])
        lienzo.paste(grabado, (MARGEN, (LIENZO[1] - alto) // 2))
        return lienzo
    return aplicar_tinta(ImageOps.fit(img, LIENZO, Image.LANCZOS, centering=imagen.centrado), imagen.tinta)
```

- [ ] **Step 4: Ejecutar y ver que pasan**

Run: `uv run pytest tests/test_ilustraciones.py -q`
Expected: `16 passed`.

- [ ] **Step 5: Commit**

```bash
git add ilustraciones.py tests/test_ilustraciones.py
git commit -q -m "feat: tinta por ambiente, recorte automático y encaje de fondos y láminas" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 3: Mapas de cuaderno con Natural Earth

**Files:**
- Modify: `ilustraciones.py`
- Test: `tests/test_ilustraciones.py`

**Interfaces:**
- Consumes: `TINTAS`, `_hex`, `LIENZO`, `MARGEN`.
- Produces: `posicion_en_mapa(lon, lat, limites, tamano=LIENZO) -> (x_rel, y_rel)` redondeado a 3 decimales; `dibujar_mapa(ruta, limites, tinta, tamano=LIENZO) -> Image` (`ruta` es un `.shp` o el `.zip` de Natural Earth).

- [ ] **Step 1: Escribir las pruebas**

```python
import shapefile

from ilustraciones import dibujar_mapa, posicion_en_mapa


def test_posicion_del_centro_es_el_centro():
    assert posicion_en_mapa(60, 47.5, (-15, 20, 135, 75)) == (0.5, 0.5)


def test_posiciones_de_los_marcadores_de_los_capitulos():
    eurasia = (-15, 20, 135, 75)
    assert posicion_en_mapa(110, 35, eurasia) == (0.811, 0.638)    # China
    assert posicion_en_mapa(-4, 40, eurasia) == (0.102, 0.583)     # España
    mundo = (-120, -40, 80, 60)
    assert posicion_en_mapa(-99, 19, mundo) == (0.131, 0.425)      # Mesoamérica


def test_mapa_pinta_tierra_y_deja_el_mar_en_papel(tmp_path):
    base = tmp_path / "tierra"
    with shapefile.Writer(str(base), shapeType=shapefile.POLYGON) as w:
        w.field("nombre", "C")
        w.poly([[(0, 0), (0, 10), (10, 10), (10, 0), (0, 0)]])
        w.record("cuadro")
    img = dibujar_mapa(base.with_suffix(".shp"), (-20, -20, 30, 30), "neolitico", tamano=(500, 500))
    papel = _hex(TINTAS["neolitico"][2])
    assert img.size == (500, 500)
    assert img.getpixel((5, 5)) == papel
    x, y = posicion_en_mapa(5, 5, (-20, -20, 30, 30), tamano=(500, 500))
    assert img.getpixel((round(x * 500), round(y * 500))) != papel
```

- [ ] **Step 2: Ejecutar y ver que fallan**

Run: `uv run pytest tests/test_ilustraciones.py -q -k mapa`
Expected: FAIL con `ImportError: cannot import name 'dibujar_mapa'`.

- [ ] **Step 3: Implementar**

Imports: añadir `import shapefile` y `ImageDraw` a `from PIL import Image, ImageDraw, ImageFilter, ImageOps`. Al final:
```python
def _proyector(limites, tamano):
    """Proyección equirrectangular centrada con márgenes: (lon, lat) → píxeles."""
    lon0, lat0, lon1, lat1 = limites
    w, h = tamano
    escala = min((w - 2 * MARGEN) / (lon1 - lon0), (h - 2 * MARGEN) / (lat1 - lat0))
    ox = (w - escala * (lon1 - lon0)) / 2
    oy = (h - escala * (lat1 - lat0)) / 2
    return lambda lon, lat: (ox + (lon - lon0) * escala, oy + (lat1 - lat) * escala)


def posicion_en_mapa(lon: float, lat: float, limites, tamano=LIENZO) -> tuple[float, float]:
    """Posición relativa (0–1) de una coordenada; sirve para colocar los marcadores del juego."""
    x, y = _proyector(limites, tamano)(lon, lat)
    return round(x / tamano[0], 3), round(y / tamano[1], 3)


def dibujar_mapa(ruta: Path, limites, tinta: str, tamano=LIENZO) -> Image.Image:
    """Mapa de cuaderno: tierra en tono claro, costas en tinta y retícula cada 15° (spec §5)."""
    oscuro, medio, papel = (_hex(c) for c in TINTAS[tinta])
    punto = _proyector(limites, tamano)
    lon0, lat0, lon1, lat1 = limites
    img = Image.new("RGB", tamano, papel)
    d = ImageDraw.Draw(img)
    tierra = tuple(round(p + (m - p) * 0.35) for p, m in zip(papel, medio))
    reticula = tuple(round(p + (o - p) * 0.15) for p, o in zip(papel, oscuro))
    for lon in range(-180, 181, 15):
        if lon0 <= lon <= lon1:
            d.line([punto(lon, lat0), punto(lon, lat1)], fill=reticula, width=1)
    for lat in range(-90, 91, 15):
        if lat0 <= lat <= lat1:
            d.line([punto(lon0, lat), punto(lon1, lat)], fill=reticula, width=1)
    with shapefile.Reader(str(ruta)) as lector:
        for forma in lector.shapes():
            partes = list(forma.parts) + [len(forma.points)]
            for a, b in zip(partes, partes[1:]):
                anillo = [punto(lon, lat) for lon, lat in forma.points[a:b]]
                if len(anillo) >= 3:
                    d.polygon(anillo, fill=tierra, outline=oscuro, width=2)
    return img
```

- [ ] **Step 4: Ejecutar y ver que pasan**

Run: `uv run pytest tests/test_ilustraciones.py -q`
Expected: `19 passed`.

- [ ] **Step 5: Commit**

```bash
git add ilustraciones.py tests/test_ilustraciones.py
git commit -q -m "feat: mapas de cuaderno con Natural Earth y posiciones de marcadores" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 4: Piezas de interfaz (esquinas redondeadas)

**Files:**
- Modify: `ilustraciones.py`
- Test: `tests/test_ilustraciones.py`

**Interfaces:**
- Produces: `UI` (dict nombre → (tamaño, radio, relleno, borde, grosor)), `pieza(tamano, radio, relleno, borde=None, grosor=0) -> Image RGBA`, `generar_ui(destino: Path) -> None`. Escribe en `game/gui/`: `marco, boton, boton_hover, boton_sec, boton_sec_hover, opcion, opcion_hover, opcion_bien, opcion_mal, letra, marca, marca_hover, marca_vista, insignia_vista, filete` (`.png`).

- [ ] **Step 1: Escribir las pruebas**

```python
from ilustraciones import UI, generar_ui, pieza


def test_pieza_tiene_esquinas_transparentes_y_centro_relleno():
    img = pieza((96, 96), 12, "#F3ECDCF5", "#CBBE9F", 2)
    assert img.mode == "RGBA" and img.size == (96, 96)
    assert img.getpixel((0, 0))[3] == 0
    assert all(abs(a - b) <= 1 for a, b in zip(img.getpixel((48, 48)), (0xF3, 0xEC, 0xDC, 0xF5)))


def test_generar_ui_escribe_todas_las_piezas(tmp_path):
    generar_ui(tmp_path)
    assert sorted(p.stem for p in tmp_path.glob("*.png")) == sorted([*UI, "filete"])
```

- [ ] **Step 2: Ejecutar y ver que fallan**

Run: `uv run pytest tests/test_ilustraciones.py -q -k "pieza or ui"`
Expected: FAIL con `ImportError: cannot import name 'UI'`.

- [ ] **Step 3: Implementar**

Después de `LAMINA_MAX`:
```python
UI = {  # nombre: (tamaño, radio, relleno, borde, grosor) con la paleta de la spec §4
    "marco": ((96, 96), 12, "#F3ECDCF5", "#CBBE9F", 2),
    "boton": ((64, 64), 8, "#2E4A3A", None, 0),
    "boton_hover": ((64, 64), 8, "#3D6450", None, 0),
    "boton_sec": ((64, 64), 8, "#F3ECDCEB", "#2A2722", 2),
    "boton_sec_hover": ((64, 64), 8, "#E9DFC8", "#2F6F8F", 3),
    "opcion": ((96, 96), 10, "#F3ECDC", "#CBBE9F", 2),
    "opcion_hover": ((96, 96), 10, "#F3ECDC", "#2F6F8F", 4),
    "opcion_bien": ((96, 96), 10, "#E7EDDF", "#2E6B47", 4),
    "opcion_mal": ((96, 96), 10, "#F3ECDC", "#9E3B2B", 4),
    "letra": ((44, 44), 8, "#00000000", "#2A2722", 2),
    "marca": ((56, 56), 28, "#F3ECDC", "#2A2722", 3),
    "marca_hover": ((56, 56), 28, "#F3ECDC", "#2F6F8F", 5),
    "marca_vista": ((56, 56), 28, "#E9DFC8", "#2A2722", 3),
    "insignia_vista": ((28, 28), 14, "#2E6B47", None, 0),
}
GUI = RAIZ / "game" / "gui"
```
Al final:
```python
def pieza(tamano, radio, relleno, borde=None, grosor=0) -> Image.Image:
    """Rectángulo redondeado con borde, dibujado a 4× para suavizar las esquinas."""
    s = 4
    w, h = tamano
    img = Image.new("RGBA", (w * s, h * s), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle(
        [0, 0, w * s - 1, h * s - 1], radius=radio * s, fill=_hex(relleno),
        outline=_hex(borde) if borde else None, width=grosor * s)
    return img.resize(tamano, Image.LANCZOS)


def generar_ui(destino: Path = GUI) -> None:
    destino.mkdir(parents=True, exist_ok=True)
    for nombre, (tamano, radio, relleno, borde, grosor) in UI.items():
        pieza(tamano, radio, relleno, borde, grosor).save(destino / f"{nombre}.png")
    filete = Image.new("RGBA", (16, 16), (0, 0, 0, 0))   # filete musgo del "Por qué"
    ImageDraw.Draw(filete).rectangle([0, 0, 4, 15], fill=_hex("#6B7A4B"))
    filete.save(destino / "filete.png")
```

- [ ] **Step 4: Ejecutar y ver que pasan**

Run: `uv run pytest tests/test_ilustraciones.py -q`
Expected: `21 passed`.

- [ ] **Step 5: Commit**

```bash
git add ilustraciones.py tests/test_ilustraciones.py
git commit -q -m "feat: piezas de interfaz con esquinas redondeadas generadas por script" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 5: Descarga con reintentos, créditos, rejilla y comando

**Files:**
- Modify: `ilustraciones.py`
- Test: `tests/test_ilustraciones.py`

**Interfaces:**
- Produces: `descargar(url, cache=CACHE, intentos=4, espera=3.0) -> Path`, `escapar_renpy(texto) -> str`, `generar_creditos(imagenes) -> str` (contenido de `game/creditos_generados.rpy` con `define CREDITOS_IMAGENES = [(atribucion, obra, pagina_fuente), ...]`), `rejilla(img) -> Image`, `salida_de(imagen) -> Path`, `procesar_imagen(imagen) -> Image`, `procesar(registro=REGISTRO) -> int`, `main(argv=None) -> int`.

- [ ] **Step 1: Escribir las pruebas**

```python
import urllib.error
import urllib.request

import ilustraciones
from ilustraciones import descargar, generar_creditos, procesar, rejilla


def test_descargar_usa_cache(tmp_path):
    origen = tmp_path / "x.jpg"
    Image.new("RGB", (10, 10)).save(origen)
    ruta = descargar(origen.as_uri(), tmp_path / "cache")
    assert ruta.read_bytes() == origen.read_bytes() and ruta.suffix == ".jpg"
    origen.unlink()
    assert descargar(origen.as_uri(), tmp_path / "cache") == ruta


def test_descargar_reintenta_ante_un_error(tmp_path, monkeypatch):
    origen = tmp_path / "x.png"
    Image.new("RGB", (4, 4)).save(origen)
    real = urllib.request.urlopen
    llamadas = []

    def falla_una_vez(peticion, timeout=None):
        llamadas.append(1)
        if len(llamadas) == 1:
            raise urllib.error.URLError("servidor caído")
        return real(peticion, timeout=timeout)

    monkeypatch.setattr(ilustraciones.urllib.request, "urlopen", falla_una_vez)
    ruta = descargar(origen.as_uri(), tmp_path / "cache", espera=0)
    assert ruta.read_bytes() == origen.read_bytes() and len(llamadas) == 2


def test_creditos_escapa_y_no_repite():
    a = entrada(atribucion="É. Riou [1863] {CC BY}", obra="Lámina 10", pagina_fuente="https://x")
    b = entrada(id="y", atribucion="É. Riou [1863] {CC BY}", obra="Lámina 10", pagina_fuente="https://x")
    texto = generar_creditos([a, b])
    assert texto.startswith("# Generado por ilustraciones.py")
    assert texto.count("Riou") == 1
    assert "[[1863]" in texto and "{{CC BY}" in texto


def test_rejilla_conserva_el_tamano():
    assert rejilla(degradado(200, 100)).size == (200, 100)


def test_procesar_rechaza_registro_invalido(tmp_path, capsys):
    ruta = tmp_path / "fuentes.toml"
    ruta.write_text('[[imagen]]\nid = "x"\n', encoding="utf-8")
    assert procesar(ruta) == 1
    assert "faltan" in capsys.readouterr().err
```

- [ ] **Step 2: Ejecutar y ver que fallan**

Run: `uv run pytest tests/test_ilustraciones.py -q`
Expected: FAIL con `ImportError: cannot import name 'descargar'`.

- [ ] **Step 3: Implementar**

Imports adicionales: `argparse, hashlib, sys, time, urllib.parse, urllib.request`. Constantes junto a `REGISTRO`:
```python
CACHE = RAIZ / ".cache" / "ilustraciones"
IMAGENES = RAIZ / "game" / "images"
CREDITOS = RAIZ / "game" / "creditos_generados.rpy"
AGENTE = "FragilidadVN/2.0 (proyecto educativo, Universidad del Valle)"
```
Al final:
```python
def descargar(url: str, cache: Path = CACHE, intentos: int = 4, espera: float = 3.0) -> Path:
    """Descarga una vez y reutiliza la copia local; reintenta ante errores del servidor."""
    cache.mkdir(parents=True, exist_ok=True)
    sufijo = Path(urllib.parse.urlparse(url).path).suffix.lower() or ".bin"
    destino = cache / (hashlib.sha1(url.encode()).hexdigest()[:16] + sufijo)
    if destino.exists():
        return destino
    for intento in range(1, intentos + 1):
        try:
            peticion = urllib.request.Request(url, headers={"User-Agent": AGENTE})
            with urllib.request.urlopen(peticion, timeout=120) as respuesta:
                destino.write_bytes(respuesta.read())
            return destino
        except OSError as error:   # URLError y HTTPError heredan de OSError
            if intento == intentos:
                raise RuntimeError(f"No se pudo descargar {url}: {error}") from error
            time.sleep(espera * intento)
    return destino


def escapar_renpy(texto: str) -> str:
    """Ren'Py interpreta [ ] y { } en los textos: se duplican para mostrarlos literales."""
    return texto.replace("[", "[[").replace("{", "{{")


def generar_creditos(imagenes: list[Imagen]) -> str:
    vistas, filas = set(), []
    for img in imagenes:
        clave = (img.atribucion, img.obra, img.pagina_fuente)
        if clave in vistas:
            continue
        vistas.add(clave)
        filas.append(f"    ({escapar_renpy(img.atribucion)!r}, {escapar_renpy(img.obra)!r}, "
                     f"{escapar_renpy(img.pagina_fuente)!r}),")
    return "\n".join(["# Generado por ilustraciones.py desde fuentes.toml. No editar a mano.", "",
                      "define CREDITOS_IMAGENES = [", *filas, "]", ""])


def rejilla(img: Image.Image) -> Image.Image:
    """Copia con líneas cada 5 % (rojas verticales, azules horizontales) para medir posiciones."""
    img = img.convert("RGB").copy()
    d = ImageDraw.Draw(img)
    for i in range(1, 20):
        x, y = round(img.width * i / 20), round(img.height * i / 20)
        d.line([(x, 0), (x, img.height)], fill=(220, 0, 0), width=1)
        d.text((x + 3, 3), str(i * 5), fill=(220, 0, 0))
        d.line([(0, y), (img.width, y)], fill=(0, 0, 220), width=1)
        d.text((3, y + 3), str(i * 5), fill=(0, 0, 220))
    return img


def salida_de(imagen: Imagen) -> Path:
    return IMAGENES / ("laminas" if imagen.uso == "lamina" else "fondos") / f"{imagen.id}.jpg"


def procesar_imagen(imagen: Imagen) -> Image.Image:
    origen = descargar(imagen.url)
    if imagen.uso == "mapa":
        return dibujar_mapa(origen, imagen.mapa, imagen.tinta)
    with Image.open(origen) as original:
        return encajar(rotar_y_recortar(original, imagen), imagen)


def procesar(registro: Path = REGISTRO) -> int:
    try:
        imagenes = cargar_registro(registro)
    except ErrorRegistro as error:
        print(error, file=sys.stderr)
        return 1
    for imagen in imagenes:
        destino = salida_de(imagen)
        destino.parent.mkdir(parents=True, exist_ok=True)
        procesar_imagen(imagen).save(destino, quality=85)
        print(f"✓ {destino.relative_to(RAIZ)}")
    generar_ui(GUI)
    CREDITOS.write_text(generar_creditos(imagenes), encoding="utf-8")
    print(f"Listo: {len(imagenes)} imágenes, piezas de interfaz y créditos.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Procesa las ilustraciones del juego desde fuentes.toml.")
    parser.add_argument("--rejilla", metavar="ID",
                        help="guarda .cache/rejilla_ID.png con una rejilla del 5 %% para medir posiciones")
    args = parser.parse_args(argv)
    if not args.rejilla:
        return procesar()
    imagen = next((i for i in cargar_registro() if i.id == args.rejilla), None)
    if imagen is None:
        print(f"No hay ninguna imagen con id {args.rejilla} en fuentes.toml", file=sys.stderr)
        return 1
    ruta = RAIZ / ".cache" / f"rejilla_{imagen.id}.png"
    ruta.parent.mkdir(parents=True, exist_ok=True)
    rejilla(procesar_imagen(imagen)).save(ruta)
    print(f"Rejilla guardada en {ruta.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Ejecutar y ver que pasan**

Run: `uv run pytest tests/test_ilustraciones.py -q`
Expected: `26 passed`.

- [ ] **Step 5: Commit**

```bash
git add ilustraciones.py tests/test_ilustraciones.py
git commit -q -m "feat: descarga con caché y reintentos, créditos generados y rejilla de medición" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 6: Voz · lectura del guion y texto para la voz

**Files:**
- Modify: `generar_voz.py` (reescritura completa)
- Create: `tests/test_generar_voz.py`

**Interfaces:**
- Produces: `leer_guion(raiz=GUION) -> dict[str, str]` (`ValueError` por id repetido o `[`), `texto_para_voz(texto) -> str`, constantes `GUION`, `VOCES`, `VOZ="em_alex"`, `VELOCIDAD=0.92`, `FRECUENCIA=24000`, `PRONUNCIACION`.

- [ ] **Step 1: Escribir las pruebas**

`tests/test_generar_voz.py`:
```python
import pytest

from generar_voz import leer_guion, texto_para_voz


def escribir(raiz, nombre, contenido):
    ruta = raiz / nombre
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(contenido, encoding="utf-8")
    return ruta


def test_lee_lineas_con_id_y_argumentos(tmp_path):
    escribir(tmp_path, "capitulos/cap2.rpy", '''
label cap2:
    n "Hace unos 13.000 años terminó la glaciación." id cap2_06
    ficha "Desapareció al terminar la glaciación." (show_titulo="Alce gigante", show_pagina="p. 15") id cap2_obs_alce
        pregunta "¿Qué relación hay?" id cap2_quiz
    n "Esta línea no tiene id."
    $ x = 1
''')
    assert leer_guion(tmp_path) == {
        "cap2_06": "Hace unos 13.000 años terminó la glaciación.",
        "cap2_obs_alce": "Desapareció al terminar la glaciación.",
        "cap2_quiz": "¿Qué relación hay?",
    }


def test_ignora_las_pruebas_del_juego(tmp_path):
    escribir(tmp_path, "tests/escenas_prueba.rpy", 'n "Prueba." id prueba_01\n')
    assert leer_guion(tmp_path) == {}


def test_id_repetido_es_error(tmp_path):
    escribir(tmp_path, "a.rpy", 'n "Uno." id cap1_01\n')
    escribir(tmp_path, "b.rpy", 'n "Dos." id cap1_01\n')
    with pytest.raises(ValueError, match="id repetido «cap1_01»"):
        leer_guion(tmp_path)


def test_interpolacion_no_permitida(tmp_path):
    escribir(tmp_path, "a.rpy", 'n "Tienes [aciertos] aciertos." id final_01\n')
    with pytest.raises(ValueError, match="interpolar"):
        leer_guion(tmp_path)


def test_texto_para_voz():
    entrada = '{i}Hacia{/i} el 7000 a.C. vivían 3 hab./km² y hace 13.000 años \\"así\\"'
    assert texto_para_voz(entrada) == ('Hacia el 7000 antes de Cristo vivían 3 habitantes por kilómetro '
                                       'cuadrado y hace trece mil años "así"')
```

- [ ] **Step 2: Ejecutar y ver que fallan**

Run: `uv run pytest tests/test_generar_voz.py -q`
Expected: FAIL con `ImportError: cannot import name 'leer_guion'`.

- [ ] **Step 3: Implementar (reemplaza el archivo entero)**

`generar_voz.py`:
```python
"""Genera las voces del juego con Kokoro TTS a partir del guion (spec §6).

Uso:
    uv run --group voz generar_voz.py              genera las voces nuevas o con texto cambiado
    uv run --group voz generar_voz.py --revisar    solo muestra qué cambiaría
    uv run --group voz generar_voz.py --duracion   minutos de voz por parte

Cada línea hablada es una sentencia say con id, en una sola línea:
    n "Texto." id cap2_03
Su voz se guarda en game/audio/voz/cap2_03.ogg. Las grabaciones propias de
game/audio/voz/grabadas/ tienen prioridad en el juego y este script no las toca.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

RAIZ = Path(__file__).parent
GUION = RAIZ / "game"
VOCES = GUION / "audio" / "voz"
VOZ = "em_alex"
VELOCIDAD = 0.92
FRECUENCIA = 24000

LINEA = re.compile(r'^\s*[A-Za-z_]\w*\s+"(?P<texto>(?:[^"\\]|\\.)*)"\s*(?:\(.*\)\s*)?id\s+(?P<id>[A-Za-z_]\w*)\s*$')
ETIQUETA = re.compile(r"\{[^{}]*\}")
PRONUNCIACION = (  # (como se escribe, como debe leerse), en este orden
    ("hab./km²", "habitantes por kilómetro cuadrado"),
    ("km²", "kilómetros cuadrados"),
    ("a.C.", "antes de Cristo"),
    ("500.000", "quinientos mil"),
    ("300.000", "trescientos mil"),
    ("100.000", "cien mil"),
    ("50.000", "cincuenta mil"),
    ("13.000", "trece mil"),
    ("9.000", "nueve mil"),
    ("—", ", "),
)


def leer_guion(raiz: Path = GUION) -> dict[str, str]:
    """{id: texto} de las líneas say con id de game/ (sin game/tests/), en orden."""
    lineas: dict[str, str] = {}
    origen: dict[str, str] = {}
    for archivo in sorted(raiz.rglob("*.rpy")):
        if "tests" in archivo.relative_to(raiz).parts:
            continue
        for n, linea in enumerate(archivo.read_text(encoding="utf-8").splitlines(), start=1):
            m = LINEA.match(linea)
            if not m:
                continue
            ident, texto = m["id"], m["texto"]
            if ident in lineas:
                raise ValueError(f"id repetido «{ident}» en {archivo.name}:{n} (ya estaba en {origen[ident]})")
            if "[" in texto:
                raise ValueError(f"{archivo.name}:{n}: las líneas habladas no pueden interpolar variables ([...])")
            lineas[ident] = texto
            origen[ident] = f"{archivo.name}:{n}"
    return lineas


def texto_para_voz(texto: str) -> str:
    """Quita etiquetas de Ren'Py y aplica el diccionario de pronunciación."""
    texto = ETIQUETA.sub("", texto).replace('\\"', '"').replace("\\n", " ")
    for escrito, hablado in PRONUNCIACION:
        texto = texto.replace(escrito, hablado)
    return " ".join(texto.split())
```

- [ ] **Step 4: Ejecutar y ver que pasan**

Run: `uv run pytest tests/test_generar_voz.py -q`
Expected: `5 passed`.

- [ ] **Step 5: Commit**

```bash
git add generar_voz.py tests/test_generar_voz.py
git commit -q -m "feat(voz): lectura de líneas con id del guion y diccionario de pronunciación" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 7: Voz · manifiesto, planificación, duración y comando

**Files:**
- Modify: `generar_voz.py`
- Test: `tests/test_generar_voz.py`

**Interfaces:**
- Consumes: `leer_guion`, `texto_para_voz` (Tarea 6).
- Produces: `firma(texto_voz) -> str` (16 hex), `planificar(lineas, manifiesto, existentes) -> (pendientes, huerfanas)`, `duraciones(voces, medir=None) -> dict[parte, minutos]`, `sintetizador_kokoro() -> callable`, `guardar_ogg(ruta, audio)`, `main(argv=None, sintetizador=None, guardar=guardar_ogg, raiz=GUION, voces=VOCES) -> int`.

- [ ] **Step 1: Escribir las pruebas**

Añadir a `tests/test_generar_voz.py`:
```python
from generar_voz import duraciones, firma, main, planificar


def test_planificar_genera_faltantes_y_cambiadas():
    lineas = {"a_01": "Uno.", "a_02": "Dos.", "a_03": "Tres."}
    manifiesto = {"a_01": firma("Uno."), "a_02": firma("Texto viejo.")}
    pendientes, huerfanas = planificar(lineas, manifiesto, existentes={"a_01", "a_02", "viejo_09"})
    assert pendientes == ["a_02", "a_03"] and huerfanas == ["viejo_09"]


def test_main_genera_y_luego_no_repite(tmp_path, capsys):
    guion, voces = tmp_path / "game", tmp_path / "game" / "audio" / "voz"
    escribir(guion, "cap.rpy", 'n "Hacia el 7000 a.C." id cap3_01\n')
    textos = []

    def falso(texto):
        textos.append(texto)
        return [0.0] * 10

    def guardar(ruta, audio):
        ruta.write_bytes(b"ogg")

    assert main([], sintetizador=falso, guardar=guardar, raiz=guion, voces=voces) == 0
    assert textos == ["Hacia el 7000 antes de Cristo."] and (voces / "cap3_01.ogg").exists()
    textos.clear()
    assert main([], sintetizador=falso, guardar=guardar, raiz=guion, voces=voces) == 0
    assert textos == [] and "al día" in capsys.readouterr().out


def test_revisar_no_genera(tmp_path):
    guion, voces = tmp_path / "game", tmp_path / "game" / "audio" / "voz"
    escribir(guion, "cap.rpy", 'n "Uno." id cap1_01\n')
    assert main(["--revisar"], sintetizador=lambda t: 1 / 0, raiz=guion, voces=voces) == 0
    assert not (voces / "cap1_01.ogg").exists()


def test_duraciones_suma_minutos_por_parte(tmp_path):
    for nombre in ("cap1_01", "cap1_02", "intro_01"):
        (tmp_path / f"{nombre}.ogg").write_bytes(b"x")
    assert duraciones(tmp_path, medir=lambda ruta: 30.0) == {"cap1": 1.0, "intro": 0.5}
```

- [ ] **Step 2: Ejecutar y ver que fallan**

Run: `uv run pytest tests/test_generar_voz.py -q`
Expected: FAIL con `ImportError: cannot import name 'duraciones'`.

- [ ] **Step 3: Implementar**

Al final de `generar_voz.py`:
```python
def firma(texto_voz: str) -> str:
    return hashlib.sha256(f"{VOZ}|{VELOCIDAD}|{texto_voz}".encode()).hexdigest()[:16]


def planificar(lineas: dict[str, str], manifiesto: dict[str, str], existentes: set[str]) -> tuple[list[str], list[str]]:
    """(ids a generar, ids huérfanos). Se genera si falta el archivo o cambió el texto."""
    pendientes = [i for i, t in lineas.items()
                  if i not in existentes or manifiesto.get(i) != firma(texto_para_voz(t))]
    return pendientes, sorted(existentes - set(lineas))


def duraciones(voces: Path = VOCES, medir=None) -> dict[str, float]:
    """Minutos de voz por parte (intro, cap1…) a partir de los OGG generados."""
    if medir is None:
        import soundfile as sf
        medir = lambda ruta: sf.info(ruta).duration  # noqa: E731
    total: dict[str, float] = {}
    for archivo in sorted(voces.glob("*.ogg")):
        parte = archivo.stem.split("_")[0]
        total[parte] = round(total.get(parte, 0.0) + medir(archivo) / 60, 2)
    return total


def sintetizador_kokoro():
    """Función texto → audio a 24 kHz. Importa Kokoro solo aquí porque carga PyTorch."""
    import numpy as np
    from kokoro import KPipeline

    pipeline = KPipeline(lang_code="e")  # "e" = español

    def sintetizar(texto: str):
        trozos = [audio for _, _, audio in pipeline(texto, voice=VOZ, speed=VELOCIDAD)]
        if not trozos:
            raise RuntimeError(f"Kokoro no generó audio para: {texto[:60]}")
        return np.concatenate(trozos)

    return sintetizar


def guardar_ogg(ruta: Path, audio) -> None:
    import soundfile as sf
    sf.write(ruta, audio, FRECUENCIA, format="OGG", subtype="VORBIS")


def main(argv=None, sintetizador=None, guardar=guardar_ogg, raiz: Path = GUION, voces: Path = VOCES) -> int:
    parser = argparse.ArgumentParser(description="Genera las voces del guion con Kokoro TTS.")
    parser.add_argument("--revisar", action="store_true", help="solo muestra qué se generaría")
    parser.add_argument("--duracion", action="store_true", help="minutos de voz por parte")
    args = parser.parse_args(argv)
    if args.duracion:
        for parte, minutos in duraciones(voces).items():
            print(f"{parte}: {minutos:.2f} min")
        return 0
    lineas = leer_guion(raiz)
    ruta_manifiesto = voces / "manifest.json"
    manifiesto = json.loads(ruta_manifiesto.read_text(encoding="utf-8")) if ruta_manifiesto.exists() else {}
    pendientes, huerfanas = planificar(lineas, manifiesto, {p.stem for p in voces.glob("*.ogg")})
    for ident in huerfanas:
        print(f"Huérfana (ya no está en el guion): {ident}.ogg")
    if not pendientes:
        print("Todas las voces están al día.")
        return 0
    print(f"{len(pendientes)} voces por generar: {', '.join(pendientes)}")
    if args.revisar:
        return 0
    sintetizar = sintetizador or sintetizador_kokoro()
    voces.mkdir(parents=True, exist_ok=True)
    for ident in pendientes:
        texto = texto_para_voz(lineas[ident])
        guardar(voces / f"{ident}.ogg", sintetizar(texto))
        manifiesto[ident] = firma(texto)
        ruta_manifiesto.write_text(json.dumps(manifiesto, ensure_ascii=False, indent=1, sort_keys=True),
                                   encoding="utf-8")
        print(f"Generada: {ident}.ogg")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Ejecutar todas las pruebas**

Run: `uv run pytest -q`
Expected: `35 passed` (26 + 9).

- [ ] **Step 5: Commit**

```bash
git add generar_voz.py tests/test_generar_voz.py
git commit -q -m "feat(voz): manifiesto por hash, voces OGG, revisión y duración por parte" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

**Sigue en** `docs/superpowers/plans/2026-10-13-novela-visual-parte2.md` (Tarea 8).
