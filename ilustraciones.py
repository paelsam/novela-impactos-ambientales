"""Procesa las ilustraciones del juego a partir de fuentes.toml (spec §5).

Uso:
    uv run ilustraciones.py                 descarga, trata y exporta todo; genera interfaz y créditos
    uv run ilustraciones.py --rejilla ID    guarda .cache/rejilla_ID.png para medir posiciones (en %)

Cada imagen del registro se descarga (con caché), se gira y recorta, recibe la
tinta de su ambiente y se exporta a game/images/. Si falta su licencia, se detiene.
"""

from __future__ import annotations

import random
import tomllib
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps

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

LIENZO = (1920, 1080)
MARGEN = 64
ANCHO_EDITORIAL = LIENZO[0] - 3 * MARGEN - 720   # deja libre el panel lateral derecho (720 px)
LAMINA_MAX = 900


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
