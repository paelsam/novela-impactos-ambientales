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


def firma(texto_voz: str) -> str:
    return hashlib.sha256(f"{VOZ}|{VELOCIDAD}|{texto_voz}".encode()).hexdigest()[:16]


def planificar(lineas: dict[str, str], manifiesto: dict[str, str], existentes: set[str]) -> tuple[list[str], list[str]]:
    """(ids a generar, ids huérfanos). Se genera si falta el archivo o cambió el texto."""
    pendientes = [i for i, t in lineas.items()
                  if i not in existentes or manifiesto.get(i) != firma(texto_para_voz(t))]
    return pendientes, sorted(existentes - set(lineas))


def duraciones(voces: Path = VOCES, medir=None) -> dict[str, float]:
    """Minutos de voz por parte (intro, cap1…) a partir de los OGG generados.

    Sigue la spec: no cuenta observaciones (_obs_) y, de las ramas de decisión
    (<parte>_dec_<letra>), cuenta únicamente la rama más larga de cada parte.
    """
    if medir is None:
        import soundfile as sf
        medir = lambda ruta: sf.info(ruta).duration  # noqa: E731

    re_rama = re.compile(r"^(?P<parte>[^_]+)_dec_[a-z0-9]+$")
    segundos_fijos: dict[str, float] = {}
    ramas_max: dict[str, float] = {}

    for archivo in sorted(voces.glob("*.ogg")):
        stem = archivo.stem
        if "_obs_" in stem:
            continue
        parte = stem.split("_")[0]
        m_rama = re_rama.match(stem)
        dur = medir(archivo)
        if m_rama:
            ramas_max[parte] = max(ramas_max.get(parte, 0.0), dur)
        else:
            segundos_fijos[parte] = segundos_fijos.get(parte, 0.0) + dur

    total: dict[str, float] = {}
    todas_partes = sorted(set(segundos_fijos) | set(ramas_max))
    for p in todas_partes:
        seg = segundos_fijos.get(p, 0.0) + ramas_max.get(p, 0.0)
        total[p] = round(seg / 60, 2)
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

