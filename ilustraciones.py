"""Procesa las ilustraciones del juego a partir de fuentes.toml (spec §5).

Uso:
    uv run ilustraciones.py                 descarga, trata y exporta todo; genera interfaz y créditos
    uv run ilustraciones.py --rejilla ID    guarda .cache/rejilla_ID.png para medir posiciones (en %)

Cada imagen del registro se descarga (con caché), se gira y recorta, recibe la
tinta de su ambiente y se exporta a game/images/. Si falta su licencia, se detiene.
"""

from __future__ import annotations

import argparse
import hashlib
import random
import sys
import time
import tomllib
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import shapefile
from PIL import Image, ImageDraw, ImageFilter, ImageOps

RAIZ = Path(__file__).parent
REGISTRO = RAIZ / "fuentes.toml"
CACHE = RAIZ / ".cache" / "ilustraciones"
IMAGENES = RAIZ / "game" / "images"
CREDITOS = RAIZ / "game" / "creditos_generados.rpy"
AGENTE = "FragilidadVN/3.0 (proyecto educativo, Universidad del Valle; https://github.com/paelsam/novela-impactos-ambientales)"

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

UI = {  # nombre: (tamaño, radio, relleno, borde, grosor) con la paleta de la spec §4
    "marco": ((96, 96), 6, "#F3ECDCF5", "#CBBE9F", 1.5),
    "boton": ((64, 64), 4, "#2E4A3A", None, 0),
    "boton_hover": ((64, 64), 4, "#3D6450", "#C9B98F", 3),
    "boton_sec": ((64, 64), 4, "#F3ECDCEB", "#2A2722", 2),
    "boton_sec_hover": ((64, 64), 4, "#E6DCBF", "#2E4A3A", 3),
    "opcion": ((96, 96), 4, "#F6F0E1", "#B7A882", 1.5),
    "opcion_hover": ((96, 96), 4, "#E8DFC4", "#2E4A3A", 3),
    "opcion_bien": ((96, 96), 4, "#DCEAD6", "#2E6B47", 4),
    "opcion_mal": ((96, 96), 4, "#F3D8D0", "#9E3B2B", 4),
    "letra": ((44, 44), 22, "#00000000", "#2A2722", 2),
    "letra_bien": ((44, 44), 22, "#2E6B47", None, 0),
    "letra_mal": ((44, 44), 22, "#9E3B2B", None, 0),
    "marca": ((56, 56), 28, "#F3ECDC", "#2A2722", 3),
    "marca_hover": ((56, 56), 28, "#F3ECDC", "#2F6F8F", 4),
    "marca_vista": ((56, 56), 28, "#E9DFC8", "#2A2722", 3),
    "insignia_vista": ((28, 28), 14, "#2E6B47", None, 0),
}
GUI = RAIZ / "game" / "gui"


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


def pieza(tamano, radio, relleno, borde=None, grosor=0) -> Image.Image:
    """Rectángulo redondeado con borde, dibujado a 4× para suavizar las esquinas."""
    s = 4
    w, h = tamano
    img = Image.new("RGBA", (w * s, h * s), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle(
        [0, 0, w * s - 1, h * s - 1], radius=radio * s, fill=_hex(relleno),
        outline=_hex(borde) if borde else None, width=round(grosor * s))
    return img.resize(tamano, Image.LANCZOS)


def generar_ui(destino: Path = GUI) -> None:
    destino.mkdir(parents=True, exist_ok=True)
    for nombre, (tamano, radio, relleno, borde, grosor) in UI.items():
        pieza(tamano, radio, relleno, borde, grosor).save(destino / f"{nombre}.png")
    filete = Image.new("RGBA", (16, 16), (0, 0, 0, 0))   # filete musgo del "Por qué"
    ImageDraw.Draw(filete).rectangle([0, 0, 4, 15], fill=_hex("#6B7A4B"))
    filete.save(destino / "filete.png")
    marco_grabado().save(destino / "marco_grabado.png")
    marco_grabado(papel="#E8DFC4F7", tinta="#2E4A3A").save(destino / "marco_grabado_hover.png")


def marco_grabado(lado: int = 120, papel: str = "#F3ECDCF7", tinta: str = "#2A2722") -> Image.Image:
    """Marco de lámina antigua: filete exterior grueso, filete interior fino y esquinas marcadas.

    Se usa como Frame de 22 px: las líneas quedan en el borde y no se deforman al estirar.
    """
    s = 4
    img = Image.new("RGBA", (lado * s, lado * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, lado * s - 1, lado * s - 1], fill=_hex(papel), outline=_hex(tinta), width=3 * s)
    d.rectangle([9 * s, 9 * s, (lado - 9) * s - 1, (lado - 9) * s - 1], outline=_hex(tinta), width=s)
    for x in (9, lado - 9):
        for y in (9, lado - 9):
            d.rectangle([(x - 3) * s, (y - 3) * s, (x + 3) * s, (y + 3) * s], fill=_hex(tinta))
    return img.resize((lado, lado), Image.LANCZOS)


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


