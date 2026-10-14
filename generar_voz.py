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
