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
